import datetime
import os
import json
import secrets
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from src.data.veri_yoneticisi import VeriYoneticisi

admin_bp = Blueprint("admin", __name__, url_prefix="/yonetici")
db = VeriYoneticisi()

ADMIN_SIFRE = os.environ.get("ADMIN_SIFRE", "JKB@admin2026!")


def admin_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_giris"):
            return redirect(url_for("admin.admin_giris"))
        return f(*args, **kwargs)
    return decorated


def _veri_oku():
    return db.veri_oku()


def _veri_yaz(data):
    db.veri_yaz(data)


def _kullanici_dict(kullanici_adi):
    return _veri_oku().get("kullanicilar", {}).get(kullanici_adi)


def _statlar(data):
    kullanicilar = data.get("kullanicilar", {})
    return {
        "toplam_kullanici": len(kullanicilar),
        "toplam_gorev": sum(len(v.get("gorevler", [])) for v in kullanicilar.values()),
        "tamamlanan_gorev": sum(sum(1 for g in v.get("gorevler", []) if g.get("tamamlandi")) for v in kullanicilar.values()),
        "toplam_fitness": sum(len(v.get("fitness_gecmisi", [])) for v in kullanicilar.values()),
        "toplam_antrenman": sum(len(v.get("antrenman_kayitlari", [])) for v in kullanicilar.values()),
        "toplam_su": sum(len(v.get("su_kayitlari", {})) for v in kullanicilar.values()),
        "toplam_hatirlatici": sum(len(v.get("hatirlaticilar", [])) for v in kullanicilar.values()),
    }


@admin_bp.route("/giris", methods=["GET", "POST"])
def admin_giris():
    if session.get("admin_giris"):
        return redirect(url_for("admin.admin_panel"))
    hata = None
    if request.method == "POST":
        sifre = request.form.get("sifre", "")
        if sifre == ADMIN_SIFRE:
            session["admin_giris"] = True
            session["admin_giris_zamani"] = datetime.datetime.now().isoformat()
            return redirect(url_for("admin.admin_panel"))
        hata = "Şifre hatalı!"
    return render_template("admin_giris.html", hata=hata)


@admin_bp.route("/cikis")
def admin_cikis():
    session.pop("admin_giris", None)
    session.pop("admin_giris_zamani", None)
    return redirect(url_for("admin.admin_giris"))


@admin_bp.route("/")
@admin_gerekli
def admin_panel():
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    stats = _statlar(data)
    kullanici_ozet = []
    for ad, v in kullanicilar.items():
        rol = v.get("rol", "user")
        durum = v.get("durum", "aktif")
        kilitli = v.get("kilitli", False)
        kullanici_ozet.append({
            "ad": ad,
            "eposta": v.get("eposta", "—"),
            "telefon": v.get("telefon", "—"),
            "gorev_sayisi": len(v.get("gorevler", [])),
            "fitness_kayit": len(v.get("fitness_gecmisi", [])),
            "antrenman": len(v.get("antrenman_kayitlari", [])),
            "hedef": v.get("fitness_profil", {}).get("hedef", "—"),
            "seviye": v.get("fitness_profil", {}).get("seviye", "—"),
            "rol": rol,
            "durum": durum,
            "kilitli": kilitli,
            "token": v.get("admin_token", ""),
        })
    return render_template(
        "admin_panel.html",
        **stats,
        db_boyutu=os.path.getsize(db.dosya_yolu) if os.path.exists(db.dosya_yolu) else 0,
        kullanici_ozet=kullanici_ozet,
        giris_zamani=session.get("admin_giris_zamani", "—"),
    )


@admin_bp.route("/kullanici/<kullanici_adi>")
@admin_gerekli
def kullanici_detay(kullanici_adi):
    kullanici = _kullanici_dict(kullanici_adi)
    if not kullanici:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    return render_template("admin_kullanici.html", ad=kullanici_adi, kullanici=kullanici)


@admin_bp.route("/kullanici/<kullanici_adi>/rol", methods=["POST"])
@admin_gerekli
def kullanici_rol_guncelle(kullanici_adi):
    rol = request.form.get("rol", "user")
    if rol not in {"user", "moderator", "admin"}:
        flash("Geçersiz rol.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi]["rol"] = rol
    kullanicilar[kullanici_adi]["admin_token"] = secrets.token_urlsafe(12) if rol == "admin" else ""
    kullanicilar[kullanici_adi]["durum"] = kullanicilar[kullanici_adi].get("durum", "aktif")
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    flash("Rol güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/durum", methods=["POST"])
@admin_gerekli
def kullanici_durum_guncelle(kullanici_adi):
    durum = request.form.get("durum", "aktif")
    if durum not in {"aktif", "pasif", "kilitli"}:
        flash("Geçersiz durum.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi]["durum"] = durum
    kullanicilar[kullanici_adi]["kilitli"] = durum == "kilitli"
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    flash("Kullanıcı durumu güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/pin", methods=["POST"])
@admin_gerekli
def kullanici_pin(kullanici_adi):
    veri = _veri_oku()
    kullanicilar = veri.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi]["admin_pinli"] = not kullanicilar[kullanici_adi].get("admin_pinli", False)
    veri["kullanicilar"] = kullanicilar
    _veri_yaz(veri)
    flash("Kullanıcı sabitleme durumu güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/sifre-sifirla", methods=["POST"])
@admin_gerekli
def kullanici_sifre_sifirla(kullanici_adi):
    yeni_sifre = request.form.get("yeni_sifre", "").strip()
    if len(yeni_sifre) < 6:
        flash("Şifre en az 6 karakter olmalı.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi]["sifre"] = yeni_sifre
    kullanicilar[kullanici_adi]["sifre_degisim_tarihi"] = datetime.datetime.now().isoformat()
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    flash("Şifre güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/eposta-guncelle", methods=["POST"])
@admin_gerekli
def kullanici_eposta_guncelle(kullanici_adi):
    yeni_eposta = request.form.get("eposta", "").strip().lower()
    if "@" not in yeni_eposta:
        flash("Geçerli bir e-posta girin.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi]["eposta"] = yeni_eposta
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    flash("E-posta güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/temizle", methods=["POST"])
@admin_gerekli
def kullanici_temizle(kullanici_adi):
    alan = request.form.get("alan", "")
    temizlenebilir = {
        "gorevler": [],
        "fitness_gecmisi": [],
        "antrenman_kayitlari": [],
        "su_kayitlari": {},
        "hatirlaticilar": [],
        "notlar": "",
        "fitness_profil": {},
        "admin_token": "",
    }
    if alan not in temizlenebilir:
        flash("Geçersiz alan.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi][alan] = temizlenebilir[alan]
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    flash(f"'{alan}' verisi temizlendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/sil", methods=["POST"])
@admin_gerekli
def kullanici_sil(kullanici_adi):
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi in kullanicilar:
        del kullanicilar[kullanici_adi]
        data["kullanicilar"] = kullanicilar
        _veri_yaz(data)
        flash(f"'{kullanici_adi}' silindi.", "success")
    else:
        flash("Kullanıcı bulunamadı.", "danger")
    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/kullanici/<kullanici_adi>/baglantilar", methods=["POST"])
@admin_gerekli
def kullanici_baglantilar(kullanici_adi):
    baglanti = request.form.get("baglanti", "")
    if baglanti not in {"tumu", "oturumu_kapat", "oturumlari_sifirla"}:
        flash("Geçersiz işlem.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    flash("Bağlantı işlemi simüle edildi.", "info")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/veritabani")
@admin_gerekli
def veritabani_goruntule():
    data = _veri_oku()
    for k in data.get("kullanicilar", {}).values():
        k["sifre"] = "***"
    return jsonify(data)


@admin_bp.route("/ayarlar", methods=["GET", "POST"])
@admin_gerekli
def ayarlar():
    veri = _veri_oku()
    uygulama_ayarlari = veri.get("uygulama_ayarlari", {
        "kayit_acik": True,
        "bakim_modu": False,
        "max_kullanici": 1000,
        "uygulama_adi": "JKB",
        "duyuru": "",
        "admin_kayit_yasak": False,
        "admin_ikinci_kontrol": True,
    })
    if request.method == "POST":
        uygulama_ayarlari["kayit_acik"] = "kayit_acik" in request.form
        uygulama_ayarlari["bakim_modu"] = "bakim_modu" in request.form
        uygulama_ayarlari["admin_kayit_yasak"] = "admin_kayit_yasak" in request.form
        uygulama_ayarlari["admin_ikinci_kontrol"] = "admin_ikinci_kontrol" in request.form
        uygulama_ayarlari["max_kullanici"] = int(request.form.get("max_kullanici", 1000))
        uygulama_ayarlari["uygulama_adi"] = request.form.get("uygulama_adi", "JKB").strip()
        uygulama_ayarlari["duyuru"] = request.form.get("duyuru", "").strip()
        veri["uygulama_ayarlari"] = uygulama_ayarlari
        _veri_yaz(veri)
        flash("Ayarlar kaydedildi.", "success")
        return redirect(url_for("admin.ayarlar"))
    return render_template("admin_ayarlar.html", ayarlar=uygulama_ayarlari)

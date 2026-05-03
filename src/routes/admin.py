import datetime
import os
import json
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


# ── Admin Giriş ───────────────────────────────────────────────────────────────

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
        else:
            hata = "Şifre hatalı!"
    return render_template("admin_giris.html", hata=hata)


@admin_bp.route("/cikis")
def admin_cikis():
    session.pop("admin_giris", None)
    session.pop("admin_giris_zamani", None)
    return redirect(url_for("admin.admin_giris"))


# ── Ana Panel ─────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@admin_gerekli
def admin_panel():
    data = db.veri_oku()
    kullanicilar = data.get("kullanicilar", {})

    toplam_kullanici = len(kullanicilar)
    toplam_gorev = sum(len(v.get("gorevler", [])) for v in kullanicilar.values())
    tamamlanan_gorev = sum(
        sum(1 for g in v.get("gorevler", []) if g.get("tamamlandi"))
        for v in kullanicilar.values()
    )
    toplam_fitness = sum(len(v.get("fitness_gecmisi", [])) for v in kullanicilar.values())
    toplam_antrenman = sum(len(v.get("antrenman_kayitlari", [])) for v in kullanicilar.values())

    db_boyutu = 0
    try:
        db_boyutu = os.path.getsize(db.dosya_yolu)
    except Exception:
        pass

    kullanici_ozet = []
    for ad, v in kullanicilar.items():
        kullanici_ozet.append({
            "ad": ad,
            "eposta": v.get("eposta", "—"),
            "telefon": v.get("telefon", "—"),
            "gorev_sayisi": len(v.get("gorevler", [])),
            "fitness_kayit": len(v.get("fitness_gecmisi", [])),
            "antrenman": len(v.get("antrenman_kayitlari", [])),
            "not_uzunluk": len(v.get("notlar", "")),
            "hedef": v.get("fitness_profil", {}).get("hedef", "—"),
            "seviye": v.get("fitness_profil", {}).get("seviye", "—"),
        })

    return render_template(
        "admin_panel.html",
        toplam_kullanici=toplam_kullanici,
        toplam_gorev=toplam_gorev,
        tamamlanan_gorev=tamamlanan_gorev,
        toplam_fitness=toplam_fitness,
        toplam_antrenman=toplam_antrenman,
        db_boyutu=db_boyutu,
        kullanici_ozet=kullanici_ozet,
        giris_zamani=session.get("admin_giris_zamani", "—"),
    )


# ── Kullanıcı Detay ───────────────────────────────────────────────────────────

@admin_bp.route("/kullanici/<kullanici_adi>")
@admin_gerekli
def kullanici_detay(kullanici_adi):
    data = db.veri_oku()
    kullanici = data.get("kullanicilar", {}).get(kullanici_adi)
    if not kullanici:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    return render_template("admin_kullanici.html",
                           ad=kullanici_adi,
                           kullanici=kullanici)


# ── Kullanıcı Sil ─────────────────────────────────────────────────────────────

@admin_bp.route("/kullanici/<kullanici_adi>/sil", methods=["POST"])
@admin_gerekli
def kullanici_sil(kullanici_adi):
    import src.data.kimlik_dogrulama as _kd_mod
    with _kd_mod._dosya_kilidi:
        try:
            with open(db.dosya_yolu, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"kullanicilar": {}}
        if kullanici_adi in data.get("kullanicilar", {}):
            del data["kullanicilar"][kullanici_adi]
            db._guvensiz_yaz(data)
            flash(f"'{kullanici_adi}' silindi.", "success")
        else:
            flash("Kullanıcı bulunamadı.", "danger")
    return redirect(url_for("admin.admin_panel"))


# ── Kullanıcı Şifre Sıfırla ───────────────────────────────────────────────────

@admin_bp.route("/kullanici/<kullanici_adi>/sifre-sifirla", methods=["POST"])
@admin_gerekli
def kullanici_sifre_sifirla(kullanici_adi):
    import src.data.kimlik_dogrulama as _kd_mod
    yeni_sifre = request.form.get("yeni_sifre", "").strip()
    if len(yeni_sifre) < 6:
        flash("Şifre en az 6 karakter olmalı.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    with _kd_mod._dosya_kilidi:
        try:
            with open(db.dosya_yolu, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"kullanicilar": {}}
        if kullanici_adi in data.get("kullanicilar", {}):
            data["kullanicilar"][kullanici_adi]["sifre"] = yeni_sifre
            db._guvensiz_yaz(data)
            flash(f"'{kullanici_adi}' şifresi güncellendi.", "success")
        else:
            flash("Kullanıcı bulunamadı.", "danger")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


# ── Kullanıcı E-posta Güncelle ────────────────────────────────────────────────

@admin_bp.route("/kullanici/<kullanici_adi>/eposta-guncelle", methods=["POST"])
@admin_gerekli
def kullanici_eposta_guncelle(kullanici_adi):
    import src.data.kimlik_dogrulama as _kd_mod
    yeni_eposta = request.form.get("eposta", "").strip().lower()
    if "@" not in yeni_eposta:
        flash("Geçerli bir e-posta girin.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    with _kd_mod._dosya_kilidi:
        try:
            with open(db.dosya_yolu, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"kullanicilar": {}}
        if kullanici_adi in data.get("kullanicilar", {}):
            data["kullanicilar"][kullanici_adi]["eposta"] = yeni_eposta
            db._guvensiz_yaz(data)
            flash("E-posta güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


# ── Kullanıcı Verilerini Temizle ──────────────────────────────────────────────

@admin_bp.route("/kullanici/<kullanici_adi>/temizle", methods=["POST"])
@admin_gerekli
def kullanici_temizle(kullanici_adi):
    import src.data.kimlik_dogrulama as _kd_mod
    alan = request.form.get("alan", "")
    temizlenebilir = {
        "gorevler": [],
        "fitness_gecmisi": [],
        "antrenman_kayitlari": [],
        "su_kayitlari": {},
        "hatirlaticilar": [],
        "notlar": "",
        "fitness_profil": {},
    }
    if alan not in temizlenebilir:
        flash("Geçersiz alan.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    with _kd_mod._dosya_kilidi:
        try:
            with open(db.dosya_yolu, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"kullanicilar": {}}
        if kullanici_adi in data.get("kullanicilar", {}):
            data["kullanicilar"][kullanici_adi][alan] = temizlenebilir[alan]
            db._guvensiz_yaz(data)
            flash(f"'{alan}' verisi temizlendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


# ── Ham Veritabanı Görüntüle (JSON) ──────────────────────────────────────────

@admin_bp.route("/veritabani")
@admin_gerekli
def veritabani_goruntule():
    data = db.veri_oku()
    # Şifreleri gizle
    for k in data.get("kullanicilar", {}).values():
        k["sifre"] = "***"
    return jsonify(data)


# ── Uygulama Ayarları ─────────────────────────────────────────────────────────

@admin_bp.route("/ayarlar", methods=["GET", "POST"])
@admin_gerekli
def ayarlar():
    import src.data.kimlik_dogrulama as _kd_mod
    veri = db.veri_oku()
    uygulama_ayarlari = veri.get("uygulama_ayarlari", {
        "kayit_acik": True,
        "bakim_modu": False,
        "max_kullanici": 1000,
        "uygulama_adi": "JKB",
        "duyuru": "",
    })
    if request.method == "POST":
        uygulama_ayarlari["kayit_acik"] = "kayit_acik" in request.form
        uygulama_ayarlari["bakim_modu"] = "bakim_modu" in request.form
        uygulama_ayarlari["max_kullanici"] = int(request.form.get("max_kullanici", 1000))
        uygulama_ayarlari["uygulama_adi"] = request.form.get("uygulama_adi", "JKB").strip()
        uygulama_ayarlari["duyuru"] = request.form.get("duyuru", "").strip()
        with _kd_mod._dosya_kilidi:
            try:
                with open(db.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"kullanicilar": {}}
            data["uygulama_ayarlari"] = uygulama_ayarlari
            db._guvensiz_yaz(data)
        flash("Ayarlar kaydedildi.", "success")
        return redirect(url_for("admin.ayarlar"))
    return render_template("admin_ayarlar.html", ayarlar=uygulama_ayarlari)

"""
JKB Moderatör Paneli
Moderatörler: kullanıcı listesi (salt-okunur), kilitleme/açma, duyuru gönderme.
Yapamadıkları: silme, rol değiştirme, şifre, site konfigürasyonu, ham DB.
"""
import datetime
import os
from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from src.data.veri_yoneticisi import VeriYoneticisi

moderator_bp = Blueprint("moderator", __name__, url_prefix="/moderator")
db = VeriYoneticisi()


def mod_veya_admin_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("mod_giris") and not session.get("admin_giris"):
            return redirect(url_for("moderator.mod_giris_sayfasi"))
        return f(*args, **kwargs)
    return decorated


def _rol_kontrol():
    """Giriş yapan kullanıcının moderatör/admin olduğunu doğrula."""
    kullanici = session.get("kullanici")
    if not kullanici:
        return False
    data = db.veri_oku()
    rol = data.get("kullanicilar", {}).get(kullanici, {}).get("rol", "user")
    return rol in ("moderator", "admin")


@moderator_bp.route("/giris", methods=["GET", "POST"])
def mod_giris_sayfasi():
    if session.get("mod_giris") or session.get("admin_giris"):
        return redirect(url_for("moderator.mod_panel"))
    hata = None
    if request.method == "POST":
        if _rol_kontrol():
            session["mod_giris"] = True
            session["mod_giris_zamani"] = datetime.datetime.now().isoformat()
            return redirect(url_for("moderator.mod_panel"))
        else:
            hata = "Bu hesabın moderatör veya admin yetkisi yok."
    return render_template("moderator_giris.html", hata=hata)


@moderator_bp.route("/kullanici-girisi")
def kullanici_ile_giris():
    """Profil sayfasından tek tıkla moderatör paneline geçiş."""
    if not session.get("kullanici"):
        return redirect(url_for("auth.giris"))
    if not _rol_kontrol():
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("panel.profil"))
    session["mod_giris"] = True
    session["mod_giris_zamani"] = datetime.datetime.now().isoformat()
    return redirect(url_for("moderator.mod_panel"))


@moderator_bp.route("/cikis")
def mod_cikis():
    session.pop("mod_giris", None)
    session.pop("mod_giris_zamani", None)
    return redirect(url_for("moderator.mod_giris_sayfasi"))


@moderator_bp.route("/")
@mod_veya_admin_gerekli
def mod_panel():
    data = db.veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    istatistik = {
        "toplam_kullanici": len(kullanicilar),
        "kilitli": sum(1 for v in kullanicilar.values() if v.get("kilitli")),
        "admin_sayisi": sum(1 for v in kullanicilar.values() if v.get("rol") == "admin"),
        "mod_sayisi": sum(1 for v in kullanicilar.values() if v.get("rol") == "moderator"),
        "toplam_gorev": sum(len(v.get("gorevler", [])) for v in kullanicilar.values()),
    }
    kullanici_liste = []
    for ad, v in kullanicilar.items():
        kullanici_liste.append({
            "ad": ad,
            "rol": v.get("rol", "user"),
            "eposta": v.get("eposta", "—"),
            "kilitli": v.get("kilitli", False),
            "durum": v.get("durum", "aktif"),
            "gorev_sayisi": len(v.get("gorevler", [])),
        })
    duyurular = data.get("uygulama_ayarlari", {}).get("duyuru", "")
    return render_template(
        "moderator_panel.html",
        istatistik=istatistik,
        kullanici_liste=kullanici_liste,
        duyuru=duyurular,
        giris_zamani=session.get("mod_giris_zamani", "—"),
        mod_kullanici=session.get("kullanici", "—"),
        active_page="panel",
    )


@moderator_bp.route("/kullanici/<kullanici_adi>/kilitle", methods=["POST"])
@mod_veya_admin_gerekli
def kullanici_kilitle(kullanici_adi):
    data = db.veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("moderator.mod_panel"))
    hedef_rol = kullanicilar[kullanici_adi].get("rol", "user")
    if hedef_rol in ("admin", "moderator"):
        flash("Admin veya moderatör hesabı kilitlenemez.", "danger")
        return redirect(url_for("moderator.mod_panel"))
    kilitli = not kullanicilar[kullanici_adi].get("kilitli", False)
    kullanicilar[kullanici_adi]["kilitli"] = kilitli
    kullanicilar[kullanici_adi]["durum"] = "kilitli" if kilitli else "aktif"
    data["kullanicilar"] = kullanicilar
    db.veri_yaz(data)
    flash(f"'{kullanici_adi}' {'kilitlendi' if kilitli else 'kilidi açıldı'}.", "success")
    return redirect(url_for("moderator.mod_panel"))


@moderator_bp.route("/duyuru", methods=["POST"])
@mod_veya_admin_gerekli
def duyuru_gonder():
    metin = request.form.get("duyuru", "").strip()
    data = db.veri_oku()
    ayarlar = data.get("uygulama_ayarlari", {})
    ayarlar["duyuru"] = metin[:500]
    data["uygulama_ayarlari"] = ayarlar
    db.veri_yaz(data)
    flash("Duyuru güncellendi.", "success")
    return redirect(url_for("moderator.mod_panel"))

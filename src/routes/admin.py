import copy
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

# ── Varsayılan Konfigürasyon ───────────────────────────────────────────────────

VARSAYILAN_NAVBAR = [
    {"id": "ana",      "label": "Ana Sayfa",  "href": "/panel",    "icon": "bi-house-door",       "aktif": True,  "siralama": 0,  "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "fitness",  "label": "Fitness",    "href": "/fitness",  "icon": "bi-activity",          "aktif": True,  "siralama": 1,  "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "gorevler", "label": "Görevler",   "href": "/gorevler", "icon": "bi-check2-square",     "aktif": True,  "siralama": 2,  "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "notlar",   "label": "Notlar",     "href": "/notlar",   "icon": "bi-journal-text",      "aktif": True,  "siralama": 3,  "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "profil",   "label": "Profil",     "href": "/profil",   "icon": "bi-person-circle",     "aktif": True,  "siralama": 4,  "sadece_giris": True,  "sadece_cikis": False, "stil": "accent"},
    {"id": "cikis",    "label": "Çıkış",      "href": "/cikis",    "icon": "bi-box-arrow-right",   "aktif": True,  "siralama": 5,  "sadece_giris": True,  "sadece_cikis": False, "stil": "danger"},
    {"id": "giris",    "label": "Giriş Yap",  "href": "/giris",    "icon": "bi-box-arrow-in-right","aktif": True,  "siralama": 0,  "sadece_giris": False, "sadece_cikis": True,  "stil": "primary"},
    {"id": "kayit",    "label": "Kayıt Ol",   "href": "/kayit",    "icon": "bi-person-plus",       "aktif": True,  "siralama": 1,  "sadece_giris": False, "sadece_cikis": True,  "stil": "secondary"},
]

VARSAYILAN_GORUNTUM = {
    "navbar_arka":        "linear-gradient(90deg, #8a4b12 0%, #b35f16 46%, #d77b22 100%)",
    "birincil_renk":      "#e94560",
    "site_basligi":       "JKB",
    "karsilama_baslik_1": "Daha düzenli.",
    "karsilama_baslik_2": "Daha güçlü.",
    "karsilama_pill":     "Kişisel yönetim • fitness • odak",
    "karsilama_metin":    "JKB; gününü, bedenini ve hedeflerini tek bir sade akışta toplar.",
    "karsilama_alt":      "Başlamak için doğru yerdesiniz.",
    "karsilama_dipnot":   "Güvenli · Ücretsiz · Kişisel",
    "imza_metin":         "Made By Picak",
    "imza_goster":        True,
}

VARSAYILAN_SAYFALAR = [
    {"id": "panel",    "label": "Ana Panel",     "href": "/panel",    "aktif": True,  "aciklama": "Kullanıcı dashboard'u"},
    {"id": "fitness",  "label": "Fitness Koçu",  "href": "/fitness",  "aktif": True,  "aciklama": "VKİ, antrenman, su takibi"},
    {"id": "gorevler", "label": "Görevler",      "href": "/gorevler", "aktif": True,  "aciklama": "Yapılacaklar listesi"},
    {"id": "notlar",   "label": "Notlar",        "href": "/notlar",   "aktif": True,  "aciklama": "Kişisel notlar"},
    {"id": "profil",   "label": "Profil",        "href": "/profil",   "aktif": True,  "aciklama": "Kullanıcı profili ve ayarları"},
    {"id": "giris",    "label": "Giriş Sayfası", "href": "/giris",    "aktif": True,  "aciklama": "Kullanıcı girişi"},
    {"id": "kayit",    "label": "Kayıt Sayfası", "href": "/kayit",    "aktif": True,  "aciklama": "Yeni kullanıcı kaydı"},
]


def get_site_konfig():
    """Veritabanından site konfigürasyonunu oku; yoksa varsayılan döndür."""
    data = db.veri_oku()
    konfig = data.get("site_konfig", {})
    return {
        "navbar_linkleri": konfig.get("navbar_linkleri", copy.deepcopy(VARSAYILAN_NAVBAR)),
        "goruntum":        konfig.get("goruntum",        copy.deepcopy(VARSAYILAN_GORUNTUM)),
        "sayfalar":        konfig.get("sayfalar",        copy.deepcopy(VARSAYILAN_SAYFALAR)),
    }


def save_site_konfig(konfig):
    data = db.veri_oku()
    data["site_konfig"] = konfig
    db.veri_yaz(data)


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
        hata = "Şifre hatalı!"
    return render_template("admin_giris.html", hata=hata)


@admin_bp.route("/cikis")
def admin_cikis():
    session.pop("admin_giris", None)
    session.pop("admin_giris_zamani", None)
    return redirect(url_for("admin.admin_giris"))


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@admin_gerekli
def admin_panel():
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    stats = _statlar(data)
    kullanici_ozet = []
    for ad, v in kullanicilar.items():
        kullanici_ozet.append({
            "ad": ad,
            "eposta": v.get("eposta", "—"),
            "gorev_sayisi": len(v.get("gorevler", [])),
            "fitness_kayit": len(v.get("fitness_gecmisi", [])),
            "antrenman": len(v.get("antrenman_kayitlari", [])),
            "hedef": v.get("fitness_profil", {}).get("hedef", "—"),
            "rol": v.get("rol", "user"),
            "kilitli": v.get("kilitli", False),
        })
    return render_template(
        "admin_panel.html",
        **stats,
        db_boyutu=os.path.getsize(db.dosya_yolu) if os.path.exists(db.dosya_yolu) else 0,
        kullanici_ozet=kullanici_ozet,
        giris_zamani=session.get("admin_giris_zamani", "—"),
        active_page="dashboard",
    )


# ── Navbar Yöneticisi ─────────────────────────────────────────────────────────

@admin_bp.route("/navbar", methods=["GET", "POST"])
@admin_gerekli
def navbar_yoneticisi():
    konfig = get_site_konfig()
    if request.method == "POST":
        raw_order = request.form.get("siralama_json", "[]")
        try:
            siralama = json.loads(raw_order)  # [{"id":..., "aktif":..., "label":..., "icon":..., "stil":...}, ...]
        except Exception:
            siralama = []

        nav_links = []
        for i, item in enumerate(siralama):
            link_id = item.get("id", "")
            kaynak = next((x for x in konfig["navbar_linkleri"] if x["id"] == link_id), None)
            if not kaynak:
                kaynak = next((x for x in VARSAYILAN_NAVBAR if x["id"] == link_id), {})
            link = dict(kaynak)
            link["siralama"] = i
            link["aktif"] = bool(item.get("aktif", True))
            link["label"] = item.get("label", link.get("label", ""))[:40]
            link["icon"] = item.get("icon", link.get("icon", "bi-circle"))
            link["stil"] = item.get("stil", link.get("stil", ""))
            nav_links.append(link)

        konfig["navbar_linkleri"] = nav_links
        save_site_konfig(konfig)
        flash("Navbar güncellendi.", "success")
        return redirect(url_for("admin.navbar_yoneticisi"))

    giris_links = sorted(
        [x for x in konfig["navbar_linkleri"] if x.get("sadece_giris")],
        key=lambda x: x.get("siralama", 99)
    )
    cikis_links = sorted(
        [x for x in konfig["navbar_linkleri"] if x.get("sadece_cikis")],
        key=lambda x: x.get("siralama", 99)
    )
    return render_template(
        "admin_navbar.html",
        giris_links=giris_links,
        cikis_links=cikis_links,
        giris_zamani=session.get("admin_giris_zamani", "—"),
        active_page="navbar",
    )


@admin_bp.route("/navbar/sifirla", methods=["POST"])
@admin_gerekli
def navbar_sifirla():
    konfig = get_site_konfig()
    konfig["navbar_linkleri"] = copy.deepcopy(VARSAYILAN_NAVBAR)
    save_site_konfig(konfig)
    flash("Navbar varsayılana sıfırlandı.", "success")
    return redirect(url_for("admin.navbar_yoneticisi"))


# ── Görünüm & Tema ────────────────────────────────────────────────────────────

@admin_bp.route("/goruntum", methods=["GET", "POST"])
@admin_gerekli
def goruntum_yoneticisi():
    konfig = get_site_konfig()
    goruntum = konfig.get("goruntum", copy.deepcopy(VARSAYILAN_GORUNTUM))
    if request.method == "POST":
        goruntum["navbar_arka"]        = request.form.get("navbar_arka", goruntum["navbar_arka"]).strip()
        goruntum["birincil_renk"]      = request.form.get("birincil_renk", goruntum["birincil_renk"]).strip()
        goruntum["site_basligi"]       = request.form.get("site_basligi", goruntum["site_basligi"]).strip()[:40]
        goruntum["karsilama_baslik_1"] = request.form.get("karsilama_baslik_1", goruntum["karsilama_baslik_1"]).strip()[:80]
        goruntum["karsilama_baslik_2"] = request.form.get("karsilama_baslik_2", goruntum["karsilama_baslik_2"]).strip()[:80]
        goruntum["karsilama_pill"]     = request.form.get("karsilama_pill", goruntum["karsilama_pill"]).strip()[:100]
        goruntum["karsilama_metin"]    = request.form.get("karsilama_metin", goruntum["karsilama_metin"]).strip()[:300]
        goruntum["karsilama_alt"]      = request.form.get("karsilama_alt", goruntum["karsilama_alt"]).strip()[:150]
        goruntum["karsilama_dipnot"]   = request.form.get("karsilama_dipnot", goruntum["karsilama_dipnot"]).strip()[:80]
        goruntum["imza_metin"]         = request.form.get("imza_metin", goruntum["imza_metin"]).strip()[:40]
        goruntum["imza_goster"]        = "imza_goster" in request.form
        konfig["goruntum"] = goruntum
        save_site_konfig(konfig)
        flash("Görünüm ayarları kaydedildi.", "success")
        return redirect(url_for("admin.goruntum_yoneticisi"))
    return render_template(
        "admin_goruntum.html",
        goruntum=goruntum,
        giris_zamani=session.get("admin_giris_zamani", "—"),
        active_page="goruntum",
    )


@admin_bp.route("/goruntum/sifirla", methods=["POST"])
@admin_gerekli
def goruntum_sifirla():
    konfig = get_site_konfig()
    konfig["goruntum"] = copy.deepcopy(VARSAYILAN_GORUNTUM)
    save_site_konfig(konfig)
    flash("Görünüm varsayılana sıfırlandı.", "success")
    return redirect(url_for("admin.goruntum_yoneticisi"))


# ── Kullanıcı Yönetimi ────────────────────────────────────────────────────────

@admin_bp.route("/kullanici/<kullanici_adi>")
@admin_gerekli
def kullanici_detay(kullanici_adi):
    data = _veri_oku()
    kullanici = data.get("kullanicilar", {}).get(kullanici_adi)
    if not kullanici:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    return render_template("admin_kullanici.html", ad=kullanici_adi, kullanici=kullanici,
                           giris_zamani=session.get("admin_giris_zamani", "—"), active_page="dashboard")


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
    flash("Durum güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/pin", methods=["POST"])
@admin_gerekli
def kullanici_pin(kullanici_adi):
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    if kullanici_adi not in kullanicilar:
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    kullanicilar[kullanici_adi]["admin_pinli"] = not kullanicilar[kullanici_adi].get("admin_pinli", False)
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    flash("Sabitleme güncellendi.", "success")
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
        "gorevler": [], "fitness_gecmisi": [], "antrenman_kayitlari": [],
        "su_kayitlari": {}, "hatirlaticilar": [], "notlar": "", "fitness_profil": {},
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


# ── Veritabanı & Ayarlar ──────────────────────────────────────────────────────

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
        "kayit_acik": True, "bakim_modu": False, "max_kullanici": 1000,
        "uygulama_adi": "JKB", "duyuru": "", "admin_kayit_yasak": False,
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
    return render_template("admin_ayarlar.html", ayarlar=uygulama_ayarlari,
                           giris_zamani=session.get("admin_giris_zamani", "—"), active_page="ayarlar")

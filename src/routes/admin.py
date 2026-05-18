import copy
import datetime
import os
import json
import shutil
import secrets
from functools import wraps
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for, flash, jsonify, send_file)
from src.data.veri_yoneticisi import VeriYoneticisi
from src.data.kimlik_dogrulama import _sifre_hashle

admin_bp = Blueprint("admin", __name__, url_prefix="/yonetici")
db = VeriYoneticisi()

ADMIN_SIFRE = os.environ.get("ADMIN_SIFRE", "JKB@admin2026!")

# ── Varsayılan Konfigürasyon ───────────────────────────────────────────────────

VARSAYILAN_NAVBAR = [
    {"id": "ana",      "label": "Ana Sayfa",  "href": "/panel",    "icon": "bi-house-door",        "aktif": True,  "siralama": 0, "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "fitness",  "label": "Fitness",    "href": "/fitness",  "icon": "bi-activity",           "aktif": True,  "siralama": 1, "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "gorevler", "label": "Görevler",   "href": "/gorevler", "icon": "bi-check2-square",      "aktif": True,  "siralama": 2, "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "notlar",   "label": "Notlar",     "href": "/notlar",   "icon": "bi-journal-text",       "aktif": True,  "siralama": 3, "sadece_giris": True,  "sadece_cikis": False, "stil": ""},
    {"id": "profil",   "label": "Profil",     "href": "/profil",   "icon": "bi-person-circle",      "aktif": True,  "siralama": 4, "sadece_giris": True,  "sadece_cikis": False, "stil": "accent"},
    {"id": "cikis",    "label": "Çıkış",      "href": "/cikis",    "icon": "bi-box-arrow-right",    "aktif": True,  "siralama": 5, "sadece_giris": True,  "sadece_cikis": False, "stil": "danger"},
    {"id": "giris",    "label": "Giriş Yap",  "href": "/giris",    "icon": "bi-box-arrow-in-right", "aktif": True,  "siralama": 0, "sadece_giris": False, "sadece_cikis": True,  "stil": "primary"},
    {"id": "kayit",    "label": "Kayıt Ol",   "href": "/kayit",    "icon": "bi-person-plus",        "aktif": True,  "siralama": 1, "sadece_giris": False, "sadece_cikis": True,  "stil": "secondary"},
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
    {"id": "panel",    "label": "Ana Panel",     "href": "/panel",    "aktif": True, "aciklama": "Kullanıcı gösterge paneli"},
    {"id": "fitness",  "label": "Fitness Koçu",  "href": "/fitness",  "aktif": True, "aciklama": "VKİ, antrenman, su takibi"},
    {"id": "gorevler", "label": "Görevler",      "href": "/gorevler", "aktif": True, "aciklama": "Yapılacaklar listesi"},
    {"id": "notlar",   "label": "Notlar",        "href": "/notlar",   "aktif": True, "aciklama": "Kişisel notlar"},
    {"id": "profil",   "label": "Profil",        "href": "/profil",   "aktif": True, "aciklama": "Kullanıcı profili ve ayarları"},
    {"id": "giris",    "label": "Giriş Sayfası", "href": "/giris",    "aktif": True, "aciklama": "Kullanıcı girişi"},
    {"id": "kayit",    "label": "Kayıt Sayfası", "href": "/kayit",    "aktif": True, "aciklama": "Yeni kullanıcı kaydı"},
]


def get_site_konfig():
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


_ADMIN_SESSION_SURESI = 4 * 3600  # 4 saat (saniye)


def admin_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_giris"):
            return redirect(url_for("admin.admin_giris"))
        # Session timeout kontrolü
        giris_zamani = session.get("admin_giris_zamani")
        if giris_zamani:
            try:
                giris_dt = datetime.datetime.strptime(giris_zamani, "%Y-%m-%d %H:%M:%S")
                gecen = (datetime.datetime.now() - giris_dt).total_seconds()
                if gecen > _ADMIN_SESSION_SURESI:
                    session.pop("admin_giris", None)
                    session.pop("admin_giris_zamani", None)
                    flash("Oturum süresi doldu. Lütfen tekrar giriş yapın.", "warning")
                    return redirect(url_for("admin.admin_giris"))
            except Exception:
                pass
        return f(*args, **kwargs)
    return decorated


def _veri_oku():
    return db.veri_oku()


def _veri_yaz(data):
    db.veri_yaz(data)


def _statlar(data):
    kullanicilar = data.get("kullanicilar", {})
    return {
        "toplam_kullanici":  len(kullanicilar),
        "toplam_gorev":      sum(len(v.get("gorevler", [])) for v in kullanicilar.values()),
        "tamamlanan_gorev":  sum(sum(1 for g in v.get("gorevler", []) if g.get("tamamlandi")) for v in kullanicilar.values()),
        "toplam_fitness":    sum(len(v.get("fitness_gecmisi", [])) for v in kullanicilar.values()),
        "toplam_antrenman":  sum(len(v.get("antrenman_kayitlari", [])) for v in kullanicilar.values()),
        "toplam_su":         sum(len(v.get("su_kayitlari", {})) for v in kullanicilar.values()),
        "toplam_hatirlatici":sum(len(v.get("hatirlaticilar", [])) for v in kullanicilar.values()),
        "kilitli_sayisi":    sum(1 for v in kullanicilar.values() if v.get("kilitli")),
    }


def _kullanici_ozet_listesi(data):
    kullanicilar = data.get("kullanicilar", {})
    liste = []
    for ad, v in kullanicilar.items():
        liste.append({
            "ad":           ad,
            "eposta":       v.get("eposta", "—"),
            "gorev_sayisi": len(v.get("gorevler", [])),
            "fitness_kayit":len(v.get("fitness_gecmisi", [])),
            "antrenman":    len(v.get("antrenman_kayitlari", [])),
            "hedef":        v.get("fitness_profil", {}).get("hedef", "—"),
            "rol":          v.get("rol", "user"),
            "kilitli":      v.get("kilitli", False),
            "durum":        v.get("durum", "aktif"),
            "kayit_tarihi": v.get("kayit_tarihi", "—"),
            "son_giris":    v.get("son_giris", "—"),
            "giris_sayaci": v.get("giris_sayaci", 0),
            "admin_pinli":  v.get("admin_pinli", False),
        })
    # Pinli kullanıcılar üste, sonra kayıt tarihine göre yeni→eski
    liste.sort(key=lambda x: (not x["admin_pinli"], x["kayit_tarihi"] or ""), reverse=True)
    return liste


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
            session["admin_giris_zamani"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.sistem_log_ekle("Yönetici Girişi", "Admin paneline giriş yapıldı.", seviye="uyari", kullanici="admin")
            return redirect(url_for("admin.admin_panel"))
        db.sistem_log_ekle("Başarısız Yönetici Girişi", "Admin paneli yanlış şifre.", seviye="hata", kullanici="admin")
        hata = "Şifre hatalı!"
    return render_template("admin_giris.html", hata=hata)


@admin_bp.route("/kullanici-girisi")
def kullanici_ile_giris():
    kullanici_adi = session.get("kullanici")
    if not kullanici_adi:
        return redirect(url_for("auth.giris"))
    data = _veri_oku()
    rol = data.get("kullanicilar", {}).get(kullanici_adi, {}).get("rol", "user")
    if rol != "admin":
        flash("Bu sayfaya erişim yetkiniz yok.", "danger")
        return redirect(url_for("panel.profil"))
    session["admin_giris"] = True
    session["admin_giris_zamani"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/cikis")
def admin_cikis():
    db.sistem_log_ekle("Yönetici Çıkışı", "Admin panelinden çıkış yapıldı.", seviye="bilgi", kullanici="admin")
    session.pop("admin_giris", None)
    session.pop("admin_giris_zamani", None)
    return redirect(url_for("admin.admin_giris"))


# ── Gösterge Paneli (Dashboard) ───────────────────────────────────────────────

@admin_bp.route("/")
@admin_gerekli
def admin_panel():
    data = _veri_oku()
    stats = _statlar(data)
    kullanici_ozet = _kullanici_ozet_listesi(data)
    db_yolu = db.dosya_yolu
    db_boyutu = os.path.getsize(db_yolu) if os.path.exists(db_yolu) else 0
    return render_template(
        "admin_panel.html",
        **stats,
        db_boyutu=db_boyutu,
        kullanici_ozet=kullanici_ozet,
        giris_zamani=session.get("admin_giris_zamani", "—"),
        active_page="panel",
    )


# ── Canlı İstatistik API (AJAX) ───────────────────────────────────────────────

@admin_bp.route("/api/istatistik")
@admin_gerekli
def api_istatistik():
    data = _veri_oku()
    stats = _statlar(data)
    db_yolu = db.dosya_yolu
    stats["db_boyutu_kb"] = round(os.path.getsize(db_yolu) / 1024, 1) if os.path.exists(db_yolu) else 0
    stats["zaman"] = datetime.datetime.now().strftime("%H:%M:%S")
    return jsonify(stats)


# ── Kullanıcı Oluştur ─────────────────────────────────────────────────────────

@admin_bp.route("/kullanici-olustur", methods=["GET", "POST"])
@admin_gerekli
def kullanici_olustur():
    if request.method == "POST":
        k_adi   = request.form.get("kullanici_adi", "").strip()
        eposta  = request.form.get("eposta", "").strip()
        sifre   = request.form.get("sifre", "").strip()
        rol     = request.form.get("rol", "user")
        if rol not in {"user", "moderator", "admin"}:
            rol = "user"
        basari, mesaj = db.kayit_et(k_adi, sifre, eposta)
        if basari:
            if rol != "user":
                db._kullanici_guncelle(k_adi, "rol", rol)
            db.sistem_log_ekle(
                "Admin Kullanıcı Oluşturdu",
                f"'{k_adi}' ({eposta}) — rol: {rol}",
                seviye="basari", kullanici="admin",
            )
            flash(f"'{k_adi}' başarıyla oluşturuldu.", "success")
            return redirect(url_for("admin.kullanici_detay", kullanici_adi=k_adi))
        flash(mesaj, "danger")
    return render_template("admin_kullanici_olustur.html",
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="panel")


# ── Navbar Yöneticisi ─────────────────────────────────────────────────────────

@admin_bp.route("/navbar", methods=["GET", "POST"])
@admin_gerekli
def navbar_yoneticisi():
    konfig = get_site_konfig()
    if request.method == "POST":
        raw_order = request.form.get("siralama_json", "[]")
        try:
            siralama = json.loads(raw_order)
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
            link["aktif"]    = bool(item.get("aktif", True))
            link["label"]    = item.get("label", link.get("label", ""))[:40]
            link["icon"]     = item.get("icon",  link.get("icon", "bi-circle"))
            link["stil"]     = item.get("stil",  link.get("stil", ""))
            nav_links.append(link)
        konfig["navbar_linkleri"] = nav_links
        save_site_konfig(konfig)
        flash("Navbar güncellendi.", "success")
        return redirect(url_for("admin.navbar_yoneticisi"))
    giris_links = sorted([x for x in konfig["navbar_linkleri"] if x.get("sadece_giris")],
                         key=lambda x: x.get("siralama", 99))
    cikis_links = sorted([x for x in konfig["navbar_linkleri"] if x.get("sadece_cikis")],
                         key=lambda x: x.get("siralama", 99))
    return render_template("admin_navbar.html",
                           giris_links=giris_links, cikis_links=cikis_links,
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="navbar")


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
        for alan in ["navbar_arka", "birincil_renk", "site_basligi",
                     "karsilama_baslik_1", "karsilama_baslik_2",
                     "karsilama_pill", "karsilama_metin", "karsilama_alt",
                     "karsilama_dipnot", "imza_metin"]:
            goruntum[alan] = request.form.get(alan, goruntum.get(alan, "")).strip()
        goruntum["imza_goster"] = "imza_goster" in request.form
        konfig["goruntum"] = goruntum
        save_site_konfig(konfig)
        flash("Görünüm ayarları kaydedildi.", "success")
        return redirect(url_for("admin.goruntum_yoneticisi"))
    return render_template("admin_goruntum.html",
                           goruntum=goruntum,
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="goruntum")


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
    return render_template("admin_kullanici.html",
                           ad=kullanici_adi, kullanici=kullanici,
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="panel")


@admin_bp.route("/kullanici/<kullanici_adi>/rol", methods=["POST"])
@admin_gerekli
def kullanici_rol_guncelle(kullanici_adi):
    rol = request.form.get("rol", "user")
    if rol not in {"user", "moderator", "admin"}:
        flash("Geçersiz rol.", "danger")
        return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))
    data = _veri_oku()
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    data["kullanicilar"][kullanici_adi]["rol"] = rol
    if rol == "admin":
        data["kullanicilar"][kullanici_adi]["admin_token"] = secrets.token_urlsafe(12)
    _veri_yaz(data)
    db.sistem_log_ekle("Rol Değiştirildi", f"'{kullanici_adi}' → {rol}", seviye="uyari", kullanici="admin")
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
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    data["kullanicilar"][kullanici_adi]["durum"] = durum
    data["kullanicilar"][kullanici_adi]["kilitli"] = (durum == "kilitli")
    _veri_yaz(data)
    db.sistem_log_ekle("Durum Değiştirildi", f"'{kullanici_adi}' → {durum}", seviye="uyari", kullanici="admin")
    flash("Durum güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/pin", methods=["POST"])
@admin_gerekli
def kullanici_pin(kullanici_adi):
    data = _veri_oku()
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    mevcut = data["kullanicilar"][kullanici_adi].get("admin_pinli", False)
    data["kullanicilar"][kullanici_adi]["admin_pinli"] = not mevcut
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
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    data["kullanicilar"][kullanici_adi]["sifre"] = _sifre_hashle(yeni_sifre)
    data["kullanicilar"][kullanici_adi]["sifre_degisim_tarihi"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _veri_yaz(data)
    db.sistem_log_ekle("Şifre Sıfırlandı (Admin)", f"'{kullanici_adi}' şifresi admin tarafından sıfırlandı.", seviye="uyari", kullanici="admin")
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
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    data["kullanicilar"][kullanici_adi]["eposta"] = yeni_eposta
    _veri_yaz(data)
    flash("E-posta güncellendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/not-guncelle", methods=["POST"])
@admin_gerekli
def kullanici_not_guncelle(kullanici_adi):
    admin_notu = request.form.get("admin_notu", "").strip()[:500]
    data = _veri_oku()
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    data["kullanicilar"][kullanici_adi]["admin_notu"] = admin_notu
    _veri_yaz(data)
    flash("Admin notu kaydedildi.", "success")
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
    if kullanici_adi not in data.get("kullanicilar", {}):
        flash("Kullanıcı bulunamadı.", "danger")
        return redirect(url_for("admin.admin_panel"))
    data["kullanicilar"][kullanici_adi][alan] = temizlenebilir[alan]
    _veri_yaz(data)
    db.sistem_log_ekle("Veri Temizlendi", f"'{kullanici_adi}' — alan: {alan}", seviye="uyari", kullanici="admin")
    flash(f"'{alan}' verisi temizlendi.", "success")
    return redirect(url_for("admin.kullanici_detay", kullanici_adi=kullanici_adi))


@admin_bp.route("/kullanici/<kullanici_adi>/sil", methods=["POST"])
@admin_gerekli
def kullanici_sil(kullanici_adi):
    data = _veri_oku()
    if kullanici_adi in data.get("kullanicilar", {}):
        del data["kullanicilar"][kullanici_adi]
        _veri_yaz(data)
        db.sistem_log_ekle("Kullanıcı Silindi", f"'{kullanici_adi}' kalıcı olarak silindi.", seviye="hata", kullanici="admin")
        flash(f"'{kullanici_adi}' silindi.", "success")
    else:
        flash("Kullanıcı bulunamadı.", "danger")
    return redirect(url_for("admin.admin_panel"))


# ── Toplu İşlemler ────────────────────────────────────────────────────────────

@admin_bp.route("/toplu-islem", methods=["POST"])
@admin_gerekli
def toplu_islem():
    islem = request.form.get("islem", "")
    secili = request.form.getlist("secili_kullanicilar")
    if not secili:
        flash("Hiç kullanıcı seçilmedi.", "warning")
        return redirect(url_for("admin.admin_panel"))
    data = _veri_oku()
    kullanicilar = data.get("kullanicilar", {})
    sayac = 0
    for k_adi in secili:
        if k_adi not in kullanicilar:
            continue
        if islem == "kilitle":
            kullanicilar[k_adi]["kilitli"] = True
            kullanicilar[k_adi]["durum"] = "kilitli"
            sayac += 1
        elif islem == "aktif_et":
            kullanicilar[k_adi]["kilitli"] = False
            kullanicilar[k_adi]["durum"] = "aktif"
            sayac += 1
        elif islem == "sil":
            del kullanicilar[k_adi]
            sayac += 1
    data["kullanicilar"] = kullanicilar
    _veri_yaz(data)
    db.sistem_log_ekle("Toplu İşlem", f"{islem} — {sayac} kullanıcı", seviye="uyari", kullanici="admin")
    flash(f"{sayac} kullanıcıya '{islem}' uygulandı.", "success")
    return redirect(url_for("admin.admin_panel"))


# ── Sistem Günlüğü ────────────────────────────────────────────────────────────

@admin_bp.route("/sistem-log")
@admin_gerekli
def sistem_log():
    filtre = request.args.get("filtre", "")
    son_n  = int(request.args.get("n", 200))
    log_kayitlari = db.sistem_log_getir(son_n)
    if filtre:
        log_kayitlari = [l for l in log_kayitlari if filtre.lower() in l.get("olay", "").lower()
                         or filtre.lower() in l.get("detay", "").lower()
                         or filtre.lower() in l.get("kullanici", "").lower()]
    return render_template("admin_log.html",
                           log_kayitlari=log_kayitlari,
                           filtre=filtre,
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="log")


@admin_bp.route("/sistem-log/temizle", methods=["POST"])
@admin_gerekli
def sistem_log_temizle():
    data = _veri_oku()
    data["sistem_log"] = []
    _veri_yaz(data)
    flash("Sistem günlüğü temizlendi.", "success")
    return redirect(url_for("admin.sistem_log"))


# ── Yedekleme ─────────────────────────────────────────────────────────────────

@admin_bp.route("/yedek")
@admin_gerekli
def yedek_sayfasi():
    yedek_klasoru = os.path.join(os.path.dirname(db.dosya_yolu), "yedekler")
    yedekler = []
    if os.path.exists(yedek_klasoru):
        for dosya in sorted(os.listdir(yedek_klasoru), reverse=True):
            if dosya.endswith(".json"):
                tam_yol = os.path.join(yedek_klasoru, dosya)
                boyut   = os.path.getsize(tam_yol)
                yedekler.append({"ad": dosya, "boyut_kb": round(boyut / 1024, 1)})
    return render_template("admin_yedek.html",
                           yedekler=yedekler,
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="yedek")


@admin_bp.route("/yedek/olustur", methods=["POST"])
@admin_gerekli
def yedek_olustur():
    yedek_klasoru = os.path.join(os.path.dirname(db.dosya_yolu), "yedekler")
    os.makedirs(yedek_klasoru, exist_ok=True)
    zaman_damgasi = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    hedef = os.path.join(yedek_klasoru, f"yedek_{zaman_damgasi}.json")
    shutil.copy2(db.dosya_yolu, hedef)
    # Eski yedekleri sil (en fazla 10 tut)
    tum_yedekler = sorted([f for f in os.listdir(yedek_klasoru) if f.endswith(".json")])
    while len(tum_yedekler) > 10:
        os.unlink(os.path.join(yedek_klasoru, tum_yedekler.pop(0)))
    db.sistem_log_ekle("Yedek Oluşturuldu", f"yedek_{zaman_damgasi}.json", seviye="basari", kullanici="admin")
    flash(f"Yedek oluşturuldu: yedek_{zaman_damgasi}.json", "success")
    return redirect(url_for("admin.yedek_sayfasi"))


@admin_bp.route("/yedek/indir/<dosya_adi>")
@admin_gerekli
def yedek_indir(dosya_adi):
    yedek_klasoru = os.path.join(os.path.dirname(db.dosya_yolu), "yedekler")
    tam_yol = os.path.join(yedek_klasoru, dosya_adi)
    if not os.path.exists(tam_yol) or not dosya_adi.endswith(".json"):
        flash("Dosya bulunamadı.", "danger")
        return redirect(url_for("admin.yedek_sayfasi"))
    return send_file(tam_yol, as_attachment=True, download_name=dosya_adi)


@admin_bp.route("/yedek/sil/<dosya_adi>", methods=["POST"])
@admin_gerekli
def yedek_sil(dosya_adi):
    yedek_klasoru = os.path.join(os.path.dirname(db.dosya_yolu), "yedekler")
    tam_yol = os.path.join(yedek_klasoru, dosya_adi)
    if os.path.exists(tam_yol) and dosya_adi.endswith(".json"):
        os.unlink(tam_yol)
        flash(f"'{dosya_adi}' silindi.", "success")
    return redirect(url_for("admin.yedek_sayfasi"))


@admin_bp.route("/yedek/canli-indir")
@admin_gerekli
def canli_yedek_indir():
    """Anlık veritabanını indir (yedek oluşturmadan)."""
    zaman = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(db.dosya_yolu, as_attachment=True,
                     download_name=f"veritabani_{zaman}.json")


# ── Uygulama Ayarları ─────────────────────────────────────────────────────────

@admin_bp.route("/ayarlar", methods=["GET", "POST"])
@admin_gerekli
def ayarlar():
    veri = _veri_oku()
    ua = veri.get("uygulama_ayarlari", {
        "kayit_acik": True, "bakim_modu": False, "max_kullanici": 1000,
        "uygulama_adi": "JKB", "duyuru": "", "admin_kayit_yasak": False,
        "admin_ikinci_kontrol": True, "duyuru_turu": "info",
        "giris_denemesi_limiti": 10, "oturum_suresi_dk": 1440,
    })
    if request.method == "POST":
        ua["kayit_acik"]            = "kayit_acik" in request.form
        ua["bakim_modu"]            = "bakim_modu" in request.form
        ua["admin_kayit_yasak"]     = "admin_kayit_yasak" in request.form
        ua["admin_ikinci_kontrol"]  = "admin_ikinci_kontrol" in request.form
        ua["max_kullanici"]         = max(1, int(request.form.get("max_kullanici", 1000)))
        ua["uygulama_adi"]          = request.form.get("uygulama_adi", "JKB").strip()[:40]
        ua["duyuru"]                = request.form.get("duyuru", "").strip()[:500]
        ua["duyuru_turu"]           = request.form.get("duyuru_turu", "info")
        ua["giris_denemesi_limiti"] = max(3, int(request.form.get("giris_denemesi_limiti", 10)))
        ua["oturum_suresi_dk"]      = max(5, int(request.form.get("oturum_suresi_dk", 1440)))
        veri["uygulama_ayarlari"]   = ua
        _veri_yaz(veri)
        db.sistem_log_ekle("Ayarlar Değiştirildi", "Uygulama ayarları güncellendi.", seviye="bilgi", kullanici="admin")
        flash("Ayarlar kaydedildi.", "success")
        return redirect(url_for("admin.ayarlar"))
    return render_template("admin_ayarlar.html",
                           ayarlar=ua,
                           giris_zamani=session.get("admin_giris_zamani", "—"),
                           active_page="ayarlar")


# ── Ham Veritabanı ────────────────────────────────────────────────────────────

@admin_bp.route("/veritabani")
@admin_gerekli
def veritabani_goruntule():
    data = _veri_oku()
    for k in data.get("kullanicilar", {}).values():
        k["sifre"] = "***"
    return jsonify(data)

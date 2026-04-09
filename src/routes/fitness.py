import datetime
import hashlib
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from src.data.veri_yoneticisi import VeriYoneticisi
from src.assets.hesaplamalar import FitnessZekasi
from src.routes.panel import giris_gerekli

fitness = Blueprint("fitness", __name__)
db = VeriYoneticisi()

AKTIVITELER = [
    "Hareketsiz (Masa başı)",
    "Az Aktif (1-2 gün/hafta)",
    "Orta Aktif (3-5 gün/hafta)",
    "Çok Aktif (6-7 gün/hafta)",
    "Profesyonel Sporcu",
]
HEDEFLER = ["Fit Kal", "Kilo Ver", "Hızlı Kilo Ver", "Kas Yap", "Hızlı Kas Yap", "Kuvvet Kazan"]
SEVIYELER = ["Başlangıç", "Orta", "İleri"]

MOTIVASYON_SOZLERI = [
    "Bugün acı çek, yarın kazanman için.",
    "Bedenine inanmak, hedefe yürümektir.",
    "Her büyük güç, küçük bir başlangıçtan doğar.",
    "Vücut başarır, zihin yönlendirir.",
    "Antrenman bitince hissedeceğin o gururu düşün.",
    "Rahatsızlık alanından çık, büyüme oradan başlar.",
    "Dün daha iyiydin. Bugün daha güçlüsün.",
    "Sonuçlar bir günde değil, günler içinde oluşur.",
    "Hareketsizlik paslandırır, hareket parlatır.",
    "Yarın için bugün ter dök.",
    "Hata yap, öğren, tekrar dene — dur asla.",
    "Hedefin küçük görünse de yürümeyi bırakma.",
    "Her damla ter, bir adım daha yakın.",
    "Güç dışarıdan değil, içinden gelir.",
    "Bugün yorgunsan, yarın daha güçlü olursun.",
    "İraden kaslarından güçlü olmalı.",
    "Vücuduna iyi davranırsan, o da sana iyi davranır.",
    "En iyi antrenman, yaptığın antrenmandır.",
    "Her tekrar, seni dünden biraz daha ileriye götürür.",
    "Kendini zorla, sınırlarını gör, sonra aş.",
    "Uyku, beslenme, antrenman — üçü bir arada zafer.",
    "Mükemmel zaman yok. Şimdi başla.",
    "Bedenin seni dinler. Onu doğru yönlendir.",
    "Küçük ilerlemeler büyük farklar yaratır.",
    "Bugün vazgeçmek, yarın tekrar başlamak zorunda kalmaktır.",
    "Disiplin, motivasyonun tükendiği yerde devreye girer.",
    "Her gün biraz, her hafta fark, her ay dönüşüm.",
    "Bir şeyler yapabileceğine inanırsan, yaparsın.",
    "Bedenin en büyük projedir — her gün çalış.",
    "Şikayet etme. Çalış.",
    "Zor olan yolu seç. Kolay olan seni nereye götüreceğini zaten biliyorsun.",
    "Başarı, her gün tekrarlanan küçük çabaların toplamıdır.",
    "Sınırların sadece zihnindedir.",
    "Antrenmanın zor olduğunda, amacını hatırla.",
    "Bugün kendinin en iyi versiyonu ol.",
]


def _sonuc_profil_ile(profil):
    """Kayıtlı profilden analiz sonucu oluştur."""
    if not profil:
        return None
    try:
        sonuc = FitnessZekasi.analiz_et(
            profil["boy"], profil["kilo"], profil["yas"],
            profil["cinsiyet"], profil["seviye"], profil["hedef"],
            profil["aktivite"], profil.get("baslangic_tarihi", "")
        )
        sonuc.update({
            "kilo": profil["kilo"], "boy": profil["boy"],
            "yas": profil["yas"], "cinsiyet": profil["cinsiyet"],
            "aktivite": profil["aktivite"],
        })
        return sonuc
    except (KeyError, ValueError, TypeError):
        return None


@fitness.route("/fitness", methods=["GET", "POST"])
@giris_gerekli
def fitness_sayfasi():
    kullanici = session["kullanici"]
    profil = db.fitness_profil_getir(kullanici)
    gecmis = db.fitness_verisi_getir(kullanici)
    sonuc = None
    hata = None
    show_tab = "analiz"

    if request.method == "POST":
        try:
            boy = float(request.form["boy"])
            kilo = float(request.form["kilo"])
            yas = int(request.form["yas"])
            cinsiyet = request.form["cinsiyet"]
            aktivite = request.form["aktivite"]
            hedef = request.form["hedef"]
            seviye = request.form["seviye"]
            baslangic = request.form.get("baslangic_tarihi", "") or profil.get("baslangic_tarihi", "")

            sonuc = FitnessZekasi.analiz_et(boy, kilo, yas, cinsiyet, seviye, hedef, aktivite, baslangic)
            sonuc.update({"kilo": kilo, "boy": boy, "yas": yas,
                          "cinsiyet": cinsiyet, "aktivite": aktivite})

            yeni_profil = {
                "boy": boy, "kilo": kilo, "yas": yas,
                "cinsiyet": cinsiyet, "aktivite": aktivite,
                "hedef": hedef, "seviye": seviye,
                "baslangic_tarihi": baslangic,
            }
            db.fitness_profil_kaydet(kullanici, yeni_profil)
            profil = yeni_profil

            kayit = {
                "tarih": datetime.date.today().isoformat(),
                "kilo": kilo, "vki": sonuc["vki"],
                "hedef_kalori": sonuc["hedef_kalori"],
            }
            db.fitness_verisi_kaydet(kullanici, kayit)
            gecmis = db.fitness_verisi_getir(kullanici)
            show_tab = "program"
        except (ValueError, KeyError) as e:
            hata = f"Lütfen tüm alanları doldurun. ({e})"

    # Profil varsa ama form gönderilmediyse profil üzerinden program yükle
    if sonuc is None and profil:
        sonuc = _sonuc_profil_ile(profil)
        if sonuc and request.method == "GET":
            show_tab = "program"

    ilerleme = FitnessZekasi.ilerleme_analizi(gecmis)

    # Su takibi
    bugun_str = datetime.date.today().isoformat()
    su_bugun = db.su_getir(kullanici, bugun_str)
    su_gecmis = db.su_gecmis_getir(kullanici, 7)

    # Antrenman takibi
    antrenman_gecmis = db.antrenman_gecmis_getir(kullanici, 5)
    seri = db.antrenman_seri_getir(kullanici)

    # Hatırlatıcılar
    hatirlaticilar = db.hatirlatici_getir(kullanici)

    # Günlük motivasyon
    h = int(hashlib.md5(f"{kullanici}{bugun_str}".encode()).hexdigest(), 16)
    motivasyon_soz = MOTIVASYON_SOZLERI[h % len(MOTIVASYON_SOZLERI)]

    return render_template(
        "fitness.html",
        sonuc=sonuc, profil=profil,
        gecmis=gecmis[-5:][::-1],
        ilerleme=ilerleme, hata=hata,
        aktiviteler=AKTIVITELER, hedefler=HEDEFLER, seviyeler=SEVIYELER,
        show_tab=show_tab,
        su_bugun=su_bugun, su_gecmis=su_gecmis,
        antrenman_gecmis=antrenman_gecmis, seri=seri,
        hatirlaticilar=hatirlaticilar,
        motivasyon_soz=motivasyon_soz,
        bugun=bugun_str,
    )


# ── API Endpoint'leri ──────────────────────────────────────────────────────────

@fitness.route("/api/fitness/su", methods=["GET", "POST"])
@giris_gerekli
def api_su():
    kullanici = session["kullanici"]
    bugun = datetime.date.today().isoformat()
    if request.method == "POST":
        miktar = request.get_json(silent=True) or {}
        yeni = max(0, min(20, int(miktar.get("miktar", 0))))
        db.su_guncelle(kullanici, bugun, yeni)
    mevcut = db.su_getir(kullanici, bugun)
    return jsonify({"bugun": mevcut, "hedef": 8, "lt": round(mevcut * 0.25, 2)})


@fitness.route("/api/fitness/antrenman", methods=["POST"])
@giris_gerekli
def api_antrenman():
    kullanici = session["kullanici"]
    data = request.get_json(silent=True) or {}
    kayit = {
        "tarih": datetime.date.today().isoformat(),
        "program": data.get("program", ""),
        "sure": data.get("sure", 0),
        "egzersizler": data.get("egzersizler", []),
    }
    db.antrenman_kaydet(kullanici, kayit)
    seri = db.antrenman_seri_getir(kullanici)
    return jsonify({"basari": True, "seri": seri})


@fitness.route("/api/fitness/hatirlaticilar", methods=["GET", "POST"])
@giris_gerekli
def api_hatirlaticilar():
    kullanici = session["kullanici"]
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        hatirlaticilar = data.get("hatirlaticilar", [])
        db.hatirlatici_kaydet(kullanici, hatirlaticilar)
        return jsonify({"basari": True})
    return jsonify(db.hatirlatici_getir(kullanici))


@fitness.route("/api/fitness/motivasyon")
@giris_gerekli
def api_motivasyon():
    kullanici = session["kullanici"]
    bugun = datetime.date.today().isoformat()
    seri = db.antrenman_seri_getir(kullanici)
    h = int(hashlib.md5(f"{kullanici}{bugun}".encode()).hexdigest(), 16)
    soz = MOTIVASYON_SOZLERI[h % len(MOTIVASYON_SOZLERI)]
    return jsonify({"soz": soz, "seri": seri})

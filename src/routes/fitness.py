import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from src.data.kimlik_dogrulama import KimlikDogrulama
from src.assets.hesaplamalar import FitnessZekasi
from src.routes.panel import giris_gerekli

fitness = Blueprint("fitness", __name__)
db = KimlikDogrulama()

AKTIVITELER = [
    "Hareketsiz (Masa başı)",
    "Az Aktif (1-2 gün/hafta)",
    "Orta Aktif (3-5 gün/hafta)",
    "Çok Aktif (6-7 gün/hafta)",
    "Profesyonel Sporcu",
]
HEDEFLER = ["Fit Kal", "Kilo Ver", "Hızlı Kilo Ver", "Kas Yap", "Hızlı Kas Yap", "Kuvvet Kazan"]
SEVIYELER = ["Başlangıç", "Orta", "İleri"]


@fitness.route("/fitness", methods=["GET", "POST"])
@giris_gerekli
def fitness_sayfasi():
    kullanici = session["kullanici"]
    sonuc = None
    profil = db.fitness_profil_getir(kullanici)
    gecmis = db.fitness_verisi_getir(kullanici)
    hata = None

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
            sonuc["kilo"] = kilo
            sonuc["boy"] = boy
            sonuc["yas"] = yas
            sonuc["cinsiyet"] = cinsiyet
            sonuc["aktivite"] = aktivite

            yeni_profil = {
                "boy": boy, "kilo": kilo, "yas": yas,
                "cinsiyet": cinsiyet, "aktivite": aktivite,
                "hedef": hedef, "seviye": seviye,
                "baslangic_tarihi": baslangic,
            }
            db.fitness_profil_kaydet(kullanici, yeni_profil)

            kayit = {
                "tarih": datetime.date.today().isoformat(),
                "kilo": kilo, "vki": sonuc["vki"],
                "hedef_kalori": sonuc["hedef_kalori"],
            }
            db.fitness_verisi_kaydet(kullanici, kayit)
            gecmis = db.fitness_verisi_getir(kullanici)
        except (ValueError, KeyError) as e:
            hata = f"Lütfen tüm alanları doldurun. ({e})"

    ilerleme = FitnessZekasi.ilerleme_analizi(gecmis)

    return render_template(
        "fitness.html",
        sonuc=sonuc, profil=profil, gecmis=gecmis[-5:][::-1],
        ilerleme=ilerleme, hata=hata,
        aktiviteler=AKTIVITELER, hedefler=HEDEFLER, seviyeler=SEVIYELER,
    )

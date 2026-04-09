from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from functools import wraps

panel = Blueprint("panel", __name__)


def giris_gerekli(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("kullanici"):
            return redirect(url_for("auth.giris"))
        return f(*args, **kwargs)
    return decorated


@panel.route("/panel")
@giris_gerekli
def ana_panel():
    from src.data.kimlik_dogrulama import KimlikDogrulama
    db = KimlikDogrulama()
    kullanici = session["kullanici"]

    gorevler = db.gorev_getir(kullanici)
    gorev_toplam = len(gorevler)
    gorev_tamamlandi = sum(1 for g in gorevler if g.get("tamamlandi"))

    gecmis = db.fitness_verisi_getir(kullanici)
    son_kilo = gecmis[-1]["kilo"] if gecmis else None
    son_vki = f"VKİ: {gecmis[-1]['vki']}" if gecmis else None
    fitness_kayit = len(gecmis)

    notlar = db.not_getir(kullanici)
    not_ozet = (notlar[:80] + "...") if len(notlar) > 80 else notlar

    return render_template(
        "panel.html",
        kullanici=kullanici,
        gorev_toplam=gorev_toplam,
        gorev_tamamlandi=gorev_tamamlandi,
        son_kilo=son_kilo,
        son_vki=son_vki,
        fitness_kayit=fitness_kayit,
        not_ozet=not_ozet,
    )


@panel.route("/profil")
@giris_gerekli
def profil():
    from src.data.kimlik_dogrulama import KimlikDogrulama
    db = KimlikDogrulama()
    kullanici = session["kullanici"]
    bilgi = db.kullanici_bilgi_getir(kullanici)
    return render_template("profil.html",
                           kullanici=kullanici,
                           eposta=bilgi.get("eposta", ""),
                           telefon=bilgi.get("telefon", ""))


@panel.route("/profil/sifre", methods=["POST"])
@giris_gerekli
def sifre_degistir():
    from src.data.kimlik_dogrulama import KimlikDogrulama
    db = KimlikDogrulama()
    kullanici = session["kullanici"]
    bilgi = db.kullanici_bilgi_getir(kullanici)

    eski = request.form.get("eski_sifre", "")
    yeni = request.form.get("yeni_sifre", "")
    yeni2 = request.form.get("yeni_sifre2", "")

    kwargs = dict(kullanici=kullanici,
                  eposta=bilgi.get("eposta", ""),
                  telefon=bilgi.get("telefon", ""))

    if yeni != yeni2:
        return render_template("profil.html", hata="Yeni şifreler uyuşmuyor!", **kwargs)
    basari, mesaj = db.sifre_degistir(kullanici, eski, yeni)
    if basari:
        return render_template("profil.html", basari=mesaj, **kwargs)
    return render_template("profil.html", hata=mesaj, **kwargs)


@panel.route("/profil/telefon", methods=["POST"])
@giris_gerekli
def telefon_guncelle():
    from src.data.kimlik_dogrulama import KimlikDogrulama
    db = KimlikDogrulama()
    kullanici = session["kullanici"]
    telefon = request.form.get("telefon", "").strip()
    db._kullanici_guncelle(kullanici, "telefon", telefon or "")
    if telefon:
        flash("Telefon numarası güncellendi.", "success")
    else:
        flash("Telefon numarası silindi.", "info")
    return redirect(url_for("panel.profil"))

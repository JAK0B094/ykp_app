from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.data.kimlik_dogrulama import KimlikDogrulama

auth = Blueprint("auth", __name__)
db = KimlikDogrulama()

@auth.route("/giris", methods=["GET", "POST"])
def giris():
    if session.get("kullanici"):
        return redirect(url_for("panel.ana_panel"))

    hata = None
    if request.method == "POST":
        kullanici_adi = request.form.get("kullanici_adi", "").strip()
        sifre = request.form.get("sifre", "")
        basari, mesaj = db.giris_kontrol(kullanici_adi, sifre)
        if basari:
            session["kullanici"] = kullanici_adi
            flash(f"Hoş geldin, {kullanici_adi}!", "success")
            return redirect(url_for("panel.ana_panel"))
        else:
            hata = mesaj

    return render_template("giris.html", hata=hata)


@auth.route("/kayit", methods=["GET", "POST"])
def kayit():
    if session.get("kullanici"):
        return redirect(url_for("panel.ana_panel"))

    hata = None
    basari_mesaj = None
    if request.method == "POST":
        kullanici_adi = request.form.get("kullanici_adi", "").strip()
        eposta = request.form.get("eposta", "").strip()
        sifre = request.form.get("sifre", "")
        sifre2 = request.form.get("sifre2", "")

        if sifre != sifre2:
            hata = "Şifreler uyuşmuyor!"
        else:
            basari, mesaj = db.kayit_et(kullanici_adi, sifre, eposta)
            if basari:
                basari_mesaj = mesaj
            else:
                hata = mesaj

    return render_template("kayit.html", hata=hata, basari_mesaj=basari_mesaj)


@auth.route("/cikis")
def cikis():
    kullanici = session.pop("kullanici", None)
    if kullanici:
        flash("Başarıyla çıkış yapıldı.", "info")
    return redirect(url_for("karsilama"))

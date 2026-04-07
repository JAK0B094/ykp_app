from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.data.kimlik_dogrulama import KimlikDogrulama
from src.routes.panel import giris_gerekli

notlar = Blueprint("notlar", __name__)
db = KimlikDogrulama()


@notlar.route("/notlar", methods=["GET", "POST"])
@giris_gerekli
def not_sayfasi():
    kullanici = session["kullanici"]
    if request.method == "POST":
        metin = request.form.get("metin", "")
        db.not_kaydet(kullanici, metin)
        flash("Notlar kaydedildi.", "success")
        return redirect(url_for("notlar.not_sayfasi"))
    metin = db.not_getir(kullanici)
    return render_template("notlar.html", metin=metin)

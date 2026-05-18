import uuid
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from src.data.kimlik_dogrulama import KimlikDogrulama
from src.routes.utils import giris_gerekli

gorevler = Blueprint("gorevler", __name__)
db = KimlikDogrulama()


@gorevler.route("/gorevler")
@giris_gerekli
def gorev_sayfasi():
    liste = db.gorev_getir(session["kullanici"])
    return render_template("gorevler.html", gorevler=liste)


@gorevler.route("/gorevler/ekle", methods=["POST"])
@giris_gerekli
def gorev_ekle():
    baslik = request.form.get("baslik", "").strip()
    if baslik:
        liste = db.gorev_getir(session["kullanici"])
        liste.append({
            "id": str(uuid.uuid4())[:8],
            "baslik": baslik[:200],
            "tamamlandi": False,
            "tarih": datetime.date.today().isoformat(),
        })
        db.gorev_kaydet(session["kullanici"], liste)
    return redirect(url_for("gorevler.gorev_sayfasi"))


@gorevler.route("/gorevler/durum/<gorev_id>", methods=["POST"])
@giris_gerekli
def gorev_durum(gorev_id):
    liste = db.gorev_getir(session["kullanici"])
    for g in liste:
        if g["id"] == gorev_id:
            g["tamamlandi"] = not g["tamamlandi"]
            break
    db.gorev_kaydet(session["kullanici"], liste)
    return redirect(url_for("gorevler.gorev_sayfasi"))


@gorevler.route("/gorevler/sil/<gorev_id>", methods=["POST"])
@giris_gerekli
def gorev_sil(gorev_id):
    liste = db.gorev_getir(session["kullanici"])
    liste = [g for g in liste if g["id"] != gorev_id]
    db.gorev_kaydet(session["kullanici"], liste)
    return redirect(url_for("gorevler.gorev_sayfasi"))

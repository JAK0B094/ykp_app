import uuid
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
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
        yeni = {
            "id": str(uuid.uuid4())[:8],
            "baslik": baslik[:200],
            "tamamlandi": False,
            "tarih": datetime.date.today().isoformat(),
        }
        try:
            db.gorev_ekle_atomik(session["kullanici"], yeni)
        except Exception as e:
            db.sistem_log_ekle("Görev Hatası", f"Ekleme başarısız: {e}", "hata", session["kullanici"])
    return redirect(url_for("gorevler.gorev_sayfasi"))


@gorevler.route("/gorevler/durum/<gorev_id>", methods=["POST"])
@giris_gerekli
def gorev_durum(gorev_id):
    try:
        db.gorev_durum_degistir_atomik(session["kullanici"], gorev_id)
    except Exception as e:
        db.sistem_log_ekle("Görev Hatası", f"Durum güncellenemedi ({gorev_id}): {e}", "hata", session["kullanici"])
    return redirect(url_for("gorevler.gorev_sayfasi"))


@gorevler.route("/gorevler/sil/<gorev_id>", methods=["POST"])
@giris_gerekli
def gorev_sil(gorev_id):
    try:
        db.gorev_sil_atomik(session["kullanici"], gorev_id)
    except Exception as e:
        db.sistem_log_ekle("Görev Hatası", f"Silme başarısız ({gorev_id}): {e}", "hata", session["kullanici"])
    return redirect(url_for("gorevler.gorev_sayfasi"))

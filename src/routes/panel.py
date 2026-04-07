from flask import Blueprint, render_template, session, redirect, url_for

panel = Blueprint("panel", __name__)

def giris_gerekli(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("kullanici"):
            return redirect(url_for("auth.giris"))
        return f(*args, **kwargs)
    return decorated

@panel.route("/panel")
@giris_gerekli
def ana_panel():
    return render_template("panel.html", kullanici=session["kullanici"])

@panel.route("/profil")
@giris_gerekli
def profil():
    return render_template("profil.html", kullanici=session["kullanici"])

import sys
import os
import copy

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, session, redirect, url_for, request
from src.routes.auth import auth
from src.routes.panel import panel
from src.routes.fitness import fitness
from src.routes.gorevler import gorevler
from src.routes.notlar import notlar
from src.routes.admin import admin_bp, get_site_konfig
from src.routes.moderator import moderator_bp

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.secret_key = os.environ.get("SECRET_KEY", "jkb-gizli-anahtar-2026")

app.register_blueprint(auth)
app.register_blueprint(panel)
app.register_blueprint(fitness)
app.register_blueprint(gorevler)
app.register_blueprint(notlar)
app.register_blueprint(admin_bp)
app.register_blueprint(moderator_bp)


@app.context_processor
def inject_site_konfig():
    """Tüm şablonlara site_konfig'i enjekte et."""
    try:
        konfig = get_site_konfig()
        return {"site_konfig": konfig}
    except Exception:
        return {"site_konfig": {"navbar_linkleri": [], "goruntum": {}, "sayfalar": []}}


@app.before_request
def bakim_modu_kontrol():
    """Bakım modunda yönetici dışındaki tüm istekleri engelle."""
    if request.path.startswith("/yonetici") or request.path.startswith("/static"):
        return
    try:
        from src.data.veri_yoneticisi import VeriYoneticisi
        db = VeriYoneticisi()
        ayarlar = db.veri_oku().get("uygulama_ayarlari", {})
        if ayarlar.get("bakim_modu", False):
            duyuru = ayarlar.get("duyuru", "")
            return render_template("bakim.html", duyuru=duyuru), 503
    except Exception:
        pass


@app.route("/")
def karsilama():
    return render_template("karsilama.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

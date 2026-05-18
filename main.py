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

# Bakım modu cache — her 30 saniyede bir DB'ye gidilir
_bakim_cache = {"aktif": False, "duyuru": "", "son_kontrol": 0.0}
_BAKIM_CACHE_TTL = 30  # saniye


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
    """Bakım modunda yönetici dışındaki tüm istekleri engelle. Cache ile verimli."""
    if request.path.startswith("/yonetici") or request.path.startswith("/static"):
        return
    import time
    global _bakim_cache
    simdi = time.time()
    if simdi - _bakim_cache["son_kontrol"] > _BAKIM_CACHE_TTL:
        try:
            from src.data.veri_yoneticisi import VeriYoneticisi
            db = VeriYoneticisi()
            ayarlar = db.veri_oku().get("uygulama_ayarlari", {})
            _bakim_cache["aktif"] = ayarlar.get("bakim_modu", False)
            _bakim_cache["duyuru"] = ayarlar.get("duyuru", "")
            _bakim_cache["son_kontrol"] = simdi
        except Exception:
            _bakim_cache["son_kontrol"] = simdi
    if _bakim_cache["aktif"]:
        return render_template("bakim.html", duyuru=_bakim_cache["duyuru"]), 503


@app.route("/")
def karsilama():
    return render_template("karsilama.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from src.routes.auth import auth
from src.routes.panel import panel
from src.routes.fitness import fitness
from src.routes.gorevler import gorevler
from src.routes.notlar import notlar

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.secret_key = os.environ.get("SECRET_KEY", "jkb-gizli-anahtar-2026")

app.register_blueprint(auth)
app.register_blueprint(panel)
app.register_blueprint(fitness)
app.register_blueprint(gorevler)
app.register_blueprint(notlar)


@app.route("/")
def karsilama():
    return render_template("karsilama.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

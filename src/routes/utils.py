from functools import wraps
from flask import session, redirect, url_for


def giris_gerekli(f):
    """Kullanıcı girişi gerektiren route'lar için dekoratör."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("kullanici"):
            return redirect(url_for("auth.giris"))
        return f(*args, **kwargs)
    return decorated

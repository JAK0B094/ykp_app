import os
import secrets
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import (Blueprint, flash, redirect, render_template,
                   request, session, url_for)
from src.data.kimlik_dogrulama import KimlikDogrulama

auth = Blueprint("auth", __name__)
db = KimlikDogrulama()


# ── Yardımcı: e-posta ile kullanıcı bul ───────────────────────────────────────
def _eposta_ile_kullanici_bul(eposta):
    data = db.veri_oku()
    for k, v in data.get("kullanicilar", {}).items():
        if v.get("eposta", "").lower() == eposta.lower():
            return k, v.get("eposta", "")
    return None, None


def _email_gonder(alici, otp):
    """OTP içeren e-posta gönder. SMTP ayarlanmamışsa konsola yazar."""
    host = os.environ.get("SMTP_HOST")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER")
    pwd = os.environ.get("SMTP_PASS")

    if not host or not user:
        print(f"[JKB OTP] {alici} → {otp}")
        return False  # e-posta gönderilmedi

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "JKB — Şifre Sıfırlama Kodu"
        msg["From"] = f"JKB <{user}>"
        msg["To"] = alici
        html = f"""
        <div style="font-family:sans-serif;max-width:420px;margin:auto;
                    background:#1a1a2e;color:#e0e0e0;border-radius:16px;padding:32px">
          <h2 style="color:#e94560;margin-bottom:8px">JKB — Şifre Sıfırla</h2>
          <p>Doğrulama kodunuz:</p>
          <div style="font-size:36px;font-weight:900;letter-spacing:10px;
                      color:#fff;background:#0f3460;border-radius:12px;
                      padding:16px 24px;text-align:center;margin:16px 0">
            {otp}
          </div>
          <p style="color:#888;font-size:13px">Bu kod 15 dakika geçerlidir.<br>
          Bu isteği siz yapmadıysanız, bu e-postayı yok sayın.</p>
        </div>
        """
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP(host, port, timeout=10) as s:
            s.ehlo(); s.starttls(); s.login(user, pwd)
            s.send_message(msg)
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False


# ── Giriş / Kayıt / Çıkış ─────────────────────────────────────────────────────

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
        telefon = request.form.get("telefon", "").strip()
        sifre = request.form.get("sifre", "")
        sifre2 = request.form.get("sifre2", "")

        if sifre != sifre2:
            hata = "Şifreler uyuşmuyor!"
        else:
            basari, mesaj = db.kayit_et(kullanici_adi, sifre, eposta)
            if basari:
                if telefon:
                    db._kullanici_guncelle(kullanici_adi, "telefon", telefon)
                basari_mesaj = mesaj
            else:
                hata = mesaj

    return render_template("kayit.html", hata=hata, basari_mesaj=basari_mesaj)


@auth.route("/cikis")
def cikis():
    kullanici = session.pop("kullanici", None)
    session.pop("reset_info", None)
    if kullanici:
        flash("Başarıyla çıkış yapıldı.", "info")
    return redirect(url_for("karsilama"))


# ── Şifre Sıfırlama (3 Adımlı OTP Akışı) ─────────────────────────────────────

@auth.route("/sifre-sifirla", methods=["GET", "POST"])
def sifre_sifirla():
    reset_info = session.get("reset_info", {})

    # GET: adım URL'den gelir
    adim = request.args.get("adim", "1")
    hata = None

    if request.method == "POST":
        adim = request.form.get("adim", "1")

        # ── Adım 1: E-posta doğrula & OTP üret ──
        if adim == "1":
            eposta = request.form.get("eposta", "").strip().lower()
            kullanici_adi, _ = _eposta_ile_kullanici_bul(eposta)

            # Güvenlik: her durumda adım 2'ye geç (kullanıcı adı doğrulaması gizle)
            if not kullanici_adi:
                hata = "Bu e-posta ile kayıtlı hesap bulunamadı."
                adim = "1"
            else:
                otp = str(secrets.randbelow(900000) + 100000)
                session["reset_info"] = {
                    "kullanici": kullanici_adi,
                    "eposta": eposta,
                    "otp": otp,
                    "son_tarih": time.time() + 900,  # 15 dakika
                    "denemeler": 0,
                    "otp_dogrulandi": False,
                }
                gonderildi = _email_gonder(eposta, otp)
                if not gonderildi:
                    # SMTP ayarlı değil: kodu flash ile göster (geliştirme modu)
                    flash(f"[Geliştirme Modu] Doğrulama kodu: {otp}", "warning")
                return redirect(url_for("auth.sifre_sifirla", adim="2"))

        # ── Adım 2: OTP doğrula ──
        elif adim == "2":
            reset_info = session.get("reset_info", {})
            if not reset_info or time.time() > reset_info.get("son_tarih", 0):
                flash("Oturum süresi dolmuş. Lütfen tekrar başlayın.", "danger")
                session.pop("reset_info", None)
                return redirect(url_for("auth.sifre_sifirla"))

            girilen = request.form.get("otp", "").strip().replace(" ", "")
            reset_info["denemeler"] = reset_info.get("denemeler", 0) + 1

            if reset_info["denemeler"] > 5:
                session.pop("reset_info", None)
                flash("Çok fazla hatalı deneme. Lütfen baştan başlayın.", "danger")
                return redirect(url_for("auth.sifre_sifirla"))

            if girilen != reset_info["otp"]:
                kalan = max(0, 5 - reset_info["denemeler"])
                session["reset_info"] = reset_info
                hata = f"Hatalı kod. {kalan} deneme hakkınız kaldı."
                adim = "2"
            else:
                reset_info["otp_dogrulandi"] = True
                session["reset_info"] = reset_info
                return redirect(url_for("auth.sifre_sifirla", adim="3"))

        # ── Adım 3: Yeni şifre ──
        elif adim == "3":
            reset_info = session.get("reset_info", {})
            if not reset_info or not reset_info.get("otp_dogrulandi"):
                flash("Geçersiz istek. Lütfen tekrar başlayın.", "danger")
                return redirect(url_for("auth.sifre_sifirla"))

            yeni = request.form.get("yeni_sifre", "")
            yeni2 = request.form.get("yeni_sifre2", "")

            if yeni != yeni2:
                hata = "Şifreler uyuşmuyor!"
                adim = "3"
            elif len(yeni) < 6 or len(yeni) > 32:
                hata = "Şifre 6-32 karakter arasında olmalıdır!"
                adim = "3"
            else:
                basari, mesaj = db.eposta_ile_sifre_sifirla(
                    reset_info["eposta"], yeni
                )
                session.pop("reset_info", None)
                if basari:
                    flash("Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.", "success")
                    return redirect(url_for("auth.giris"))
                else:
                    hata = mesaj
                    adim = "3"

    return render_template("sifre_sifirla.html",
                           adim=adim,
                           hata=hata,
                           reset_info=session.get("reset_info", {}))

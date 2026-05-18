import hashlib
import json
import os
import secrets
import threading
import tempfile
import shutil
import time
import datetime

# Uygulama genelinde tek bir kilit — çoklu kullanıcı/thread güvenliği
_dosya_kilidi = threading.Lock()

# ── Şifre Yardımcıları ─────────────────────────────────────────────────────────

def _sifre_hashle(sifre: str) -> str:
    """SHA-256 + rastgele salt ile şifre hashle. Format: salt$hash"""
    salt = secrets.token_hex(16)
    h = hashlib.sha256(f"{salt}{sifre}".encode("utf-8")).hexdigest()
    return f"{salt}${h}"


def _sifre_dogrula(sifre: str, kayitli: str) -> bool:
    """Kaydedilmiş hash ile girilen şifreyi doğrula. Düz metin geçişi de destekler."""
    if "$" in kayitli:
        salt, h = kayitli.split("$", 1)
        return hashlib.sha256(f"{salt}{sifre}".encode("utf-8")).hexdigest() == h
    # Eski düz metin şifre — doğrudan karşılaştır (sonra hash'e geçirilecek)
    return str(kayitli) == str(sifre)


# ── KimlikDogrulama Sınıfı ─────────────────────────────────────────────────────

class KimlikDogrulama:
    def __init__(self, dosya_yolu="src/data/veritabani.json"):
        self.dosya_yolu = os.path.abspath(dosya_yolu)
        self._baslangic_kontrol()

    def _baslangic_kontrol(self):
        """Veritabanı dosyası yoksa oluştur, bozuksa yedekten kurtar. Eksik alanları tamamla."""
        try:
            klasor = os.path.dirname(self.dosya_yolu)
            if klasor and not os.path.exists(klasor):
                os.makedirs(klasor, exist_ok=True)
            if not os.path.exists(self.dosya_yolu):
                self._guvensiz_yaz({"kullanicilar": {}, "sistem_log": []})
            else:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Mevcut kullanıcılarda eksik alanları tamamla (migration)
                degisti = False
                simdiki = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for k_adi, v in data.get("kullanicilar", {}).items():
                    if "kayit_tarihi" not in v:
                        v["kayit_tarihi"] = simdiki
                        degisti = True
                    if "son_giris" not in v:
                        v["son_giris"] = ""
                        degisti = True
                    if "giris_sayaci" not in v:
                        v["giris_sayaci"] = 0
                        degisti = True
                    if "durum" not in v:
                        v["durum"] = "aktif"
                        degisti = True
                    if "kilitli" not in v:
                        v["kilitli"] = False
                        degisti = True
                    if "admin_notu" not in v:
                        v["admin_notu"] = ""
                        degisti = True
                    if "rol" not in v:
                        v["rol"] = "user"
                        degisti = True
                if degisti:
                    self._guvensiz_yaz(data)
        except (json.JSONDecodeError, Exception):
            yedek = self.dosya_yolu + ".bak"
            try:
                shutil.copy2(self.dosya_yolu, yedek)
            except Exception:
                pass
            self._guvensiz_yaz({"kullanicilar": {}, "sistem_log": []})

    def _guvensiz_yaz(self, data):
        """Kilitsiz yazma — sadece iç kullanım. Atomik (tmp→rename)."""
        klasor = os.path.dirname(self.dosya_yolu)
        try:
            fd, tmp_yol = tempfile.mkstemp(dir=klasor or ".", suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            shutil.move(tmp_yol, self.dosya_yolu)
        except Exception:
            try:
                os.unlink(tmp_yol)
            except Exception:
                pass
            raise

    def veri_oku(self):
        """Thread-safe okuma. Hata durumunda boş yapı döner."""
        with _dosya_kilidi:
            for _ in range(3):
                try:
                    with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if not isinstance(data, dict):
                        return {"kullanicilar": {}, "sistem_log": []}
                    data.setdefault("kullanicilar", {})
                    data.setdefault("sistem_log", [])
                    return data
                except json.JSONDecodeError:
                    time.sleep(0.05)
                except FileNotFoundError:
                    self._guvensiz_yaz({"kullanicilar": {}, "sistem_log": []})
                    return {"kullanicilar": {}, "sistem_log": []}
                except Exception:
                    time.sleep(0.05)
            return {"kullanicilar": {}, "sistem_log": []}

    def veri_yaz(self, data):
        """Thread-safe atomik yazma. Yarım yazma asla olmaz."""
        with _dosya_kilidi:
            try:
                self._guvensiz_yaz(data)
            except Exception as e:
                raise IOError(f"Veritabanına yazılamadı: {e}")

    def _kullanici_guncelle(self, kullanici_adi, alan, deger):
        """Tek bir alanı güncellemek için kısa yol."""
        with _dosya_kilidi:
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"kullanicilar": {}, "sistem_log": []}
            if kullanici_adi in data.get("kullanicilar", {}):
                data["kullanicilar"][kullanici_adi][alan] = deger
                self._guvensiz_yaz(data)

    # ── Sistem Günlüğü ────────────────────────────────────────────────────────

    def sistem_log_ekle(self, olay, detay="", seviye="bilgi", kullanici="—"):
        """Sistem olayını günlüğe ekle. Thread-safe. Son 500 kayıt tutulur."""
        with _dosya_kilidi:
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"kullanicilar": {}, "sistem_log": []}
            data.setdefault("sistem_log", [])
            giris = {
                "zaman": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "olay": olay,
                "detay": detay[:300],
                "seviye": seviye,
                "kullanici": kullanici,
            }
            data["sistem_log"].append(giris)
            if len(data["sistem_log"]) > 500:
                data["sistem_log"] = data["sistem_log"][-500:]
            self._guvensiz_yaz(data)

    def sistem_log_getir(self, son_n=100):
        try:
            data = self.veri_oku()
            log = data.get("sistem_log", [])
            return list(reversed(log[-son_n:]))
        except Exception:
            return []

    # ── Kimlik Doğrulama ──────────────────────────────────────────────────────

    def giris_kontrol(self, kullanici_adi, sifre):
        if not kullanici_adi or not sifre:
            return False, "Kullanıcı adı ve şifre boş olamaz!"
        kullanici_adi = kullanici_adi.strip()
        try:
            with _dosya_kilidi:
                try:
                    with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    return False, "Sistem hatası: veritabanı okunamadı."
                kullanicilar = data.get("kullanicilar", {})
                if kullanici_adi not in kullanicilar:
                    return False, "Kullanıcı bulunamadı!"
                k = kullanicilar[kullanici_adi]
                if k.get("kilitli", False):
                    return False, "Bu hesap kilitlenmiştir. Yöneticiye başvurun."
                if k.get("durum", "aktif") == "pasif":
                    return False, "Bu hesap askıya alınmıştır."
                kayitli_sifre = str(k.get("sifre", ""))
                if not _sifre_dogrula(sifre, kayitli_sifre):
                    return False, "Şifre hatalı!"
                # Düz metin ise şeffaf migration: hash'e çevir
                if "$" not in kayitli_sifre:
                    kullanicilar[kullanici_adi]["sifre"] = _sifre_hashle(sifre)
                # Son giriş ve sayaç güncelle
                simdiki = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                kullanicilar[kullanici_adi]["son_giris"] = simdiki
                kullanicilar[kullanici_adi]["giris_sayaci"] = k.get("giris_sayaci", 0) + 1
                data["kullanicilar"] = kullanicilar
                self._guvensiz_yaz(data)
                return True, "Giriş başarılı!"
        except Exception as e:
            return False, f"Sistem hatası: {e}"

    def kayit_et(self, kullanici_adi, sifre, eposta):
        kullanici_adi = kullanici_adi.strip() if kullanici_adi else ""
        eposta = eposta.strip().lower() if eposta else ""

        if not kullanici_adi:
            return False, "Kullanıcı adı boş olamaz!"
        if len(kullanici_adi) < 3 or len(kullanici_adi) > 46:
            return False, "Kullanıcı adı 3-46 karakter arasında olmalıdır!"
        if not eposta or "@" not in eposta:
            return False, "Geçerli bir e-posta adresi girin!"
        if len(sifre) < 6 or len(sifre) > 32:
            return False, "Şifre 6-32 karakter arasında olmalıdır!"

        try:
            with _dosya_kilidi:
                try:
                    with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception:
                    data = {"kullanicilar": {}, "sistem_log": []}

                kullanicilar = data.get("kullanicilar", {})
                if kullanici_adi in kullanicilar:
                    return False, "Bu kullanıcı adı zaten alınmış!"
                for v in kullanicilar.values():
                    if v.get("eposta", "").lower() == eposta:
                        return False, "Bu e-posta adresi zaten kayıtlı!"

                simdiki = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                kullanicilar[kullanici_adi] = {
                    "sifre":              _sifre_hashle(sifre),
                    "eposta":             eposta,
                    "kayit_tarihi":       simdiki,
                    "son_giris":          "",
                    "giris_sayaci":       0,
                    "durum":              "aktif",
                    "kilitli":            False,
                    "rol":                "user",
                    "admin_notu":         "",
                    "fitness_gecmisi":    [],
                    "gorevler":           [],
                    "notlar":             "",
                    "fitness_profil":     {},
                    "antrenman_kayitlari":[],
                    "su_kayitlari":       {},
                    "hatirlaticilar":     [],
                }
                data["kullanicilar"] = kullanicilar
                data.setdefault("sistem_log", [])
                data["sistem_log"].append({
                    "zaman":    simdiki,
                    "olay":     "Yeni Kayıt",
                    "detay":    f"'{kullanici_adi}' kayıt oldu — {eposta}",
                    "seviye":   "basari",
                    "kullanici": kullanici_adi,
                })
                if len(data["sistem_log"]) > 500:
                    data["sistem_log"] = data["sistem_log"][-500:]
                self._guvensiz_yaz(data)
                return True, "Kayıt başarılı! Giriş yapabilirsiniz."
        except Exception as e:
            return False, f"Kayıt sırasında hata oluştu: {e}"

    def eposta_ile_sifre_sifirla(self, eposta, yeni_sifre):
        if len(yeni_sifre) < 6 or len(yeni_sifre) > 32:
            return False, "Şifre 6-32 karakter arasında olmalıdır!"
        eposta = eposta.strip().lower()
        try:
            with _dosya_kilidi:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k, v in data["kullanicilar"].items():
                    if v.get("eposta", "").lower() == eposta:
                        data["kullanicilar"][k]["sifre"] = _sifre_hashle(yeni_sifre)
                        data["kullanicilar"][k]["sifre_degisim_tarihi"] = (
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        self._guvensiz_yaz(data)
                        return True, "Şifre başarıyla güncellendi!"
            return False, "Bu e-posta ile kayıtlı kullanıcı bulunamadı!"
        except Exception as e:
            return False, f"Hata: {e}"

    def sifre_degistir(self, kullanici_adi, eski_sifre, yeni_sifre):
        basari, _ = self.giris_kontrol(kullanici_adi, eski_sifre)
        if not basari:
            return False, "Mevcut şifre hatalı!"
        if len(yeni_sifre) < 6 or len(yeni_sifre) > 32:
            return False, "Yeni şifre 6-32 karakter arasında olmalıdır!"
        try:
            self._kullanici_guncelle(kullanici_adi, "sifre", _sifre_hashle(yeni_sifre))
            self._kullanici_guncelle(
                kullanici_adi, "sifre_degisim_tarihi",
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            return True, "Şifre başarıyla değiştirildi!"
        except Exception as e:
            return False, f"Hata: {e}"

    # ── Fitness ───────────────────────────────────────────────────────────────

    def fitness_verisi_kaydet(self, kullanici_adi, yeni_veri):
        try:
            with _dosya_kilidi:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if kullanici_adi in data.get("kullanicilar", {}):
                    gecmis = data["kullanicilar"][kullanici_adi].setdefault("fitness_gecmisi", [])
                    gecmis.append(yeni_veri)
                    self._guvensiz_yaz(data)
        except Exception as e:
            raise IOError(f"Fitness verisi kaydedilemedi: {e}")

    def fitness_verisi_getir(self, kullanici_adi):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(kullanici_adi, {}).get("fitness_gecmisi", [])
        except Exception:
            return []

    def fitness_profil_kaydet(self, kullanici_adi, profil):
        self._kullanici_guncelle(kullanici_adi, "fitness_profil", profil)

    def fitness_profil_getir(self, kullanici_adi):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(kullanici_adi, {}).get("fitness_profil", {})
        except Exception:
            return {}

    # ── Görevler ──────────────────────────────────────────────────────────────

    def gorev_kaydet(self, kullanici_adi, gorevler):
        try:
            self._kullanici_guncelle(kullanici_adi, "gorevler", gorevler)
        except Exception as e:
            raise IOError(f"Görevler kaydedilemedi: {e}")

    def gorev_getir(self, kullanici_adi):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(kullanici_adi, {}).get("gorevler", [])
        except Exception:
            return []

    # ── Notlar ────────────────────────────────────────────────────────────────

    def not_kaydet(self, kullanici_adi, not_metni):
        try:
            self._kullanici_guncelle(kullanici_adi, "notlar", not_metni)
        except Exception as e:
            raise IOError(f"Not kaydedilemedi: {e}")

    def not_getir(self, kullanici_adi):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(kullanici_adi, {}).get("notlar", "")
        except Exception:
            return ""

    # ── Genel ─────────────────────────────────────────────────────────────────

    def kullanici_bilgi_getir(self, kullanici_adi):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(kullanici_adi, {})
        except Exception:
            return {}

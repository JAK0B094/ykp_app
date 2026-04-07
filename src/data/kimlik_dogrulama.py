import json
import os
import threading
import tempfile
import shutil
import time

# Uygulama genelinde tek bir kilit — çoklu kullanıcı/thread güvenliği
_dosya_kilidi = threading.Lock()

class KimlikDogrulama:
    def __init__(self, dosya_yolu="src/data/veritabani.json"):
        self.dosya_yolu = os.path.abspath(dosya_yolu)
        self._baslangic_kontrol()

    def _baslangic_kontrol(self):
        """Veritabanı dosyası yoksa oluştur, bozuksa yedekten kurtar."""
        try:
            klasor = os.path.dirname(self.dosya_yolu)
            if klasor and not os.path.exists(klasor):
                os.makedirs(klasor, exist_ok=True)
            if not os.path.exists(self.dosya_yolu):
                self._guvensiz_yaz({"kullanicilar": {}})
            else:
                # Dosya bozuk mu kontrol et
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    json.load(f)
        except (json.JSONDecodeError, Exception):
            # Bozuk dosyayı yedekle, temizden başla
            yedek = self.dosya_yolu + ".bak"
            try:
                shutil.copy2(self.dosya_yolu, yedek)
            except Exception:
                pass
            self._guvensiz_yaz({"kullanicilar": {}})

    def _guvensiz_yaz(self, data):
        """Kilitsiz yazma — sadece iç kullanım."""
        klasor = os.path.dirname(self.dosya_yolu)
        try:
            fd, tmp_yol = tempfile.mkstemp(dir=klasor or ".", suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
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
            for deneme in range(3):
                try:
                    with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if not isinstance(data, dict):
                        return {"kullanicilar": {}}
                    if "kullanicilar" not in data:
                        data["kullanicilar"] = {}
                    return data
                except json.JSONDecodeError:
                    time.sleep(0.05)
                except FileNotFoundError:
                    self._guvensiz_yaz({"kullanicilar": {}})
                    return {"kullanicilar": {}}
                except Exception:
                    time.sleep(0.05)
            return {"kullanicilar": {}}

    def veri_yaz(self, data):
        """Thread-safe atomik yazma. Yarım yazma asla olmaz."""
        with _dosya_kilidi:
            try:
                self._guvensiz_yaz(data)
            except Exception as e:
                raise IOError(f"Veritabanına yazılamadı: {e}")

    def _kullanici_guncelle(self, kullanici_adi, alan, deger):
        """Tek bir alanı güncellemek için kısa yol — tam okuma/yazma döngüsü."""
        with _dosya_kilidi:
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"kullanicilar": {}}
            if kullanici_adi in data.get("kullanicilar", {}):
                data["kullanicilar"][kullanici_adi][alan] = deger
                self._guvensiz_yaz(data)

    # ── Kimlik Doğrulama ──────────────────────────────────────────────────────

    def giris_kontrol(self, kullanici_adi, sifre):
        if not kullanici_adi or not sifre:
            return False, "Kullanıcı adı ve şifre boş olamaz!"
        kullanici_adi = kullanici_adi.strip()
        try:
            data = self.veri_oku()
            kullanicilar = data.get("kullanicilar", {})
            if kullanici_adi in kullanicilar:
                if str(kullanicilar[kullanici_adi].get("sifre", "")) == str(sifre):
                    return True, "Giriş başarılı!"
                return False, "Şifre hatalı!"
            return False, "Kullanıcı bulunamadı!"
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
                    data = {"kullanicilar": {}}

                kullanicilar = data.get("kullanicilar", {})
                if kullanici_adi in kullanicilar:
                    return False, "Bu kullanıcı adı zaten alınmış!"
                for v in kullanicilar.values():
                    if v.get("eposta", "").lower() == eposta:
                        return False, "Bu e-posta adresi zaten kayıtlı!"

                kullanicilar[kullanici_adi] = {
                    "sifre": sifre,
                    "eposta": eposta,
                    "fitness_gecmisi": [],
                    "gorevler": [],
                    "notlar": "",
                    "fitness_profil": {}
                }
                data["kullanicilar"] = kullanicilar
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
                        data["kullanicilar"][k]["sifre"] = yeni_sifre
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
            self._kullanici_guncelle(kullanici_adi, "sifre", yeni_sifre)
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
        """Kullanıcının kalıcı fitness profilini (cinsiyet, baslangic tarihi vb.) sakla."""
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

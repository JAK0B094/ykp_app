import json
import os

class KimlikDogrulama:
    def __init__(self, dosya_yolu="src/data/veritabani.json"):
        self.dosya_yolu = dosya_yolu
        if not os.path.exists(self.dosya_yolu):
            with open(self.dosya_yolu, "w", encoding="utf-8") as f:
                json.dump({"kullanicilar": {}}, f)

    def veri_oku(self):
        try:
            with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"kullanicilar": {}}

    def veri_yaz(self, data):
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def giris_kontrol(self, kullanici_adi, sifre):
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        if kullanici_adi in kullanicilar:
            if str(kullanicilar[kullanici_adi].get("sifre", "")) == str(sifre):
                return True, "Giriş başarılı!"
            else:
                return False, "Şifre hatalı!"
        return False, "Kullanıcı bulunamadı!"

    def kayit_et(self, kullanici_adi, sifre, eposta):
        if len(sifre) < 6 or len(sifre) > 32:
            return False, "Şifre 6-32 karakter arasında olmalıdır!"
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        if kullanici_adi in kullanicilar:
            return False, "Bu kullanıcı adı zaten alınmış!"
        for k, v in kullanicilar.items():
            if v.get("eposta") == eposta:
                return False, "Bu e-posta adresi zaten kayıtlı!"
        kullanicilar[kullanici_adi] = {
            "sifre": sifre,
            "eposta": eposta,
            "fitness_gecmisi": [],
            "gorevler": [],
            "notlar": ""
        }
        data["kullanicilar"] = kullanicilar
        self.veri_yaz(data)
        return True, "Kayıt başarılı! Giriş yapabilirsiniz."

    def eposta_ile_sifre_sifirla(self, eposta, yeni_sifre):
        if len(yeni_sifre) < 6 or len(yeni_sifre) > 32:
            return False, "Şifre 6-32 karakter arasında olmalıdır!"
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        for k, v in kullanicilar.items():
            if v.get("eposta") == eposta:
                kullanicilar[k]["sifre"] = yeni_sifre
                data["kullanicilar"] = kullanicilar
                self.veri_yaz(data)
                return True, "Şifre başarıyla güncellendi!"
        return False, "Bu e-posta adresiyle kayıtlı kullanıcı bulunamadı!"

    def sifre_degistir(self, kullanici_adi, eski_sifre, yeni_sifre):
        basari, _ = self.giris_kontrol(kullanici_adi, eski_sifre)
        if not basari:
            return False, "Mevcut şifre hatalı!"
        if len(yeni_sifre) < 6 or len(yeni_sifre) > 32:
            return False, "Yeni şifre 6-32 karakter arasında olmalıdır!"
        data = self.veri_oku()
        data["kullanicilar"][kullanici_adi]["sifre"] = yeni_sifre
        self.veri_yaz(data)
        return True, "Şifre başarıyla değiştirildi!"

    def fitness_verisi_kaydet(self, kullanici_adi, yeni_veri):
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        if kullanici_adi in kullanicilar:
            if "fitness_gecmisi" not in kullanicilar[kullanici_adi]:
                kullanicilar[kullanici_adi]["fitness_gecmisi"] = []
            kullanicilar[kullanici_adi]["fitness_gecmisi"].append(yeni_veri)
            data["kullanicilar"] = kullanicilar
            self.veri_yaz(data)

    def fitness_verisi_getir(self, kullanici_adi):
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        if kullanici_adi in kullanicilar:
            return kullanicilar[kullanici_adi].get("fitness_gecmisi", [])
        return []

    def gorev_kaydet(self, kullanici_adi, gorevler):
        data = self.veri_oku()
        if kullanici_adi in data.get("kullanicilar", {}):
            data["kullanicilar"][kullanici_adi]["gorevler"] = gorevler
            self.veri_yaz(data)

    def gorev_getir(self, kullanici_adi):
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        if kullanici_adi in kullanicilar:
            return kullanicilar[kullanici_adi].get("gorevler", [])
        return []

    def not_kaydet(self, kullanici_adi, not_metni):
        data = self.veri_oku()
        if kullanici_adi in data.get("kullanicilar", {}):
            data["kullanicilar"][kullanici_adi]["notlar"] = not_metni
            self.veri_yaz(data)

    def not_getir(self, kullanici_adi):
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        if kullanici_adi in kullanicilar:
            return kullanicilar[kullanici_adi].get("notlar", "")
        return ""

    def kullanici_bilgi_getir(self, kullanici_adi):
        data = self.veri_oku()
        kullanicilar = data.get("kullanicilar", {})
        return kullanicilar.get(kullanici_adi, {})

import json
import os

class KimlikDogrulama:
    def __init__(self, dosya_yolu="src/data/veritabani.json"):
        self.dosya_yolu = dosya_yolu
        if not os.path.exists(self.dosya_yolu):
            with open(self.dosya_yolu, "w") as f:
                json.dump({"kullanicilar": []}, f)

    def veri_oku(self):
        try:
            with open(self.dosya_yolu, "r") as f:
                return json.load(f)
        except:
            return {"kullanicilar": []}

    def fitness_verisi_kaydet(self, kullanici_adi, yeni_veri):
        data = self.veri_oku()
        for k in data["kullanicilar"]:
            if k["kullanici_adi"] == kullanici_adi:
                # Kullanıcıya özel 'fitness_gecmisi' çekmecesi
                if "fitness_gecmisi" not in k:
                    k["fitness_gecmisi"] = []
                
                # Yeni veriyi ekle
                k["fitness_gecmisi"].append(yeni_veri)
                # Sadece son 10 kaydı tutarak şişmeyi önleyebiliriz (opsiyonel)
                break
        
        with open(self.dosya_yolu, "w") as f:
            json.dump(data, f, indent=4)

    def fitness_verisi_getir(self, kullanici_adi):
        data = self.veri_oku()
        for k in data["kullanicilar"]:
            if k["kullanici_adi"] == kullanici_adi:
                return k.get("fitness_gecmisi", [])
        return []
import json
import os

class FitnessVeriYonetimi:
    def __init__(self):
        self.dosya_yolu = os.path.join("src", "data", "veritabani.json")

    def antrenman_kaydet(self, kullanici_adi, antrenman_notu):
        with open(self.dosya_yolu, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Eğer kullanıcı için fitness alanı yoksa oluştur
        if "fitness" not in data:
            data["fitness"] = {}
        
        if kullanici_adi not in data["fitness"]:
            data["fitness"][kullanici_adi] = []
            
        data["fitness"][kullanici_adi].append(antrenman_notu)
        
        with open(self.dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
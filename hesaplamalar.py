import datetime

class FitnessZekasi:
    @staticmethod
    def analiz_et(boy, kilo, yas, seviye, hedef, baslangic_tarihi=None):
        metre_boy = boy / 100
        vki = kilo / (metre_boy ** 2)
        
        # Zaman takibi (Kaçıncı haftadayız?)
        hafta_sayisi = 1
        if baslangic_tarihi:
            basla = datetime.datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
            fark = datetime.datetime.now() - basla
            hafta_sayisi = (fark.days // 7) + 1

        # Program Belirleme (Haftalık değişen zeka)
        program = {"ad": "", "liste": [], "tavsiye": ""}
        
        if seviye == "Başlangıç":
            if hafta_sayisi <= 4: # İlk 1 ay adaptasyon
                program["ad"] = f"Adaptasyon Fazı (Hafta {hafta_sayisi})"
                program["liste"] = ["Squat: 3x12", "Bench Press: 3x12", "Lat Pulldown: 3x12"]
                program["tavsiye"] = "Hareketi doğru yapmaya odaklan."
            else: # 1 aydan sonra ağırlık artışı başlar
                program["ad"] = f"Güç Fazı 1 (Hafta {hafta_sayisi})"
                program["liste"] = ["Squat: 5x5", "Bench Press: 5x5", "Deadlift: 1x5"]
                program["tavsiye"] = "Ağırsağlam 5x5 mantığı: Ağırlıkları 2.5kg artır."
        
        return {
            "vki": round(vki, 1),
            "hafta": hafta_sayisi,
            "program_adi": program["ad"],
            "program_liste": program["liste"],
            "tavsiye": program["tavsiye"]
        }
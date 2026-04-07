import datetime

class FitnessZekasi:
    @staticmethod
    def vki_kategori(vki):
        if vki < 18.5:
            return "Zayıf", "#3498db"
        elif vki < 25.0:
            return "Normal (İdeal)", "#27ae60"
        elif vki < 30.0:
            return "Fazla Kilolu", "#f39c12"
        else:
            return "Obez", "#e74c3c"

    @staticmethod
    def analiz_et(boy, kilo, yas, seviye, hedef, baslangic_tarihi=None):
        metre_boy = boy / 100
        vki = kilo / (metre_boy ** 2)

        hafta_sayisi = 1
        if baslangic_tarihi:
            try:
                basla = datetime.datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
                fark = datetime.datetime.now() - basla
                hafta_sayisi = max(1, (fark.days // 7) + 1)
            except:
                hafta_sayisi = 1

        program = {"ad": "", "liste": [], "tavsiye": ""}

        if seviye == "Başlangıç":
            if hafta_sayisi <= 4:
                program["ad"] = f"Adaptasyon Fazı (Hafta {hafta_sayisi})"
                program["liste"] = [
                    "Squat: 3x12", "Bench Press: 3x12", "Lat Pulldown: 3x12",
                    "Shoulder Press: 3x12", "Plank: 3x30sn"
                ]
                program["tavsiye"] = "Hareketi doğru yapmaya odaklan. Ağırlık önemli değil, form önemli."
            elif hafta_sayisi <= 8:
                program["ad"] = f"Güç Fazı 1 (Hafta {hafta_sayisi})"
                program["liste"] = [
                    "Squat: 4x8", "Bench Press: 4x8", "Bent-Over Row: 4x8",
                    "Overhead Press: 4x8", "Romanian Deadlift: 3x10"
                ]
                program["tavsiye"] = "Her haftada ağırlığa 2.5kg ekle. Dinlenme süresi 90 saniye."
            else:
                program["ad"] = f"Güç Fazı 2 (Hafta {hafta_sayisi})"
                program["liste"] = [
                    "Squat: 5x5", "Bench Press: 5x5", "Deadlift: 1x5",
                    "Pull-up: 3x max", "Dip: 3x max"
                ]
                program["tavsiye"] = "5x5 programı: Ağırlıkları 2.5kg artır. Geri dönemiyorsan sabit tut."

        elif seviye == "Orta":
            if hafta_sayisi <= 4:
                program["ad"] = f"Hipertrofi Fazı (Hafta {hafta_sayisi})"
                program["liste"] = [
                    "Squat: 4x10", "Incline Bench: 4x10", "Cable Row: 4x10",
                    "Lateral Raise: 3x15", "Barbell Curl: 3x12", "Tricep Pushdown: 3x12"
                ]
                program["tavsiye"] = "Kas hacmini artırmak için 60-90sn dinlenme. Negatif fazı yavaş yap."
            else:
                program["ad"] = f"PPL Programı (Hafta {hafta_sayisi})"
                program["liste"] = [
                    "Push: Bench + Shoulder + Tricep",
                    "Pull: Deadlift + Row + Curl",
                    "Legs: Squat + Leg Press + Calf",
                    "Haftada 6 gün antrenman"
                ]
                program["tavsiye"] = "Push-Pull-Legs split: Her kas grubuna haftada 2 kez çalış."

        elif seviye == "İleri":
            program["ad"] = f"İleri Seviye Periodizasyon (Hafta {hafta_sayisi})"
            program["liste"] = [
                "Squat: 6x3 (%85 1RM)", "Bench Press: 5x3 (%85 1RM)",
                "Deadlift: 4x2 (%90 1RM)", "Weighted Pull-up: 4x5",
                "Paused Squat: 3x3", "Romanian Deadlift: 4x6"
            ]
            program["tavsiye"] = "Periodizasyon: Her 4 haftada deload haftası uygula. Max kuvvet gelişimi için."

        else:
            program["ad"] = "Genel Kondisyon"
            program["liste"] = [
                "Yürüyüş: 30dk", "Squat: 3x15 (Vücut ağırlığı)",
                "Push-up: 3x10", "Plank: 3x30sn"
            ]
            program["tavsiye"] = "Düzenli hareket et. Seviyeni seçerek kişiselleştirilmiş program al."

        kategori, renk = FitnessZekasi.vki_kategori(round(vki, 1))

        return {
            "vki": round(vki, 1),
            "vki_kategori": kategori,
            "vki_renk": renk,
            "hafta": hafta_sayisi,
            "program_adi": program["ad"],
            "program_liste": program["liste"],
            "tavsiye": program["tavsiye"]
        }

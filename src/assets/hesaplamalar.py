"""
JKB FitnessZekası — Kapsamlı Kişisel Fitness Algoritması
=========================================================
Her kullanıcıya özgü: hedef × seviye × ekipman × gün sayısı × hafta fazı
"""
import datetime


# ── Egzersiz Veritabanı (kas gruplarına göre) ─────────────────────────────────

EGZERSIZ_DB = {
    # FORMAT: "İsim": {"kaslar": [...], "ekipman": [...], "seviye": [...], "katki": "primer|yardimci|izolasyon"}
    "Barbell Bench Press":          {"kaslar": ["Pectoralis Major", "Ön Deltoid", "Triceps"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Dumbbell Bench Press":         {"kaslar": ["Pectoralis Major", "Ön Deltoid", "Triceps"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Incline DB Press":             {"kaslar": ["Üst Pectoralis", "Ön Deltoid", "Triceps"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Decline Bench Press":          {"kaslar": ["Alt Pectoralis", "Triceps"], "ekipman": ["salon"], "seviye": ["orta", "ileri"], "tip": "primer"},
    "Cable Fly":                    {"kaslar": ["Pectoralis Major (izolasyon)"], "ekipman": ["salon"], "seviye": ["orta", "ileri"], "tip": "izolasyon"},
    "Dumbbell Fly":                 {"kaslar": ["Pectoralis Major (izolasyon)"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Push-up":                      {"kaslar": ["Pectoralis Major", "Triceps", "Ön Deltoid", "Core"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Diamond Push-up":              {"kaslar": ["Triceps", "Pectoralis Major (iç)"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Wide Push-up":                 {"kaslar": ["Pectoralis Major (dış)", "Ön Deltoid"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic"], "tip": "primer"},
    "Dip":                          {"kaslar": ["Pectoralis Major (alt)", "Triceps", "Ön Deltoid"], "ekipman": ["salon", "ev"], "seviye": ["orta", "ileri"], "tip": "primer"},

    "Barbell Squat":                {"kaslar": ["Quadriceps", "Gluteus Maximus", "Hamstrings", "Core"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Goblet Squat":                 {"kaslar": ["Quadriceps", "Gluteus Maximus", "Core"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Bulgarian Split Squat":        {"kaslar": ["Quadriceps", "Gluteus Maximus", "Hamstrings", "Denge"], "ekipman": ["salon", "ev"], "seviye": ["orta", "ileri"], "tip": "primer"},
    "Leg Press":                    {"kaslar": ["Quadriceps", "Gluteus Maximus", "Hamstrings"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Leg Extension":                {"kaslar": ["Quadriceps (izolasyon)"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Leg Curl":                     {"kaslar": ["Hamstrings (izolasyon)"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Romanian Deadlift (RDL)":      {"kaslar": ["Hamstrings", "Gluteus Maximus", "Erektör Spina"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Hip Thrust":                   {"kaslar": ["Gluteus Maximus", "Hamstrings"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Calf Raise":                   {"kaslar": ["Gastrocnemius", "Soleus"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Bodyweight Squat":             {"kaslar": ["Quadriceps", "Gluteus Maximus", "Core"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic"], "tip": "primer"},
    "Lunge":                        {"kaslar": ["Quadriceps", "Gluteus Maximus", "Hamstrings"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Step-up":                      {"kaslar": ["Quadriceps", "Gluteus Maximus"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Glute Bridge":                 {"kaslar": ["Gluteus Maximus", "Hamstrings", "Core"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic"], "tip": "primer"},
    "Wall Sit":                     {"kaslar": ["Quadriceps", "Gluteus Maximus"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic"], "tip": "izolasyon"},

    "Deadlift":                     {"kaslar": ["Erektör Spina", "Gluteus Maximus", "Hamstrings", "Trapezius", "Core"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Pull-up":                      {"kaslar": ["Latissimus Dorsi", "Biceps Brachii", "Orta Trapezius"], "ekipman": ["salon", "ev"], "seviye": ["orta", "ileri"], "tip": "primer"},
    "Negative Pull-up":             {"kaslar": ["Latissimus Dorsi", "Biceps Brachii"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Lat Pulldown":                 {"kaslar": ["Latissimus Dorsi", "Biceps Brachii", "Orta Trapezius"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Bent-Over Barbell Row":        {"kaslar": ["Latissimus Dorsi", "Rhomboids", "Orta Trapezius", "Biceps"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Dumbbell Row":                 {"kaslar": ["Latissimus Dorsi", "Rhomboids", "Biceps"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Cable Row":                    {"kaslar": ["Latissimus Dorsi", "Rhomboids", "Biceps"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Face Pull":                    {"kaslar": ["Arka Deltoid", "Rotator Cuff", "Orta Trapezius"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "yardimci"},
    "Inverted Row":                 {"kaslar": ["Latissimus Dorsi", "Rhomboids", "Biceps"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta"], "tip": "primer"},

    "Overhead Press (OHP)":         {"kaslar": ["Deltoid (ön+orta)", "Triceps", "Üst Trapezius"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Dumbbell Shoulder Press":      {"kaslar": ["Deltoid (ön+orta)", "Triceps"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "primer"},
    "Lateral Raise":                {"kaslar": ["Orta Deltoid (izolasyon)"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Rear Delt Fly":                {"kaslar": ["Arka Deltoid (izolasyon)"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Arnold Press":                 {"kaslar": ["Deltoid (tüm başlar)", "Triceps"], "ekipman": ["salon", "ev"], "seviye": ["orta", "ileri"], "tip": "primer"},
    "Pike Push-up":                 {"kaslar": ["Ön Deltoid", "Triceps"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "primer"},
    "Handstand Push-up":            {"kaslar": ["Deltoid", "Triceps", "Trapezius"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["ileri"], "tip": "primer"},

    "Barbell Curl":                 {"kaslar": ["Biceps Brachii", "Brachialis"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Dumbbell Curl":                {"kaslar": ["Biceps Brachii", "Brachialis"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Hammer Curl":                  {"kaslar": ["Brachialis", "Brachioradialis", "Biceps Brachii"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Tricep Pushdown":              {"kaslar": ["Triceps Brachii (tüm başlar)"], "ekipman": ["salon"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Skull Crusher":                {"kaslar": ["Triceps Brachii (uzun başı)"], "ekipman": ["salon"], "seviye": ["orta", "ileri"], "tip": "izolasyon"},
    "Overhead Tricep Extension":    {"kaslar": ["Triceps Brachii (uzun baş)"], "ekipman": ["salon", "ev"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Close-Grip Push-up":           {"kaslar": ["Triceps Brachii", "Pectoralis Major (iç)"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "izolasyon"},

    "Plank":                        {"kaslar": ["Rectus Abdominis", "Transversus Abdominis", "Core Stabilizatörler"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Crunch":                       {"kaslar": ["Rectus Abdominis"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "izolasyon"},
    "Leg Raise":                    {"kaslar": ["Alt Rectus Abdominis", "Hip Flexors"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta", "ileri"], "tip": "izolasyon"},
    "Russian Twist":                {"kaslar": ["Obliquus Externus", "Rectus Abdominis"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "izolasyon"},
    "Ab Wheel Rollout":             {"kaslar": ["Rectus Abdominis", "Latissimus Dorsi", "Core"], "ekipman": ["salon", "ev"], "seviye": ["orta", "ileri"], "tip": "izolasyon"},
    "Mountain Climber":             {"kaslar": ["Core", "Hip Flexors", "Omuz Stabilizatörü"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "izolasyon"},

    "Burpee":                       {"kaslar": ["Full Body", "Kardiyovasküler"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta", "ileri"], "tip": "kardiyo"},
    "Jump Squat":                   {"kaslar": ["Quadriceps", "Gluteus", "Kardiyovasküler"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "kardiyo"},
    "High Knees":                   {"kaslar": ["Hip Flexors", "Quadriceps", "Kardiyovasküler"], "ekipman": ["salon", "ev", "vucutagirligi"], "seviye": ["baslangic", "orta"], "tip": "kardiyo"},
    "Box Jump":                     {"kaslar": ["Quadriceps", "Gluteus", "Kardiyovasküler", "Patlayıcı Güç"], "ekipman": ["salon"], "seviye": ["orta", "ileri"], "tip": "kardiyo"},
}

# ── Kas Anatomisi Eğitim Veritabanı ──────────────────────────────────────────

KAS_ANATOMISI = [
    {
        "grup": "Göğüs (Pectoralis)",
        "ikon": "bi-heart-pulse",
        "renk": "#e74c3c",
        "alt_kaslar": ["Pectoralis Major (büyük göğüs)", "Pectoralis Minor (küçük göğüs)"],
        "fonksiyon": "Kolu içe doğru çekme (adduction), fleksiyon ve medial rotasyon.",
        "en_iyi_egzersizler": ["Bench Press", "Incline DB Press", "Dip", "Cable Fly"],
        "bilgi": "Göğüs kası 3 bölgeye ayrılır: üst (incline hareketler), orta (flat hareketler), alt (decline/dip). En hızlı büyüyen kaslardan biridir.",
        "hata": "Omuzları öne almak (yaralanma riski). Omuzları geriye bastırarak çalış."
    },
    {
        "grup": "Sırt (Latissimus & Trapezius)",
        "ikon": "bi-rulers",
        "renk": "#3498db",
        "alt_kaslar": ["Latissimus Dorsi (lat, kanat kası)", "Trapezius (tuzak kası)", "Rhomboids (kürek kemiği kasları)", "Erektör Spina (bel dikleştirici)"],
        "fonksiyon": "Kolu aşağı ve geriye çekme, omuzları geriye toparlama, postür.",
        "en_iyi_egzersizler": ["Deadlift", "Pull-up", "Lat Pulldown", "Bent-Over Row", "Cable Row"],
        "bilgi": "Vücudun en büyük kas grubu. Geniş sırt 'V şekli' verir. Pull-up, en fonksiyonel ve etkili sırt egzersizidir.",
        "hata": "Beli bükmek, kürek kemiklerini kullanmamak. Hareketi dirseklerle başlat, ellerle değil."
    },
    {
        "grup": "Omuz (Deltoid)",
        "ikon": "bi-arrow-up-circle",
        "renk": "#9b59b6",
        "alt_kaslar": ["Ön Deltoid (anterior)", "Orta Deltoid (lateral)", "Arka Deltoid (posterior)"],
        "fonksiyon": "Kolun tüm yönlerde hareketi; omuz ekleminin stabilitesi.",
        "en_iyi_egzersizler": ["Overhead Press", "Lateral Raise", "Rear Delt Fly", "Face Pull"],
        "bilgi": "Omuz 3 farklı başa sahiptir. Çoğu kişi ön deltoidi fazla, arka deltoidi az çalıştırır. Dengesizlik omuz yaralanmasına yol açar.",
        "hata": "Arka deltoidi ihmal etmek. Her press hareketine ek olarak face pull ve rear delt çalış."
    },
    {
        "grup": "Bacak Ön (Quadriceps)",
        "ikon": "bi-lightning",
        "renk": "#f39c12",
        "alt_kaslar": ["Rectus Femoris", "Vastus Lateralis", "Vastus Medialis (VMO)", "Vastus Intermedius"],
        "fonksiyon": "Diz ekstansiyonu (açılması), kalça fleksiyonu.",
        "en_iyi_egzersizler": ["Barbell Squat", "Leg Press", "Bulgarian Split Squat", "Leg Extension"],
        "bilgi": "4 kasın birleşiminden oluşur. Squat, tüm quadricepsi aynı anda çalıştırır. Diz sağlığı için VMO güçlendirmesi kritik.",
        "hata": "Diz içe dönmesi (valgus). Ayak parmakları dışa, diz parmaklar hizasında olmalı."
    },
    {
        "grup": "Bacak Arka (Hamstrings & Gluteus)",
        "ikon": "bi-chevron-double-down",
        "renk": "#27ae60",
        "alt_kaslar": ["Biceps Femoris", "Semitendinosus", "Semimembranosus", "Gluteus Maximus", "Gluteus Medius"],
        "fonksiyon": "Diz fleksiyonu, kalça ekstansiyonu, kalça stabilitesi.",
        "en_iyi_egzersizler": ["Romanian Deadlift", "Hip Thrust", "Leg Curl", "Bulgarian Split Squat"],
        "bilgi": "En çok ihmal edilen kas grubu. Hamstring güçsüzlüğü ACL yırtılmalarının başlıca sebebidir. Hip Thrust, glute için en etkili izolasyon hareketidir.",
        "hata": "RDL'de beli bükmek. Kalçadan eğil, beli nötr tut ve strechi hisset."
    },
    {
        "grup": "Kol Ön (Biceps & Brachialis)",
        "ikon": "bi-hand-thumbs-up",
        "renk": "#e74c3c",
        "alt_kaslar": ["Biceps Brachii (uzun baş + kısa baş)", "Brachialis", "Brachioradialis"],
        "fonksiyon": "Dirsek fleksiyonu, ön kol supinasyonu (avuç yukarı döndürme).",
        "en_iyi_egzersizler": ["Barbell Curl", "Dumbbell Curl", "Hammer Curl", "Pull-up"],
        "bilgi": "Biceps 2 başlı kastır. Kısa baş 'kabarıklık', uzun baş 'uzunluk' verir. Pull-up'ta da yoğun çalışır. Brachialis daha derine yerleşmiş, kolun görsel genişliğini artırır.",
        "hata": "Sallanarak kaldırmak (momentum). Dirseği sabit tut, sadece ön kol hareket etmeli."
    },
    {
        "grup": "Kol Arka (Triceps)",
        "ikon": "bi-arrow-clockwise",
        "renk": "#8e44ad",
        "alt_kaslar": ["Triceps Brachii — Uzun Baş", "Triceps Brachii — Lateral Baş", "Triceps Brachii — Medial Baş"],
        "fonksiyon": "Dirsek ekstansiyonu (kol açma), kol stabilitesi.",
        "en_iyi_egzersizler": ["Tricep Pushdown", "Skull Crusher", "Overhead Tricep Extension", "Dip"],
        "bilgi": "Kolun %60-70'ini oluşturur. Büyük kol için bicepsten çok tricepse odaklan. Uzun baş sadece overhead pozisyonda tam aktive olur.",
        "hata": "Overhead egzersizi yapmamak. Triceps'in uzun başını görmezden gelme."
    },
    {
        "grup": "Core (Karın & Gövde Stabilizatörleri)",
        "ikon": "bi-circle",
        "renk": "#1abc9c",
        "alt_kaslar": ["Rectus Abdominis (6-pack kası)", "Transversus Abdominis (derin stabilizatör)", "Obliquus Externus & Internus (yanlar)", "Erektör Spina"],
        "fonksiyon": "Omurga stabilitesi, güç transferi, postür korunması.",
        "en_iyi_egzersizler": ["Plank", "Ab Wheel Rollout", "Leg Raise", "Deadlift", "Squat"],
        "bilgi": "6-pack kası görmek için vücut yağı düşmeli (%10-15 erkek, %18-24 kadın). Core kasları tüm bileşik hareketlerde aktif çalışır. Sadece crunch ile güçlü core olmaz.",
        "hata": "Sadece crunch yapmak. Plank, leg raise ve rotasyonel hareketlerle tüm core'u çalıştır."
    },
]


class FitnessZekasi:

    # ── Temel Hesaplamalar ────────────────────────────────────────────────────

    @staticmethod
    def vki_kategori(vki):
        if vki < 16.0:   return "Ciddi Zayıf",   "#c0392b"
        elif vki < 18.5: return "Zayıf",          "#3498db"
        elif vki < 25.0: return "Normal (İdeal)", "#27ae60"
        elif vki < 30.0: return "Fazla Kilolu",   "#f39c12"
        elif vki < 35.0: return "Obez (Sınıf I)", "#e74c3c"
        else:            return "Obez (Sınıf II+)","#8e44ad"

    @staticmethod
    def bmr_hesapla(kilo, boy, yas, cinsiyet):
        """Mifflin-St Jeor formülü — en güvenilir BMR."""
        if cinsiyet == "Erkek":
            return 10 * kilo + 6.25 * boy - 5 * yas + 5
        else:
            return 10 * kilo + 6.25 * boy - 5 * yas - 161

    @staticmethod
    def tdee_hesapla(bmr, aktivite):
        carpan = {
            "Hareketsiz (Masa başı)":        1.2,
            "Az Aktif (1-2 gün/hafta)":      1.375,
            "Orta Aktif (3-5 gün/hafta)":    1.55,
            "Çok Aktif (6-7 gün/hafta)":     1.725,
            "Profesyonel Sporcu":             1.9
        }
        return bmr * carpan.get(aktivite, 1.375)

    @staticmethod
    def vucut_yag_tahmini(vki, yas, cinsiyet):
        """Deurenberg formülü ile vücut yağ % tahmini."""
        sex = 1 if cinsiyet == "Erkek" else 0
        bf = (1.20 * vki) + (0.23 * yas) - (10.8 * sex) - 5.4
        return round(max(3, min(60, bf)), 1)

    @staticmethod
    def yag_kategorisi(bf, cinsiyet):
        if cinsiyet == "Erkek":
            if bf < 6:   return "Esansiyel Yağ", "#c0392b"
            elif bf < 14: return "Sporcu",        "#27ae60"
            elif bf < 18: return "Fitness",       "#2ecc71"
            elif bf < 25: return "Ortalama",      "#f39c12"
            else:         return "Obez",          "#e74c3c"
        else:
            if bf < 14:   return "Esansiyel Yağ","#c0392b"
            elif bf < 21: return "Sporcu",        "#27ae60"
            elif bf < 25: return "Fitness",       "#2ecc71"
            elif bf < 32: return "Ortalama",      "#f39c12"
            else:         return "Obez",          "#e74c3c"

    @staticmethod
    def ffmi_hesapla(kilo, boy, bf_yuzde):
        """Fat-Free Mass Index — kas gelişimi göstergesi."""
        yag_kilo = kilo * (bf_yuzde / 100)
        kas_kilo = kilo - yag_kilo
        boy_m = boy / 100
        ffmi = kas_kilo / (boy_m ** 2)
        duzeltilmis = ffmi + 6.1 * (1.8 - boy_m)
        return round(ffmi, 1), round(duzeltilmis, 1), round(kas_kilo, 1)

    @staticmethod
    def ffmi_yorum(ffmi, cinsiyet):
        if cinsiyet == "Erkek":
            if ffmi < 17:  return "Zayıf — başlangıç", "#888"
            elif ffmi < 20: return "Ortalama",          "#f39c12"
            elif ffmi < 22: return "Atletik",           "#27ae60"
            elif ffmi < 24: return "Gelişmiş",          "#2ecc71"
            elif ffmi < 26: return "İleri Düzey",       "#3498db"
            else:           return "Elite / Üst Sınır", "#9b59b6"
        else:
            if ffmi < 14:  return "Zayıf",              "#888"
            elif ffmi < 17: return "Ortalama",           "#f39c12"
            elif ffmi < 19: return "Atletik",            "#27ae60"
            elif ffmi < 21: return "İleri Düzey",        "#2ecc71"
            else:           return "Elite",              "#9b59b6"

    @staticmethod
    def ideal_agirlik(boy, cinsiyet):
        boy_m = boy / 100
        alt = 18.5 * (boy_m ** 2)
        ust = 24.9 * (boy_m ** 2)
        return round(alt, 1), round(ust, 1)

    @staticmethod
    def kalori_hedefi(tdee, hedef):
        h = hedef
        if h == "Kilo Ver":               return round(tdee - 400), "Kalori Açığı (-400 kal)"
        elif h == "Hızlı Kilo Ver":       return round(tdee - 700), "Agresif Açık (-700 kal)"
        elif h == "Kas Yap":              return round(tdee + 250), "Lean Bulk (+250 kal)"
        elif h == "Hızlı Kas Yap":        return round(tdee + 500), "Dirty Bulk (+500 kal)"
        elif h == "Kuvvet Kazan":         return round(tdee + 200), "Güç Surplus (+200 kal)"
        elif h == "Vücut Geliştirme":     return round(tdee + 300), "Hipertrofi Fazı (+300 kal)"
        elif h == "Güç + Hipertrofi":     return round(tdee + 200), "Powerbuilding (+200 kal)"
        elif h == "Kardiyo & Dayanıklılık": return round(tdee - 100), "İdame/Hafif Açık (-100 kal)"
        else:                             return round(tdee), "İdame"

    @staticmethod
    def makro_hesapla(kalori, hedef, kilo):
        h = hedef
        if h in ("Kas Yap", "Hızlı Kas Yap", "Vücut Geliştirme", "Güç + Hipertrofi"):
            protein_g = round(kilo * 2.2)
            yag_g = round(kilo * 1.0)
        elif h == "Kuvvet Kazan":
            protein_g = round(kilo * 2.0)
            yag_g = round(kilo * 1.1)
        elif h in ("Kilo Ver", "Hızlı Kilo Ver"):
            protein_g = round(kilo * 2.5)  # kas koruma için yüksek protein
            yag_g = round(kilo * 0.8)
        elif h == "Kardiyo & Dayanıklılık":
            protein_g = round(kilo * 1.6)
            yag_g = round(kilo * 0.8)
        else:  # Fit Kal
            protein_g = round(kilo * 1.8)
            yag_g = round(kilo * 0.9)
        protein_kal = protein_g * 4
        yag_kal = yag_g * 9
        karb_kal = max(0, kalori - protein_kal - yag_kal)
        karb_g = round(karb_kal / 4)
        return protein_g, karb_g, yag_g

    @staticmethod
    def su_ihtiyaci(kilo, aktivite):
        baz = kilo * 0.033
        if aktivite in ("Çok Aktif (6-7 gün/hafta)", "Profesyonel Sporcu"):
            baz += 0.75
        elif aktivite == "Orta Aktif (3-5 gün/hafta)":
            baz += 0.5
        return round(baz, 1)

    # ── Program Üretici ───────────────────────────────────────────────────────

    @staticmethod
    def _ekipman_kodu(ekipman):
        e = ekipman.lower()
        if "salon" in e or "tam" in e: return "salon"
        if "ev" in e or "dumbbell" in e: return "ev"
        return "vucutagirligi"

    @staticmethod
    def _seviye_kodu(seviye):
        s = seviye.lower()
        if "başl" in s: return "baslangic"
        if "orta" in s: return "orta"
        return "ileri"

    @staticmethod
    def _gun_kodlari(gun_sayisi):
        g = str(gun_sayisi)
        if "3" in g: return 3
        if "4" in g: return 4
        return 5

    # ── Antrenman Programları ─────────────────────────────────────────────────

    @staticmethod
    def program_olustur(hedef, seviye_str, ekipman_str, gun_sayisi_str, hafta):
        sev = FitnessZekasi._seviye_kodu(seviye_str)
        ekp = FitnessZekasi._ekipman_kodu(ekipman_str)
        gun = FitnessZekasi._gun_kodlari(gun_sayisi_str)
        deload = (hafta % 5 == 0 and sev in ("orta", "ileri") and hafta > 4)

        if deload:
            return FitnessZekasi._deload_programi(hafta)

        h = hedef
        if h in ("Kilo Ver", "Hızlı Kilo Ver"):
            return FitnessZekasi._kilo_verme_programi(sev, ekp, gun, hafta)
        elif h in ("Kas Yap", "Hızlı Kas Yap", "Vücut Geliştirme"):
            return FitnessZekasi._hipertrofi_programi(sev, ekp, gun, hafta, h)
        elif h == "Kuvvet Kazan":
            return FitnessZekasi._kuvvet_programi(sev, ekp, gun, hafta)
        elif h == "Güç + Hipertrofi":
            return FitnessZekasi._powerbuilding_programi(sev, ekp, gun, hafta)
        elif h == "Kardiyo & Dayanıklılık":
            return FitnessZekasi._kardiyo_programi(sev, ekp, gun, hafta)
        else:  # Fit Kal
            return FitnessZekasi._fitkal_programi(sev, ekp, gun, hafta)

    # ── Kilo Verme Programı ───────────────────────────────────────────────────

    @staticmethod
    def _kilo_verme_programi(sev, ekp, gun, hafta):
        faz = "Yakma Fazı" if hafta <= 8 else "İleri Yakma"
        if gun == 3:
            egzersizler = [
                ("Goblet Squat / Barbell Squat" if ekp == "salon" else "Bodyweight Squat", "4 × 15", "45-60 sn", "Quadriceps, Glute", "Hızlı tempo, kısa mola"),
                ("Dumbbell Bench Press / Push-up" if ekp != "salon" else "Bench Press", "4 × 12", "45 sn", "Göğüs, Triceps", "Göğsü sık, kontrollü in"),
                ("Dumbbell Row / Inverted Row", "4 × 12", "45 sn", "Sırt, Biceps", "Kürek kemiklerini kullan"),
                ("Dumbbell Shoulder Press / Pike Push-up", "3 × 12", "45 sn", "Deltoid", "Tam ROM"),
                ("Lunge", "3 × 12/taraf", "45 sn", "Quadriceps, Glute", "Diz öne geçmesin"),
                ("Plank", "3 × 45 sn", "30 sn", "Core", "Kalça düz"),
                ("Burpee / High Knees", "3 × 15", "30 sn", "Full Body + Kardiyo", "Maks hız"),
            ]
            splits = [{"gun_adi": f"Gün A — Full Body Ağırlık ({['Pazartesi', 'Çarşamba', 'Cuma'][i % 3]})", "egzersizler": egzersizler} for i in range(3)]
        else:
            gA = [
                ("Barbell Squat / Goblet Squat", "4 × 12", "60 sn", "Quadriceps, Glute", ""),
                ("Romanian Deadlift", "4 × 12", "60 sn", "Hamstrings, Erektör", "Kalçadan eğil"),
                ("Bulgarian Split Squat", "3 × 10/taraf", "60 sn", "Quadriceps, Glute", "Denge öncelikli"),
                ("Calf Raise", "4 × 20", "30 sn", "Baldır", "Tam ROM"),
                ("Mountain Climber", "3 × 30 sn", "20 sn", "Core + Kardiyo", "Hızlı"),
            ]
            gB = [
                ("Bench Press / Dumbbell Press", "4 × 12", "60 sn", "Göğüs, Triceps", ""),
                ("Lat Pulldown / Pull-up Negatif", "4 × 12", "60 sn", "Lat, Biceps", ""),
                ("Dumbbell Shoulder Press", "3 × 12", "60 sn", "Deltoid", ""),
                ("Tricep Pushdown / Close-Grip Push-up", "3 × 15", "45 sn", "Triceps", ""),
                ("Dumbbell Curl", "3 × 15", "45 sn", "Biceps", ""),
                ("Plank + Crunch", "3 × 30 sn + 20", "30 sn", "Core", ""),
            ]
            splits = [
                {"gun_adi": "Pazartesi — Alt Vücut", "egzersizler": gA},
                {"gun_adi": "Salı — Üst Vücut", "egzersizler": gB},
                {"gun_adi": "Çarşamba — HIIT Kardiyo (30-40 dk)", "egzersizler": [
                    ("Burpee × 15", "4 tur", "30 sn", "Full Body", ""),
                    ("Jump Squat × 15", "4 tur", "30 sn", "Bacak", ""),
                    ("High Knees × 30 sn", "4 tur", "20 sn", "Kardiyovasküler", ""),
                ]},
                {"gun_adi": "Perşembe — Alt Vücut (Hafif+)", "egzersizler": gA},
                {"gun_adi": "Cuma — Üst Vücut + Karın", "egzersizler": gB},
            ][:gun]
        return {
            "ad": f"Yağ Yakma — {faz} (Hafta {hafta})",
            "gunler": f"Haftada {gun} gün · Kısa mola · Yüksek tekrar",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for g in splits for e in g["egzersizler"]],
            "dinlenme": "Dinlenme günleri: tempolu yürüyüş 30-45 dk (aktif dinlenme)",
            "tavsiye": (
                f"Kalori açığını diyetle yarat, antrenmanla kasını koru. "
                f"Kısa molalar (30-60 sn) metabolizmanı yüksek tutar. "
                f"Protein alımına dikkat — günde minimum {int(0)}g/kg gerekiyor. "
                "Her haftada ağırlığı %5-10 artır (progressive overload)."
            ),
            "kardiyo": "Haftada 2-3 gün LISS (40-50 dk yürüyüş/bisiklet) + haftada 1 HIIT",
            "uyku_oneri": "7-9 saat. Kortizol seviyesi yağ yakmayı etkiler.",
        }

    # ── Hipertrofi (Kas Yapma / Vücut Geliştirme) ─────────────────────────────

    @staticmethod
    def _hipertrofi_programi(sev, ekp, gun, hafta, hedef_str):
        blok = (hafta - 1) // 4 + 1

        if gun == 3:  # Full Body
            liste = [
                ("Barbell Squat / Goblet Squat", "4 × 8-10", "90 sn", "Quadriceps, Glute", "Progressive overload"),
                ("Bench Press / DB Press", "4 × 8-10", "90 sn", "Göğüs, Triceps", "Tam hareket açısı"),
                ("Bent-Over Row / Dumbbell Row", "4 × 8-10", "90 sn", "Lat, Rhomboid", "Kürek kemiği devreye al"),
                ("Romanian Deadlift", "3 × 10-12", "90 sn", "Hamstring, Glute", "Kontrollü eccentric"),
                ("Overhead Press / DB Shoulder Press", "3 × 10-12", "60 sn", "Deltoid", ""),
                ("Dumbbell Curl + Tricep Extension", "3 × 12-15", "45 sn", "Biceps, Triceps", "Süperset"),
                ("Plank / Ab Wheel", "3 × 30-45 sn", "30 sn", "Core", ""),
            ]
            splits = [{"gun_adi": f"Full Body {['A','B','C'][i]} — {['Pazartesi','Çarşamba','Cuma'][i]}", "egzersizler": liste} for i in range(3)]

        elif gun == 4:  # Upper/Lower
            ust_A = [
                ("Bench Press / DB Press", "4 × 6-8", "2 dk", "Göğüs, Triceps", "Ağır / güç odaklı"),
                ("Barbell Row / Dumbbell Row", "4 × 6-8", "2 dk", "Lat, Biceps", "Ağır / güç"),
                ("Overhead Press", "3 × 8-10", "90 sn", "Deltoid", ""),
                ("Incline DB Press", "3 × 10-12", "60 sn", "Üst Göğüs", "Pump odaklı"),
                ("Cable Row / Face Pull", "3 × 12-15", "60 sn", "Orta Sırt, Arka Delt", ""),
                ("Dumbbell Curl + Tricep Pushdown", "3 × 12-15", "45 sn", "Biceps, Triceps", "Süperset"),
            ]
            alt_A = [
                ("Barbell Squat", "4 × 6-8", "2-3 dk", "Quadriceps, Glute", "Ağır / güç odaklı"),
                ("Romanian Deadlift", "4 × 8-10", "90 sn", "Hamstring, Glute", ""),
                ("Leg Press", "3 × 10-12", "90 sn", "Quadriceps, Glute", "Pump"),
                ("Leg Curl", "3 × 12-15", "60 sn", "Hamstrings", "İzolasyon"),
                ("Calf Raise", "4 × 15-20", "45 sn", "Baldır", ""),
                ("Plank + Leg Raise", "3 × 30-20", "30 sn", "Core", ""),
            ]
            ust_B = [
                ("Incline DB Press", "4 × 10-12", "90 sn", "Üst Göğüs", "Pump"),
                ("Lat Pulldown / Pull-up", "4 × 10-12", "90 sn", "Lat", ""),
                ("Arnold Press", "3 × 12", "60 sn", "Deltoid (tüm)", ""),
                ("Cable Fly / DB Fly", "3 × 12-15", "60 sn", "Göğüs İzolasyon", ""),
                ("Rear Delt Fly + Lateral Raise", "3 × 15", "45 sn", "Arka+Orta Delt", "Süperset"),
                ("Hammer Curl + Skull Crusher", "3 × 12", "45 sn", "Kol", "Süperset"),
            ]
            alt_B = [
                ("Deadlift", "4 × 5", "3 dk", "Full Posterior Chain", "Hafif haftada daha az"),
                ("Bulgarian Split Squat", "3 × 10/taraf", "90 sn", "Quadriceps, Glute", ""),
                ("Hip Thrust", "4 × 12-15", "60 sn", "Glute Maximus", ""),
                ("Leg Extension + Leg Curl", "3 × 15", "45 sn", "Quad+Hamstring", "Süperset"),
                ("Calf Raise", "4 × 20", "30 sn", "Baldır", ""),
            ]
            splits = [
                {"gun_adi": "Pazartesi — Üst Vücut A (Güç)", "egzersizler": ust_A},
                {"gun_adi": "Salı — Alt Vücut A (Güç)", "egzersizler": alt_A},
                {"gun_adi": "Perşembe — Üst Vücut B (Hacim)", "egzersizler": ust_B},
                {"gun_adi": "Cuma — Alt Vücut B (Hacim)", "egzersizler": alt_B},
            ]

        else:  # PPL × 2 (6 gün) veya 5 gün
            push = [
                ("Bench Press", "4 × 6-8", "2 dk", "Orta Göğüs", "Güç seti"),
                ("Incline DB Press", "4 × 10-12", "90 sn", "Üst Göğüs", "Pump"),
                ("Overhead Press", "4 × 8-10", "90 sn", "Ön+Orta Deltoid", ""),
                ("Cable Fly / DB Fly", "3 × 12-15", "60 sn", "Göğüs Strech", ""),
                ("Lateral Raise", "4 × 15-20", "45 sn", "Orta Deltoid", "Hafif ağırlık"),
                ("Tricep Pushdown + Skull Crusher", "3 × 12-15", "45 sn", "Triceps", ""),
            ]
            pull = [
                ("Deadlift", "3 × 5", "3 dk", "Full Posterior Chain", "Ağır"),
                ("Pull-up / Lat Pulldown", "4 × 8-10", "90 sn", "Lat", ""),
                ("Barbell Row", "4 × 8-10", "90 sn", "Orta Sırt", ""),
                ("Face Pull", "3 × 15-20", "45 sn", "Arka Delt, Rotator Cuff", "Omuz sağlığı"),
                ("Rear Delt Fly", "3 × 15", "45 sn", "Arka Deltoid", ""),
                ("Barbell/DB Curl + Hammer Curl", "3 × 12-15", "45 sn", "Biceps, Brachialis", ""),
            ]
            legs = [
                ("Barbell Squat", "4 × 6-8", "2-3 dk", "Quadriceps, Glute", "Ağır"),
                ("Romanian Deadlift", "4 × 10-12", "90 sn", "Hamstring, Glute", ""),
                ("Leg Press", "3 × 12-15", "90 sn", "Quadriceps, Glute", ""),
                ("Bulgarian Split Squat", "3 × 10/taraf", "90 sn", "Quad, Glute", ""),
                ("Leg Curl + Leg Extension", "3 × 15", "60 sn", "İzolasyon", "Süperset"),
                ("Hip Thrust", "3 × 15", "60 sn", "Glute Maximus", ""),
                ("Calf Raise", "5 × 15-20", "30 sn", "Baldır", ""),
                ("Plank + Ab Wheel", "3 tur", "30 sn", "Core", ""),
            ]
            splits = [
                {"gun_adi": "Pazartesi — Push (İtiş: Göğüs/Omuz/Triceps)", "egzersizler": push},
                {"gun_adi": "Salı — Pull (Çekiş: Sırt/Biceps/Arka Delt)", "egzersizler": pull},
                {"gun_adi": "Çarşamba — Legs (Bacak/Core)", "egzersizler": legs},
                {"gun_adi": "Perşembe — Push B (Tekrar)", "egzersizler": push},
                {"gun_adi": "Cuma — Pull B (Tekrar)", "egzersizler": pull},
                {"gun_adi": "Cumartesi — Legs B (Tekrar)", "egzersizler": legs},
            ][:gun]

        return {
            "ad": f"{'Vücut Geliştirme' if hedef_str == 'Vücut Geliştirme' else 'Kas Hipertrofisi'} — Blok {blok} (Hafta {hafta})",
            "gunler": f"{'Upper/Lower 4 gün' if gun == 4 else ('PPL '+str(gun)+' gün' if gun >= 5 else 'Full Body 3 gün')}",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for g in splits for e in g["egzersizler"]],
            "dinlenme": "Dinlenme: 60-90 sn hacim setleri, 2-3 dk güç setleri. Haftada en az 1-2 tam dinlenme günü.",
            "tavsiye": (
                f"Blok {blok}: Progressive overload öncelikli — her haftada ağırlık veya tekrar artır. "
                "Hipertrofi için 60-75% 1RM ile 8-15 tekrar hedefle. "
                "Son sette RIR (rezerv tekrar) 1-2 olmalı — neredeyse başarısızlık. "
                "Uyku ve protein olmadan kas büyümez."
            ),
            "kardiyo": "Haftada 1-2 kez düşük yoğunluklu kardiyo (20-30 dk LISS)",
            "uyku_oneri": "8-9 saat. Büyüme hormonu derin uyku fazında salgılanır.",
        }

    # ── Kuvvet (Powerlifting) Programı ───────────────────────────────────────

    @staticmethod
    def _kuvvet_programi(sev, ekp, gun, hafta):
        blok = (hafta - 1) // 4 + 1
        yuzde_1rm = [75, 80, 85, 90][min((hafta - 1) % 4, 3)]
        gunler_map = {
            3: ["Pazartesi — Squat Ağırlıklı", "Çarşamba — Bench Ağırlıklı", "Cuma — Deadlift Ağırlıklı"],
            4: ["Pazartesi — Squat", "Salı — Bench", "Perşembe — Squat Yardımcı", "Cuma — Deadlift"],
            5: ["Pazartesi — Max Effort Squat", "Salı — Max Effort Bench", "Çarşamba — Dinlenme",
                "Perşembe — Dynamic Effort Squat/DL", "Cuma — Dynamic Effort Bench"],
        }
        temel = [
            ("Barbell Squat", f"5 × 3-5  @{yuzde_1rm}% 1RM", "3-4 dk", "Quad, Glute, Core", "Ağır — bel düz, kalça tam aşağı"),
            ("Barbell Bench Press", f"5 × 3-5  @{yuzde_1rm}% 1RM", "3-4 dk", "Göğüs, Triceps, Ön Delt", "Güçlü taban, köprü kur"),
            ("Deadlift", f"3 × 3  @{yuzde_1rm}% 1RM", "4-5 dk", "Full Posterior Chain", "Haftanın en ağır seti"),
            ("Overhead Press", "4 × 5", "2-3 dk", "Deltoid, Triceps", "Güç geliştirici yardımcı"),
            ("Close-Grip Bench", "3 × 6-8", "2 dk", "Triceps, Bench geliştirici", ""),
            ("Romanian Deadlift", "3 × 8", "2 dk", "Hamstring yardımcı", ""),
            ("Barbell Row", "4 × 6", "2 dk", "Sırt güçlendirici", ""),
            ("Face Pull + Band Pull-Apart", "3 × 15", "45 sn", "Omuz sağlığı", "Zorunlu"),
        ]
        return {
            "ad": f"Kuvvet Periodizasyon — Blok {blok} ({yuzde_1rm}% 1RM Haftası {hafta})",
            "gunler": f"Haftada {gun} gün · Yüksek yoğunluk · Uzun mola",
            "splits": [{"gun_adi": gunler_map.get(gun, gunler_map[3])[i], "egzersizler": temel} for i in range(min(gun, 3))],
            "program_liste": [(e[0], e[1], e[4]) for e in temel],
            "dinlenme": "3-5 dakika ağır setler arası. Kaliteli uyku zorunlu.",
            "tavsiye": (
                f"Bu hafta yoğunluk: %{yuzde_1rm} 1RM. "
                "Kuvvet antrenmanı doğru teknikle yapılmadığında yaralanma riski çok yüksektir. "
                "Her 4. haftada deload: ağırlığı %60'a indir, hacmi azalt. "
                "RPE sistemi öğren: RPE 8 = 2 tekrar rezerv, RPE 9 = 1 rezerv, RPE 10 = maksimum."
            ),
            "kardiyo": "Minimal kardiyo. Kuvveti bozmaması için haftada 1-2 × 20 dk hafif yürüyüş",
            "uyku_oneri": "8+ saat. CNS (merkezi sinir sistemi) toparlanması kritik.",
        }

    # ── Powerbuilding ────────────────────────────────────────────────────────

    @staticmethod
    def _powerbuilding_programi(sev, ekp, gun, hafta):
        blok = (hafta - 1) // 4 + 1
        splits = [
            {
                "gun_adi": "Pazartesi — Squat Güç + Bacak Hacim",
                "egzersizler": [
                    ("Barbell Squat", "4 × 4-6 (ağır)", "3 dk", "Quadriceps, Glute", "Güç seti"),
                    ("Leg Press", "3 × 10-12", "90 sn", "Quadriceps", "Hacim"),
                    ("Romanian Deadlift", "3 × 10", "90 sn", "Hamstring", ""),
                    ("Bulgarian Split Squat", "2 × 10/taraf", "90 sn", "Quad, Glute", ""),
                    ("Leg Curl", "3 × 12-15", "60 sn", "Hamstring izolasyon", ""),
                    ("Calf Raise", "4 × 15", "30 sn", "Baldır", ""),
                ],
            },
            {
                "gun_adi": "Salı — Bench Güç + Göğüs Hacim",
                "egzersizler": [
                    ("Barbell Bench Press", "4 × 4-6 (ağır)", "3 dk", "Göğüs, Triceps", "Güç seti"),
                    ("Incline DB Press", "3 × 10-12", "90 sn", "Üst Göğüs", "Hacim"),
                    ("Cable Fly", "3 × 12-15", "60 sn", "Göğüs izolasyon", ""),
                    ("Overhead Press", "3 × 8-10", "90 sn", "Deltoid", ""),
                    ("Lateral Raise", "3 × 15-20", "45 sn", "Orta Delt", ""),
                    ("Tricep Pushdown + Skull Crusher", "3 × 12", "45 sn", "Triceps", ""),
                ],
            },
            {
                "gun_adi": "Perşembe — Deadlift Güç + Sırt Hacim",
                "egzersizler": [
                    ("Deadlift", "3 × 3-5 (ağır)", "4 dk", "Full Posterior", "Güç seti"),
                    ("Pull-up / Lat Pulldown", "4 × 8-10", "90 sn", "Lat", "Hacim"),
                    ("Barbell Row", "4 × 8-10", "90 sn", "Orta Sırt", ""),
                    ("Face Pull", "3 × 15", "45 sn", "Arka Delt, Omuz sağlığı", "Atlama"),
                    ("Dumbbell Curl + Hammer Curl", "3 × 12", "45 sn", "Biceps", ""),
                ],
            },
            {
                "gun_adi": "Cuma — Yardımcı Hareketler + Zayıf Noktalar",
                "egzersizler": [
                    ("Close-Grip Bench / Dip", "3 × 8", "90 sn", "Triceps güçlendirici", ""),
                    ("Hip Thrust", "3 × 12", "60 sn", "Glute", ""),
                    ("Rear Delt Fly + Band Pull-Apart", "3 × 15", "45 sn", "Omuz sağlığı", "Zorunlu"),
                    ("Core: Plank + Ab Wheel", "3 tur", "30 sn", "Core", ""),
                ],
            },
        ]
        return {
            "ad": f"Powerbuilding — Blok {blok} (Hafta {hafta})",
            "gunler": f"Haftada {min(gun,4)} gün · Güç + Hacim Hibrid",
            "splits": splits[:min(gun, 4)],
            "program_liste": [(e[0], e[1], e[4]) for g in splits for e in g["egzersizler"]],
            "dinlenme": "Güç setleri: 3-4 dk. Hacim setleri: 60-90 sn.",
            "tavsiye": (
                "Powerbuilding: bileşik hareketlerde güç artışı + izolasyon ile estetik. "
                "Ağır setlerden (4-6 tekrar) hacim setlerine (10-15 tekrar) aynı antrenmanda geçiş. "
                "Her 4 haftada 1 deload haftası uygula."
            ),
            "kardiyo": "Haftada 1-2 × 20-30 dk orta yoğunluk",
            "uyku_oneri": "8 saat — hem güç hem de büyüme için kritik.",
        }

    # ── Kardiyo & Dayanıklılık ─────────────────────────────────────────────

    @staticmethod
    def _kardiyo_programi(sev, ekp, gun, hafta):
        faz = "Temel Dayanıklılık" if hafta <= 6 else "İleri Dayanıklılık"
        kor = [
            ("Burpee", f"3 × {'10' if sev=='baslangic' else '15'}", "45 sn", "Full Body + Kardiyovasküler", "Tempo artır"),
            ("Jump Squat", "3 × 15", "30 sn", "Bacak + Kardiyovasküler", "Yumuşak iniş"),
            ("High Knees", "3 × 30 sn", "20 sn", "Kardiyovasküler + Core", "Diz yükseğe"),
            ("Mountain Climber", "3 × 30 sn", "20 sn", "Core + Kardiyovasküler", "Hızlı"),
            ("Plank to Push-up", "3 × 10", "30 sn", "Core, Omuz, Triceps", ""),
            ("Box Jump / Step-up", "3 × 10", "45 sn", "Patlayıcı güç + Kardiyovasküler", ""),
            ("Push-up + Crunch Süperset", "3 × 15+15", "30 sn", "Göğüs + Core", "Dinlenmeden geç"),
        ]
        splits = [{"gun_adi": f"Gün {i+1} — HIIT / Dayanıklılık Devresi", "egzersizler": kor} for i in range(min(gun, 5))]
        return {
            "ad": f"Kardiyo & Dayanıklılık — {faz} (Hafta {hafta})",
            "gunler": f"Haftada {gun} gün HIIT/Kardiyo + 2 gün LISS",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for e in kor],
            "dinlenme": "Devreler arası 30-45 sn. Tam devre arası 2 dk.",
            "tavsiye": (
                "HIIT: maksimum 20-30 dakika yeterli. "
                "LISS (Tempolu yürüyüş/bisiklet): 45-60 dk 2× hafta. "
                "VO2max artışı için 'zone 2' kardiyo (nefes kontrol edebiliyorsun ama zorlanıyorsun). "
                "Dayanıklılık gelişimi 6-12 hafta sürer."
            ),
            "kardiyo": "Her gün farklı: HIIT + LISS + aktif dinlenme rotation",
            "uyku_oneri": "7-8 saat. Kardiyovasküler toparlanma uyku sırasında gerçekleşir.",
        }

    # ── Fit Kal (İdame) Programı ─────────────────────────────────────────────

    @staticmethod
    def _fitkal_programi(sev, ekp, gun, hafta):
        liste = [
            ("Squat / Goblet Squat", "3 × 12", "60 sn", "Bacak", ""),
            ("Push-up / Bench Press", "3 × 12", "60 sn", "Göğüs, Triceps", ""),
            ("Dumbbell Row / Lat Pulldown", "3 × 12", "60 sn", "Sırt, Biceps", ""),
            ("Shoulder Press / Pike Push-up", "3 × 12", "60 sn", "Omuz", ""),
            ("Romanian Deadlift / Hip Thrust", "3 × 12", "60 sn", "Arka zincir", ""),
            ("Plank + Crunch + Leg Raise", "3 tur", "30 sn", "Core", ""),
            ("Lateral Raise + Rear Delt", "3 × 15", "30 sn", "Omuz dengesi", ""),
        ]
        splits = [{"gun_adi": f"Full Body {['A','B','C'][i%3]} — Genel Fitness", "egzersizler": liste} for i in range(gun)]
        return {
            "ad": f"Fit Kal — Genel Sağlık & Form (Hafta {hafta})",
            "gunler": f"Haftada {gun} gün Full Body",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for e in liste],
            "dinlenme": "60-90 sn setler arası. Dinlenme günü aktif ol (yürüyüş, bisiklet).",
            "tavsiye": (
                "Genel sağlık için haftada 150 dk orta yoğunluk veya 75 dk yüksek yoğunluk egzersiz yeterli. "
                "Her antrenman biraz daha zorlaştır (progressive overload). "
                "Esneklik ve mobilite için her antrenman sonrası 10 dk stretching ekle."
            ),
            "kardiyo": "Haftada 2-3 × 30 dk tempolu yürüyüş veya bisiklet",
            "uyku_oneri": "7-8 saat. Sağlıklı yaşam için yeterli uyku zorunlu.",
        }

    # ── Deload ────────────────────────────────────────────────────────────────

    @staticmethod
    def _deload_programi(hafta):
        return {
            "ad": f"⚡ Deload Haftası (Hafta {hafta}) — Toparlanma & Adaptasyon",
            "gunler": "3 gün — tüm ağırlıklar %50-60'a düşürülür",
            "splits": [{
                "gun_adi": "Deload — Full Body Hafif",
                "egzersizler": [
                    ("Squat @ %60 1RM", "3 × 5", "2 dk", "Quadriceps", "Teknik odaklı"),
                    ("Bench Press @ %60 1RM", "3 × 5", "2 dk", "Göğüs", "Kontrollü"),
                    ("Deadlift @ %60 1RM", "2 × 3", "2 dk", "Full Chain", "Sadece form"),
                    ("Row / Pull-up", "3 × 8 hafif", "90 sn", "Sırt", ""),
                    ("Plank + Stretching", "3 × 30 sn", "—", "Core + Mobilite", ""),
                ],
            }],
            "program_liste": [("Squat hafif", "3×5 @60%", ""), ("Bench hafif", "3×5 @60%", ""),
                              ("Deadlift hafif", "2×3 @60%", ""), ("Aktif dinlenme + stretching", "", "")],
            "dinlenme": "Deload'da maksimum uyku ve beslenme kalitesi",
            "tavsiye": (
                "Deload ZORUNLUDUR. Antrenman sırasında değil, dinlenirken büyürsün. "
                "Bu hafta kas lifleri onarılır, CNS toparlanır, tendon-ligament güçlenir. "
                "Deload'u atlayanlarda plateau (ilerleme durması) ve yaralanma riski artar."
            ),
            "kardiyo": "Sadece hafif yürüyüş, yoga veya stretching",
            "uyku_oneri": "Bu hafta 9+ saat hedefle. Toparlanma maksimum önemli.",
        }

    # ── Ana Analiz ─────────────────────────────────────────────────────────────

    @staticmethod
    def analiz_et(boy, kilo, yas, cinsiyet, seviye, hedef, aktivite,
                  baslangic_tarihi=None, ekipman=None, gun_sayisi=None):
        boy  = max(100, min(250, float(boy)))
        kilo = max(30,  min(300, float(kilo)))
        yas  = max(10,  min(100, int(yas)))
        ekipman   = ekipman   or "Spor Salonu (Tam Ekipman)"
        gun_sayisi = gun_sayisi or "3 Gün/Hafta"

        metre_boy = boy / 100
        vki = round(kilo / (metre_boy ** 2), 1)
        vki_kategori, vki_renk = FitnessZekasi.vki_kategori(vki)

        bmr  = round(FitnessZekasi.bmr_hesapla(kilo, boy, yas, cinsiyet))
        tdee = round(FitnessZekasi.tdee_hesapla(bmr, aktivite))
        hedef_kalori, kalori_aciklamasi = FitnessZekasi.kalori_hedefi(tdee, hedef)
        protein_g, karb_g, yag_g = FitnessZekasi.makro_hesapla(hedef_kalori, hedef, kilo)
        su = FitnessZekasi.su_ihtiyaci(kilo, aktivite)
        ideal_alt, ideal_ust = FitnessZekasi.ideal_agirlik(boy, cinsiyet)

        # Vücut kompozisyonu
        bf = FitnessZekasi.vucut_yag_tahmini(vki, yas, cinsiyet)
        bf_kategori, bf_renk = FitnessZekasi.yag_kategorisi(bf, cinsiyet)
        ffmi, ffmi_duz, kas_kilo = FitnessZekasi.ffmi_hesapla(kilo, boy, bf)
        ffmi_kategori, ffmi_renk = FitnessZekasi.ffmi_yorum(ffmi_duz, cinsiyet)

        hafta_sayisi = 1
        if baslangic_tarihi:
            try:
                basla = datetime.datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
                fark  = datetime.datetime.now() - basla
                hafta_sayisi = max(1, (fark.days // 7) + 1)
            except Exception:
                hafta_sayisi = 1

        prog = FitnessZekasi.program_olustur(hedef, seviye, ekipman, gun_sayisi, hafta_sayisi)

        if vki < 18.5:
            vki_tavsiye = f"Kilonu artırman gerekiyor. Sağlıklı hedef: {ideal_alt}–{ideal_ust} kg."
        elif vki < 25:
            vki_tavsiye = f"Harika! İdeal aralıktasın ({ideal_alt}–{ideal_ust} kg). Hedefine odaklan."
        elif vki < 30:
            vki_tavsiye = f"İdeal kiloya ulaşmak için yaklaşık {round(kilo-ideal_ust,1)} kg vermelisin."
        else:
            vki_tavsiye = f"Sağlıklı kilo hedefi: {round(kilo-ideal_ust,1)} kg azaltma. Doktorana danış."

        # Supplement önerileri
        supps = []
        if hedef in ("Kas Yap", "Hızlı Kas Yap", "Vücut Geliştirme", "Güç + Hipertrofi", "Kuvvet Kazan"):
            supps = ["Kreatin Monohidrat (3-5g/gün) — kanıtlanmış güç ve kütle artışı",
                     f"Whey Protein — günlük {protein_g}g proteine ulaşmak için",
                     "Kafein (antrenmandan 30-45 dk önce) — performans artışı"]
        elif hedef in ("Kilo Ver", "Hızlı Kilo Ver"):
            supps = [f"Protein tozu — kas korumak için günlük {protein_g}g protein şart",
                     "Kafein — yağ yakımı ve enerji için",
                     "Omega-3 — inflamasyon kontrolü, toparlanma"]
        elif hedef == "Kardiyo & Dayanıklılık":
            supps = ["Elektrolit (sodyum, potasyum, magnezyum) — dayanıklılık için",
                     "Beta-Alanin — dayanıklılık kapasitesi",
                     "Kafein — VO2max performansı"]

        return {
            "vki": vki, "vki_kategori": vki_kategori, "vki_renk": vki_renk, "vki_tavsiye": vki_tavsiye,
            "ideal_alt": ideal_alt, "ideal_ust": ideal_ust,
            "bmr": bmr, "tdee": tdee, "hedef_kalori": hedef_kalori, "kalori_aciklamasi": kalori_aciklamasi,
            "protein_g": protein_g, "karb_g": karb_g, "yag_g": yag_g,
            "su_lt": su,
            "hafta": hafta_sayisi,
            # Vücut kompozisyonu
            "bf_yuzde": bf, "bf_kategori": bf_kategori, "bf_renk": bf_renk,
            "ffmi": ffmi, "ffmi_duzeltilmis": ffmi_duz, "ffmi_kategori": ffmi_kategori, "ffmi_renk": ffmi_renk,
            "kas_kilo": kas_kilo, "yag_kilo": round(kilo * bf / 100, 1),
            # Program
            "program_adi": prog["ad"],
            "program_gunler": prog["gunler"],
            "program_liste": prog["program_liste"],
            "program_splits": prog.get("splits", []),
            "program_dinlenme": prog.get("dinlenme", ""),
            "program_kardiyo": prog.get("kardiyo", ""),
            "program_uyku": prog.get("uyku_oneri", ""),
            "tavsiye": prog["tavsiye"],
            "hedef": hedef, "seviye": seviye, "ekipman": ekipman, "gun_sayisi": gun_sayisi,
            "supplementler": supps,
            "kas_anatomisi": KAS_ANATOMISI,
        }

    @staticmethod
    def ilerleme_analizi(gecmis_listesi):
        if len(gecmis_listesi) < 2:
            return None
        son = gecmis_listesi[-1]
        ilk = gecmis_listesi[0]
        kilo_fark = round(son.get("kilo", 0) - ilk.get("kilo", 0), 1)
        vki_fark  = round(son.get("vki", 0)  - ilk.get("vki", 0), 1)
        gun_fark  = 0
        try:
            t1 = datetime.datetime.strptime(ilk["tarih"], "%Y-%m-%d")
            t2 = datetime.datetime.strptime(son["tarih"], "%Y-%m-%d")
            gun_fark = (t2 - t1).days
        except Exception:
            pass
        yonelim = "artıyor" if kilo_fark > 0 else ("azalıyor" if kilo_fark < 0 else "sabit")
        return {
            "kilo_fark": kilo_fark, "vki_fark": vki_fark, "gun_fark": gun_fark,
            "kayit_sayisi": len(gecmis_listesi), "yonelim": yonelim,
        }

import datetime

class FitnessZekasi:

    # ── Temel Hesaplamalar ────────────────────────────────────────────────────

    @staticmethod
    def vki_kategori(vki):
        if vki < 16.0:
            return "Ciddi Zayıf", "#c0392b"
        elif vki < 18.5:
            return "Zayıf", "#3498db"
        elif vki < 25.0:
            return "Normal (İdeal)", "#27ae60"
        elif vki < 30.0:
            return "Fazla Kilolu", "#f39c12"
        elif vki < 35.0:
            return "Obez (Sınıf I)", "#e74c3c"
        else:
            return "Obez (Sınıf II+)", "#8e44ad"

    @staticmethod
    def bmr_hesapla(kilo, boy, yas, cinsiyet):
        """Mifflin-St Jeor formülü — en güvenilir BMR hesabı."""
        if cinsiyet == "Erkek":
            return 10 * kilo + 6.25 * boy - 5 * yas + 5
        else:
            return 10 * kilo + 6.25 * boy - 5 * yas - 161

    @staticmethod
    def tdee_hesapla(bmr, aktivite):
        """TDEE = Toplam Günlük Enerji Harcaması."""
        carpan = {
            "Hareketsiz (Masa başı)": 1.2,
            "Az Aktif (1-2 gün/hafta)": 1.375,
            "Orta Aktif (3-5 gün/hafta)": 1.55,
            "Çok Aktif (6-7 gün/hafta)": 1.725,
            "Profesyonel Sporcu": 1.9
        }
        return bmr * carpan.get(aktivite, 1.375)

    @staticmethod
    def ideal_agirlik(boy, cinsiyet):
        """Devine formülü ile ideal ağırlık aralığı."""
        boy_m = boy / 100
        alt = 18.5 * (boy_m ** 2)
        ust = 24.9 * (boy_m ** 2)
        return round(alt, 1), round(ust, 1)

    @staticmethod
    def kalori_hedefi(tdee, hedef):
        """Hedefe göre günlük kalori hedefi."""
        if hedef == "Kilo Ver":
            return round(tdee - 500), "Açık (-500 kal)"
        elif hedef == "Hızlı Kilo Ver":
            return round(tdee - 750), "Agresif Açık (-750 kal)"
        elif hedef == "Kas Yap":
            return round(tdee + 300), "Hafif Fazla (+300 kal)"
        elif hedef == "Hızlı Kas Yap":
            return round(tdee + 500), "Fazla (+500 kal)"
        elif hedef == "Kuvvet Kazan":
            return round(tdee + 200), "Hafif Fazla (+200 kal)"
        else:  # Fit Kal / İdame
            return round(tdee), "İdame"

    @staticmethod
    def makro_hesapla(kalori, hedef, kilo):
        """Protein / Karbonhidrat / Yağ dağılımı (gram)."""
        if hedef in ("Kas Yap", "Hızlı Kas Yap", "Kuvvet Kazan"):
            protein_g = round(kilo * 2.2)  # 2.2g/kg
            yag_g = round(kilo * 1.0)
        elif hedef in ("Kilo Ver", "Hızlı Kilo Ver"):
            protein_g = round(kilo * 2.4)  # Kas korumak için yüksek protein
            yag_g = round(kilo * 0.8)
        else:
            protein_g = round(kilo * 1.8)
            yag_g = round(kilo * 0.9)
        protein_kal = protein_g * 4
        yag_kal = yag_g * 9
        karb_kal = max(0, kalori - protein_kal - yag_kal)
        karb_g = round(karb_kal / 4)
        return protein_g, karb_g, yag_g

    @staticmethod
    def su_ihtiyaci(kilo, aktivite):
        """Günlük su ihtiyacı (litre)."""
        baz = kilo * 0.033
        if aktivite in ("Çok Aktif (6-7 gün/hafta)", "Profesyonel Sporcu"):
            baz += 0.75
        elif aktivite in ("Orta Aktif (3-5 gün/hafta)",):
            baz += 0.5
        return round(baz, 1)

    # ── Antrenman Programları ─────────────────────────────────────────────────

    @staticmethod
    def _baslangic_programi(hafta, hedef):
        if hafta <= 4:
            return {
                "ad": f"Adaptasyon & Temel Güç (Hafta {hafta}/4)",
                "gunler": "Pazartesi / Çarşamba / Cuma  (3 gün)",
                "liste": [
                    ("Squat (Ağırlıksız veya Hafif)", "3 × 15", "Dizleri ayak parmak hizasında tut"),
                    ("Bench Press / Şınav", "3 × 10", "Göğsüne kadar indir"),
                    ("Lat Pulldown / Kürek Çekiş", "3 × 12", "Kürek kemiklerini birleştir"),
                    ("Shoulder Press (Dumbbell)", "3 × 12", "Dirsekleri 90° tut"),
                    ("Romanian Deadlift (Hafif)", "3 × 12", "Bel düz, kalçadan eğil"),
                    ("Plank", "3 × 30 sn", "Karın kaslarını sık"),
                ],
                "dinlenme": "Antrenman günleri arası en az 1 gün dinlen",
                "tavsiye": (
                    "İlk ay amacın doğru formu öğrenmek. Ağırlık önemli değil, "
                    "hareket kalitesi her şey. Her sette son 2 tekrarı zor hissetmelisin. "
                    "Acı hissetmiyorsan ağırlığı biraz artır."
                )
            }
        elif hafta <= 8:
            return {
                "ad": f"Temel Güç Gelişimi (Hafta {hafta}/8)",
                "gunler": "Pazartesi / Çarşamba / Cuma  (3 gün)",
                "liste": [
                    ("Barbell Squat", "4 × 8", "Ağırlığı her haftada 2.5 kg artır"),
                    ("Bench Press", "4 × 8", "Bilek dik, dirsek 45°"),
                    ("Bent-Over Barbell Row", "4 × 8", "Bel düz, göbeğe çek"),
                    ("Overhead Press", "3 × 10", "Baş arkadan geçme"),
                    ("Deadlift", "3 × 6", "Haftanın en önemli hareketi"),
                    ("Dumbbell Curl + Tricep Pushdown", "3 × 12", "Süperset yapabilirsin"),
                ],
                "dinlenme": "Dinlenme günleri: Salı, Perşembe, hafta sonu",
                "tavsiye": (
                    "Lineer ilerleme dönemi: her antrenmanda 2.5 kg ekle. "
                    "Artıramazsan aynı ağırlıkta kal, azaltma. "
                    "Protein alımına dikkat — günde " + str(0) + " g/kg."
                )
            }
        else:
            return {
                "ad": f"İlk Güç Bloğu — 5×5 (Hafta {hafta})",
                "gunler": "A/B Dönüşümlü  (Haftada 3 gün)",
                "liste": [
                    ("Antrenman A: Squat 5×5 / Bench 5×5 / Row 5×5", "", ""),
                    ("Antrenman B: Squat 5×5 / Press 5×5 / Deadlift 1×5", "", ""),
                    ("Accessory: Weighted Plank / Pull-up Negatif", "3 × maks", ""),
                ],
                "dinlenme": "A-dinlenme-B-dinlenme-A ... şeklinde dön",
                "tavsiye": (
                    "StrongLifts 5×5 yöntemi: tüm setleri tamamladıysan 2.5 kg ekle. "
                    "Başaramazsan aynı ağırlıkta kal. Squat her antrenmanda yapılır."
                )
            }

    @staticmethod
    def _orta_programi(hafta, hedef):
        if hedef in ("Kas Yap", "Hızlı Kas Yap"):
            if hafta <= 6:
                return {
                    "ad": f"Hipertrofi Bloğu — Upper/Lower (Hafta {hafta})",
                    "gunler": "Pazartesi/Salı/Perşembe/Cuma  (4 gün)",
                    "liste": [
                        ("Üst A: Bench 4×8 / Row 4×8 / Shoulder 3×10 / Bicep-Tricep 3×12", "", ""),
                        ("Alt A: Squat 4×8 / RDL 4×8 / Leg Press 3×10 / Calf 4×15", "", ""),
                        ("Üst B: Incline DB 4×10 / Pull-up 4×8 / Cable Fly 3×12", "", ""),
                        ("Alt B: Deadlift 4×5 / Bulgarian Split 3×10 / Leg Curl 3×12", "", ""),
                    ],
                    "dinlenme": "Çar-Hafta sonu dinlenme",
                    "tavsiye": (
                        "Her kas grubu haftada 2 kez çalışır. "
                        "60-90 sn dinlenme ile metabolik stres yarat. "
                        "Son sette 'teknik başarısızlık'a kadar git."
                    )
                }
            else:
                return {
                    "ad": f"PPL (Push-Pull-Legs) Programı (Hafta {hafta})",
                    "gunler": "6 gün / 1 gün dinlenme",
                    "liste": [
                        ("Push: Bench+Incline / Shoulder Press / Lateral / Tricep", "4-5 set", ""),
                        ("Pull: Deadlift / Pull-up / Row / Face Pull / Curl", "4-5 set", ""),
                        ("Legs: Squat / Leg Press / RDL / Leg Curl / Calf", "4-5 set", ""),
                        ("Tekrar: Push-Pull-Legs", "", "Her grup haftada 2×"),
                    ],
                    "dinlenme": "Pazar dinlenme",
                    "tavsiye": "PPL en verimli split. Her grup haftada 2 kez uyarılır."
                }
        else:  # Kilo Ver
            return {
                "ad": f"Full Body HIIT + Ağırlık (Hafta {hafta})",
                "gunler": "Pazartesi/Çarşamba/Cuma Ağırlık + Salı/Perşembe Kardiyo",
                "liste": [
                    ("Squat 4×12", "", "Dinlenme 45 sn"),
                    ("Bench Press 4×12", "", ""),
                    ("Bent Row 4×12", "", ""),
                    ("Kardiyo: 20 dk HIIT veya 40 dk tempolu yürüyüş", "", ""),
                    ("Haftada 1 uzun kardiyo (60 dk düşük yoğunluk)", "", ""),
                ],
                "dinlenme": "Hafta sonu 1-2 gün aktif dinlenme (yürüyüş)",
                "tavsiye": "Kalori açığını antrenmanla değil diyetle yarat. Antrenman kasını korur."
            }

    @staticmethod
    def _ileri_programi(hafta, hedef):
        deload = (hafta % 4 == 0)
        if deload:
            return {
                "ad": f"Deload Haftası (Hafta {hafta})",
                "gunler": "3 gün — tüm ağırlıklar %60'a düşür",
                "liste": [
                    ("Squat: 3×3 @ %60 1RM", "", ""),
                    ("Bench: 3×3 @ %60 1RM", "", ""),
                    ("Deadlift: 2×2 @ %60 1RM", "", ""),
                    ("Hafif mobiliyte + esneme çalışması", "", ""),
                ],
                "dinlenme": "Bu hafta bol uyu, iyi beslen",
                "tavsiye": (
                    "Deload zorunlu! Adaptasyon dinlenirken olur. "
                    "Bu haftayı atlarsan uzun vadede daha yavaş gelişirsin."
                )
            }
        if hedef == "Kuvvet Kazan":
            return {
                "ad": f"Kuvvet Periodizasyon — Blok {((hafta-1)//4)+1} (Hafta {hafta})",
                "gunler": "4 gün (Max Effor + Dinamik Effor)",
                "liste": [
                    ("ME Squat/Deadlift varyasyonu × 1RM çalış", "", ""),
                    ("ME Bench varyasyonu × 1RM çalış", "", ""),
                    ("DE Squat: 8×2 @ %65 1RM — HIZLI", "", ""),
                    ("DE Bench: 8×3 @ %65 1RM — HIZLI", "", ""),
                    ("Yardımcı: GHD / Hyperextension / Face Pull / Band çalışma", "", ""),
                ],
                "dinlenme": "ME ve DE günleri arası 1-2 gün",
                "tavsiye": (
                    "Westside Barbell tipi konjugat metod. "
                    "Her haftada farklı egzersiz seç (max effort). "
                    "Dinamik günlerde hız öncelikli."
                )
            }
        else:
            return {
                "ad": f"İleri Hipertrofi — PHAT (Hafta {hafta})",
                "gunler": "5 gün",
                "liste": [
                    ("Üst Güç: Low-rep compound 3-5×3-5", "", ""),
                    ("Alt Güç: Low-rep compound 3-5×3-5", "", ""),
                    ("Dinlenme", "", ""),
                    ("Üst Hipertrofi: 3-4×8-15 pump çalışması", "", ""),
                    ("Alt Hipertrofi + Karın: 3-4×8-15", "", ""),
                ],
                "dinlenme": "Her 4 haftada deload",
                "tavsiye": (
                    "PHAT protokolü güç ve hacmi birleştirir. "
                    "Güç günleri %80-90 1RM, hipertrofi günleri %60-75 1RM."
                )
            }

    # ── Ana Analiz Fonksiyonu ─────────────────────────────────────────────────

    @staticmethod
    def analiz_et(boy, kilo, yas, cinsiyet, seviye, hedef, aktivite, baslangic_tarihi=None):
        # Güvenlik kontrolleri
        boy = max(100, min(250, float(boy)))
        kilo = max(30, min(300, float(kilo)))
        yas = max(10, min(100, int(yas)))

        # VKİ
        metre_boy = boy / 100
        vki = round(kilo / (metre_boy ** 2), 1)
        vki_kategori, vki_renk = FitnessZekasi.vki_kategori(vki)

        # BMR & TDEE
        bmr = round(FitnessZekasi.bmr_hesapla(kilo, boy, yas, cinsiyet))
        tdee = round(FitnessZekasi.tdee_hesapla(bmr, aktivite))

        # Kalori hedefi
        hedef_kalori, kalori_aciklamasi = FitnessZekasi.kalori_hedefi(tdee, hedef)

        # Makrolar
        protein_g, karb_g, yag_g = FitnessZekasi.makro_hesapla(hedef_kalori, hedef, kilo)

        # Su ihtiyacı
        su = FitnessZekasi.su_ihtiyaci(kilo, aktivite)

        # İdeal ağırlık
        ideal_alt, ideal_ust = FitnessZekasi.ideal_agirlik(boy, cinsiyet)

        # Kaçıncı haftadayız
        hafta_sayisi = 1
        if baslangic_tarihi:
            try:
                basla = datetime.datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
                fark = datetime.datetime.now() - basla
                hafta_sayisi = max(1, (fark.days // 7) + 1)
            except Exception:
                hafta_sayisi = 1

        # Program seç
        if seviye == "Başlangıç":
            prog = FitnessZekasi._baslangic_programi(hafta_sayisi, hedef)
        elif seviye == "Orta":
            prog = FitnessZekasi._orta_programi(hafta_sayisi, hedef)
        else:
            prog = FitnessZekasi._ileri_programi(hafta_sayisi, hedef)

        # Kişisel VKİ tavsiyesi
        if vki < 18.5:
            vki_tavsiye = f"Kilonu artırman gerekiyor. İdeal aralık: {ideal_alt}–{ideal_ust} kg."
        elif vki < 25:
            vki_tavsiye = f"Harika! İdeal aralıkta ({ideal_alt}–{ideal_ust} kg). Hedefine odaklan."
        elif vki < 30:
            kg_fazla = round(kilo - ideal_ust, 1)
            vki_tavsiye = f"İdeal kilona ulaşmak için yaklaşık {kg_fazla} kg vermelisin ({ideal_alt}–{ideal_ust} kg arası hedef)."
        else:
            kg_fazla = round(kilo - ideal_ust, 1)
            vki_tavsiye = f"Sağlıklı kilo için {kg_fazla} kg verme hedefi. Doktorana danışmanı öneririz."

        return {
            "vki": vki,
            "vki_kategori": vki_kategori,
            "vki_renk": vki_renk,
            "vki_tavsiye": vki_tavsiye,
            "ideal_alt": ideal_alt,
            "ideal_ust": ideal_ust,
            "bmr": bmr,
            "tdee": tdee,
            "hedef_kalori": hedef_kalori,
            "kalori_aciklamasi": kalori_aciklamasi,
            "protein_g": protein_g,
            "karb_g": karb_g,
            "yag_g": yag_g,
            "su_lt": su,
            "hafta": hafta_sayisi,
            "program_adi": prog["ad"],
            "program_gunler": prog.get("gunler", ""),
            "program_liste": prog["liste"],
            "program_dinlenme": prog.get("dinlenme", ""),
            "tavsiye": prog["tavsiye"],
            "hedef": hedef,
            "seviye": seviye,
        }

    @staticmethod
    def ilerleme_analizi(gecmis_listesi):
        """Geçmiş kayıtlara göre ilerleme özeti üret."""
        if len(gecmis_listesi) < 2:
            return None
        son = gecmis_listesi[-1]
        ilk = gecmis_listesi[0]
        kilo_fark = round(son.get("kilo", 0) - ilk.get("kilo", 0), 1)
        vki_fark = round(son.get("vki", 0) - ilk.get("vki", 0), 1)
        gun_fark = 0
        try:
            t1 = datetime.datetime.strptime(ilk["tarih"], "%Y-%m-%d")
            t2 = datetime.datetime.strptime(son["tarih"], "%Y-%m-%d")
            gun_fark = (t2 - t1).days
        except Exception:
            pass
        return {
            "kilo_fark": kilo_fark,
            "vki_fark": vki_fark,
            "gun_fark": gun_fark,
            "kayit_sayisi": len(gecmis_listesi),
        }

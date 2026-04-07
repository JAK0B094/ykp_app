import customtkinter as ctk
from src.assets.hesaplamalar import FitnessZekasi
from src.data.kimlik_dogrulama import KimlikDogrulama
import datetime

class FitnessKocuSayfasi(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        self.kullanici = kullanici_adi
        self.auth = KimlikDogrulama()
        self.son_analiz = None

        self.sol_panel = ctk.CTkFrame(self, width=290, corner_radius=12)
        self.sol_panel.pack(side="left", fill="y", padx=(12, 6), pady=12)
        self.sol_panel.pack_propagate(False)

        self.sag_panel = ctk.CTkFrame(self, corner_radius=12)
        self.sag_panel.pack(side="right", fill="both", expand=True, padx=(6, 12), pady=12)

        self._sol_panel_olustur()
        self._sag_panel_olustur()
        self._profil_yukle()

    # ── Sol Panel ─────────────────────────────────────────────────────────────

    def _sol_panel_olustur(self):
        ctk.CTkLabel(self.sol_panel, text="🏋️ Fitness Koçu",
                     font=("Roboto", 17, "bold")).pack(pady=(18, 2))
        ctk.CTkLabel(self.sol_panel, text="Bilgilerini doldur, koçun seni yönlendirsin.",
                     font=("Roboto", 10), text_color="gray", wraplength=250).pack(pady=(0, 12))

        def alan(parent, etiket, widget):
            ctk.CTkLabel(parent, text=etiket, font=("Roboto", 11)).pack(anchor="w", padx=14)
            widget.pack(fill="x", padx=14, pady=(2, 8))

        self.boy_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Boy (cm) — Örn: 175", height=34)
        alan(self.sol_panel, "Boy (cm):", self.boy_e)

        self.kilo_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Kilo (kg) — Örn: 70", height=34)
        alan(self.sol_panel, "Kilo (kg):", self.kilo_e)

        self.yas_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Yaş — Örn: 25", height=34)
        alan(self.sol_panel, "Yaş:", self.yas_e)

        self.cinsiyet_cb = ctk.CTkComboBox(self.sol_panel, values=["Erkek", "Kadın"],
                                            height=34, state="readonly")
        self.cinsiyet_cb.set("Erkek")
        alan(self.sol_panel, "Cinsiyet:", self.cinsiyet_cb)

        self.aktivite_cb = ctk.CTkComboBox(self.sol_panel, height=34, state="readonly",
            values=["Hareketsiz (Masa başı)", "Az Aktif (1-2 gün/hafta)",
                    "Orta Aktif (3-5 gün/hafta)", "Çok Aktif (6-7 gün/hafta)",
                    "Profesyonel Sporcu"])
        self.aktivite_cb.set("Orta Aktif (3-5 gün/hafta)")
        alan(self.sol_panel, "Aktivite Seviyesi:", self.aktivite_cb)

        self.seviye_cb = ctk.CTkComboBox(self.sol_panel, values=["Başlangıç", "Orta", "İleri"],
                                          height=34, state="readonly")
        self.seviye_cb.set("Başlangıç")
        alan(self.sol_panel, "Antrenman Seviyesi:", self.seviye_cb)

        self.hedef_cb = ctk.CTkComboBox(self.sol_panel, height=34, state="readonly",
            values=["Kas Yap", "Hızlı Kas Yap", "Kilo Ver", "Hızlı Kilo Ver",
                    "Kuvvet Kazan", "Fit Kal"])
        self.hedef_cb.set("Kas Yap")
        alan(self.sol_panel, "Hedef:", self.hedef_cb)

        ctk.CTkButton(self.sol_panel, text="🔍  Analizi Başlat",
                      command=self.guncelle, height=40,
                      fg_color="#e67e22", hover_color="#d35400",
                      font=("Roboto", 13, "bold")).pack(fill="x", padx=14, pady=(4, 4))

        self.btn_kaydet = ctk.CTkButton(self.sol_panel, text="💾  Bugünü Kaydet",
                                         command=self.veriyi_kaydet, height=40,
                                         fg_color="#27ae60", hover_color="#1e8449",
                                         font=("Roboto", 12), state="disabled")
        self.btn_kaydet.pack(fill="x", padx=14, pady=4)

        self.hata_label = ctk.CTkLabel(self.sol_panel, text="", font=("Roboto", 10),
                                        text_color="#e74c3c", wraplength=255)
        self.hata_label.pack(pady=4)

    # ── Sağ Panel ─────────────────────────────────────────────────────────────

    def _sag_panel_olustur(self):
        self.sekme = ctk.CTkTabview(self.sag_panel, corner_radius=10)
        self.sekme.pack(fill="both", expand=True, padx=8, pady=8)
        for s in ["📊 Analiz", "📋 Program", "🥗 Beslenme", "📈 İlerleme"]:
            self.sekme.add(s)

        self._analiz_sekmesi()
        self._program_sekmesi()
        self._beslenme_sekmesi()
        self._ilerleme_sekmesi()

    def _analiz_sekmesi(self):
        t = self.sekme.tab("📊 Analiz")

        # VKİ kartı
        self.vki_kart = ctk.CTkFrame(t, corner_radius=12, height=105)
        self.vki_kart.pack(fill="x", padx=10, pady=(10, 6))
        self.vki_kart.pack_propagate(False)

        sol = ctk.CTkFrame(self.vki_kart, fg_color="transparent")
        sol.pack(side="left", fill="both", expand=True)
        sag = ctk.CTkFrame(self.vki_kart, fg_color="transparent")
        sag.pack(side="right", fill="both", expand=True)

        self.vki_label = ctk.CTkLabel(sol, text="VKİ: —",
                                       font=("Roboto", 30, "bold"), text_color="#3498db")
        self.vki_label.pack(anchor="w", padx=16, pady=(16, 2))
        self.kategori_label = ctk.CTkLabel(sol, text="Analiz bekleniyor...",
                                            font=("Roboto", 12), text_color="gray")
        self.kategori_label.pack(anchor="w", padx=16)

        self.bmr_label = ctk.CTkLabel(sag, text="BMR: — kal",
                                       font=("Roboto", 12), text_color="gray")
        self.bmr_label.pack(anchor="e", padx=16, pady=(14, 2))
        self.tdee_label = ctk.CTkLabel(sag, text="TDEE: — kal",
                                        font=("Roboto", 12), text_color="gray")
        self.tdee_label.pack(anchor="e", padx=16)
        self.hedef_kal_label = ctk.CTkLabel(sag, text="Hedef: — kal",
                                              font=("Roboto", 12, "bold"), text_color="#e67e22")
        self.hedef_kal_label.pack(anchor="e", padx=16)

        # İdeal kilo
        self.ideal_frame = ctk.CTkFrame(t, corner_radius=10, height=42)
        self.ideal_frame.pack(fill="x", padx=10, pady=4)
        self.ideal_frame.pack_propagate(False)
        self.ideal_label = ctk.CTkLabel(self.ideal_frame, text="İdeal Kilo: —",
                                         font=("Roboto", 12))
        self.ideal_label.pack(side="left", padx=16, pady=10)
        self.su_label = ctk.CTkLabel(self.ideal_frame, text="Su: — lt/gün",
                                      font=("Roboto", 12), text_color="#3498db")
        self.su_label.pack(side="right", padx=16)

        # VKİ tavsiyesi
        self.tavsiye_frame = ctk.CTkFrame(t, corner_radius=10)
        self.tavsiye_frame.pack(fill="both", expand=True, padx=10, pady=4)
        ctk.CTkLabel(self.tavsiye_frame, text="💡 Koç Yorumu",
                     font=("Roboto", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 3))
        self.tavsiye_label = ctk.CTkLabel(self.tavsiye_frame, text="Lütfen önce analiz başlat.",
                                           font=("Roboto", 11), text_color="gray",
                                           wraplength=420, justify="left")
        self.tavsiye_label.pack(anchor="w", padx=14, pady=(0, 10))

        # Hafta bilgisi
        hafta_frame = ctk.CTkFrame(t, corner_radius=10, height=40)
        hafta_frame.pack(fill="x", padx=10, pady=4)
        hafta_frame.pack_propagate(False)
        self.hafta_label = ctk.CTkLabel(hafta_frame, text="Program haftası: —", font=("Roboto", 12))
        self.hafta_label.pack(side="left", padx=16, pady=10)
        self.hedef_label = ctk.CTkLabel(hafta_frame, text="Hedef: —", font=("Roboto", 12))
        self.hedef_label.pack(side="right", padx=16)

    def _program_sekmesi(self):
        t = self.sekme.tab("📋 Program")
        self.prog_baslik = ctk.CTkLabel(t, text="Analiz yapıldıktan sonra program oluşturulacak.",
                                         font=("Roboto", 14, "bold"), wraplength=450)
        self.prog_baslik.pack(pady=(14, 2))
        self.prog_gunler = ctk.CTkLabel(t, text="", font=("Roboto", 11), text_color="#3498db")
        self.prog_gunler.pack()
        self.prog_dinlenme = ctk.CTkLabel(t, text="", font=("Roboto", 11), text_color="gray",
                                           wraplength=450)
        self.prog_dinlenme.pack(pady=(2, 6))

        self.egzersiz_frame = ctk.CTkScrollableFrame(t, corner_radius=8, label_text="Egzersizler")
        self.egzersiz_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.prog_tavsiye_label = ctk.CTkLabel(t, text="", font=("Roboto", 11),
                                                text_color="#f39c12", wraplength=450, justify="left")
        self.prog_tavsiye_label.pack(padx=14, pady=6)

    def _beslenme_sekmesi(self):
        t = self.sekme.tab("🥗 Beslenme")

        # Kalori/makro kartı
        self.makro_frame = ctk.CTkScrollableFrame(t, corner_radius=8)
        self.makro_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.makro_placeholder = ctk.CTkLabel(self.makro_frame,
            text="Analiz yaptıktan sonra kişiselleştirilmiş beslenme planın burada görünecek.",
            font=("Roboto", 12), text_color="gray", wraplength=420)
        self.makro_placeholder.pack(pady=40)

    def _ilerleme_sekmesi(self):
        t = self.sekme.tab("📈 İlerleme")

        self.ozet_frame = ctk.CTkFrame(t, corner_radius=10, height=70)
        self.ozet_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.ozet_frame.pack_propagate(False)
        self.ozet_label = ctk.CTkLabel(self.ozet_frame, text="İlerleme özeti için en az 2 kayıt gerekli.",
                                        font=("Roboto", 12), text_color="gray")
        self.ozet_label.pack(pady=20)

        ctk.CTkLabel(t, text="Geçmiş Kayıtlar", font=("Roboto", 13, "bold")).pack(anchor="w", padx=14, pady=(6, 2))
        self.gecmis_frame = ctk.CTkScrollableFrame(t, corner_radius=8)
        self.gecmis_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self._gecmis_yukle()

    # ── Yardımcı ─────────────────────────────────────────────────────────────

    def _profil_yukle(self):
        """Kaydedilmiş profil varsa formu önceden doldur."""
        try:
            profil = self.auth.fitness_profil_getir(self.kullanici)
            if not profil:
                return
            for alan, widget in [
                ("boy", self.boy_e), ("kilo", self.kilo_e), ("yas", self.yas_e)
            ]:
                if profil.get(alan):
                    widget.delete(0, "end")
                    widget.insert(0, str(profil[alan]))
            if profil.get("cinsiyet") in ("Erkek", "Kadın"):
                self.cinsiyet_cb.set(profil["cinsiyet"])
            if profil.get("aktivite"):
                self.aktivite_cb.set(profil["aktivite"])
            if profil.get("seviye"):
                self.seviye_cb.set(profil["seviye"])
            if profil.get("hedef"):
                self.hedef_cb.set(profil["hedef"])
        except Exception:
            pass

    def _gecmis_yukle(self):
        for w in self.gecmis_frame.winfo_children():
            w.destroy()

        try:
            gecmis = self.auth.fitness_verisi_getir(self.kullanici)
        except Exception:
            gecmis = []

        if not gecmis:
            ctk.CTkLabel(self.gecmis_frame,
                         text="Henüz kayıt yok. Analiz yap ve 'Bugünü Kaydet' butonuna bas.",
                         font=("Roboto", 12), text_color="gray").pack(pady=30)
            return

        # İlerleme özeti
        ozet = FitnessZekasi.ilerleme_analizi(gecmis)
        if ozet:
            kilo_fark = ozet["kilo_fark"]
            vki_fark = ozet["vki_fark"]
            gun_fark = ozet["gun_fark"]
            yon_kilo = "▲" if kilo_fark > 0 else ("▼" if kilo_fark < 0 else "━")
            renk = "#27ae60" if kilo_fark < 0 else ("#e74c3c" if kilo_fark > 0 else "gray")
            ozet_txt = (f"{ozet['kayit_sayisi']} kayıt  |  {gun_fark} gün  |  "
                        f"Kilo: {yon_kilo} {abs(kilo_fark)} kg  |  VKİ: {vki_fark:+.1f}")
            self.ozet_label.configure(text=ozet_txt, text_color=renk)

        # Kayıtları listele
        for kayit in reversed(gecmis[-20:]):
            satir = ctk.CTkFrame(self.gecmis_frame, corner_radius=8, height=48)
            satir.pack(fill="x", padx=5, pady=2)
            satir.pack_propagate(False)

            ctk.CTkLabel(satir, text=f"📅 {kayit.get('tarih','?')}",
                         font=("Roboto", 11), text_color="gray", width=105).pack(side="left", padx=8)

            ctk.CTkLabel(satir, text=f"⚖️ {kayit.get('kilo','?')} kg",
                         font=("Roboto", 12)).pack(side="left", padx=8)

            vki = kayit.get("vki", None)
            if vki is not None:
                try:
                    _, renk = FitnessZekasi.vki_kategori(float(vki))
                except Exception:
                    renk = "gray"
                ctk.CTkLabel(satir, text=f"VKİ: {vki}",
                             font=("Roboto", 12, "bold"), text_color=renk).pack(side="left", padx=8)

            if kayit.get("hedef_kalori"):
                ctk.CTkLabel(satir, text=f"🔥 {kayit['hedef_kalori']} kal",
                             font=("Roboto", 11), text_color="#e67e22").pack(side="left", padx=4)

            prog = kayit.get("program", "")
            if prog:
                ctk.CTkLabel(satir, text=prog[:30] + ("…" if len(prog) > 30 else ""),
                             font=("Roboto", 10), text_color="gray").pack(side="right", padx=8)

    # ── Analiz ───────────────────────────────────────────────────────────────

    def guncelle(self):
        self.hata_label.configure(text="")
        try:
            boy_str = self.boy_e.get().strip().replace(",", ".")
            kilo_str = self.kilo_e.get().strip().replace(",", ".")
            yas_str = self.yas_e.get().strip()

            if not boy_str or not kilo_str or not yas_str:
                self.hata_label.configure(text="Boy, kilo ve yaş alanlarını doldur!")
                return

            b = float(boy_str)
            k = float(kilo_str)
            y = int(yas_str)

            if not (100 <= b <= 250):
                self.hata_label.configure(text="Boy 100–250 cm arasında olmalıdır.")
                return
            if not (30 <= k <= 300):
                self.hata_label.configure(text="Kilo 30–300 kg arasında olmalıdır.")
                return
            if not (10 <= y <= 100):
                self.hata_label.configure(text="Yaş 10–100 arasında olmalıdır.")
                return

            cinsiyet = self.cinsiyet_cb.get()
            seviye = self.seviye_cb.get()
            hedef = self.hedef_cb.get()
            aktivite = self.aktivite_cb.get()

            # Başlangıç tarihini profilden al veya bugün kabul et
            profil = self.auth.fitness_profil_getir(self.kullanici) or {}
            baslangic = profil.get("baslangic_tarihi", str(datetime.date.today()))

            self.son_analiz = FitnessZekasi.analiz_et(
                b, k, y, cinsiyet, seviye, hedef, aktivite, baslangic
            )

            self._analiz_goster()
            self._program_goster()
            self._beslenme_goster()

            self.btn_kaydet.configure(state="normal", fg_color="#27ae60",
                                       text="💾  Bugünü Kaydet")

            # Profili otomatik kaydet
            try:
                self.auth.fitness_profil_kaydet(self.kullanici, {
                    "boy": b, "kilo": k, "yas": y,
                    "cinsiyet": cinsiyet, "aktivite": aktivite,
                    "seviye": seviye, "hedef": hedef,
                    "baslangic_tarihi": baslangic
                })
            except Exception:
                pass

            self.sekme.set("📊 Analiz")

        except ValueError:
            self.hata_label.configure(text="Lütfen geçerli sayısal değer girin.")
        except Exception as e:
            self.hata_label.configure(text=f"Hata: {e}")

    def _analiz_goster(self):
        a = self.son_analiz
        self.vki_label.configure(text=f"VKİ: {a['vki']}", text_color=a["vki_renk"])
        self.kategori_label.configure(
            text=f"Kategori: {a['vki_kategori']}  |  İdeal: {a['ideal_alt']}–{a['ideal_ust']} kg",
            text_color=a["vki_renk"])
        self.bmr_label.configure(text=f"BMR: {a['bmr']} kal/gün")
        self.tdee_label.configure(text=f"TDEE: {a['tdee']} kal/gün")
        self.hedef_kal_label.configure(
            text=f"Hedef: {a['hedef_kalori']} kal  ({a['kalori_aciklamasi']})")
        self.ideal_label.configure(
            text=f"İdeal Kilo: {a['ideal_alt']}–{a['ideal_ust']} kg")
        self.su_label.configure(text=f"💧 {a['su_lt']} lt/gün")
        self.tavsiye_label.configure(text=a["vki_tavsiye"])
        self.hafta_label.configure(text=f"Program haftası: {a['hafta']}")
        self.hedef_label.configure(text=f"Hedef: {a['hedef']}")

    def _program_goster(self):
        a = self.son_analiz
        self.prog_baslik.configure(text=a["program_adi"])
        self.prog_gunler.configure(text=f"📆 {a['program_gunler']}")
        self.prog_dinlenme.configure(text=f"😴 {a['program_dinlenme']}")
        self.prog_tavsiye_label.configure(text=f"💡 {a['tavsiye']}")

        for w in self.egzersiz_frame.winfo_children():
            w.destroy()

        for i, egzersiz in enumerate(a.get("program_liste", [])):
            if isinstance(egzersiz, tuple):
                ad, set_rep, not_ = egzersiz
                satir = ctk.CTkFrame(self.egzersiz_frame, corner_radius=7)
                satir.pack(fill="x", padx=5, pady=3)
                ust = ctk.CTkFrame(satir, fg_color="transparent")
                ust.pack(fill="x", padx=10, pady=(6, 1))
                ctk.CTkLabel(ust, text=f"{i+1}.", font=("Roboto", 12, "bold"),
                             width=22, text_color="#e67e22").pack(side="left")
                ctk.CTkLabel(ust, text=ad, font=("Roboto", 12, "bold")).pack(side="left", padx=4)
                if set_rep:
                    ctk.CTkLabel(ust, text=set_rep, font=("Roboto", 11),
                                 text_color="#3498db").pack(side="right")
                if not_:
                    ctk.CTkLabel(satir, text=f"   ↳ {not_}", font=("Roboto", 10),
                                 text_color="gray").pack(anchor="w", padx=14, pady=(0, 5))
            else:
                satir = ctk.CTkFrame(self.egzersiz_frame, corner_radius=7, height=36)
                satir.pack(fill="x", padx=5, pady=2)
                satir.pack_propagate(False)
                ctk.CTkLabel(satir, text=f"{i+1}.  {egzersiz}",
                             font=("Roboto", 11)).pack(side="left", padx=12, pady=8)

    def _beslenme_goster(self):
        a = self.son_analiz
        for w in self.makro_frame.winfo_children():
            w.destroy()

        # Kalori Kartı
        kal_kart = ctk.CTkFrame(self.makro_frame, corner_radius=10)
        kal_kart.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(kal_kart, text="🔥 Günlük Kalori Hedefi",
                     font=("Roboto", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        ctk.CTkLabel(kal_kart,
                     text=f"{a['hedef_kalori']} kal  —  {a['kalori_aciklamasi']}",
                     font=("Roboto", 18, "bold"), text_color="#e67e22").pack(padx=14, pady=(2, 4))
        ctk.CTkLabel(kal_kart,
                     text=f"BMR: {a['bmr']} kal  |  TDEE: {a['tdee']} kal",
                     font=("Roboto", 11), text_color="gray").pack(pady=(0, 10))

        # Makro Kartı
        makro_kart = ctk.CTkFrame(self.makro_frame, corner_radius=10)
        makro_kart.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(makro_kart, text="⚖️ Makro Besin Dağılımı",
                     font=("Roboto", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 5))

        for etiket, deger, birim, renk, aciklama in [
            ("💪 Protein", a["protein_g"], "g/gün", "#e74c3c",
             f"~{a['protein_g']*4} kal · {round(a['protein_g']/a['hedef_kalori']*100)}% oran"),
            ("🌾 Karbonhidrat", a["karb_g"], "g/gün", "#f39c12",
             f"~{a['karb_g']*4} kal · {round(a['karb_g']*4/a['hedef_kalori']*100)}% oran"),
            ("🫒 Yağ", a["yag_g"], "g/gün", "#27ae60",
             f"~{a['yag_g']*9} kal · {round(a['yag_g']*9/a['hedef_kalori']*100)}% oran"),
        ]:
            satir = ctk.CTkFrame(makro_kart, fg_color="transparent", height=48)
            satir.pack(fill="x", padx=14)
            satir.pack_propagate(False)
            ctk.CTkLabel(satir, text=etiket, font=("Roboto", 12)).pack(side="left", pady=10)
            ctk.CTkLabel(satir, text=f"{deger} {birim}",
                         font=("Roboto", 13, "bold"), text_color=renk).pack(side="right", padx=5)
            ctk.CTkLabel(satir, text=aciklama,
                         font=("Roboto", 10), text_color="gray").pack(side="right", padx=10)
        ctk.CTkFrame(makro_kart, height=8, fg_color="transparent").pack()

        # Su
        su_kart = ctk.CTkFrame(self.makro_frame, corner_radius=10, height=58)
        su_kart.pack(fill="x", padx=5, pady=5)
        su_kart.pack_propagate(False)
        ctk.CTkLabel(su_kart, text=f"💧 Günlük Su: {a['su_lt']} litre",
                     font=("Roboto", 13, "bold"), text_color="#3498db").pack(side="left", padx=14)
        ctk.CTkLabel(su_kart, text="≈ 8-12 bardak", font=("Roboto", 11),
                     text_color="gray").pack(side="right", padx=14)

        # Beslenme İpuçları
        ipucu_kart = ctk.CTkFrame(self.makro_frame, corner_radius=10)
        ipucu_kart.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(ipucu_kart, text="📌 Beslenme Tavsiyeleri",
                     font=("Roboto", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 5))

        hedef = a.get("hedef", "")
        if hedef in ("Kas Yap", "Hızlı Kas Yap"):
            ipuclar = [
                "Proteini gün içine dengeli dağıt (her 3-4 saatte bir).",
                "Antrenman öncesi karbonhidrat, sonrası protein ağırlıklı beslen.",
                "Yatmadan önce kazein protein (yoğurt, süt) kas sentezini artırır.",
                "Kreatinin monohydrat 3-5g/gün kuvveti artırır (bilimsel kanıt var).",
                "Haftalık kalori fazlasını 200-300 kal'de tut — hızlı bulk yağ yapar.",
            ]
        elif hedef in ("Kilo Ver", "Hızlı Kilo Ver"):
            ipuclar = [
                "Proteini yüksek tut — kas kaybını önler ve tokluk verir.",
                "Karbonhidratı antrenman etrafına topla, geceleri azalt.",
                "Öğün atlamak yerine porsiyonları küçült.",
                "Yüksek lifli sebzeler hacim katar, az kalori içerir.",
                "Kalori açığını 500-750 ile sınırla — fazlası kas yitirir.",
            ]
        elif hedef == "Kuvvet Kazan":
            ipuclar = [
                "Karbonhidrat antrenman performansının temelidir, azaltma.",
                "Antrenman öncesi 1-2 saat karbonhidrat+protein al.",
                "Kreatinin ve beta-alanin kuvvet için destek sağlar.",
                "Haftalık +200 kal fazla tut — kuvvet için kalori şart.",
                "Dinlenme günlerinde protein alımını sabit tut, karbonhidratı düşür.",
            ]
        else:
            ipuclar = [
                "TDEE'ye eşit kalori al, kilo sabit kalır.",
                "Besin çeşitliliğini artır, işlenmiş gıdayı azalt.",
                "Her ana öğünde protein kaynağı olsun.",
                "Sebze ve meyveyi ihmal etme — mikro besinler kritik.",
            ]

        for ip in ipuclar:
            ctk.CTkLabel(ipucu_kart, text=f"• {ip}", font=("Roboto", 11),
                         text_color="gray", anchor="w", justify="left",
                         wraplength=430).pack(anchor="w", padx=14, pady=2)
        ctk.CTkFrame(ipucu_kart, height=8, fg_color="transparent").pack()

    # ── Kaydet ───────────────────────────────────────────────────────────────

    def veriyi_kaydet(self):
        if not self.son_analiz:
            return
        try:
            k = float(self.kilo_e.get().replace(",", "."))
        except Exception:
            k = 0
        kayit = {
            "tarih": str(datetime.date.today()),
            "kilo": k,
            "vki": self.son_analiz["vki"],
            "hedef_kalori": self.son_analiz["hedef_kalori"],
            "program": self.son_analiz["program_adi"],
            "seviye": self.son_analiz["seviye"],
        }
        try:
            self.auth.fitness_verisi_kaydet(self.kullanici, kayit)
            self.btn_kaydet.configure(text="✓ Kaydedildi!", state="disabled", fg_color="#7f8c8d")
            self._gecmis_yukle()
            self.sekme.set("📈 İlerleme")
            self.after(3000, lambda: self.btn_kaydet.configure(
                text="💾  Bugünü Kaydet", state="normal", fg_color="#27ae60"))
        except Exception as e:
            self.hata_label.configure(text=f"Kaydedilemedi: {e}")

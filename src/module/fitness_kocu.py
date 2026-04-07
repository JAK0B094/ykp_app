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

        # Ana düzen: sol panel + sağ panel
        self.sol_panel = ctk.CTkFrame(self, width=300, corner_radius=12)
        self.sol_panel.pack(side="left", fill="y", padx=(15, 8), pady=15)
        self.sol_panel.pack_propagate(False)

        self.sag_panel = ctk.CTkFrame(self, corner_radius=12)
        self.sag_panel.pack(side="right", fill="both", expand=True, padx=(8, 15), pady=15)

        self._sol_panel_olustur()
        self._sag_panel_olustur()

    def _sol_panel_olustur(self):
        ctk.CTkLabel(
            self.sol_panel, text="🏋️ Fitness Koçu",
            font=("Roboto", 18, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.sol_panel, text="Bilgilerini girerek kişisel\nantrenman programını al.",
            font=("Roboto", 11), text_color="gray"
        ).pack(pady=(0, 15))

        ctk.CTkLabel(self.sol_panel, text="Boy (cm):", font=("Roboto", 12)).pack(anchor="w", padx=15)
        self.boy_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Örn: 175", height=38)
        self.boy_e.pack(fill="x", padx=15, pady=(3, 10))

        ctk.CTkLabel(self.sol_panel, text="Kilo (kg):", font=("Roboto", 12)).pack(anchor="w", padx=15)
        self.kilo_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Örn: 70", height=38)
        self.kilo_e.pack(fill="x", padx=15, pady=(3, 10))

        ctk.CTkLabel(self.sol_panel, text="Yaş:", font=("Roboto", 12)).pack(anchor="w", padx=15)
        self.yas_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Örn: 25", height=38)
        self.yas_e.pack(fill="x", padx=15, pady=(3, 10))

        ctk.CTkLabel(self.sol_panel, text="Seviye:", font=("Roboto", 12)).pack(anchor="w", padx=15)
        self.seviye_cb = ctk.CTkComboBox(
            self.sol_panel,
            values=["Başlangıç", "Orta", "İleri"],
            height=38, state="readonly"
        )
        self.seviye_cb.set("Başlangıç")
        self.seviye_cb.pack(fill="x", padx=15, pady=(3, 10))

        ctk.CTkLabel(self.sol_panel, text="Hedef:", font=("Roboto", 12)).pack(anchor="w", padx=15)
        self.hedef_cb = ctk.CTkComboBox(
            self.sol_panel,
            values=["Kas Yap", "Kilo Ver", "Fit Kal", "Kuvvet Kazan"],
            height=38, state="readonly"
        )
        self.hedef_cb.set("Kas Yap")
        self.hedef_cb.pack(fill="x", padx=15, pady=(3, 15))

        ctk.CTkButton(
            self.sol_panel, text="🔍 Analizi Başlat", command=self.guncelle,
            height=42, fg_color="#e67e22", hover_color="#d35400",
            font=("Roboto", 13, "bold")
        ).pack(fill="x", padx=15, pady=5)

        self.btn_kaydet = ctk.CTkButton(
            self.sol_panel, text="💾 Bugünü Kaydet", command=self.veriyi_islet,
            height=42, fg_color="#27ae60", hover_color="#1e8449",
            font=("Roboto", 13), state="disabled"
        )
        self.btn_kaydet.pack(fill="x", padx=15, pady=5)

        self.hata_label = ctk.CTkLabel(
            self.sol_panel, text="", font=("Roboto", 11), text_color="#e74c3c", wraplength=250
        )
        self.hata_label.pack(pady=5)

    def _sag_panel_olustur(self):
        self.sekme = ctk.CTkTabview(self.sag_panel, corner_radius=10)
        self.sekme.pack(fill="both", expand=True, padx=10, pady=10)
        self.sekme.add("📊 Analiz")
        self.sekme.add("📋 Program")
        self.sekme.add("📈 Geçmiş")

        # Analiz sekmesi
        analiz = self.sekme.tab("📊 Analiz")
        self.vki_frame = ctk.CTkFrame(analiz, corner_radius=12, height=110)
        self.vki_frame.pack(fill="x", padx=10, pady=10)
        self.vki_frame.pack_propagate(False)

        self.vki_label = ctk.CTkLabel(
            self.vki_frame, text="VKİ: —",
            font=("Roboto", 32, "bold"), text_color="#3498db"
        )
        self.vki_label.pack(pady=(15, 3))

        self.kategori_label = ctk.CTkLabel(
            self.vki_frame, text="Analiz yapmak için sol paneli doldur",
            font=("Roboto", 13), text_color="gray"
        )
        self.kategori_label.pack()

        bilgi_frame = ctk.CTkFrame(analiz, corner_radius=10)
        bilgi_frame.pack(fill="x", padx=10, pady=5)

        self.hafta_label = ctk.CTkLabel(bilgi_frame, text="Hafta: —", font=("Roboto", 13))
        self.hafta_label.pack(side="left", padx=20, pady=10)

        self.hedef_label = ctk.CTkLabel(bilgi_frame, text="Hedef: —", font=("Roboto", 13))
        self.hedef_label.pack(side="right", padx=20, pady=10)

        self.tavsiye_frame = ctk.CTkFrame(analiz, corner_radius=10)
        self.tavsiye_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(self.tavsiye_frame, text="💡 Koç Tavsiyesi", font=("Roboto", 13, "bold")).pack(anchor="w", padx=15, pady=(12, 3))
        self.tavsiye_label = ctk.CTkLabel(
            self.tavsiye_frame, text="—",
            font=("Roboto", 12), wraplength=380, justify="left", text_color="gray"
        )
        self.tavsiye_label.pack(anchor="w", padx=15, pady=(0, 12))

        # Program sekmesi
        program = self.sekme.tab("📋 Program")
        self.program_baslik = ctk.CTkLabel(
            program, text="Program henüz oluşturulmadı",
            font=("Roboto", 15, "bold")
        )
        self.program_baslik.pack(pady=15)

        self.egzersiz_frame = ctk.CTkScrollableFrame(program, label_text="Egzersizler", corner_radius=8)
        self.egzersiz_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Geçmiş sekmesi
        gecmis = self.sekme.tab("📈 Geçmiş")
        ctk.CTkLabel(gecmis, text="Fitness Geçmişi", font=("Roboto", 15, "bold")).pack(pady=10)

        self.gecmis_frame = ctk.CTkScrollableFrame(gecmis, corner_radius=8)
        self.gecmis_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self._gecmis_yukle()

    def _gecmis_yukle(self):
        for w in self.gecmis_frame.winfo_children():
            w.destroy()

        gecmis = self.auth.fitness_verisi_getir(self.kullanici)
        if not gecmis:
            ctk.CTkLabel(
                self.gecmis_frame, text="Henüz kayıtlı veri yok.\nAnaliz yap ve 'Bugünü Kaydet' butonuna tıkla.",
                font=("Roboto", 12), text_color="gray"
            ).pack(pady=30)
            return

        for kayit in reversed(gecmis[-15:]):
            satir = ctk.CTkFrame(self.gecmis_frame, corner_radius=8, height=52)
            satir.pack(fill="x", padx=5, pady=3)
            satir.pack_propagate(False)

            ctk.CTkLabel(
                satir, text=f"📅 {kayit.get('tarih', '?')}",
                font=("Roboto", 11), text_color="gray", width=100
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                satir, text=f"⚖️ {kayit.get('kilo', '?')} kg",
                font=("Roboto", 12)
            ).pack(side="left", padx=10)

            vki = kayit.get("vki", "?")
            _, renk = FitnessZekasi.vki_kategori(float(vki)) if vki != "?" else ("—", "gray")
            ctk.CTkLabel(
                satir, text=f"VKİ: {vki}",
                font=("Roboto", 12, "bold"), text_color=renk
            ).pack(side="left", padx=10)

            ctk.CTkLabel(
                satir, text=kayit.get("program", ""),
                font=("Roboto", 11), text_color="gray"
            ).pack(side="right", padx=10)

    def guncelle(self):
        self.hata_label.configure(text="")
        try:
            b = float(self.boy_e.get())
            k = float(self.kilo_e.get())
            y = int(self.yas_e.get()) if self.yas_e.get().strip() else 25
            sev = self.seviye_cb.get()
            hedef = self.hedef_cb.get()

            if not (100 <= b <= 250):
                self.hata_label.configure(text="Boy 100-250 cm arasında olmalıdır.")
                return
            if not (30 <= k <= 300):
                self.hata_label.configure(text="Kilo 30-300 kg arasında olmalıdır.")
                return

            self.son_analiz = FitnessZekasi.analiz_et(b, k, y, sev, hedef, "2026-01-01")
            self.son_analiz["hedef"] = hedef
            self._analiz_goster(self.son_analiz)
            self.btn_kaydet.configure(state="normal", fg_color="#27ae60")
            self.sekme.set("📊 Analiz")
        except ValueError:
            self.hata_label.configure(text="Lütfen geçerli sayısal değer girin.")
        except Exception as e:
            self.hata_label.configure(text=f"Hata: {e}")

    def _analiz_goster(self, analiz):
        vki = analiz["vki"]
        kategori = analiz["vki_kategori"]
        renk = analiz["vki_renk"]

        self.vki_label.configure(text=f"VKİ: {vki}", text_color=renk)
        self.kategori_label.configure(text=f"Kategori: {kategori}", text_color=renk)
        self.hafta_label.configure(text=f"Hafta: {analiz['hafta']}")
        self.hedef_label.configure(text=f"Hedef: {analiz.get('hedef', '—')}")
        self.tavsiye_label.configure(text=analiz["tavsiye"] or "—")

        self.program_baslik.configure(text=analiz["program_adi"] or "Program")
        for w in self.egzersiz_frame.winfo_children():
            w.destroy()

        for i, egzersiz in enumerate(analiz.get("program_liste", [])):
            satir = ctk.CTkFrame(self.egzersiz_frame, corner_radius=7, height=38)
            satir.pack(fill="x", padx=5, pady=2)
            satir.pack_propagate(False)
            no_label = ctk.CTkLabel(
                satir, text=f"{i+1}.", font=("Roboto", 12, "bold"),
                width=25, text_color="#e67e22"
            )
            no_label.pack(side="left", padx=(10, 5), pady=5)
            ctk.CTkLabel(satir, text=egzersiz, font=("Roboto", 12)).pack(side="left", pady=5)

    def veriyi_islet(self):
        if self.son_analiz:
            kayit_objesi = {
                "tarih": str(datetime.date.today()),
                "kilo": float(self.kilo_e.get()),
                "vki": self.son_analiz["vki"],
                "program": self.son_analiz["program_adi"]
            }
            self.auth.fitness_verisi_kaydet(self.kullanici, kayit_objesi)
            self.btn_kaydet.configure(text="✓ Kaydedildi!", state="disabled", fg_color="#7f8c8d")
            self._gecmis_yukle()
            self.after(3000, lambda: self.btn_kaydet.configure(
                text="💾 Bugünü Kaydet", state="normal", fg_color="#27ae60"
            ))

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

        self.sol_panel = ctk.CTkFrame(self, width=280)
        self.sol_panel.pack(side="left", fill="y", padx=10, pady=10)

        self.sag_panel = ctk.CTkFrame(self)
        self.sag_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.sol_panel, text="Fitness Koçu", font=("Roboto", 20, "bold")).pack(pady=20)

        ctk.CTkLabel(self.sol_panel, text="Boy (cm):").pack(pady=(10, 0))
        self.boy_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Örn: 175", width=200)
        self.boy_e.pack(pady=5)

        ctk.CTkLabel(self.sol_panel, text="Kilo (kg):").pack(pady=(10, 0))
        self.kilo_e = ctk.CTkEntry(self.sol_panel, placeholder_text="Örn: 70", width=200)
        self.kilo_e.pack(pady=5)

        ctk.CTkLabel(self.sol_panel, text="Seviye:").pack(pady=(10, 0))
        self.seviye_cb = ctk.CTkComboBox(self.sol_panel, values=["Başlangıç", "Orta", "İleri"], width=200)
        self.seviye_cb.pack(pady=5)

        ctk.CTkButton(self.sol_panel, text="Analizi Başlat", command=self.guncelle, fg_color="#FF8C00").pack(pady=10)

        self.btn_kaydet = ctk.CTkButton(self.sol_panel, text="Bugünü Kaydet", command=self.veriyi_islet, fg_color="#27ae60", state="disabled")
        self.btn_kaydet.pack(pady=5)

        ctk.CTkLabel(self.sag_panel, text="Analiz Sonuçları", font=("Roboto", 18, "bold")).pack(pady=10)

        self.vki_label = ctk.CTkLabel(self.sag_panel, text="VKİ: -", font=("Roboto", 14))
        self.vki_label.pack(pady=5)

        self.program_label = ctk.CTkLabel(self.sag_panel, text="Program: -", font=("Roboto", 14))
        self.program_label.pack(pady=5)

        self.tavsiye_label = ctk.CTkLabel(self.sag_panel, text="Tavsiye: -", font=("Roboto", 12), wraplength=400)
        self.tavsiye_label.pack(pady=5)

        self.liste_frame = ctk.CTkScrollableFrame(self.sag_panel, label_text="Egzersiz Listesi", height=200)
        self.liste_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def guncelle(self):
        try:
            b, k = float(self.boy_e.get()), float(self.kilo_e.get())
            sev = self.seviye_cb.get()
            self.son_analiz = FitnessZekasi.analiz_et(b, k, 25, sev, "Kas Yap", "2026-03-30")
            self.liste_guncelle(self.son_analiz)
            self.btn_kaydet.configure(state="normal")
        except:
            pass

    def liste_guncelle(self, analiz):
        self.vki_label.configure(text=f"VKİ: {analiz['vki']}")
        self.program_label.configure(text=f"Program: {analiz['program_adi']}")
        self.tavsiye_label.configure(text=f"Tavsiye: {analiz['tavsiye']}")
        for w in self.liste_frame.winfo_children():
            w.destroy()
        for egzersiz in analiz.get("program_liste", []):
            ctk.CTkLabel(self.liste_frame, text=f"• {egzersiz}").pack(anchor="w", pady=2, padx=10)

    def veriyi_islet(self):
        if self.son_analiz:
            kayit_objesi = {
                "tarih": str(datetime.date.today()),
                "kilo": float(self.kilo_e.get()),
                "vki": self.son_analiz["vki"],
                "program": self.son_analiz["program_adi"]
            }
            self.auth.fitness_verisi_kaydet(self.kullanici, kayit_objesi)
            self.btn_kaydet.configure(text="Kaydedildi!", state="disabled", fg_color="gray")

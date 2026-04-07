import customtkinter as ctk
from src.assets.hesaplamalar import FitnessZekasi
from src.data.kimlik_dogrulama import KimlikDogrulama
import datetime

class FitnessKocuSayfasi(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        self.kullanici = kullanici_adi
        self.auth = KimlikDogrulama()
        self.son_analiz = None # Kaydedilecek veriyi burada tutacağız

        # ... (Önceki giriş alanları aynı kalıyor) ...

        ctk.CTkButton(self.sol_panel, text="Analizi Başlat", command=self.guncelle, fg_color="#FF8C00").pack(pady=10)
        
        # 💾 KAYDET BUTONU
        self.btn_kaydet = ctk.CTkButton(self.sol_panel, text="Bugünü Kaydet", command=self.veriyi_islet, fg_color="#27ae60", state="disabled")
        self.btn_kaydet.pack(pady=5)

    def guncelle(self):
        try:
            b, k = float(self.boy_e.get()), float(self.kilo_e.get())
            sev = self.seviye_cb.get()
            
            # Zekayı çalıştır
            self.son_analiz = FitnessZekasi.analiz_et(b, k, 25, sev, "Kas Yap", "2026-03-30")
            
            # Arayüzü güncelle (Sağ paneldeki liste vb.)
            self.liste_guncelle(self.son_analiz)
            self.btn_kaydet.configure(state="normal") # Analiz başarılıysa kaydı aktif et
        except:
            pass

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
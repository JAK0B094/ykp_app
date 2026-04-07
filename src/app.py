import customtkinter as ctk
from PIL import Image
import os

from src.module.karsilama_sayfasi import KarsilamaSayfasi
from src.module.giris_sayfasi import GirisSayfasi
from src.module.kayit_sayfasi import KayitSayfasi
from src.module.ana_panel import AnaPanel
from src.module.fitness_kocu import FitnessKocuSayfasi
from src.module.sifre_sifirlama_sayfasi import SifreSifirlamaSayfasi
from src.module.gorev_modulu import GorevModulu
from src.module.not_modulu import NotModulu

class JKBApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JKB")
        self.geometry("1000x700")
        self.logo_path = os.path.join("src", "assets", "logo.png")
        self.su_anki_sayfa = None
        self.sayfa_goster("karsilama")

    def sayfa_goster(self, sayfa_adi, kullanici_adi=""):
        if self.su_anki_sayfa is not None:
            self.su_anki_sayfa.destroy()

        kapat_fonk = self.destroy 

        if sayfa_adi == "karsilama":
            self.su_anki_sayfa = KarsilamaSayfasi(self, 
                giris_git=lambda: self.sayfa_goster("giris"),
                kayit_git=lambda: self.sayfa_goster("kayit"),
                kapat_fonk=kapat_fonk,
                logo_path=self.logo_path)
        
        elif sayfa_adi == "giris":
            self.su_anki_sayfa = GirisSayfasi(self, 
                geris_don_fonk=lambda: self.sayfa_goster("karsilama"),
                basarili_giris_fonk=lambda u: self.sayfa_goster("ana_panel", u),
                sifre_unuttum_fonk=lambda: self.sayfa_goster("sifre_sifirla"),
                kapat_fonk=kapat_fonk)
        
        elif sayfa_adi == "kayit":
            self.su_anki_sayfa = KayitSayfasi(self, 
                geri_don_fonk=lambda: self.sayfa_goster("karsilama"),
                kapat_fonk=kapat_fonk)
                
        elif sayfa_adi == "sifre_sifirla":
            self.su_anki_sayfa = SifreSifirlamaSayfasi(self,
                geri_don_fonk=lambda: self.sayfa_goster("giris"),
                kapat_fonk=kapat_fonk)
        
        elif sayfa_adi == "ana_panel":
            self.su_anki_sayfa = AnaPanel(self, 
                kullanici_adi=kullanici_adi,
                cikis_yap_fonk=lambda: self.sayfa_goster("karsilama"),
                fitness_git_fonk=lambda: self.sayfa_goster("fitness_kocu", kullanici_adi),
                gorev_git_fonk=lambda: self.sayfa_goster("gorevler", kullanici_adi),
                notlar_git_fonk=lambda: self.sayfa_goster("notlar", kullanici_adi),
                logo_path=self.logo_path)
        
        elif sayfa_adi == "fitness_kocu":
            self.su_anki_sayfa = FitnessKocuSayfasi(self, kullanici_adi=kullanici_adi)
            ctk.CTkButton(self.su_anki_sayfa, text="<- Geri Dön", command=lambda: self.sayfa_goster("ana_panel", kullanici_adi)).pack(pady=10)

        elif sayfa_adi == "gorevler":
            self.su_anki_sayfa = GorevModulu(self, kullanici_adi=kullanici_adi)
            ctk.CTkButton(self.su_anki_sayfa, text="<- Geri Dön", command=lambda: self.sayfa_goster("ana_panel", kullanici_adi)).pack(pady=10)

        elif sayfa_adi == "notlar":
            self.su_anki_sayfa = NotModulu(self, kullanici_adi=kullanici_adi)
            ctk.CTkButton(self.su_anki_sayfa, text="<- Geri Dön", command=lambda: self.sayfa_goster("ana_panel", kullanici_adi)).pack(pady=10)

        self.su_anki_sayfa.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = JKBApp()
    app.mainloop()
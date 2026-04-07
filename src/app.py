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
from src.module.profil_sayfasi import ProfilSayfasi

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JKBApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JKB — Kişisel Yönetim")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.logo_path = os.path.join("src", "assets", "logo.png")
        self.su_anki_sayfa = None
        self.sayfa_goster("karsilama")

    def sayfa_goster(self, sayfa_adi, kullanici_adi=""):
        if self.su_anki_sayfa is not None:
            self.su_anki_sayfa.destroy()

        kapat_fonk = self.destroy

        if sayfa_adi == "karsilama":
            self.su_anki_sayfa = KarsilamaSayfasi(
                self,
                giris_git=lambda: self.sayfa_goster("giris"),
                kayit_git=lambda: self.sayfa_goster("kayit"),
                kapat_fonk=kapat_fonk,
                logo_path=self.logo_path
            )

        elif sayfa_adi == "giris":
            self.su_anki_sayfa = GirisSayfasi(
                self,
                geris_don_fonk=lambda: self.sayfa_goster("karsilama"),
                basarili_giris_fonk=lambda u: self.sayfa_goster("ana_panel", u),
                sifre_unuttum_fonk=lambda: self.sayfa_goster("sifre_sifirla"),
                kapat_fonk=kapat_fonk
            )

        elif sayfa_adi == "kayit":
            self.su_anki_sayfa = KayitSayfasi(
                self,
                geri_don_fonk=lambda: self.sayfa_goster("karsilama"),
                kapat_fonk=kapat_fonk
            )

        elif sayfa_adi == "sifre_sifirla":
            self.su_anki_sayfa = SifreSifirlamaSayfasi(
                self,
                geri_don_fonk=lambda: self.sayfa_goster("giris"),
                kapat_fonk=kapat_fonk
            )

        elif sayfa_adi == "ana_panel":
            self.su_anki_sayfa = AnaPanel(
                self,
                kullanici_adi=kullanici_adi,
                cikis_yap_fonk=lambda: self.sayfa_goster("karsilama"),
                fitness_git_fonk=lambda: self.sayfa_goster("fitness_kocu", kullanici_adi),
                gorev_git_fonk=lambda: self.sayfa_goster("gorevler", kullanici_adi),
                notlar_git_fonk=lambda: self.sayfa_goster("notlar", kullanici_adi),
                profil_git_fonk=lambda: self.sayfa_goster("profil", kullanici_adi),
                logo_path=self.logo_path
            )

        elif sayfa_adi == "fitness_kocu":
            self.su_anki_sayfa = ctk.CTkFrame(self)
            nav = ctk.CTkFrame(self.su_anki_sayfa, height=45, corner_radius=0)
            nav.pack(fill="x")
            nav.pack_propagate(False)
            ctk.CTkButton(nav, text="← Geri Dön", width=110, height=35,
                          command=lambda: self.sayfa_goster("ana_panel", kullanici_adi),
                          fg_color="transparent", hover_color="#1e2d3d",
                          font=("Roboto", 12)).pack(side="left", padx=10, pady=5)
            FitnessKocuSayfasi(self.su_anki_sayfa, kullanici_adi=kullanici_adi).pack(fill="both", expand=True)

        elif sayfa_adi == "gorevler":
            self.su_anki_sayfa = ctk.CTkFrame(self)
            nav = ctk.CTkFrame(self.su_anki_sayfa, height=45, corner_radius=0)
            nav.pack(fill="x")
            nav.pack_propagate(False)
            ctk.CTkButton(nav, text="← Geri Dön", width=110, height=35,
                          command=lambda: self.sayfa_goster("ana_panel", kullanici_adi),
                          fg_color="transparent", hover_color="#1e2d3d",
                          font=("Roboto", 12)).pack(side="left", padx=10, pady=5)
            GorevModulu(self.su_anki_sayfa, kullanici_adi=kullanici_adi).pack(fill="both", expand=True)

        elif sayfa_adi == "notlar":
            self.su_anki_sayfa = ctk.CTkFrame(self)
            nav = ctk.CTkFrame(self.su_anki_sayfa, height=45, corner_radius=0)
            nav.pack(fill="x")
            nav.pack_propagate(False)
            ctk.CTkButton(nav, text="← Geri Dön", width=110, height=35,
                          command=lambda: self.sayfa_goster("ana_panel", kullanici_adi),
                          fg_color="transparent", hover_color="#1e2d3d",
                          font=("Roboto", 12)).pack(side="left", padx=10, pady=5)
            NotModulu(self.su_anki_sayfa, kullanici_adi=kullanici_adi).pack(fill="both", expand=True)

        elif sayfa_adi == "profil":
            self.su_anki_sayfa = ctk.CTkFrame(self)
            nav = ctk.CTkFrame(self.su_anki_sayfa, height=45, corner_radius=0)
            nav.pack(fill="x")
            nav.pack_propagate(False)
            ctk.CTkButton(nav, text="← Geri Dön", width=110, height=35,
                          command=lambda: self.sayfa_goster("ana_panel", kullanici_adi),
                          fg_color="transparent", hover_color="#1e2d3d",
                          font=("Roboto", 12)).pack(side="left", padx=10, pady=5)
            ProfilSayfasi(self.su_anki_sayfa, kullanici_adi=kullanici_adi).pack(fill="both", expand=True)

        if self.su_anki_sayfa:
            self.su_anki_sayfa.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = JKBApp()
    app.mainloop()

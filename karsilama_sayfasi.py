import customtkinter as ctk
# Resim işlemek için gerekli kütüphaneleri import ediyoruz
from PIL import Image

class KarsilamaSayfasi(ctk.CTkFrame):
    def __init__(self, master, giris_git, kayit_git, kapat_fonk, logo_path, **kwargs):
        super().__init__(master, **kwargs)

        # ⚠️ Değişiklik: Yazı yerine logo resmini yüklüyoruz ve yerleştiriyoruz.
        # Resim boyutunu Karşılama ekranına uygun şekilde büyütüyoruz (örn: 250x150)
        logo_image = ctk.CTkImage(light_image=Image.open(logo_path),
                                    dark_image=Image.open(logo_path),
                                    size=(250, 150))
        
        self.logo_label = ctk.CTkLabel(self, image=logo_image, text="") # text="" yaparak yazı koymuyoruz
        self.logo_label.pack(pady=(80, 20))

        ctk.CTkLabel(self, text="Hoş geldiniz! Lütfen seçim yapın.", font=("Roboto", 14), text_color="gray").pack(pady=(0, 40))

        ctk.CTkButton(self, text="Giriş Yap", command=giris_git, width=280, height=50).pack(pady=10)
        ctk.CTkButton(self, text="Kayıt Ol", command=kayit_git, width=280, height=50, fg_color="#27ae60", hover_color="#1e8449").pack(pady=10)
        
        ctk.CTkButton(self, text="Uygulamayı Kapat", command=kapat_fonk, width=280, height=50, fg_color="#c0392b", hover_color="#a93226").pack(pady=10)

        ctk.CTkLabel(self, text="Made By YKP", font=("Ravie", 14), text_color="#c0392b").pack(side="bottom", anchor="se", padx=20, pady=20)
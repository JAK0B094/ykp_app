import customtkinter as ctk
from src.data.kimlik_dogrulama import KimlikDogrulama

class GirisSayfasi(ctk.CTkFrame):
    def __init__(self, master, geris_don_fonk, basarili_giris_fonk, sifre_unuttum_fonk, kapat_fonk, **kwargs):
        super().__init__(master, **kwargs)
        self.auth = KimlikDogrulama()
        self.basarili_giris_fonk = basarili_giris_fonk

        ctk.CTkLabel(self, text="GİRİŞ YAP", font=("Roboto", 24, "bold")).pack(pady=(50, 20))

        self.u_entry = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adı", width=280, height=45)
        self.u_entry.pack(pady=10)

        self.p_entry = ctk.CTkEntry(self, placeholder_text="Şifre", show="*", width=280, height=45)
        self.p_entry.pack(pady=10)

        ctk.CTkButton(self, text="Sisteme Gir", command=self.giris_yap, width=280, height=50).pack(pady=20)
        
        ctk.CTkButton(self, text="Şifremi Unuttum", command=sifre_unuttum_fonk, fg_color="transparent", text_color="gray").pack()
        ctk.CTkButton(self, text="<- Geri Dön", command=geris_don_fonk, fg_color="gray", width=135).pack(pady=10)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=10)

    def giris_yap(self):
        u, p = self.u_entry.get().strip(), self.p_entry.get().strip()
        basari, mesaj = self.auth.giris_kontrol(u, p)
        if basari:
            self.basarili_giris_fonk(u)
        else:
            self.msg.configure(text=mesaj, text_color="red")
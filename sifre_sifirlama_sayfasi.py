import customtkinter as ctk
from src.data.kimlik_dogrulama import KimlikDogrulama

class SifreSifirlamaSayfasi(ctk.CTkFrame):
    def __init__(self, master, geri_don_fonk, kapat_fonk, **kwargs):
        super().__init__(master, **kwargs)
        self.auth = KimlikDogrulama()

        ctk.CTkLabel(self, text="ŞİFRE SIFIRLAMA", font=("Roboto", 24, "bold")).pack(pady=(40, 10))
        ctk.CTkLabel(self, text="Kayıtlı E-Posta adresinizi girin.", text_color="gray").pack(pady=(0, 20))

        self.e_entry = ctk.CTkEntry(self, placeholder_text="E-posta", width=280, height=45)
        self.e_entry.pack(pady=10)

        self.s1_entry = ctk.CTkEntry(self, placeholder_text="Yeni Şifre (6-32 karakter)", show="*", width=280, height=45)
        self.s1_entry.pack(pady=10)

        self.s2_entry = ctk.CTkEntry(self, placeholder_text="Yeni Şifre Tekrar", show="*", width=280, height=45)
        self.s2_entry.pack(pady=10)

        ctk.CTkButton(self, text="Şifreyi Güncelle", command=self.guncelle, width=280, height=50, fg_color="#27ae60", hover_color="#1e8449").pack(pady=20)
        
        # Alt Butonlar
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="<- Geri Dön", command=geri_don_fonk, fg_color="gray", width=135).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Uygulamayı Kapat", command=kapat_fonk, fg_color="#c0392b", width=135).pack(side="left", padx=5)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=10)

    def guncelle(self):
        e, s1, s2 = self.e_entry.get().strip(), self.s1_entry.get().strip(), self.s2_entry.get().strip()
        if not e or not s1 or s2 != s1:
            self.msg.configure(text="Hata: Bilgileri kontrol edin!", text_color="red")
            return
        basari, mesaj = self.auth.eposta_ile_sifre_sifirla(e, s1)
        self.msg.configure(text=mesaj, text_color="green" if basari else "red")
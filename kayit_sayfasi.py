import customtkinter as ctk
from src.data.kimlik_dogrulama import KimlikDogrulama

class KayitSayfasi(ctk.CTkFrame):
    def __init__(self, master, geri_don_fonk, kapat_fonk, **kwargs):
        super().__init__(master, **kwargs)
        self.auth = KimlikDogrulama()

        ctk.CTkLabel(self, text="KAYIT OL", font=("Roboto", 24, "bold")).pack(pady=(30, 20))

        # Form Alanları
        self.u_entry = ctk.CTkEntry(self, placeholder_text="Kullanıcı Adı (3-46 karakter)", width=280, height=45)
        self.u_entry.pack(pady=10)

        self.e_entry = ctk.CTkEntry(self, placeholder_text="E-Posta Adresi", width=280, height=45)
        self.e_entry.pack(pady=10)

        self.p_entry = ctk.CTkEntry(self, placeholder_text="Şifre (6-32 karakter)", show="*", width=280, height=45)
        self.p_entry.pack(pady=10)

        self.p_tekrar_entry = ctk.CTkEntry(self, placeholder_text="Şifre Tekrar", show="*", width=280, height=45)
        self.p_tekrar_entry.pack(pady=10)

        # Kayıt Butonu
        ctk.CTkButton(self, text="Hesabı Oluştur", command=self.kayit_ol, width=280, height=50, fg_color="#27ae60", hover_color="#1e8449").pack(pady=20)
        
        # Alt Butonlar (Geri Dön ve Kapat)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="<- Geri Dön", command=geri_don_fonk, fg_color="gray", width=135).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Uygulamayı Kapat", command=kapat_fonk, fg_color="#c0392b", width=135).pack(side="left", padx=5)

        self.msg = ctk.CTkLabel(self, text="")
        self.msg.pack(pady=10)

    def kayit_ol(self):
        u, e, p, pt = self.u_entry.get().strip(), self.e_entry.get().strip(), self.p_entry.get().strip(), self.p_tekrar_entry.get().strip()
        if not u or not e or not p or not pt:
            self.msg.configure(text="Lütfen tüm alanları doldurun!", text_color="orange")
            return
        if len(u) < 3 or len(u) > 46:
            self.msg.configure(text="Kullanıcı adı geçersiz uzunlukta!", text_color="orange")
            return
        if p != pt:
            self.msg.configure(text="Şifreler uyuşmuyor!", text_color="red")
            return
        
        basari, mesaj = self.auth.kayit_et(u, p, e)
        self.msg.configure(text=mesaj, text_color="green" if basari else "red")
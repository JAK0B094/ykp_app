import customtkinter as ctk
from PIL import Image

class AnaPanel(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, cikis_yap_fonk, fitness_git_fonk, gorev_git_fonk, notlar_git_fonk, logo_path, **kwargs):
        super().__init__(master, **kwargs)

        # Sidebar (Sol Menü)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        # Logo
        try:
            logo_img = ctk.CTkImage(light_image=Image.open(logo_path), dark_image=Image.open(logo_path), size=(100, 60))
            self.logo_label = ctk.CTkLabel(self.sidebar, image=logo_img, text="")
            self.logo_label.pack(pady=30)
        except:
            ctk.CTkLabel(self.sidebar, text="JKB", font=("Roboto", 24, "bold")).pack(pady=30)
        
        # Menü Butonları
        ctk.CTkButton(self.sidebar, text="🏠 Ana Sayfa", fg_color="transparent").pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="🏋️ Fitness Koçu", command=fitness_git_fonk).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="📅 Görevler", command=gorev_git_fonk).pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="📓 Kişisel Notlar", command=notlar_git_fonk).pack(pady=5, padx=10)
        
        ctk.CTkButton(self.sidebar, text="Çıkış Yap", fg_color="#e74c3c", command=cikis_yap_fonk).pack(side="bottom", pady=20, padx=10)

        # Sağ İçerik
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(self.main_content, text=f"Hoş Geldin, {kullanici_adi}!", font=("Roboto", 26, "bold")).pack(pady=40)
        ctk.CTkLabel(self.main_content, text="Yönetmek istediğin modülü soldan seçebilirsin.", font=("Roboto", 16)).pack()
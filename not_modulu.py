import customtkinter as ctk

class NotModulu(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="📓 KİŞİSEL NOT DEFTERİ", font=("Roboto", 20, "bold")).pack(pady=20)
        
        # Araç Çubuğu
        tool_frame = ctk.CTkFrame(self)
        tool_frame.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(tool_frame, text="Kaydet", width=80, fg_color="#27ae60").pack(side="left", padx=5, pady=5)
        ctk.CTkButton(tool_frame, text="Şifrele 🔒", width=80, fg_color="#8e44ad").pack(side="left", padx=5, pady=5)
        
        # Not Yazma Alanı
        self.not_alani = ctk.CTkTextbox(self, font=("Consolas", 14), width=600, height=400)
        self.not_alani.pack(pady=10, padx=20, fill="both", expand=True)
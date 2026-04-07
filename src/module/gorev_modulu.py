import customtkinter as ctk

class GorevModulu(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        
        ctk.CTkLabel(self, text="📅 GÖREVLER VE ANIMSATICILAR", font=("Roboto", 20, "bold")).pack(pady=20)
        
        # Görev Ekleme Alanı
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        self.gorev_entry = ctk.CTkEntry(input_frame, placeholder_text="Yeni görev yaz...", width=400)
        self.gorev_entry.pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(input_frame, text="Ekle", width=100, command=self.gorev_ekle).pack(side="left", padx=10)
        
        # Liste Alanı
        self.liste_frame = ctk.CTkScrollableFrame(self, width=500, height=350)
        self.liste_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def gorev_ekle(self):
        text = self.gorev_entry.get()
        if text:
            cb = ctk.CTkCheckBox(self.liste_frame, text=text)
            cb.pack(anchor="w", pady=5, padx=10)
            self.gorev_entry.delete(0, 'end')
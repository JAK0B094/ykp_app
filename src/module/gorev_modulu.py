import customtkinter as ctk
from src.data.kimlik_dogrulama import KimlikDogrulama

class GorevModulu(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        self.kullanici = kullanici_adi
        self.auth = KimlikDogrulama()
        self.gorev_listesi = []

        # Başlık Alanı
        baslik_frame = ctk.CTkFrame(self, fg_color="transparent")
        baslik_frame.pack(fill="x", padx=25, pady=(20, 5))

        ctk.CTkLabel(baslik_frame, text="📅 GÖREVLER", font=("Roboto", 22, "bold")).pack(side="left")
        self.sayac_label = ctk.CTkLabel(baslik_frame, text="", font=("Roboto", 13), text_color="gray")
        self.sayac_label.pack(side="right")

        # Görev Ekleme Alanı
        input_frame = ctk.CTkFrame(self, corner_radius=10)
        input_frame.pack(pady=10, padx=25, fill="x")

        self.gorev_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Yeni görev yaz ve Enter'a bas...",
            font=("Roboto", 13),
            height=42
        )
        self.gorev_entry.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.gorev_entry.bind("<Return>", lambda e: self.gorev_ekle())

        ctk.CTkButton(
            input_frame, text="+ Ekle", width=90, height=42,
            command=self.gorev_ekle, fg_color="#2980b9", hover_color="#2471a3",
            font=("Roboto", 13, "bold")
        ).pack(side="right", padx=10, pady=10)

        # Filtre Butonları
        filtre_frame = ctk.CTkFrame(self, fg_color="transparent")
        filtre_frame.pack(fill="x", padx=25, pady=(0, 5))

        self.filtre = ctk.StringVar(value="hepsi")
        for text, val in [("Tümü", "hepsi"), ("Bekleyen", "bekleyen"), ("Tamamlanan", "tamamlanan")]:
            ctk.CTkRadioButton(
                filtre_frame, text=text, variable=self.filtre, value=val,
                command=self.listeyi_yenile, font=("Roboto", 12)
            ).pack(side="left", padx=10)

        ctk.CTkButton(
            filtre_frame, text="🗑 Tamamlananları Sil", width=160, height=28,
            command=self.tamamlananlari_sil, fg_color="#c0392b", hover_color="#a93226",
            font=("Roboto", 11)
        ).pack(side="right")

        # Liste Alanı
        self.liste_frame = ctk.CTkScrollableFrame(
            self, label_text="", corner_radius=10
        )
        self.liste_frame.pack(pady=5, padx=25, fill="both", expand=True)

        # Alt Bar - Kaydet
        alt_frame = ctk.CTkFrame(self, fg_color="transparent")
        alt_frame.pack(fill="x", padx=25, pady=(5, 15))

        self.durum_label = ctk.CTkLabel(alt_frame, text="", font=("Roboto", 11), text_color="gray")
        self.durum_label.pack(side="left")

        ctk.CTkButton(
            alt_frame, text="💾 Kaydet", width=100, height=32,
            command=self.kaydet, fg_color="#27ae60", hover_color="#1e8449",
            font=("Roboto", 12)
        ).pack(side="right")

        # Verileri yükle
        self._verileri_yukle()

    def _verileri_yukle(self):
        kayitli = self.auth.gorev_getir(self.kullanici)
        self.gorev_listesi = kayitli if kayitli else []
        self.listeyi_yenile()

    def gorev_ekle(self):
        text = self.gorev_entry.get().strip()
        if text:
            self.gorev_listesi.append({"metin": text, "tamamlandi": False})
            self.gorev_entry.delete(0, "end")
            self.listeyi_yenile()
            self.kaydet()

    def listeyi_yenile(self):
        for w in self.liste_frame.winfo_children():
            w.destroy()

        filtre = self.filtre.get()
        gosterilen = 0

        for i, gorev in enumerate(self.gorev_listesi):
            if filtre == "bekleyen" and gorev["tamamlandi"]:
                continue
            if filtre == "tamamlanan" and not gorev["tamamlandi"]:
                continue

            satir = ctk.CTkFrame(self.liste_frame, corner_radius=8, height=40)
            satir.pack(fill="x", padx=5, pady=3)
            satir.pack_propagate(False)

            var = ctk.BooleanVar(value=gorev["tamamlandi"])

            def on_check(idx=i, v=var):
                self.gorev_listesi[idx]["tamamlandi"] = v.get()
                self.listeyi_yenile()
                self.kaydet()

            renk = "#888" if gorev["tamamlandi"] else "white"
            stil = "overstrike" if gorev["tamamlandi"] else "normal"

            cb = ctk.CTkCheckBox(
                satir, text=gorev["metin"], variable=var, command=on_check,
                font=("Roboto", 13), text_color=renk,
                checkmark_color="#27ae60", border_color="#555"
            )
            cb.pack(side="left", padx=10, pady=8)

            ctk.CTkButton(
                satir, text="✕", width=28, height=28,
                command=lambda idx=i: self.gorev_sil(idx),
                fg_color="#c0392b", hover_color="#a93226",
                font=("Roboto", 11), corner_radius=6
            ).pack(side="right", padx=8)

            gosterilen += 1

        if gosterilen == 0:
            ctk.CTkLabel(
                self.liste_frame,
                text="Henüz görev yok. Yukarıdan yeni görev ekle!",
                font=("Roboto", 13), text_color="gray"
            ).pack(pady=30)

        tamamlanan = sum(1 for g in self.gorev_listesi if g["tamamlandi"])
        toplam = len(self.gorev_listesi)
        self.sayac_label.configure(text=f"{tamamlanan}/{toplam} tamamlandı")

    def gorev_sil(self, idx):
        if 0 <= idx < len(self.gorev_listesi):
            self.gorev_listesi.pop(idx)
            self.listeyi_yenile()
            self.kaydet()

    def tamamlananlari_sil(self):
        self.gorev_listesi = [g for g in self.gorev_listesi if not g["tamamlandi"]]
        self.listeyi_yenile()
        self.kaydet()

    def kaydet(self):
        self.auth.gorev_kaydet(self.kullanici, self.gorev_listesi)
        self.durum_label.configure(text="✓ Kaydedildi", text_color="#27ae60")
        self.after(2000, lambda: self.durum_label.configure(text=""))

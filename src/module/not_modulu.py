import customtkinter as ctk
from src.data.kimlik_dogrulama import KimlikDogrulama
import datetime

class NotModulu(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        self.kullanici = kullanici_adi
        self.auth = KimlikDogrulama()
        self.kaydedilmedi = False

        # Başlık + Araç Çubuğu
        ust_frame = ctk.CTkFrame(self, fg_color="transparent")
        ust_frame.pack(fill="x", padx=25, pady=(20, 5))

        ctk.CTkLabel(ust_frame, text="📓 KİŞİSEL NOT DEFTERİ", font=("Roboto", 22, "bold")).pack(side="left")

        self.durum_label = ctk.CTkLabel(ust_frame, text="", font=("Roboto", 11), text_color="gray")
        self.durum_label.pack(side="right")

        # Araç Çubuğu
        tool_frame = ctk.CTkFrame(self, corner_radius=10)
        tool_frame.pack(pady=5, padx=25, fill="x")

        ctk.CTkButton(
            tool_frame, text="💾 Kaydet  (Ctrl+S)", width=130, height=36,
            command=self.kaydet, fg_color="#27ae60", hover_color="#1e8449",
            font=("Roboto", 12)
        ).pack(side="left", padx=8, pady=8)

        ctk.CTkButton(
            tool_frame, text="🗑 Temizle", width=100, height=36,
            command=self.temizle, fg_color="#7f8c8d", hover_color="#6c7a7d",
            font=("Roboto", 12)
        ).pack(side="left", padx=4, pady=8)

        self.tarih_label = ctk.CTkLabel(
            tool_frame, text="", font=("Roboto", 11), text_color="gray"
        )
        self.tarih_label.pack(side="right", padx=12)

        self.karakter_label = ctk.CTkLabel(
            tool_frame, text="0 karakter", font=("Roboto", 11), text_color="gray"
        )
        self.karakter_label.pack(side="right", padx=8)

        # Not Yazma Alanı
        not_cerceve = ctk.CTkFrame(self, corner_radius=10)
        not_cerceve.pack(pady=5, padx=25, fill="both", expand=True)

        self.not_alani = ctk.CTkTextbox(
            not_cerceve,
            font=("Consolas", 14),
            wrap="word",
            corner_radius=8
        )
        self.not_alani.pack(fill="both", expand=True, padx=5, pady=5)
        self.not_alani.bind("<KeyRelease>", self._degisiklik_izle)
        self.not_alani.bind("<Control-s>", lambda e: self.kaydet())

        # Alt Bar
        alt_frame = ctk.CTkFrame(self, fg_color="transparent")
        alt_frame.pack(fill="x", padx=25, pady=(3, 12))

        ctk.CTkLabel(
            alt_frame,
            text="İpucu: Ctrl+S ile hızlıca kaydet",
            font=("Roboto", 11), text_color="#555"
        ).pack(side="left")

        # Verileri yükle
        self._verileri_yukle()

    def _verileri_yukle(self):
        not_metni = self.auth.not_getir(self.kullanici)
        if not_metni:
            self.not_alani.delete("1.0", "end")
            self.not_alani.insert("1.0", not_metni)
            self.tarih_label.configure(text="Kayıtlı not yüklendi")
            self._karakter_guncelle()

    def _degisiklik_izle(self, event=None):
        self.kaydedilmedi = True
        self.durum_label.configure(text="● Kaydedilmemiş değişiklik", text_color="#e67e22")
        self._karakter_guncelle()

    def _karakter_guncelle(self):
        icerik = self.not_alani.get("1.0", "end-1c")
        kar = len(icerik)
        kelime = len(icerik.split()) if icerik.strip() else 0
        self.karakter_label.configure(text=f"{kar} karakter · {kelime} kelime")

    def kaydet(self):
        icerik = self.not_alani.get("1.0", "end-1c")
        self.auth.not_kaydet(self.kullanici, icerik)
        self.kaydedilmedi = False
        simdi = datetime.datetime.now().strftime("%H:%M")
        self.durum_label.configure(text=f"✓ Kaydedildi", text_color="#27ae60")
        self.tarih_label.configure(text=f"Son kayıt: {simdi}")
        self.after(3000, lambda: self.durum_label.configure(text=""))

    def temizle(self):
        self.not_alani.delete("1.0", "end")
        self._karakter_guncelle()
        self.durum_label.configure(text="● Kaydedilmemiş değişiklik", text_color="#e67e22")

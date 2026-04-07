import customtkinter as ctk
from src.data.kimlik_dogrulama import KimlikDogrulama
import datetime

class ProfilSayfasi(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, **kwargs):
        super().__init__(master, **kwargs)
        self.kullanici = kullanici_adi
        self.auth = KimlikDogrulama()

        icerik = ctk.CTkScrollableFrame(self, fg_color="transparent")
        icerik.pack(fill="both", expand=True, padx=20, pady=10)

        # Başlık
        ctk.CTkLabel(icerik, text="👤 PROFİLİM", font=("Roboto", 22, "bold")).pack(anchor="w", padx=15, pady=(15, 5))

        # Kullanıcı Kartı
        kullanici_kart = ctk.CTkFrame(icerik, corner_radius=12)
        kullanici_kart.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            kullanici_kart, text="👤",
            font=("Roboto", 40)
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            kullanici_kart, text=kullanici_adi,
            font=("Roboto", 20, "bold")
        ).pack()

        bilgi = self.auth.kullanici_bilgi_getir(kullanici_adi)
        eposta = bilgi.get("eposta", "—")
        ctk.CTkLabel(
            kullanici_kart, text=eposta,
            font=("Roboto", 12), text_color="gray"
        ).pack(pady=(2, 20))

        # İstatistikler
        ctk.CTkLabel(icerik, text="İstatistikler", font=("Roboto", 16, "bold")).pack(anchor="w", padx=15, pady=(10, 5))

        istat_frame = ctk.CTkFrame(icerik, corner_radius=10)
        istat_frame.pack(fill="x", padx=10, pady=5)

        gorevler = bilgi.get("gorevler", [])
        toplam_g = len(gorevler)
        tamamlanan_g = sum(1 for g in gorevler if g.get("tamamlandi"))

        fitness_gecmisi = bilgi.get("fitness_gecmisi", [])
        son_vki = fitness_gecmisi[-1]["vki"] if fitness_gecmisi else None

        istatler = [
            ("📅 Toplam Görev", str(toplam_g)),
            ("✅ Tamamlanan Görev", str(tamamlanan_g)),
            ("🏋️ Fitness Kaydı", str(len(fitness_gecmisi))),
            ("📊 Son VKİ", str(son_vki) if son_vki else "—"),
        ]

        for i, (etiket, deger) in enumerate(istatler):
            satir = ctk.CTkFrame(istat_frame, fg_color="transparent", height=40)
            satir.pack(fill="x", padx=15)
            satir.pack_propagate(False)
            ctk.CTkLabel(satir, text=etiket, font=("Roboto", 12), text_color="gray").pack(side="left", pady=8)
            ctk.CTkLabel(satir, text=deger, font=("Roboto", 13, "bold")).pack(side="right", pady=8)
            if i < len(istatler) - 1:
                ctk.CTkFrame(istat_frame, height=1, fg_color="#333").pack(fill="x", padx=15)

        # Fitness Geçmişi Son 5
        if fitness_gecmisi:
            ctk.CTkLabel(icerik, text="Son Fitness Kayıtları", font=("Roboto", 16, "bold")).pack(anchor="w", padx=15, pady=(15, 5))

            gecmis_frame = ctk.CTkFrame(icerik, corner_radius=10)
            gecmis_frame.pack(fill="x", padx=10, pady=5)

            for kayit in reversed(fitness_gecmisi[-5:]):
                satir = ctk.CTkFrame(gecmis_frame, fg_color="transparent", height=38)
                satir.pack(fill="x", padx=15)
                satir.pack_propagate(False)
                ctk.CTkLabel(satir, text=f"📅 {kayit.get('tarih','?')}", font=("Roboto", 11), text_color="gray").pack(side="left", pady=8)
                ctk.CTkLabel(satir, text=f"⚖️ {kayit.get('kilo','?')} kg  |  VKİ: {kayit.get('vki','?')}", font=("Roboto", 11)).pack(side="right", pady=8)

        # Şifre Değiştir
        ctk.CTkLabel(icerik, text="Şifre Değiştir", font=("Roboto", 16, "bold")).pack(anchor="w", padx=15, pady=(20, 5))

        sifre_frame = ctk.CTkFrame(icerik, corner_radius=10)
        sifre_frame.pack(fill="x", padx=10, pady=5)

        self.eski_sifre = ctk.CTkEntry(sifre_frame, placeholder_text="Mevcut Şifre", show="*", height=38)
        self.eski_sifre.pack(fill="x", padx=15, pady=(12, 5))

        self.yeni_sifre = ctk.CTkEntry(sifre_frame, placeholder_text="Yeni Şifre (6-32 karakter)", show="*", height=38)
        self.yeni_sifre.pack(fill="x", padx=15, pady=5)

        self.yeni_sifre2 = ctk.CTkEntry(sifre_frame, placeholder_text="Yeni Şifre Tekrar", show="*", height=38)
        self.yeni_sifre2.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            sifre_frame, text="Şifreyi Değiştir", height=38,
            command=self.sifre_degistir,
            fg_color="#8e44ad", hover_color="#7d3c98",
            font=("Roboto", 12)
        ).pack(fill="x", padx=15, pady=(5, 12))

        self.sifre_msg = ctk.CTkLabel(sifre_frame, text="", font=("Roboto", 11))
        self.sifre_msg.pack(pady=(0, 8))

    def sifre_degistir(self):
        eski = self.eski_sifre.get().strip()
        yeni = self.yeni_sifre.get().strip()
        yeni2 = self.yeni_sifre2.get().strip()

        if not eski or not yeni or not yeni2:
            self.sifre_msg.configure(text="Tüm alanları doldurun!", text_color="orange")
            return
        if yeni != yeni2:
            self.sifre_msg.configure(text="Yeni şifreler uyuşmuyor!", text_color="red")
            return

        basari, mesaj = self.auth.sifre_degistir(self.kullanici, eski, yeni)
        self.sifre_msg.configure(text=mesaj, text_color="#27ae60" if basari else "red")
        if basari:
            self.eski_sifre.delete(0, "end")
            self.yeni_sifre.delete(0, "end")
            self.yeni_sifre2.delete(0, "end")

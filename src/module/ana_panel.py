import customtkinter as ctk
from PIL import Image
from src.data.kimlik_dogrulama import KimlikDogrulama
import datetime

class AnaPanel(ctk.CTkFrame):
    def __init__(self, master, kullanici_adi, cikis_yap_fonk, fitness_git_fonk,
                 gorev_git_fonk, notlar_git_fonk, profil_git_fonk=None, logo_path="", **kwargs):
        super().__init__(master, **kwargs)
        self.kullanici = kullanici_adi
        self.auth = KimlikDogrulama()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open(logo_path),
                dark_image=Image.open(logo_path),
                size=(110, 66)
            )
            ctk.CTkLabel(self.sidebar, image=logo_img, text="").pack(pady=(25, 5))
        except:
            ctk.CTkLabel(self.sidebar, text="JKB", font=("Roboto", 26, "bold")).pack(pady=(25, 5))

        ctk.CTkLabel(
            self.sidebar, text=kullanici_adi,
            font=("Roboto", 13, "bold"), text_color="#3498db"
        ).pack(pady=(0, 20))

        # Ayırıcı
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#333").pack(fill="x", padx=15, pady=5)

        menu_butonlar = [
            ("🏠  Ana Sayfa", None, True),
            ("🏋️  Fitness Koçu", fitness_git_fonk, False),
            ("📅  Görevler", gorev_git_fonk, False),
            ("📓  Kişisel Notlar", notlar_git_fonk, False),
        ]
        if profil_git_fonk:
            menu_butonlar.append(("👤  Profilim", profil_git_fonk, False))

        for text, cmd, aktif in menu_butonlar:
            if aktif:
                ctk.CTkButton(
                    self.sidebar, text=text, command=cmd,
                    fg_color="#1a5276", hover_color="#1a5276",
                    anchor="w", font=("Roboto", 13)
                ).pack(fill="x", padx=12, pady=3)
            else:
                ctk.CTkButton(
                    self.sidebar, text=text, command=cmd,
                    fg_color="transparent", hover_color="#1e2d3d",
                    anchor="w", font=("Roboto", 13)
                ).pack(fill="x", padx=12, pady=3)

        ctk.CTkButton(
            self.sidebar, text="🚪  Çıkış Yap",
            command=cikis_yap_fonk,
            fg_color="#c0392b", hover_color="#a93226",
            font=("Roboto", 13)
        ).pack(side="bottom", fill="x", padx=12, pady=20)

        # Sağ İçerik
        self.icerik = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.icerik.pack(side="right", fill="both", expand=True)

        self._icerik_olustur(fitness_git_fonk, gorev_git_fonk, notlar_git_fonk, profil_git_fonk)

    def _icerik_olustur(self, fitness_git_fonk, gorev_git_fonk, notlar_git_fonk, profil_git_fonk):
        # Üst Hoş Geldin
        saat = datetime.datetime.now().hour
        if saat < 12:
            selam = "Günaydın"
        elif saat < 18:
            selam = "İyi Günler"
        else:
            selam = "İyi Akşamlar"

        ctk.CTkLabel(
            self.icerik,
            text=f"{selam}, {self.kullanici}! 👋",
            font=("Roboto", 26, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 3))

        ctk.CTkLabel(
            self.icerik,
            text=datetime.datetime.now().strftime("%d %B %Y, %A"),
            font=("Roboto", 13), text_color="gray"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        # İstatistik Kartları
        kartlar_frame = ctk.CTkFrame(self.icerik, fg_color="transparent")
        kartlar_frame.pack(fill="x", padx=20, pady=5)

        bilgi = self.auth.kullanici_bilgi_getir(self.kullanici)
        gorevler = bilgi.get("gorevler", [])
        toplam_g = len(gorevler)
        tamamlanan_g = sum(1 for g in gorevler if g.get("tamamlandi"))
        bekleyen_g = toplam_g - tamamlanan_g

        fitness_gecmisi = bilgi.get("fitness_gecmisi", [])
        son_vki = fitness_gecmisi[-1]["vki"] if fitness_gecmisi else None

        not_var = bool(bilgi.get("notlar", "").strip())

        kart_bilgileri = [
            ("📅", "Görevler", f"{tamamlanan_g}/{toplam_g} tamamlandı", f"{bekleyen_g} bekliyor", "#2980b9"),
            ("🏋️", "Son VKİ", str(son_vki) if son_vki else "—", "Fitness analizi" if son_vki else "Analiz yapılmadı", "#27ae60"),
            ("📓", "Notlar", "Var ✓" if not_var else "Boş", "Kişisel not defteri", "#8e44ad"),
        ]

        for ikon, baslik, deger, alt, renk in kart_bilgileri:
            self._kart_olustur(kartlar_frame, ikon, baslik, deger, alt, renk)

        # Modüller başlığı
        ctk.CTkLabel(
            self.icerik, text="Modüller",
            font=("Roboto", 17, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 8))

        # Modül Butonları
        modul_frame = ctk.CTkFrame(self.icerik, fg_color="transparent")
        modul_frame.pack(fill="x", padx=20, pady=5)

        moduller = [
            ("🏋️\nFitness Koçu", "VKİ analizi ve\nantrenman programı", fitness_git_fonk, "#e67e22"),
            ("📅\nGörevler", "Görevlerini yönet\nve takip et", gorev_git_fonk, "#2980b9"),
            ("📓\nKişisel Notlar", "Notlarını kaydet\nve görüntüle", notlar_git_fonk, "#8e44ad"),
        ]

        for text, aciklama, cmd, renk in moduller:
            self._modul_karti_olustur(modul_frame, text, aciklama, cmd, renk)

    def _kart_olustur(self, parent, ikon, baslik, deger, alt, renk):
        kart = ctk.CTkFrame(parent, corner_radius=12, width=160, height=100)
        kart.pack(side="left", padx=8, pady=5)
        kart.pack_propagate(False)

        ctk.CTkLabel(kart, text=f"{ikon}  {baslik}", font=("Roboto", 11), text_color="gray").pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(kart, text=deger, font=("Roboto", 18, "bold"), text_color=renk).pack(anchor="w", padx=12)
        ctk.CTkLabel(kart, text=alt, font=("Roboto", 10), text_color="gray").pack(anchor="w", padx=12)

    def _modul_karti_olustur(self, parent, text, aciklama, cmd, renk):
        kart = ctk.CTkButton(
            parent, text=f"{text}\n\n{aciklama}",
            command=cmd,
            width=170, height=130,
            corner_radius=12,
            fg_color=renk,
            hover_color=renk,
            font=("Roboto", 13, "bold")
        )
        kart.pack(side="left", padx=8, pady=5)

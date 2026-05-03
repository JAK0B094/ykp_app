# JKB — Kişisel Yönetim ve Fitness Takip Uygulaması

## Proje Hakkında
Flask tabanlı PWA (Progressive Web App). Mobil öncelikli tasarım, Bootstrap 5, dark navy tema, vanilla JS. Veriler `src/data/veritabani.json` dosyasında tutulur.

## Özellikler
- Kullanıcı kaydı, girişi, şifre sıfırlama (OTP e-posta akışı)
- **Fitness Koçu:** VKİ hesaplama, antrenman programı, geçmiş, su takibi, hatırlatıcılar, motivasyon
- **Görevler:** Ekleme, tamamlama, silme, filtreleme
- **Kişisel Notlar:** Markdown benzeri metin editörü
- **Profil:** Şifre değiştirme, telefon güncelleme
- **PWA:** Service Worker, manifest, offline destek
- **Gizli Admin Paneli:** `/yonetici/giris` — tam kontrol merkezi

## Admin Paneli
- URL: `/yonetici/giris` (hiçbir yerde linklenmez)
- Varsayılan şifre: `JKB@admin2026!` (env var `ADMIN_SIFRE` ile değiştirilebilir)
- Oturum anahtarı: `session["admin_giris"]` — normal kullanıcı oturumundan tamamen bağımsız
- Blueprint: `src/routes/admin.py`, url_prefix `/yonetici`

### Admin Özellikleri
| Rota | Açıklama |
|------|----------|
| `GET /yonetici/` | Dashboard — istatistikler + kullanıcı tablosu |
| `GET /yonetici/kullanici/<ad>` | Kullanıcı detay + yönetim |
| `POST /yonetici/kullanici/<ad>/sil` | Hesap sil |
| `POST /yonetici/kullanici/<ad>/sifre-sifirla` | Şifre sıfırla |
| `POST /yonetici/kullanici/<ad>/eposta-guncelle` | E-posta değiştir |
| `POST /yonetici/kullanici/<ad>/temizle` | Belirli bir veri alanını temizle |
| `GET /yonetici/veritabani` | Ham JSON görüntüle (şifreler gizli) |
| `GET/POST /yonetici/ayarlar` | Uygulama ayarları |
| `GET /yonetici/cikis` | Admin oturumu kapat |

### Uygulama Ayarları (admin panelinden)
- `kayit_acik`: Yeni kullanıcı kaydına izin ver/ver
- `bakim_modu`: Aktifken tüm kullanıcı sayfaları `/bakim` mesajına yönlendirilir (admin URL'leri açık kalır)
- `max_kullanici`: Maksimum kayıt sayısı
- `duyuru`: Kullanıcılara gösterilen duyuru mesajı

## Proje Yapısı
```
main.py                       # Flask uygulaması, Blueprint kayıtları, bakım modu middleware
src/
  routes/
    auth.py                   # Giriş, kayıt, çıkış, şifre sıfırlama
    panel.py                  # Ana panel, profil, şifre değiştirme
    fitness.py                # Fitness koçu rotaları
    gorevler.py               # Görev yönetimi
    notlar.py                 # Not yönetimi
    admin.py                  # Gizli admin paneli (Blueprint: admin_bp)
  data/
    kimlik_dogrulama.py       # KimlikDogrulama: thread-safe JSON CRUD
    veri_yoneticisi.py        # VeriYoneticisi (extends KimlikDogrulama): su, antrenman, hatırlatıcı
    veritabani.json           # Tüm kullanıcı verisi
  templates/
    base.html                 # Ana şablon (navbar, flash, tema toggle)
    karsilama.html            # Hoşgeldin sayfası
    giris.html / kayit.html   # Auth sayfaları
    panel.html                # Kullanıcı dashboard
    fitness.html              # Fitness koçu (sekmeli)
    gorevler.html             # Görevler
    notlar.html               # Notlar
    profil.html               # Profil ayarları
    sifre_sifirla.html        # 3 adımlı OTP akışı
    bakim.html                # Bakım modu sayfası (503)
    admin_giris.html          # Admin giriş (standalone, base.html kullanmaz)
    admin_panel.html          # Admin dashboard (sidebar layout)
    admin_kullanici.html      # Kullanıcı yönetim sayfası
    admin_ayarlar.html        # Uygulama ayarları
  static/
    css/
      style.css               # Ana CSS (CSS vars, dark/light tema)
      admin.css               # Admin paneli CSS (tamamen bağımsız)
    js/
      app.js                  # PWA, tema
      fitness.js              # Fitness JS
    manifest.json / sw.js     # PWA dosyaları
  assets/
    hesaplamalar.py           # FitnessZekasi: makro + program hesaplama
```

## CSS Değişkenleri
```css
--jkb-bg, --jkb-surface, --jkb-card, --jkb-accent,
--jkb-primary, --jkb-text, --jkb-muted
```

## Teknolojiler
- Python 3.12 + Flask
- Bootstrap 5.3 + Bootstrap Icons
- Vanilla JS
- JSON dosya veritabanı (thread-safe, atomik yazma)

## Çalıştırma
```bash
python main.py   # http://0.0.0.0:5000
```

## Workflow
- **Start application**: `python main.py`

## Ortam Değişkenleri
| Değişken | Açıklama | Varsayılan |
|----------|----------|-----------|
| `SECRET_KEY` | Flask session şifrelemesi | `jkb-gizli-anahtar-2026` |
| `ADMIN_SIFRE` | Admin panel şifresi | `JKB@admin2026!` |
| `SMTP_HOST` | OTP e-posta sunucusu | (boşsa konsola yazar) |
| `SMTP_PORT` | SMTP port | 587 |
| `SMTP_USER` | SMTP kullanıcı adı | — |
| `SMTP_PASS` | SMTP şifre | — |

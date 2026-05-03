# JKB — Kişisel Yönetim ve Fitness Takip Uygulaması

## Proje Hakkında
Flask tabanlı PWA (Progressive Web App). Mobil öncelikli tasarım, Bootstrap 5, dark navy tema, vanilla JS. Veriler `src/data/veritabani.json` dosyasında tutulur.

## Özellikler
- Kullanıcı kaydı, girişi, şifre sıfırlama (OTP e-posta akışı)
- **Fitness Koçu:** VKİ, BMR, TDEE, FFMI, vücut kompozisyonu, 5 uzman program tipi (yakma/hipertrofi/kuvvet/powerbuilding/kardiyo), periodizasyon, deload haftası, su takibi, hatırlatıcılar, motivasyon
- **Kas Anatomisi Ansiklopedisi:** 14 kas grubu — alt kaslar, köken/yapışma, fonksiyon, lif tipi, en etkili egzersizler, sık hatalar, prehab önerileri
- **Egzersiz Ansiklopedisi:** 70+ egzersiz — birincil/ikincil kaslar, mekanik, teknik, hatalar, varyasyonlar, GIF görselleri (fitnessprogramer.com)
- **Egzersiz GIF Kartları:** Split program görünümünde her egzersiz canlı GIF ile gösterilir, tamamlama checkbox'ı var, detay modal açılır
- **Görevler:** Ekleme, tamamlama, silme, filtreleme
- **Kişisel Notlar:** Markdown benzeri metin editörü
- **Profil:** Şifre değiştirme, telefon güncelleme
- **PWA:** Service Worker, manifest, offline destek
- **Gizli Admin Paneli:** `/yonetici` — tam kontrol merkezi

## Admin Paneli
- URL: `/yonetici/giris` (hiçbir yerde linklenmez)
- Varsayılan şifre: `JKB@admin2026!` (env var `ADMIN_SIFRE` ile değiştirilebilir)
- Oturum anahtarı: `session["admin_giris"]` — normal kullanıcı oturumundan tamamen bağımsız
- Blueprint: `src/routes/admin.py`, url_prefix `/yonetici`
- Sidebar: `src/templates/admin_sidebar.html` (tüm admin sayfalarında `{% include %}` ile kullanılır)

### Admin Rotaları
| Rota | Açıklama |
|------|----------|
| `GET /yonetici/` | Dashboard — istatistikler + kullanıcı tablosu |
| `GET/POST /yonetici/navbar` | Sürükle-bırak navbar yöneticisi |
| `GET/POST /yonetici/goruntum` | Görünüm & tema editörü |
| `GET/POST /yonetici/ayarlar` | Uygulama ayarları |
| `GET /yonetici/kullanici/<ad>` | Kullanıcı detay + yönetim |
| `POST /yonetici/kullanici/<ad>/sil` | Hesap sil |
| `POST /yonetici/kullanici/<ad>/sifre-sifirla` | Şifre sıfırla |
| `POST /yonetici/kullanici/<ad>/eposta-guncelle` | E-posta değiştir |
| `POST /yonetici/kullanici/<ad>/rol` | Rol değiştir (user/moderator/admin) |
| `POST /yonetici/kullanici/<ad>/durum` | Durum değiştir (aktif/pasif/kilitli) |
| `POST /yonetici/kullanici/<ad>/pin` | Admin'de sabitle/kaldır |
| `POST /yonetici/kullanici/<ad>/temizle` | Belirli veri alanını temizle |
| `POST /yonetici/navbar/sifirla` | Navbar'ı varsayılana döndür |
| `POST /yonetici/goruntum/sifirla` | Görünümü varsayılana döndür |
| `GET /yonetici/veritabani` | Ham JSON görüntüle (şifreler gizli) |
| `GET /yonetici/cikis` | Admin oturumu kapat |

### Site Konfigürasyonu (`veritabani.json` → `site_konfig`)
```json
{
  "site_konfig": {
    "navbar_linkleri": [ { "id", "label", "href", "icon", "aktif", "siralama",
                           "sadece_giris", "sadece_cikis", "stil" } ],
    "goruntum": {
      "navbar_arka": "CSS gradient/renk",
      "birincil_renk": "#e94560",
      "site_basligi": "JKB",
      "karsilama_baslik_1", "karsilama_baslik_2",
      "karsilama_pill", "karsilama_metin", "karsilama_alt", "karsilama_dipnot",
      "imza_metin", "imza_goster": true
    },
    "sayfalar": [ { "id", "label", "href", "aktif", "aciklama" } ]
  }
}
```

### Context Processor
`main.py`'de `inject_site_konfig()` tüm şablonlara `site_konfig` değişkenini enjekte eder.
- `base.html`: Navbar linkleri + tema CSS override'ları dinamik olarak uygulanır
- `karsilama.html`: Hero metinleri dinamik olarak okunur

## Proje Yapısı
```
main.py                       # Flask uygulaması, Blueprint kayıtları, bakım modu, context_processor
src/
  routes/
    auth.py                   # Giriş, kayıt, çıkış, şifre sıfırlama
    panel.py                  # Ana panel, profil, şifre değiştirme
    fitness.py                # Fitness koçu rotaları
    gorevler.py               # Görev yönetimi
    notlar.py                 # Not yönetimi
    admin.py                  # Gizli admin paneli (Blueprint: admin_bp)
                              #   — get_site_konfig(), VARSAYILAN_NAVBAR, VARSAYILAN_GORUNTUM
  data/
    kimlik_dogrulama.py       # KimlikDogrulama: thread-safe JSON CRUD
    veri_yoneticisi.py        # VeriYoneticisi: su, antrenman, hatırlatıcı
    veritabani.json           # Tüm kullanıcı verisi + site_konfig
  templates/
    base.html                 # Ana şablon — dinamik navbar + tema CSS override
    karsilama.html            # Hoşgeldin — dinamik hero metinleri
    giris.html / kayit.html   # Auth sayfaları
    panel.html                # Kullanıcı dashboard
    fitness.html              # Fitness koçu (sekmeli)
    gorevler.html             # Görevler
    notlar.html               # Notlar
    profil.html               # Profil ayarları
    sifre_sifirla.html        # 3 adımlı OTP akışı
    bakim.html                # Bakım modu sayfası (503)
    admin_giris.html          # Admin giriş (standalone)
    admin_sidebar.html        # Paylaşılan sidebar (tüm admin sayfaları include eder)
    admin_panel.html          # Admin dashboard
    admin_navbar.html         # Sürükle-bırak navbar yöneticisi (SortableJS)
    admin_goruntum.html       # Görünüm & tema editörü (canlı önizleme)
    admin_kullanici.html      # Kullanıcı yönetim sayfası
    admin_ayarlar.html        # Uygulama ayarları
  static/
    css/
      style.css               # Ana CSS (CSS vars, dark/light tema)
      admin.css               # Admin paneli CSS (bağımsız)
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
`--jkb-primary` ve `.jkb-navbar` background admin'den dinamik override edilebilir.

## Teknolojiler
- Python 3.12 + Flask
- Bootstrap 5.3 + Bootstrap Icons
- SortableJS 1.15.2 (admin drag-and-drop)
- Vanilla JS
- JSON dosya veritabanı (thread-safe, atomik yazma)

## Çalıştırma
```bash
python main.py   # http://0.0.0.0:5000
```

## Ortam Değişkenleri
| Değişken | Açıklama | Varsayılan |
|----------|----------|-----------|
| `SECRET_KEY` | Flask session şifrelemesi | `jkb-gizli-anahtar-2026` |
| `ADMIN_SIFRE` | Admin panel şifresi | `JKB@admin2026!` |
| `SMTP_HOST` | OTP e-posta sunucusu | (boşsa konsola yazar) |
| `SMTP_PORT` | SMTP port | 587 |
| `SMTP_USER` | SMTP kullanıcı adı | — |
| `SMTP_PASS` | SMTP şifre | — |

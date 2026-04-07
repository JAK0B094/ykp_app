# JKB — Kişisel Yönetim ve Fitness Takip Uygulaması

## Proje Hakkında
Python ile yazılmış masaüstü kişisel yönetim uygulaması. CustomTkinter GUI framework'ü kullanılır. Karanlık tema varsayılandır.

## Özellikler
- Kullanıcı kaydı, girişi ve şifre sıfırlama
- **Fitness Koçu:** VKİ hesaplama + kategori (Zayıf/Normal/Fazla Kilolu/Obez), 3 seviye (Başlangıç/Orta/İleri), antrenman programı, geçmiş kayıtları
- **Görevler:** Ekleme, tamamlama, silme, filtreleme (hepsi/bekleyen/tamamlanan), kalıcı kayıt
- **Kişisel Notlar:** Kullanıcıya özel kayıt/yükleme, karakter/kelime sayacı, Ctrl+S ile hızlı kayıt
- **Profil Sayfası:** İstatistikler, fitness geçmişi, şifre değiştirme
- **Ana Panel:** İstatistik kartları, selamlama, modül butonları

## Proje Yapısı
```
main.py              # Başlangıç noktası
src/
  app.py             # Ana uygulama sınıfı (JKBApp), tema ayarı, sayfa yönetimi
  __init__.py
  module/            # UI sayfaları
    karsilama_sayfasi.py
    giris_sayfasi.py
    kayit_sayfasi.py
    ana_panel.py          # İstatistik kartlı dashboard
    fitness_kocu.py       # 3 sekme: Analiz, Program, Geçmiş
    gorev_modulu.py       # Kalıcı görev yönetimi
    not_modulu.py         # Kalıcı not defteri
    profil_sayfasi.py     # Kullanıcı profili ve şifre değiştirme
    sifre_sifirlama_sayfasi.py
    ozel_butonlar.py
  assets/
    hesaplamalar.py       # FitnessZekasi: 3 seviye program + VKİ kategorisi
    fitness_verisi.py
    logo.png
  data/
    kimlik_dogrulama.py   # KimlikDogrulama: CRUD + görev/not/fitness
    veritabani.json       # Kullanıcı verisi (JSON)
```

## Teknolojiler
- Python 3.12
- CustomTkinter 5.2.2
- Pillow (PIL)

## Çalıştırma
```bash
python main.py
```
Uygulama VNC modu ile masaüstü penceresi olarak açılır.

## Varsayılan Kullanıcı
- Kullanıcı adı: `ykp`
- Şifre: `949494`

## Workflow
- **Start application**: `python main.py` (VNC çıkış modu)

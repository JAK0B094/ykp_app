# JKB - Kişisel Yönetim ve Fitness Takip Uygulaması

## Proje Hakkında
Python ile yazılmış masaüstü bir kişisel yönetim uygulaması. CustomTkinter GUI framework'ü kullanılır.

## Özellikler
- Kullanıcı kaydı ve girişi
- Fitness koçu (VKİ hesaplama, antrenman programı önerisi)
- Görev yönetimi (Todo listesi)
- Kişisel not defteri
- Şifre sıfırlama

## Proje Yapısı
```
main.py              # Başlangıç noktası
src/
  app.py             # Ana uygulama sınıfı (JKBApp) ve sayfa yönetimi
  __init__.py
  module/            # UI sayfaları
    karsilama_sayfasi.py
    giris_sayfasi.py
    kayit_sayfasi.py
    ana_panel.py
    fitness_kocu.py
    gorev_modulu.py
    not_modulu.py
    sifre_sifirlama_sayfasi.py
    ozel_butonlar.py
  assets/            # Hesaplama mantığı ve görseller
    hesaplamalar.py  # FitnessZekasi sınıfı
    fitness_verisi.py
    logo.png
  data/              # Veri katmanı
    kimlik_dogrulama.py  # KimlikDogrulama sınıfı
    veritabani.json      # Kullanıcı verisi (JSON)
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
- **Start application**: `python main.py` (VNC modu)

import json
import datetime
from src.data.kimlik_dogrulama import KimlikDogrulama
import src.data.kimlik_dogrulama as _kd_mod


class VeriYoneticisi(KimlikDogrulama):
    """KimlikDogrulama'yı genişletir: su takibi, antrenman, hatırlatıcı."""

    def _nested_guncelle(self, kullanici_adi, ust_alan, alt_alan, deger):
        with _kd_mod._dosya_kilidi:
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"kullanicilar": {}}
            if kullanici_adi in data.get("kullanicilar", {}):
                field = data["kullanicilar"][kullanici_adi].setdefault(ust_alan, {})
                field[alt_alan] = deger
                self._guvensiz_yaz(data)

    def _liste_ekle(self, kullanici_adi, alan, eleman, maks=200):
        with _kd_mod._dosya_kilidi:
            try:
                with open(self.dosya_yolu, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {"kullanicilar": {}}
            if kullanici_adi in data.get("kullanicilar", {}):
                liste = data["kullanicilar"][kullanici_adi].setdefault(alan, [])
                liste.append(eleman)
                if len(liste) > maks:
                    liste[:] = liste[-maks:]
                self._guvensiz_yaz(data)

    # ── Su Takibi ──────────────────────────────────────────────────────────────

    def su_guncelle(self, kullanici_adi, tarih, miktar):
        self._nested_guncelle(kullanici_adi, "su_kayitlari", tarih,
                              max(0, min(20, int(miktar))))

    def su_getir(self, kullanici_adi, tarih):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(
                kullanici_adi, {}).get("su_kayitlari", {}).get(tarih, 0)
        except Exception:
            return 0

    def su_gecmis_getir(self, kullanici_adi, son_n=7):
        try:
            data = self.veri_oku()
            kayitlar = data.get("kullanicilar", {}).get(
                kullanici_adi, {}).get("su_kayitlari", {})
            gunler = sorted(kayitlar.keys())[-son_n:]
            return {g: kayitlar[g] for g in gunler}
        except Exception:
            return {}

    # ── Antrenman Takibi ───────────────────────────────────────────────────────

    def antrenman_kaydet(self, kullanici_adi, kayit):
        self._liste_ekle(kullanici_adi, "antrenman_kayitlari", kayit)

    def antrenman_gecmis_getir(self, kullanici_adi, son_n=10):
        try:
            data = self.veri_oku()
            kayitlar = data.get("kullanicilar", {}).get(
                kullanici_adi, {}).get("antrenman_kayitlari", [])
            return kayitlar[-son_n:][::-1]
        except Exception:
            return []

    def antrenman_seri_getir(self, kullanici_adi):
        """Ardışık antrenman günü serisi hesapla."""
        try:
            data = self.veri_oku()
            kayitlar = data.get("kullanicilar", {}).get(
                kullanici_adi, {}).get("antrenman_kayitlari", [])
            if not kayitlar:
                return 0
            tarihler = sorted(set(
                k.get("tarih", "") for k in kayitlar
                if k.get("tarih")
            ), reverse=True)
            seri = 0
            bugun = datetime.date.today()
            for i, t in enumerate(tarihler):
                gun = datetime.date.fromisoformat(t)
                if (bugun - gun).days == i:
                    seri += 1
                else:
                    break
            return seri
        except Exception:
            return 0

    # ── Hatırlatıcılar ─────────────────────────────────────────────────────────

    def hatirlatici_kaydet(self, kullanici_adi, hatirlaticilar):
        self._kullanici_guncelle(kullanici_adi, "hatirlaticilar", hatirlaticilar)

    def hatirlatici_getir(self, kullanici_adi):
        try:
            data = self.veri_oku()
            return data.get("kullanicilar", {}).get(
                kullanici_adi, {}).get("hatirlaticilar", [])
        except Exception:
            return []

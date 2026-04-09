/* ──── Egzersiz Resim Haritası ──────────────────────────────────────────── */
const EG_RESIMLERI = {
  'squat':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Squat.gif',
  'bench press':  'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif',
  'bench':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif',
  'deadlift':     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Deadlift.gif',
  'pull-up':      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-Up.gif',
  'pull up':      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-Up.gif',
  'pullup':       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-Up.gif',
  'şınav':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif',
  'push':         'https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif',
  'plank':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Plank.gif',
  'row':          'https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Barbell-Row.gif',
  'kürek':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Barbell-Row.gif',
  'shoulder':     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif',
  'omuz':         'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif',
  'press':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif',
  'romanian':     'https://fitnessprogramer.com/wp-content/uploads/2021/06/Romanian-Deadlift.gif',
  'rdl':          'https://fitnessprogramer.com/wp-content/uploads/2021/06/Romanian-Deadlift.gif',
  'lat':          'https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif',
  'pulldown':     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif',
  'overhead':     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Overhead-Press.gif',
  'curl':         'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bicep-Curl.gif',
  'bicep':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bicep-Curl.gif',
  'tricep':       'https://fitnessprogramer.com/wp-content/uploads/2021/06/Tricep-Pushdown.gif',
  'incline':      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Dumbbell-Press.gif',
  'leg press':    'https://fitnessprogramer.com/wp-content/uploads/2021/02/Leg-Press.gif',
  'leg curl':     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Leg-Curl.gif',
  'calf':         'https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Calf-Raise.gif',
  'bulgarian':    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bulgarian-Split-Squat.gif',
  'split':        'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bulgarian-Split-Squat.gif',
  'fly':          'https://fitnessprogramer.com/wp-content/uploads/2022/01/Cable-Fly.gif',
  'face pull':    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Face-Pull.gif',
  'hiit':         'https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jacks.gif',
  'kardiyo':      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jacks.gif',
};

function egzersizResimBul(isim) {
  const kucuk = isim.toLowerCase();
  for (const [anahtar, url] of Object.entries(EG_RESIMLERI)) {
    if (kucuk.includes(anahtar)) return url;
  }
  return null;
}

/* ──── Sayfa Yüklenince ─────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  egzersizResimleriniYukle();
  bildirimDurumunuGoster();
  hatirlaticiKontrolunuBaslat();
  gunlukGorevleriYukle();
});

/* ──── Egzersiz Resimleri ────────────────────────────────────────────────── */
function egzersizResimleriniYukle() {
  document.querySelectorAll('.egzersiz-resim').forEach(img => {
    const isim = img.dataset.isim || '';
    const url = egzersizResimBul(isim);
    if (url) {
      img.src = url;
      img.style.display = 'block';
    } else {
      img.style.display = 'none';
      const ph = img.nextElementSibling;
      if (ph) ph.style.display = 'flex';
    }
  });
}

/* ──── Su Takibi ─────────────────────────────────────────────────────────── */
let suMiktari = typeof SU_BUGUN !== 'undefined' ? SU_BUGUN : 0;

function suBardakTikla(n) {
  const yeni = suMiktari === n ? n - 1 : n;
  suGuncelleAPI(yeni);
}

function suGuncelle(delta) {
  suGuncelleAPI(suMiktari + delta);
}

function suGuncelleAPI(yeni) {
  yeni = Math.max(0, Math.min(20, yeni));
  fetch('/api/fitness/su', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ miktar: yeni })
  })
    .then(r => r.json())
    .then(d => { suMiktari = d.bugun; suUIGuncelle(); })
    .catch(() => { suMiktari = yeni; suUIGuncelle(); });
}

function suUIGuncelle() {
  const bardaklar = document.querySelectorAll('.su-bardak');
  bardaklar.forEach((btn, i) => {
    const n = i + 1;
    btn.classList.toggle('dolu', n <= suMiktari);
    const ikon = btn.querySelector('i');
    if (ikon) {
      ikon.className = n <= suMiktari
        ? 'bi bi-cup-straw-fill'
        : 'bi bi-cup-straw';
    }
  });
  const pct = Math.min(suMiktari / 8 * 100, 100);
  const prog = document.getElementById('suProgress');
  if (prog) prog.style.width = pct + '%';
  const adet = document.getElementById('suAdet');
  if (adet) adet.textContent = suMiktari + ' / 8 bardak';
  const lt = document.getElementById('suLt');
  if (lt) lt.textContent = (suMiktari * 0.25).toFixed(2) + ' L';
  if (suMiktari >= 8) bildirimGonder('Su Takibi', 'Günlük su hedefinize ulaştınız!', '💧');
}

/* ──── Antrenman Tamamla ─────────────────────────────────────────────────── */
const btnTamamla = document.getElementById('btnAntrenmanTamamla');
if (btnTamamla) {
  btnTamamla.addEventListener('click', () => {
    const tamamlananlar = [...document.querySelectorAll('.egzersiz-cb:checked')]
      .map(cb => cb.value);
    const ozet = document.getElementById('antrenmanTamamOzet');
    if (ozet) {
      ozet.textContent = tamamlananlar.length > 0
        ? 'Tamamlanan: ' + tamamlananlar.join(', ')
        : 'Tüm egzersizler tamamlandı.';
    }
    const modal = new bootstrap.Modal(document.getElementById('modalAntrenman'));
    modal.show();
  });
}

const btnKaydet = document.getElementById('btnAntrenmanKaydet');
if (btnKaydet) {
  btnKaydet.addEventListener('click', () => {
    const sure = parseInt(document.getElementById('antrenmanSure')?.value || '45');
    const egzersizler = [...document.querySelectorAll('.egzersiz-cb:checked')].map(cb => cb.value);
    fetch('/api/fitness/antrenman', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ program: PROGRAM_ADI, sure, egzersizler })
    })
      .then(r => r.json())
      .then(d => {
        bootstrap.Modal.getInstance(document.getElementById('modalAntrenman'))?.hide();
        bildirimGonder('Antrenman Tamamlandı!',
          `${sure} dakika antrenman kaydedildi. Seri: ${d.seri} gün 🔥`, '💪');
        document.querySelectorAll('.egzersiz-cb').forEach(cb => cb.checked = false);
        setTimeout(() => location.reload(), 1500);
      })
      .catch(() => alert('Antrenman kaydedilemedi.'));
  });
}

/* ──── Hatırlatıcı Sistemi ──────────────────────────────────────────────── */
let hatirlaticilar = typeof HATIRLATICILAR !== 'undefined' ? [...HATIRLATICILAR] : [];

function hatirlaticiEkle() {
  const tur = document.getElementById('hatTur')?.value || 'genel';
  const saat = document.getElementById('hatSaat')?.value || '09:00';
  const mesaj = document.getElementById('hatMesaj')?.value?.trim() || '';
  if (!mesaj) { alert('Mesaj boş olamaz!'); return; }

  const yeni = {
    id: Date.now().toString(),
    tur, saat, mesaj, aktif: true
  };
  hatirlaticilar.push(yeni);
  hatirlaticiKaydet();
  hatirlaticiListeGuncelle();
  document.getElementById('hatMesaj').value = '';
}

function hatirlaticiSil(id) {
  hatirlaticilar = hatirlaticilar.filter(h => h.id !== id);
  hatirlaticiKaydet();
  hatirlaticiListeGuncelle();
}

function hatirlaticiToggle(id) {
  const h = hatirlaticilar.find(h => h.id === id);
  if (h) { h.aktif = !h.aktif; hatirlaticiKaydet(); hatirlaticiListeGuncelle(); }
}

function hatirlaticiKaydet() {
  fetch('/api/fitness/hatirlaticilar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ hatirlaticilar })
  }).catch(() => {});
}

function hatirlaticiListeGuncelle() {
  const liste = document.getElementById('hatirlaticiListe');
  if (!liste) return;
  if (hatirlaticilar.length === 0) {
    liste.innerHTML = '<p class="text-muted small">Henüz hatırlatıcı yok.</p>';
    return;
  }
  liste.innerHTML = hatirlaticilar.map(h => `
    <div class="hatirlatici-karti d-flex justify-content-between align-items-center mb-2" data-id="${h.id}">
      <div>
        <div class="d-flex align-items-center gap-2">
          <span class="badge bg-secondary">${h.saat}</span>
          <span class="small text-white">${h.mesaj}</span>
        </div>
        <div class="small text-muted">${h.tur}${h.aktif ? '' : ' · Duraklatıldı'}</div>
      </div>
      <div class="d-flex gap-1">
        <button class="btn btn-outline-secondary btn-sm py-0 px-1"
                onclick="hatirlaticiToggle('${h.id}')">
          ${h.aktif ? 'Durdur' : 'Başlat'}
        </button>
        <button class="btn btn-outline-danger btn-sm py-0 px-1"
                onclick="hatirlaticiSil('${h.id}')">✕</button>
      </div>
    </div>
  `).join('');
}

function hatirlaticiKontrolunuBaslat() {
  setInterval(hatirlaticiKontrolEt, 60000);
  hatirlaticiKontrolEt();
}

function hatirlaticiKontrolEt() {
  if (!Array.isArray(hatirlaticilar)) return;
  const simdiki = new Date();
  const saat = String(simdiki.getHours()).padStart(2, '0');
  const dakika = String(simdiki.getMinutes()).padStart(2, '0');
  const simdi = `${saat}:${dakika}`;
  hatirlaticilar.forEach(h => {
    if (h.aktif && h.saat === simdi) {
      bildirimGonder(hatirlaticiTuruAd(h.tur), h.mesaj, hatirlaticiTuruEmoji(h.tur));
      alarmiCal();
    }
  });
}

function hatirlaticiTuruAd(tur) {
  const adlar = { su: 'Su Hatırlatıcısı', antrenman: 'Antrenman Zamanı',
                  beslenme: 'Beslenme', uyku: 'Uyku Vakti', genel: 'Hatırlatıcı' };
  return adlar[tur] || 'Hatırlatıcı';
}

function hatirlaticiTuruEmoji(tur) {
  const emojiler = { su: '💧', antrenman: '💪', beslenme: '🥗', uyku: '😴', genel: '🔔' };
  return emojiler[tur] || '🔔';
}

/* ──── Browser Bildirimleri ─────────────────────────────────────────────── */
function bildirimIzniIste() {
  if (!('Notification' in window)) {
    alert('Tarayıcınız bildirimleri desteklemiyor.');
    return;
  }
  Notification.requestPermission().then(p => bildirimDurumunuGoster());
}

function bildirimDurumunuGoster() {
  const durum = document.getElementById('bildirimDurumu');
  const btn = document.getElementById('btnBildirimIzni');
  if (!durum || !('Notification' in window)) return;
  const p = Notification.permission;
  if (p === 'granted') {
    durum.textContent = '✓ Bildirimler aktif.';
    durum.className = 'small text-success';
    if (btn) btn.style.display = 'none';
  } else if (p === 'denied') {
    durum.textContent = '✗ Bildirimler engellendi. Tarayıcı ayarlarından açın.';
    durum.className = 'small text-danger';
  } else {
    durum.textContent = 'Hatırlatıcılar için bildirim iznine ihtiyaç var.';
    durum.className = 'small text-muted';
  }
}

function bildirimGonder(baslik, mesaj, emoji = '🏋️') {
  if (Notification.permission !== 'granted') return;
  try {
    new Notification(`${emoji} ${baslik}`, {
      body: mesaj,
      icon: '/static/logo.png'
    });
  } catch (e) { }
}

/* ──── Alarm Sesi (Web Audio API) ──────────────────────────────────────── */
function alarmiCal() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    [0, 0.2, 0.4].forEach(offset => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain); gain.connect(ctx.destination);
      osc.frequency.value = 880;
      osc.type = 'sine';
      gain.gain.setValueAtTime(0.3, ctx.currentTime + offset);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + offset + 0.3);
      osc.start(ctx.currentTime + offset);
      osc.stop(ctx.currentTime + offset + 0.3);
    });
  } catch (e) { }
}

/* ──── Günlük Görevler ──────────────────────────────────────────────────── */
function gunlukGorevleriYukle() {
  const bugun = new Date().toISOString().split('T')[0];
  const kayit = JSON.parse(localStorage.getItem('jkb_gunluk_' + bugun) || '{}');
  ['gv1', 'gv2', 'gv3', 'gv4'].forEach(id => {
    const el = document.getElementById(id);
    if (el && kayit[id]) el.checked = true;
  });
  gunlukProgressGuncelle();
}

function gorevTamamla(cb, tur) {
  const bugun = new Date().toISOString().split('T')[0];
  const kayit = JSON.parse(localStorage.getItem('jkb_gunluk_' + bugun) || '{}');
  kayit[cb.id] = cb.checked;
  localStorage.setItem('jkb_gunluk_' + bugun, JSON.stringify(kayit));
  gunlukProgressGuncelle();
  if (cb.checked) {
    const mesajlar = {
      antrenman: 'Antrenman tamamlandı, muhteşem! 💪',
      su: 'Su hedefine ulaştın! 💧',
      beslenme: 'Beslenme hedefi tamamlandı! 🥗',
      uyku: 'İyi uyku kaydedildi! 😴',
    };
    bildirimGonder('Görev Tamamlandı!', mesajlar[tur] || 'Görev tamamlandı!', '✅');
  }
}

function gunlukProgressGuncelle() {
  const checkboxlar = document.querySelectorAll('#gunlukGorevler .form-check-input');
  const toplam = checkboxlar.length;
  const tamamlanan = [...checkboxlar].filter(c => c.checked).length;
  const pct = toplam > 0 ? (tamamlanan / toplam * 100) : 0;
  const prog = document.getElementById('gunlukProgress');
  if (prog) prog.style.width = pct + '%';
}

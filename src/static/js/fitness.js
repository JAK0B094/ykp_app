/* ══════════════════════════════════════════════════════════════════════════
   JKB FitnessZekası — Egzersiz Görsel & Etkileşim Motoru
   ══════════════════════════════════════════════════════════════════════════ */

/* ── Egzersiz GIF Haritası (fitnessprogramer.com) ──────────────────────── */
const EG_RESIMLERI = {
  // GÖĞÜS
  'barbell bench press':         'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif',
  'bench press':                 'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bench-Press.gif',
  'incline barbell press':       'https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Barbell-Bench-Press.gif',
  'incline bench':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Barbell-Bench-Press.gif',
  'incline dumbbell press':      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Dumbbell-Press.gif',
  'incline press':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Dumbbell-Press.gif',
  'dumbbell bench press':        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bench-Press.gif',
  'dumbbell press':              'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bench-Press.gif',
  'decline bench press':         'https://fitnessprogramer.com/wp-content/uploads/2021/06/Decline-Barbell-Bench-Press.gif',
  'decline':                     'https://fitnessprogramer.com/wp-content/uploads/2021/06/Decline-Barbell-Bench-Press.gif',
  'dumbbell fly':                'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Fly.gif',
  'db fly':                      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Fly.gif',
  'cable fly':                   'https://fitnessprogramer.com/wp-content/uploads/2022/01/Cable-Fly.gif',
  'cable crossover':             'https://fitnessprogramer.com/wp-content/uploads/2022/01/Cable-Fly.gif',
  'pec deck':                    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Pec-Deck.gif',
  'machine chest':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Pec-Deck.gif',
  'chest dip':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/Chest-Dip.gif',
  'push-up':                     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif',
  'push up':                     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif',
  'şınav':                       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Push-Up.gif',
  'diamond push':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Diamond-Push-up.gif',
  // SIRTI
  'conventional deadlift':       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Deadlift.gif',
  'deadlift':                    'https://fitnessprogramer.com/wp-content/uploads/2021/02/Deadlift.gif',
  'sumo deadlift':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Sumo-Deadlift.gif',
  'romanian deadlift':           'https://fitnessprogramer.com/wp-content/uploads/2021/06/Romanian-Deadlift.gif',
  'rdl':                         'https://fitnessprogramer.com/wp-content/uploads/2021/06/Romanian-Deadlift.gif',
  'stiff-leg':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/Romanian-Deadlift.gif',
  'pull-up':                     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-Up.gif',
  'pull up':                     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-Up.gif',
  'pullup':                      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Pull-Up.gif',
  'chin-up':                     'https://fitnessprogramer.com/wp-content/uploads/2021/06/Chin-Up.gif',
  'chin up':                     'https://fitnessprogramer.com/wp-content/uploads/2021/06/Chin-Up.gif',
  'lat pulldown':                'https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif',
  'pulldown':                    'https://fitnessprogramer.com/wp-content/uploads/2021/02/Lat-Pulldown.gif',
  'straight-arm lat':            'https://fitnessprogramer.com/wp-content/uploads/2021/06/Straight-Arm-Lat-Pulldown.gif',
  'straight arm':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Straight-Arm-Lat-Pulldown.gif',
  'bent-over barbell row':       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Barbell-Row.gif',
  'barbell row':                 'https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Barbell-Row.gif',
  'kürek':                       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Bent-Over-Barbell-Row.gif',
  'dumbbell row':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/One-Arm-Dumbbell-Row.gif',
  'one-arm row':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/One-Arm-Dumbbell-Row.gif',
  'seated cable row':            'https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Cable-Row.gif',
  'cable row':                   'https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Cable-Row.gif',
  't-bar row':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/T-Bar-Row.gif',
  'face pull':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/Face-Pull.gif',
  'barbell shrug':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Shrug.gif',
  'shrug':                       'https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Shrug.gif',
  'back extension':              'https://fitnessprogramer.com/wp-content/uploads/2021/06/Back-Extension.gif',
  'hyperextension':              'https://fitnessprogramer.com/wp-content/uploads/2021/06/Back-Extension.gif',
  'good morning':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Good-Morning.gif',
  // OMUZ
  'barbell overhead press':      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Overhead-Press.gif',
  'overhead press':              'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Overhead-Press.gif',
  'military press':              'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Overhead-Press.gif',
  'dumbbell shoulder press':     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif',
  'shoulder press':              'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif',
  'omuz':                        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Shoulder-Press.gif',
  'arnold press':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Arnold-Press.gif',
  'arnold':                      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Arnold-Press.gif',
  'lateral raise':               'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif',
  'yan kaldırma':                'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Lateral-Raise.gif',
  'cable lateral':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Cable-Lateral-Raise.gif',
  'rear delt fly':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Rear-Delt-Fly.gif',
  'rear delt':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/Rear-Delt-Fly.gif',
  'front raise':                 'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Front-Raise.gif',
  'upright row':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Upright-Row.gif',
  // BİCEPS
  'barbell curl':                'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Bicep-Curl.gif',
  'dumbbell curl':               'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bicep-Curl.gif',
  'bicep curl':                  'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bicep-Curl.gif',
  'bicep':                       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Dumbbell-Bicep-Curl.gif',
  'hammer curl':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/Hammer-Curl.gif',
  'hammer':                      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Hammer-Curl.gif',
  'concentration curl':          'https://fitnessprogramer.com/wp-content/uploads/2021/06/Concentration-Curl.gif',
  'preacher curl':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Preacher-Curl.gif',
  'preacher':                    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Preacher-Curl.gif',
  'incline dumbbell curl':       'https://fitnessprogramer.com/wp-content/uploads/2021/06/Incline-Dumbbell-Curl.gif',
  'cable curl':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Cable-Curl.gif',
  'reverse curl':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Reverse-Barbell-Curl.gif',
  'ez bar curl':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/EZ-Bar-Curl.gif',
  // TRİCEPS
  'tricep pushdown':             'https://fitnessprogramer.com/wp-content/uploads/2021/06/Tricep-Pushdown.gif',
  'tricep push':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/Tricep-Pushdown.gif',
  'rope pushdown':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Tricep-Rope-Pushdown.gif',
  'skull crusher':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Skull-Crusher.gif',
  'skullcrusher':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Skull-Crusher.gif',
  'overhead tricep':             'https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Overhead-Triceps-Extension.gif',
  'tricep extension':            'https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Overhead-Triceps-Extension.gif',
  'close-grip bench':            'https://fitnessprogramer.com/wp-content/uploads/2021/06/Close-Grip-Bench-Press.gif',
  'close grip':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Close-Grip-Bench-Press.gif',
  'tricep dip':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Triceps-Dip.gif',
  // BACAK
  'barbell back squat':          'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Squat.gif',
  'back squat':                  'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Squat.gif',
  'squat':                       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Barbell-Squat.gif',
  'front squat':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/Front-Squat.gif',
  'hack squat':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Hack-Squat.gif',
  'goblet squat':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Goblet-Squat.gif',
  'goblet':                      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Goblet-Squat.gif',
  'leg press':                   'https://fitnessprogramer.com/wp-content/uploads/2021/02/Leg-Press.gif',
  'bulgarian split squat':       'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bulgarian-Split-Squat.gif',
  'bulgarian':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bulgarian-Split-Squat.gif',
  'split squat':                 'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bulgarian-Split-Squat.gif',
  'lunge':                       'https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Lunge.gif',
  'akciğer':                     'https://fitnessprogramer.com/wp-content/uploads/2021/06/Dumbbell-Lunge.gif',
  'leg extension':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Leg-Extension.gif',
  'lying leg curl':              'https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Leg-Curl.gif',
  'leg curl':                    'https://fitnessprogramer.com/wp-content/uploads/2021/02/Seated-Leg-Curl.gif',
  'seated leg curl':             'https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-Leg-Curl.gif',
  'nordic hamstring':            'https://fitnessprogramer.com/wp-content/uploads/2021/06/Nordic-Hamstring-Curl.gif',
  'nordic':                      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Nordic-Hamstring-Curl.gif',
  'hip thrust':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Barbell-Hip-Thrust.gif',
  'glute bridge':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Glute-Bridge.gif',
  'standing calf raise':         'https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Calf-Raise.gif',
  'calf raise':                  'https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Calf-Raise.gif',
  'seated calf raise':           'https://fitnessprogramer.com/wp-content/uploads/2021/06/Seated-Calf-Raise.gif',
  'baldır':                      'https://fitnessprogramer.com/wp-content/uploads/2021/05/Standing-Calf-Raise.gif',
  // CORE
  'plank':                       'https://fitnessprogramer.com/wp-content/uploads/2021/02/Plank.gif',
  'side plank':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Side-Plank.gif',
  'ab wheel':                    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Ab-Wheel-Rollout.gif',
  'rollout':                     'https://fitnessprogramer.com/wp-content/uploads/2021/06/Ab-Wheel-Rollout.gif',
  'cable crunch':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Cable-Crunch.gif',
  'crunch':                      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Crunch.gif',
  'hanging leg raise':           'https://fitnessprogramer.com/wp-content/uploads/2021/06/Hanging-Leg-Raise.gif',
  'leg raise':                   'https://fitnessprogramer.com/wp-content/uploads/2021/06/Hanging-Leg-Raise.gif',
  'russian twist':               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Russian-Twist.gif',
  'pallof press':                'https://fitnessprogramer.com/wp-content/uploads/2021/06/Pallof-Press.gif',
  'dead bug':                    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Dead-Bug.gif',
  'bird dog':                    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bird-Dog.gif',
  'bird-dog':                    'https://fitnessprogramer.com/wp-content/uploads/2021/06/Bird-Dog.gif',
  'mountain climber':            'https://fitnessprogramer.com/wp-content/uploads/2021/02/Mountain-Climber.gif',
  // FONKSİYONEL
  'kettlebell swing':            'https://fitnessprogramer.com/wp-content/uploads/2021/06/Kettlebell-Swing.gif',
  'kettlebell':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Kettlebell-Swing.gif',
  "farmer's walk":               'https://fitnessprogramer.com/wp-content/uploads/2021/06/Farmers-Walk.gif',
  'farmer':                      'https://fitnessprogramer.com/wp-content/uploads/2021/06/Farmers-Walk.gif',
  'push press':                  'https://fitnessprogramer.com/wp-content/uploads/2021/06/Push-Press.gif',
  'burpee':                      'https://fitnessprogramer.com/wp-content/uploads/2021/02/Burpees.gif',
  'jumping jacks':               'https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jacks.gif',
  'hiit':                        'https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jacks.gif',
  'kardiyo':                     'https://fitnessprogramer.com/wp-content/uploads/2021/02/Jumping-Jacks.gif',
};

/* Kas grubu renk ve ikon haritası */
const KAS_GRUP_MAP = {
  'göğüs':        { renk: '#e74c3c', ikon: 'bi-heart-pulse-fill' },
  'chest':        { renk: '#e74c3c', ikon: 'bi-heart-pulse-fill' },
  'sırt':         { renk: '#3498db', ikon: 'bi-rulers' },
  'back':         { renk: '#3498db', ikon: 'bi-rulers' },
  'lat':          { renk: '#3498db', ikon: 'bi-rulers' },
  'omuz':         { renk: '#9b59b6', ikon: 'bi-arrow-up-circle-fill' },
  'delt':         { renk: '#9b59b6', ikon: 'bi-arrow-up-circle-fill' },
  'shoulder':     { renk: '#9b59b6', ikon: 'bi-arrow-up-circle-fill' },
  'bicep':        { renk: '#c0392b', ikon: 'bi-hand-thumbs-up-fill' },
  'tricep':       { renk: '#8e44ad', ikon: 'bi-chevron-bar-right' },
  'kol':          { renk: '#c0392b', ikon: 'bi-hand-thumbs-up-fill' },
  'bacak':        { renk: '#f39c12', ikon: 'bi-lightning-charge-fill' },
  'quad':         { renk: '#f39c12', ikon: 'bi-lightning-charge-fill' },
  'hamstring':    { renk: '#27ae60', ikon: 'bi-chevron-double-down' },
  'glute':        { renk: '#27ae60', ikon: 'bi-chevron-double-down' },
  'kalça':        { renk: '#27ae60', ikon: 'bi-chevron-double-down' },
  'baldır':       { renk: '#16a085', ikon: 'bi-arrow-down-circle-fill' },
  'calf':         { renk: '#16a085', ikon: 'bi-arrow-down-circle-fill' },
  'core':         { renk: '#1abc9c', ikon: 'bi-circle-fill' },
  'karın':        { renk: '#1abc9c', ikon: 'bi-circle-fill' },
  'full body':    { renk: '#f8d800', ikon: 'bi-person-arms-up' },
  'trap':         { renk: '#2980b9', ikon: 'bi-grid-3x2' },
};

function egzersizResimBul(isim) {
  const kucuk = isim.toLowerCase();
  // Önce tam eşleşme
  if (EG_RESIMLERI[kucuk]) return EG_RESIMLERI[kucuk];
  // Sonra içeren
  for (const [anahtar, url] of Object.entries(EG_RESIMLERI)) {
    if (kucuk.includes(anahtar)) return url;
  }
  return null;
}

function kasGrupBul(kasText) {
  if (!kasText) return null;
  const kucuk = kasText.toLowerCase();
  for (const [anahtar, bilgi] of Object.entries(KAS_GRUP_MAP)) {
    if (kucuk.includes(anahtar)) return bilgi;
  }
  return null;
}

/* ── Sayfa Yüklenince ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  splitKartlarinaGifYukle();
  egzersizResimleriniYukle();      // eski kart uyumluluğu
  ansiklopediAramasiKur();
  bildirimDurumunuGoster();
  hatirlaticiKontrolunuBaslat();
  gunlukGorevleriYukle();
});

/* ── Split Akordeon Egzersiz Kartları — GIF Yükle ─────────────────────── */
function splitKartlarinaGifYukle() {
  document.querySelectorAll('.egzersiz-split-karti').forEach(kart => {
    const isim = kart.dataset.egzersiz || '';
    const kaslar = kart.dataset.kaslar || '';
    const gifAlan = kart.querySelector('.eg-gif-alan');
    const ikonAlan = kart.querySelector('.eg-kas-ikon');

    // GIF yükle
    if (gifAlan) {
      const url = egzersizResimBul(isim);
      if (url) {
        const img = document.createElement('img');
        img.src = url;
        img.alt = isim;
        img.className = 'eg-gif-img';
        img.onerror = function() {
          this.parentElement.innerHTML = ikonAlaniOlustur(kaslar, isim);
        };
        gifAlan.innerHTML = '';
        gifAlan.appendChild(img);
      } else {
        gifAlan.innerHTML = ikonAlaniOlustur(kaslar, isim);
      }
    }

    // Kas grubu ikon
    if (ikonAlan && kaslar) {
      const kg = kasGrupBul(kaslar);
      if (kg) {
        ikonAlan.innerHTML = `<i class="${kg.ikon}" style="color:${kg.renk};font-size:14px"></i>`;
        ikonAlan.style.background = kg.renk + '22';
        ikonAlan.style.borderColor = kg.renk + '44';
      }
    }
  });
}

function ikonAlaniOlustur(kaslar, isim) {
  const kg = kasGrupBul(kaslar) || kasGrupBul(isim) || { renk: '#666', ikon: 'bi-activity' };
  return `<div class="eg-gif-placeholder" style="background:${kg.renk}11;border:2px dashed ${kg.renk}33">
    <i class="${kg.ikon}" style="color:${kg.renk};font-size:28px;opacity:0.7"></i>
  </div>`;
}

/* ── Eski format resim yükleyici ────────────────────────────────────────── */
function egzersizResimleriniYukle() {
  document.querySelectorAll('.egzersiz-resim').forEach(img => {
    const isim = img.dataset.isim || '';
    const url  = egzersizResimBul(isim);
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

/* ── Ansiklopedi Arama ──────────────────────────────────────────────────── */
function ansiklopediAramasiKur() {
  const input = document.getElementById('ansiklopediArama');
  if (!input) return;
  input.addEventListener('input', function() {
    const q = this.value.toLowerCase().trim();
    document.querySelectorAll('.ansiklopedi-karti').forEach(k => {
      const metin = k.dataset.arama || '';
      k.style.display = metin.includes(q) ? '' : 'none';
    });
    const goruntulenen = document.querySelectorAll('.ansiklopedi-karti:not([style*="none"])').length;
    const sayac = document.getElementById('ansiklopediSayac');
    if (sayac) sayac.textContent = goruntulenen + ' egzersiz';
  });

  // Kategori filtreleme
  document.querySelectorAll('.ans-filtre-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.ans-filtre-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const kat = this.dataset.kategori || '';
      document.querySelectorAll('.ansiklopedi-karti').forEach(k => {
        if (!kat || k.dataset.kategori === kat) {
          k.style.display = '';
        } else {
          k.style.display = 'none';
        }
      });
      if (input.value) input.dispatchEvent(new Event('input'));
    });
  });
}

/* ── Su Takibi ──────────────────────────────────────────────────────────── */
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
  document.querySelectorAll('.su-bardak').forEach((btn, i) => {
    const n = i + 1;
    btn.classList.toggle('dolu', n <= suMiktari);
    const ikon = btn.querySelector('i');
    if (ikon) ikon.className = n <= suMiktari ? 'bi bi-cup-straw-fill' : 'bi bi-cup-straw';
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

/* ── Antrenman Tamamla ──────────────────────────────────────────────────── */
const btnTamamla = document.getElementById('btnAntrenmanTamamla');
if (btnTamamla) {
  btnTamamla.addEventListener('click', () => {
    const tamamlananlar = [...document.querySelectorAll('.egzersiz-cb:checked')].map(cb => cb.value);
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

/* ── Hatırlatıcı Sistemi ────────────────────────────────────────────────── */
let hatirlaticilar = typeof HATIRLATICILAR !== 'undefined' ? [...HATIRLATICILAR] : [];

function hatirlaticiEkle() {
  const tur  = document.getElementById('hatTur')?.value  || 'genel';
  const saat = document.getElementById('hatSaat')?.value || '09:00';
  const mesaj= document.getElementById('hatMesaj')?.value || 'Hatırlatıcı';
  if (!mesaj.trim()) { alert('Mesaj girin.'); return; }
  fetch('/api/fitness/hatirlatici', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tur, saat, mesaj, aktif: true })
  })
    .then(r => r.json())
    .then(d => {
      hatirlaticilar = d.hatirlaticilar || [];
      hatirlaticiListeGuncelle();
      document.getElementById('hatMesaj').value = '';
    })
    .catch(() => alert('Eklenemedi.'));
}

function hatirlaticiSil(id) {
  fetch(`/api/fitness/hatirlatici/${id}`, { method: 'DELETE' })
    .then(r => r.json())
    .then(d => { hatirlaticilar = d.hatirlaticilar || []; hatirlaticiListeGuncelle(); })
    .catch(() => {});
}

function hatirlaticiToggle(id) {
  fetch(`/api/fitness/hatirlatici/${id}/toggle`, { method: 'POST' })
    .then(r => r.json())
    .then(d => { hatirlaticilar = d.hatirlaticilar || []; hatirlaticiListeGuncelle(); })
    .catch(() => {});
}

function hatirlaticiListeGuncelle() {
  const liste = document.getElementById('hatirlaticiListe');
  if (!liste) return;
  if (!hatirlaticilar.length) { liste.innerHTML = '<p class="text-muted small">Henüz hatırlatıcı yok.</p>'; return; }
  liste.innerHTML = hatirlaticilar.map(h => `
    <div class="hatirlatici-karti d-flex justify-content-between align-items-center mb-2">
      <div>
        <div class="d-flex align-items-center gap-2">
          <span class="badge bg-secondary">${h.saat}</span>
          <span class="small text-white">${h.mesaj}</span>
        </div>
        <div class="small text-muted">${h.tur} · ${h.aktif ? '🟢 Aktif' : '🔴 Durduruldu'}</div>
      </div>
      <div class="d-flex gap-1">
        <button class="btn btn-outline-secondary btn-sm py-0 px-1" onclick="hatirlaticiToggle('${h.id}')">
          ${h.aktif ? 'Durdur' : 'Başlat'}
        </button>
        <button class="btn btn-outline-danger btn-sm py-0 px-1" onclick="hatirlaticiSil('${h.id}')">✕</button>
      </div>
    </div>`).join('');
}

/* ── Bildirim Sistemi ───────────────────────────────────────────────────── */
function bildirimIzniIste() {
  if (!('Notification' in window)) {
    document.getElementById('bildirimDurumu').textContent = 'Tarayıcınız bildirimleri desteklemiyor.';
    return;
  }
  Notification.requestPermission().then(p => bildirimDurumunuGoster());
}

function bildirimDurumunuGoster() {
  const el = document.getElementById('bildirimDurumu');
  if (!el) return;
  if (!('Notification' in window)) { el.textContent = 'Tarayıcı desteklemiyor.'; return; }
  const d = { granted: '✅ Bildirimler aktif.', denied: '❌ Bildirimler engellendi.', default: '⚠️ İzin bekleniyor.' };
  el.textContent = d[Notification.permission] || '?';
}

function bildirimGonder(baslik, metin, ikon = '💪') {
  if (Notification.permission === 'granted') {
    new Notification(ikon + ' ' + baslik, { body: metin });
  }
}

function hatirlaticiKontrolunuBaslat() {
  setInterval(() => {
    const simdi = new Date();
    const suan = `${String(simdi.getHours()).padStart(2,'0')}:${String(simdi.getMinutes()).padStart(2,'0')}`;
    hatirlaticilar.filter(h => h.aktif && h.saat === suan).forEach(h => {
      bildirimGonder(h.tur.charAt(0).toUpperCase() + h.tur.slice(1), h.mesaj, '🔔');
    });
  }, 60000);
}

/* ── Günlük Görevler ────────────────────────────────────────────────────── */
let tamamlananGorevler = new Set();

function gorevTamamla(cb, id) {
  if (cb.checked) tamamlananGorevler.add(id); else tamamlananGorevler.delete(id);
  const pct = (tamamlananGorevler.size / 4) * 100;
  const prog = document.getElementById('gunlukProgress');
  if (prog) prog.style.width = pct + '%';
  if (tamamlananGorevler.size === 4) {
    bildirimGonder('Harika!', 'Günün tüm görevlerini tamamladın! 🏆', '🎯');
  }
}

function gunlukGorevleriYukle() {
  const kayitli = JSON.parse(localStorage.getItem('jkb_gunluk_gorevler_' + new Date().toDateString()) || '[]');
  kayitli.forEach(id => {
    tamamlananGorevler.add(id);
    const cb = document.querySelector(`[onchange*="${id}"]`);
    if (cb) cb.checked = true;
  });
  const pct = (tamamlananGorevler.size / 4) * 100;
  const prog = document.getElementById('gunlukProgress');
  if (prog) prog.style.width = pct + '%';
}

/* ── Egzersiz Modal Detayı ─────────────────────────────────────────────── */
function egzersizDetayGoster(isim, kategori, birincil, ikincil, teknik, hata, degiskenler) {
  const modal = document.getElementById('egzersizDetayModal');
  if (!modal) return;
  document.getElementById('egzersizDetayAdi').textContent  = isim;
  document.getElementById('egzersizDetayKat').textContent  = kategori;
  const gifEl = document.getElementById('egzersizDetayGif');
  if (gifEl) {
    const url = egzersizResimBul(isim.toLowerCase());
    if (url) {
      gifEl.innerHTML = `<img src="${url}" alt="${isim}" class="img-fluid rounded" style="max-height:220px;width:auto" onerror="this.parentElement.innerHTML='<div class=text-center><i class=bi-activity style=font-size:60px></i></div>'">`;
    } else {
      const kg = kasGrupBul(birincil);
      gifEl.innerHTML = kg
        ? `<div class="d-flex align-items-center justify-content-center h-100"><i class="${kg.ikon}" style="color:${kg.renk};font-size:60px;opacity:0.8"></i></div>`
        : `<div class="d-flex align-items-center justify-content-center h-100"><i class="bi-activity" style="font-size:60px;opacity:0.4"></i></div>`;
    }
  }
  document.getElementById('egzersizDetayBirincil').innerHTML = birincil.split(',').map(k => `<span class="badge bg-danger me-1">${k.trim()}</span>`).join('');
  document.getElementById('egzersizDetayIkincil').innerHTML  = ikincil.split(',').map(k => `<span class="badge bg-secondary me-1">${k.trim()}</span>`).join('');
  document.getElementById('egzersizDetayTeknik').textContent = teknik;
  document.getElementById('egzersizDetayHata').textContent   = hata;
  document.getElementById('egzersizDetayDeg').innerHTML      = degiskenler.split(',').map(d => `<span class="badge bg-outline me-1" style="border:1px solid rgba(255,255,255,0.2)">${d.trim()}</span>`).join('');
  new bootstrap.Modal(modal).show();
}

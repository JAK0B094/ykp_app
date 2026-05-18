"""
JKB FitnessZekası — Master Seviye Fitness Algoritması
=====================================================
Spor bilimi + anatomi ansiklopedisi + kişiselleştirilmiş program motoru
"""
import datetime


# ══════════════════════════════════════════════════════════════════════════════
#  KAS ANATOMİSİ ANSİKLOPEDİSİ
# ══════════════════════════════════════════════════════════════════════════════

KAS_ANATOMISI = [
    {
        "grup": "Pectoralis (Göğüs)",
        "ikon": "bi-heart-pulse-fill",
        "renk": "#e74c3c",
        "alt_kaslar": [
            "Pectoralis Major — Klaviküler Baş (Üst Göğüs)",
            "Pectoralis Major — Sternal Baş (Orta/Alt Göğüs)",
            "Pectoralis Minor (küçük göğüs, öne çekme)",
            "Serratus Anterior (dişli kas, stabilizatör)"
        ],
        "koken_yapismak": "Klavikula, sternum ve 2-6. kosta kıkırdaklarından başlayıp humerusun büyük tüberküline yapışır.",
        "fonksiyon": "Kolu öne ve içe doğru çekme (fleksiyon + adduction + iç rotasyon). Klaviküler baş kolu yukarı/öne, sternal baş aşağı/öne çeker.",
        "lif_tipi": "Hızlı kasılan (tip IIa/IIb) ağırlıklı — güç ve boyut için düşük-orta tekrar aralığı idealdir.",
        "en_iyi_egzersizler": [
            "Barbell Bench Press (Orta göğüs — primer hareket)",
            "Incline DB/BB Press (Üst göğüs — klaviküler baş)",
            "Decline Bench Press (Alt göğüs — sternal alt)",
            "Cable Fly (low/mid/high) (izolasyon + tam ROM)",
            "Pec Deck Machine (izolasyon + sabit gerilim)",
            "Dumbbell Fly (incline/flat) (strech pozisyonu)",
            "Dip (alt göğüs + tricep)",
        ],
        "bilgi": (
            "Göğüs kası anatomik olarak 3 bölgeye ayrılır: üst (incline hareketler, 30-45°), "
            "orta (flat hareketler), alt (decline/dip, aşağı baskı). Her bölge ayrı antrenman gerektirir. "
            "En büyük büyüme potansiyeli olan kas gruplarından biri. "
            "Optimal hipertrofi için: compound (BP, DP) + izolasyon (fly, pec deck) kombinasyonu. "
            "Kablo exerciselerinde TUT (Time Under Tension) ve sabit gerilim avantajlıdır. "
            "Haftada 12-20 toplam set, 2 frekansta optimal."
        ),
        "hata": (
            "1) Omuzları öne almak — hem yaralanma riski hem de göğüs aktivasyonu düşer. "
            "Kürek kemiklerini çekerek sabitlerken sırtı nötr tut. "
            "2) Sadece orta göğüsü çalıştırmak — incline ve cable ile dengeyi kur. "
            "3) Egzersizler arası tam ROM yapmamak."
        ),
        "prehab": "Band pull-apart, face pull, rear delt fly (omuz dengesi için haftada 2-3×15-20)",
    },
    {
        "grup": "Latissimus Dorsi (Geniş Sırt)",
        "ikon": "bi-rulers",
        "renk": "#3498db",
        "alt_kaslar": [
            "Latissimus Dorsi (L. kısmı — en büyük sırt kası)",
            "Teres Major (küçük yuvarlak — lat yardımcısı)",
            "Teres Minor (küçük yuvarlak — rotator cuff üyesi)",
        ],
        "koken_yapismak": "T7-L5 omur dikenlerinden, pelvik kreastten, alt 3-4 kostadan başlayıp humerusun intertüberküler oluğuna yapışır.",
        "fonksiyon": "Kolu aşağı ve geriye çekme (extension + adduction + iç rotasyon). 'Kanat' görünümü verir. Havuzcu ve jimnastikçinin güç kası.",
        "lif_tipi": "Karma lif tipi — hem dayanıklılık hem güç setlerine yanıt verir. 6-15 tekrar aralığı.",
        "en_iyi_egzersizler": [
            "Pull-up / Chin-up (en fonksiyonel lat hareketi)",
            "Lat Pulldown — geniş/dar tutuş (lat izolasyonu)",
            "Bent-Over Barbell Row (lat + orta sırt)",
            "Dumbbell Row / T-Bar Row (tek taraflı/bilateral)",
            "Cable Row (seated/standing) (sıkıştırma odaklı)",
            "Straight-Arm Lat Pulldown (saf lat izolasyon)",
        ],
        "bilgi": (
            "Vücudun en büyük kas grubu. 'V şekli' latissimus genişliğinden gelir. "
            "Pull-up'ta geniş tutuş (pronated) lat genişliğini, dar tutuş (supinated/chin-up) lat kalınlığını vurgular. "
            "Kürek kemiğini kullanarak başlatmak (scapular depression + retraction) aktivasyonu 2 kat artırır. "
            "Deadlift'te sekonder olarak yoğun çalışır. "
            "Haftada 14-22 set, 2 frekans önerilen."
        ),
        "hata": (
            "1) Hareketi ellerle başlatmak — dirsekleri öne/aşağı çekerek lat aktive et. "
            "2) Kürek kemiklerini kullanmamak — depresyon ve retraksiyon ile başla. "
            "3) Aşırı gövde sallanması (momentum) — lat değil bel çalışır."
        ),
        "prehab": "Scapular pull-up (kürek kemiği egzersizi), bayrak tipi rotator cuff çalışma",
    },
    {
        "grup": "Trapezius & Rhomboids (Orta/Üst Sırt)",
        "ikon": "bi-grid-3x2",
        "renk": "#2980b9",
        "alt_kaslar": [
            "Trapezius — Üst Lif (omuz kaldırma, boyun)",
            "Trapezius — Orta Lif (kürek kemiği retraksiyon)",
            "Trapezius — Alt Lif (kürek kemiği depresyon)",
            "Rhomboid Major & Minor (kürek kemiği iç/geri çekme)",
            "Levator Scapulae (boyun + omuz kaldırıcı)",
        ],
        "koken_yapismak": "C7-T12 omurlarından başlayıp skapulaya (kürek kemiği) ve klavikulaya yapışır.",
        "fonksiyon": "Kürek kemiğini stabilize eder, döndürür, aşağı/geri çeker. Postürün temelidir.",
        "lif_tipi": "Alt trapezius: yavaş kasılan (postür), üst trap: hızlı kasılan (güç).",
        "en_iyi_egzersizler": [
            "Face Pull (arka delt + orta trap + rotator cuff)",
            "Barbell/DB Shrug (üst trap izolasyon)",
            "Bent-Over Rear Delt Fly (orta trap + arka delt)",
            "Seated Cable Row with scapular squeeze",
            "Band Pull-Apart (üst sırt aktivasyonu)",
            "Chest-Supported Row (izole sırt çalışma)",
        ],
        "bilgi": (
            "Trapezius 3 farklı yönde çalışan liflere sahip. Üst trap çoğu kişide aşırı gelişmiş, "
            "alt trap zayıf kalmaktadır — bu durum omuz ağrısına ve kötü postüre yol açar. "
            "Rhomboidler omuz sağlığı için kritik ama genellikle ihmal edilir. "
            "Face pull, hem postür hem de rotator cuff için en önemli egzersizdir."
        ),
        "hata": (
            "1) Sadece shrug yapmak — üst trap kasılır ama orta/alt ihmal edilir. "
            "2) Row hareketlerinde kürek kemiğini sıkıştırmamak. "
            "3) Omuz arkasını hiç çalıştırmamak."
        ),
        "prehab": "Face pull (haftada 2-3 × 15-20), band pull-apart zorunludur",
    },
    {
        "grup": "Deltoid (Omuz)",
        "ikon": "bi-arrow-up-circle-fill",
        "renk": "#9b59b6",
        "alt_kaslar": [
            "Anterior Deltoid — Ön Baş (fleksiyon, iç rotasyon)",
            "Medial Deltoid — Orta Baş (abduction — en görünür bölüm)",
            "Posterior Deltoid — Arka Baş (extension, dış rotasyon)",
        ],
        "koken_yapismak": "Klavikulanın 1/3 dış kısmı, akromiyon ve skapuladan başlayıp humerus deltoid tüberkülüne yapışır.",
        "fonksiyon": "Kolun tüm yönlerde hareketi: ön baş öne kaldırır, orta baş yana kaldırır, arka baş geriye çeker.",
        "lif_tipi": "Orta baş: hızlı kasılan (yüksek tekrar için iyi yanıt); arka baş: yavaş (dayanıklılık).",
        "en_iyi_egzersizler": [
            "Barbell/DB Overhead Press (anterior + medial primer)",
            "Arnold Press (tüm deltoid başları)",
            "Lateral Raise — DB/Cable (medial izolasyon)",
            "Cable Lateral Raise (sabit gerilim avantajı)",
            "Rear Delt Fly — DB/Cable/Machine (posterior izolasyon)",
            "Face Pull (posterior + rotator cuff)",
            "Upright Row (medial + üst trap — dikkatli!)",
            "Front Raise (anterior — genellikle fazla çalışır)",
        ],
        "bilgi": (
            "Anterior deltoid bench press ve overhead press'te sekonder olarak yoğun çalışır. "
            "Bu nedenle çoğu kişide ön baş aşırı, arka baş yetersiz gelişmiştir. "
            "Geniş ve yuvarlak omuz görünümü için medial deltoid önceliklidir. "
            "Lateral raise'de ağırlık değil ROM ve kontrol önceliklidir. "
            "Arka deltoid için prone (yüzüstü) egzersizler ve cable en etkilidir."
        ),
        "hata": (
            "1) Arka deltoidi ihmal etmek — yaralanma ve kötü postür riski. "
            "2) Lateral raise'de çok ağır kullanmak (trapezius devralır). "
            "3) Upright row'da dirseği omuz üstüne çıkarmak (impingement riski)."
        ),
        "prehab": "External rotation egzersizleri (90-90 ER), rotator cuff güçlendirme, face pull",
    },
    {
        "grup": "Rotator Cuff (Döndürücü Manşet)",
        "ikon": "bi-arrow-clockwise",
        "renk": "#e67e22",
        "alt_kaslar": [
            "Supraspinatus (başlangıç kaldırma 0-30°, stabilizatör)",
            "Infraspinatus (dış rotasyon — güçlü)",
            "Teres Minor (dış rotasyon — yardımcı)",
            "Subscapularis (iç rotasyon — en güçlü rotator cuff kası)",
        ],
        "koken_yapismak": "Skapuladan humerus başına yapışır — omuz kapsülünü dört yandan sarar.",
        "fonksiyon": "Glenohumeral eklemde (omuz) başı stabilize eder, iç ve dış rotasyon.",
        "lif_tipi": "Ağırlıklı Tip I (yavaş kasılan, dayanıklılık) — yüksek tekrar, hafif ağırlık.",
        "en_iyi_egzersizler": [
            "External Rotation (90-90 pozisyonunda — infraspinatus/teres minor)",
            "Internal Rotation (subscapularis)",
            "Face Pull (infraspinatus + teres minor + arka delt)",
            "Band Pull-Apart (posterior rotator cuff)",
            "Side-Lying External Rotation",
            "Prone Y-T-W (tüm rotator cuff + trapezius)",
        ],
        "bilgi": (
            "Rotator cuff spor dünyasındaki en sık yaralanan kas grubu. "
            "Özellikle bench press ağır yapan kişilerde internal rotators dominant olur ve "
            "external rotators zayıf kalır — bu omuz impingement ve yırtılmaya davetiye çıkarır. "
            "Prehab egzersizlerini antrenman programına haftada 2-3 × 15-20 tekrar ekle."
        ),
        "hata": (
            "1) Hiç çalıştırmamak — en yaygın hata. "
            "2) Ağır ağırlık kullanmak — bu küçük kaslar için hafif ağırlık yeterli. "
            "3) Sadece compound hareketlere güvenmek."
        ),
        "prehab": "Bu KAS GRUBUNUN TAMAMI PREHAB'TIR — hafif bantlarla haftada 3× yapılmalı",
    },
    {
        "grup": "Biceps Brachii & Brachialis (Kol Ön)",
        "ikon": "bi-hand-thumbs-up-fill",
        "renk": "#c0392b",
        "alt_kaslar": [
            "Biceps Brachii — Uzun Baş (kıl yanı, 'kabarıklık')",
            "Biceps Brachii — Kısa Baş (gövde yanı, 'genişlik')",
            "Brachialis (daha derin, kol kalınlığı — görsel açıdan kritik)",
            "Brachioradialis (ön kol üst bölümü)",
        ],
        "koken_yapismak": "Supraglenoid tüberkülden (uzun baş) ve coracoid'den (kısa baş) başlar, radyusun tuberositas'ına yapışır.",
        "fonksiyon": "Dirsek fleksiyonu + ön kol supinasyonu (avuç yukarı dönme). Uzun baş daha fazla kabarıklık, kısa baş genişlik verir.",
        "lif_tipi": "Hızlı kasılan (tip II) ağırlıklı — orta-düşük tekrar aralığı.",
        "en_iyi_egzersizler": [
            "Barbell Curl (en etkili — maksimum yük kapasitesi)",
            "Dumbbell Curl (supinasyon ile brachii tam aktivasyon)",
            "Hammer Curl (brachialis öncelikli — kol kalınlığı)",
            "Concentration Curl (peak contraction — kısa baş)",
            "Preacher Curl (uzun baş gerimi izolasyonu)",
            "Incline Dumbbell Curl (uzun baş tam uzama gerilimi)",
            "Cable Curl (sabit gerilim — TUT avantajı)",
            "Chin-up (bileşik biceps aktivasyonu)",
        ],
        "bilgi": (
            "Biceps 2 başlı kas — kıl (uzun baş) ve gövde yanı (kısa baş). "
            "Supinasyon sırasında biceps en iyi aktive olur — dumbbell curlda avucu döndür. "
            "Brachialis bicepsin altında oturur; geliştikçe bicepsi yukarı iter ve daha yüksek peak yaratır. "
            "Hammer curl brachialis'i doğrudan hedef alır. "
            "Uzun baş: incline curl veya high cable curl (tam uzama pozisyonu). "
            "Kısa baş: preacher curl veya concentration curl (kısalmış pozisyon)."
        ),
        "hata": (
            "1) Sallanarak kaldırmak (momentum) — brachii'nin kasılma kapasitesi azalır. "
            "2) Sadece supinated curl yapmak — brachialis'i atlama. "
            "3) Tam ROM yapmamak — dirseği tam açıp tam bükmek şart."
        ),
        "prehab": "Wrist flexion/extension egzersizleri (önkol sağlığı için)",
    },
    {
        "grup": "Triceps Brachii (Kol Arka)",
        "ikon": "bi-chevron-bar-right",
        "renk": "#8e44ad",
        "alt_kaslar": [
            "Triceps — Uzun Baş (kolun %60'ı — overhead pozisyonda tam aktif)",
            "Triceps — Lateral Baş (dış görünüm — horseshoe şekli)",
            "Triceps — Medial Baş (derin, tüm hareketlerde aktif)",
        ],
        "koken_yapismak": "Uzun baş infraglenoid tüberküle, lateral ve medial başlar humerus arka yüzüne yapışır; ulna'nın olekranonuna oturur.",
        "fonksiyon": "Dirsek ekstansiyonu (kol açma). Uzun baş ayrıca omuz ekstansiyonuna katkıda bulunur.",
        "lif_tipi": "Hızlı kasılan (tip II) ağırlıklı — orta ağırlık, 8-15 tekrar.",
        "en_iyi_egzersizler": [
            "Close-Grip Bench Press (en ağır yükleme — tüm başlar)",
            "Skull Crusher / EZ-Bar Extension (uzun + lateral baş)",
            "Overhead Tricep Extension — DB/Cable (uzun baş öncelikli)",
            "Tricep Pushdown — Rope/V-Bar (lateral baş, peak kontraksiyon)",
            "Cable Overhead Extension (uzun baş tam uzama)",
            "Diamond Push-up (vücut ağırlığıyla yükleme)",
            "Tricep Dip (ağır yükleme — tüm başlar)",
        ],
        "bilgi": (
            "Triceps kolun %60-70'ini oluşturur — büyük kol için bicepsten çok tricepse odaklan. "
            "Uzun baş sadece overhead pozisyonda (kol yukarıda) tam olarak uzar ve aktive olur. "
            "Bu nedenle pushdown tek başına yeterli değil — overhead extension zorunludur. "
            "Lateral baş horseshoe görünümü için pushdown ve close-grip bench. "
            "Haftada 12-18 toplam set, 2 frekans."
        ),
        "hata": (
            "1) Sadece pushdown yapmak — uzun baş aktivasyonu minimum. "
            "2) Skull crusher'da dirseğin dışa açılması — lateral gerilim, yaralanma riski. "
            "3) Overhead extension'da ağır gitmek — formu koru."
        ),
        "prehab": "Elbow flexion/extension mobility, wrist mobilizasyonu",
    },
    {
        "grup": "Quadriceps (Bacak Ön)",
        "ikon": "bi-lightning-charge-fill",
        "renk": "#f39c12",
        "alt_kaslar": [
            "Rectus Femoris (diz açma + kalça fleksiyonu — çift eklemli)",
            "Vastus Lateralis (dış quad — en büyük)",
            "Vastus Medialis / VMO (iç quad — diz stabilitesi, 'teardrop')",
            "Vastus Intermedius (derin — diz direkt açma)",
        ],
        "koken_yapismak": "İliak kanattan ve femur üst bölümünden başlar, patella ve tibia tüberkülüne yapışır.",
        "fonksiyon": "Diz ekstansiyonu (açılması) ve rectus femoris için kalça fleksiyonu.",
        "lif_tipi": "Hızlı kasılan ağırlıklı (tip II) — güç ve hipertrofi için 6-12 tekrar.",
        "en_iyi_egzersizler": [
            "Barbell Back Squat (en etkili kompound hareket)",
            "Front Squat (quad vurgulu, daha dikey gövde)",
            "Hack Squat Makinesi (quad izolasyon)",
            "Leg Press (45°, dar+yüksek pozisyon — quad)",
            "Leg Extension Makinesi (saf quad izolasyon)",
            "Bulgarian Split Squat (tek taraflı, derin ROM)",
            "Goblet Squat (başlangıç + egzersiz kalitesi)",
            "Lunge — İleri/Geri/Yürüyen (fonksiyonel)",
        ],
        "bilgi": (
            "Quadriceps 4 başlı kastır — her birinin farklı egzersiz vurgusu var. "
            "Rectus femoris sadece squat dışında front squat'ta tam aktive olur (çift eklemli). "
            "VMO (teardrop) için son 30° diz açılımı kritik — leg extension sonunda sık. "
            "Derin squat (ATG — ass to grass) daha fazla ROM = daha fazla hipertrofi. "
            "Vastus lateralis için geniş duruş, VMO için dar duruş."
        ),
        "hata": (
            "1) Diz içe dönmesi (valgus) — quad aktivasyonu azalır, ACL stres artar. "
            "2) Squat'ta öne eğilmek — quad yerine arka zincir çalışır. "
            "3) Tam derinliğe inmemek — hipertrofi potansiyeli azalır."
        ),
        "prehab": "VMO aktivasyon egzersizleri, hip flexor stretching, IT band mobilizasyon",
    },
    {
        "grup": "Hamstrings & Gluteus (Arka Zincir)",
        "ikon": "bi-chevron-double-down",
        "renk": "#27ae60",
        "alt_kaslar": [
            "Biceps Femoris — Uzun Baş (diz bükme + dış rotasyon)",
            "Biceps Femoris — Kısa Baş (sadece diz bükme)",
            "Semitendinosus (diz bükme + iç rotasyon)",
            "Semimembranosus (diz bükme + iç rotasyon — daha derin)",
            "Gluteus Maximus (kalça ekstansiyonu — vücudun en güçlü kası)",
            "Gluteus Medius (kalça abduksiyonu + pelvik stabilite)",
            "Gluteus Minimus (kalça abduksiyonu + stabilizatör)",
        ],
        "koken_yapismak": "Hamstrings ischial tuberosityden (oturma kemiği), glute'lar iliak kemikten başlar; tibia ve fibulanın proksimaline yapışır.",
        "fonksiyon": "Hamstrings: diz fleksiyonu + kalça ekstansiyonu. Gluteus maximus: en güçlü kalça extensoru. G. medius: tek ayak duruşunda pelvik stabilite.",
        "lif_tipi": "Hamstrings: karma; Gluteus: Tip I ağırlıklı (yüksek TUT ve hacim iyi yanıt verir).",
        "en_iyi_egzersizler": [
            "Romanian Deadlift — RDL (hamstring uzama gerilimi — en etkili)",
            "Hip Thrust (gluteus maximus — en yüksek EMG aktivasyonu)",
            "Nordic Hamstring Curl (hamstring eksantrik — yaralanma önleyici)",
            "Lying Leg Curl (hamstring izolasyon — diz fleksiyonu)",
            "Seated Leg Curl (biceps femoris uzun baş vurgusu)",
            "Bulgarian Split Squat (tek taraflı — hamstring + glute)",
            "Sumo Deadlift (gluteus vurgulu deadlift)",
            "Glute Bridge / Hip Thrust (glute aktivasyonu)",
            "Cable Pull-Through (kalça menteşesi öğrenme)",
            "Good Morning (hamstring + erektör)",
        ],
        "bilgi": (
            "En çok ihmal edilen kas grubu. Hamstring güçsüzlüğü ACL yırtılmalarının %70'inden sorumludur. "
            "Hamstrings çift eklemlidir: hem kalçada uzar hem dizde büzülür. "
            "RDL: kalça menteşesi ile, bel düz, hamstrings uzayarak çalışır. "
            "Hip thrust: 1996'da Bret Contreras tarafından araştırılmış — gluteus maximus için en yüksek EMG. "
            "Nordic curl: %51 hamstring yaralanma riski azaltır (çalışmalar destekliyor). "
            "G. medius zayıflığı: Trendelenburg yürüyüşü ve diz problemleri."
        ),
        "hata": (
            "1) RDL'de beli bükmek — nötr bel + kalçadan menteşe. "
            "2) Hip thrust'ta beli fazla hiper-ekstansiyona sokmak. "
            "3) Leg curl'ü tek hamstring egzersizi saymak."
        ),
        "prehab": "Nordic curl, Copenhagen plank (adductor sağlığı), glute activation (clamshell)",
    },
    {
        "grup": "Gastrocnemius & Soleus (Baldır)",
        "ikon": "bi-arrow-down-circle-fill",
        "renk": "#16a085",
        "alt_kaslar": [
            "Gastrocnemius — Medial Baş (daha büyük, görünür 'elma')",
            "Gastrocnemius — Lateral Baş (dış yüz)",
            "Soleus (gastrocnemius'un altı — diz bükülüyken tam aktif)",
        ],
        "koken_yapismak": "Gastrocnemius femur kondillerinden, soleus tibia/fibuladan başlar; ikisi Achilles tendonu ile calcaneus'a (topuk) bağlanır.",
        "fonksiyon": "Ayak bileği plantar fleksiyon (ayak ucu kaldırma). Gastrocnemius ayrıca diz fleksiyonuna katkıda bulunur.",
        "lif_tipi": "Soleus: Tip I (yavaş — yüksek tekrar/TUT iyi). Gastrocnemius: Tip II (güç için düşük tekrar da yanıt verir).",
        "en_iyi_egzersizler": [
            "Standing Calf Raise (diz düz — gastrocnemius vurgulu)",
            "Seated Calf Raise (diz bükülü — soleus izolasyonu)",
            "Leg Press Calf Raise (ağır yükleme)",
            "Donkey Calf Raise (gövde eğik — tam ROM)",
            "Single-Leg Calf Raise (tek bacak — dengesizlik artı)",
            "Jump Rope (fonksiyonel + kardiyovasküler)",
        ],
        "bilgi": (
            "Baldır en dirençli kas gruplarından biri — yüksek tekrar toleransı var (günde binlerce adım). "
            "Soleus'u hedeflemek için diz bükülü pozisyon (seated calf raise) şart. "
            "Tam ROM kritik: topuk zemine değmeli, maksimum stretche ulaşmalı. "
            "Haftada 16-22 set, 3 frekans, 10-20+ tekrar."
        ),
        "hata": (
            "1) Kısa ROM (sadece half calf raise) — gastrocnemius tam aktive olmaz. "
            "2) Sadece standing raise — soleus ihmal edilir. "
            "3) Çok hızlı tempo — bouncing (zıplama momentum), kasılma yok."
        ),
        "prehab": "Soleus stretch, Achilles tendon esnekliği, plantar fascia masajı",
    },
    {
        "grup": "Core — Abdominals & Stabilizatörler",
        "ikon": "bi-circle-fill",
        "renk": "#1abc9c",
        "alt_kaslar": [
            "Rectus Abdominis (6-pack kası — gövde fleksiyonu)",
            "External Oblique (dışa eğilme + rotasyon)",
            "Internal Oblique (içten rotasyon yardımcısı)",
            "Transversus Abdominis (derin — intra-abdominal basınç, 'doğal korse')",
            "Multifidus (omurga stabilizatörü — derin sırt)",
            "Psoas Major / Iliacus (kalça fleksörü — core + bel)",
            "Quadratus Lumborum (lateral bel stabilizatörü)",
        ],
        "koken_yapismak": "Pelvis + kostalar arası bağlantı. Transversus: 'korse gibi' tüm gövdeyi sarar.",
        "fonksiyon": "Omurga stabilitesi ve koruma, güç transferi, nefes alma, intra-abdominal basınç yönetimi.",
        "lif_tipi": "Transversus ve multifidus: Tip I (sürekli aktif, postür kası). Rectus: Tip II (güç için).",
        "en_iyi_egzersizler": [
            "Plank (transversus + multifidus aktivasyonu)",
            "Side Plank (QL + oblique + hip abductor)",
            "Ab Wheel Rollout (rectus + lat + serratus)",
            "Cable Crunch (yüklenmiş rectus — en etkili crunch)",
            "Hanging Knee/Leg Raise (alt rectus + hip flexor)",
            "Russian Twist (oblique rotasyon)",
            "Pallof Press (anti-rotasyon — fonksiyonel)",
            "Dead Bug (transversus + kalça koordinasyonu)",
            "Deadlift + Squat (core sekonder olarak yoğun)",
        ],
        "bilgi": (
            "6-pack görmek kas büyüklüğüyle değil vücut yağıyla ilgilidir: erkek <%12, kadın <%20. "
            "Core sadece estetik değil — tüm sporların güç transferini sağlar. "
            "Transversus abdominis: doğru nefes ve 'bracing' (korse tekniği) ile aktive edilir. "
            "Plank, crunch'tan 3 kat daha etkili core aktivasyonu sağlar."
        ),
        "hata": (
            "1) Sadece crunch yapmak — rectus'u izole eder, fonksiyonel core geliştirmez. "
            "2) Hip flexor egzersizini core sanmak (ayak tutmalı crunch). "
            "3) Core'u sadece antrenman sonunda yapmak — her ağır harekette zaten çalışır."
        ),
        "prehab": "Diaphragmatic breathing, bird-dog, dead bug — temel omurga sağlığı",
    },
    {
        "grup": "Erector Spinae (Alt Sırt / Bel)",
        "ikon": "bi-align-center",
        "renk": "#e67e22",
        "alt_kaslar": [
            "Iliocostalis (en lateral — lomber bölge)",
            "Longissimus (orta — T12'den kafaya kadar)",
            "Spinalis (en medial — omurga üzeri)",
            "Multifidus (derin segmental stabilizatör)",
        ],
        "koken_yapismak": "Sakrum ve iliak kemikten başlayıp omurlar ve kostalar boyunca yukarı uzanır.",
        "fonksiyon": "Gövde ekstansiyonu (dik durma), omurga stabilitesi, rotasyon, lateral fleksiyon.",
        "lif_tipi": "Tip I ağırlıklı (postür, yüksek dayanıklılık) + bazı Tip II lifleri.",
        "en_iyi_egzersizler": [
            "Deadlift (en etkili — ağır yükleme)",
            "Romanian Deadlift (izometrik erektör yükleme)",
            "Good Morning (erektör + hamstring)",
            "Back Extension / Hyperextension (izolasyon)",
            "Barbell Row (sekonder aktivasyon)",
            "Bird-Dog (multifidus stabilizasyon)",
        ],
        "bilgi": (
            "Alt sırt dünyada en sık ağrı yaşanan bölge. Güçlü erektör spina bel sağlığının temelidir. "
            "Deadlift'te omurga nötral tutulursa erektör güçlenir ve korunur. "
            "Aşırı zorlanma ve kötü form yaralanmaya yol açar — form > ağırlık."
        ),
        "hata": (
            "1) Beli bükmek (flexion under load) — disk hernisi riski. "
            "2) Hiperextension'da aşırı germe — lomber impingement. "
            "3) Deadlift'te çekim sırasında beli yuvarlamamak için core sıkıştırmayı unutmak."
        ),
        "prehab": "Cat-cow, child's pose, McGill Big 3 (curl-up, side plank, bird-dog)",
    },
    {
        "grup": "Hip Flexors & Adductors (Kalça Ön/İç)",
        "ikon": "bi-symmetry-horizontal",
        "renk": "#d35400",
        "alt_kaslar": [
            "Iliopsoas — Psoas Major + Iliacus (derin kalça fleksörü)",
            "Rectus Femoris (quad + kalça fleksörü)",
            "Tensor Fasciae Latae — TFL (IT band ile bağlantılı)",
            "Adductor Magnus (en büyük iç uyluk kası)",
            "Adductor Longus/Brevis (iç uyluk medial kısım)",
            "Gracilis (ince — adductor + diz fleksörü)",
            "Pectineus (üst iç uyluk)",
        ],
        "koken_yapismak": "Pelvis ve femurdan başlar, femur medial kondil ve tibia'ya yapışır.",
        "fonksiyon": "Kalça fleksiyonu (bacağı öne kaldırma), adduction (içe çekme), pelvik tilt kontrolü.",
        "lif_tipi": "Karma — psoas Tip I, adduktorlar karma.",
        "en_iyi_egzersizler": [
            "Copenhagen Plank (adductor — en etkili)",
            "Sumo Squat / Sumo Deadlift (adductor vurgulu)",
            "Cable Hip Adduction (izolasyon)",
            "Lying Hip Adduction (makinede)",
            "Lunge (hip flexor gerimi + aktivasyon)",
            "Dragon Flag (psoas + rectus — ileri seviye)",
        ],
        "bilgi": (
            "Hip flexorlar masa başı çalışanların en sıkışık kas grubu. "
            "Kısalmış psoas: bel ağrısı ve anterior pelvik tilt'e yol açar. "
            "Adduktorlar kasık incinmelerinin başlıca nedeni — futbol, sprint, manevra sporlarda kritik. "
            "Copenhagen plank, hamstring nordic curl kadar etkili adductor güçlendiricisidir."
        ),
        "hata": (
            "1) Hiç esnetmemek (masa başı çalışanlar için felaket). "
            "2) Adduktorları tamamen ihmal etmek. "
            "3) Lunge'da gövdeyi fazla öne eğmek."
        ),
        "prehab": "Hip flexor lunge stretch, pigeon pose, Copenhagen plank, 90-90 hip rotation",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
#  EGZERSİZ ANSİKLOPEDİSİ  (Master Seviye)
# ══════════════════════════════════════════════════════════════════════════════

EGZERSIZ_ANSIKLOPEDISI = {
    # ── GÖĞÜS ────────────────────────────────────────────────────────────────
    "Barbell Bench Press": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrow-down-up",
        "ekipman": "Barbell + Bench",
        "birincil": ["Pectoralis Major (orta)"],
        "ikincil": ["Ön Deltoid", "Triceps Brachii"],
        "mekanik": "Bileşik — kapalı kinetik zincir",
        "teknik": "Kürek kemiklerini çek ve sabitle. Sırtını hafif ark yap (köprü). Barı göğsüne değdir, dirsekler 45-75° açıda. Alt kısmında tutunmak için gövdende sıkıştır.",
        "hatalar": "Omuzları öne almak, dirseği 90°'ye açmak (omuz impingement), barı göğse değdirmemek.",
        "degiskenler": ["Incline Bench Press", "Decline Bench Press", "Close-Grip BP", "Paused BP"],
        "gif_anahtar": "barbell bench press",
    },
    "Incline Barbell Press": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrow-up-right",
        "ekipman": "Barbell + İncline Bench (30-45°)",
        "birincil": ["Pectoralis Major — Klaviküler Baş (Üst)"],
        "ikincil": ["Ön Deltoid", "Triceps"],
        "mekanik": "Bileşik",
        "teknik": "30-45° açı ideal. 60°+ üstü omuz hakimiyetine geçer. Kürek kemiklerini sıkıştır.",
        "hatalar": "Açıyı çok yüksek ayarlamak, kürek serbest bırakmak.",
        "degiskenler": ["Incline DB Press", "Low-to-High Cable Fly"],
        "gif_anahtar": "incline bench press",
    },
    "Incline Dumbbell Press": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrow-up-right",
        "ekipman": "Dumbbell + İncline Bench",
        "birincil": ["Üst Pectoralis Major"],
        "ikincil": ["Ön Deltoid", "Triceps"],
        "mekanik": "Bileşik",
        "teknik": "Dumbbell'ları göğsün üst kısmına doğru bas. Tam ROM ile üstte bitiştir.",
        "hatalar": "Çok geniş dirsek açısı, ağırlıkları yeterince indirmemek.",
        "degiskenler": ["Incline BB Press", "Cable Fly (high-to-low)"],
        "gif_anahtar": "incline dumbbell press",
    },
    "Dumbbell Bench Press": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrow-down-up",
        "ekipman": "Dumbbell + Bench",
        "birincil": ["Pectoralis Major"],
        "ikincil": ["Ön Deltoid", "Triceps"],
        "mekanik": "Bileşik",
        "teknik": "Barbell'a göre daha fazla ROM. Üstte nötrden pronasyona dön. Göğsü tam sıkıştır.",
        "hatalar": "Ağırlıkları yeterince indirmemek, gövde stabilizasyonu eksikliği.",
        "degiskenler": ["Barbell Bench Press", "DB Fly"],
        "gif_anahtar": "dumbbell bench press",
    },
    "Dumbbell Fly": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrows-expand",
        "ekipman": "Dumbbell + Bench",
        "birincil": ["Pectoralis Major (strech pozisyonu)"],
        "ikincil": ["Ön Deltoid (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Hafif dirsek bükümü (10-20°) sabit tut. Göğsün üzerinde çay kasesi taşır gibi. Aşağıda stretchi hisset.",
        "hatalar": "Ağır gitmek (tricep devralır), dirseği çok bükmek (press olur).",
        "degiskenler": ["Cable Fly", "Incline DB Fly", "Pec Deck"],
        "gif_anahtar": "dumbbell fly",
    },
    "Cable Fly (Mid)": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrows-expand",
        "ekipman": "Kablo Makine",
        "birincil": ["Pectoralis Major (sabit gerilim)"],
        "ikincil": ["Ön Deltoid"],
        "mekanik": "İzolasyon",
        "teknik": "Kolları göğüs hizasında kapıdan girip birleştir. TUT — sabit gerilim avantajı. Crossover'da kolları çapraz geçir.",
        "hatalar": "Dirsekleri fazla bükmek, gövde sallanması.",
        "degiskenler": ["High Cable Fly (alt göğüs)", "Low Cable Fly (üst göğüs)", "Pec Deck"],
        "gif_anahtar": "cable fly",
    },
    "Pec Deck Machine": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrows-expand",
        "ekipman": "Pec Deck Makinesi",
        "birincil": ["Pectoralis Major (izolasyon)"],
        "ikincil": ["Ön Deltoid (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Sırtı mindere tam daya. Kolları kanatlar gibi yay. Strech pozisyonunda kontrollü dur.",
        "hatalar": "Çok ağır gitmek (shoulder impingement), tam strech yapmamak.",
        "degiskenler": ["Cable Fly", "DB Fly"],
        "gif_anahtar": "pec deck",
    },
    "Decline Bench Press": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-arrow-down-left",
        "ekipman": "Barbell + Decline Bench (-15° ile -30°)",
        "birincil": ["Pectoralis Major — Sternal Alt"],
        "ikincil": ["Triceps", "Ön Deltoid (minimal)"],
        "mekanik": "Bileşik",
        "teknik": "Alt göğüsü hedefler. Barbell'ı alt göğse göster. Ön deltoid stresi düşer.",
        "hatalar": "Çok fazla decline açısı, omuzları serbest bırakmak.",
        "degiskenler": ["Decline DB Press", "Dip"],
        "gif_anahtar": "decline bench press",
    },
    "Push-up": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-person-arms-up",
        "ekipman": "Vücut Ağırlığı",
        "birincil": ["Pectoralis Major"],
        "ikincil": ["Triceps", "Ön Deltoid", "Core"],
        "mekanik": "Bileşik",
        "teknik": "Vücut düz bir tahta gibi. Dirsekler 45° açı. Tam aşağı in, tam yukarı çık. Core sıkı.",
        "hatalar": "Kalça düşmesi (core zayıflığı), boynu öne uzatmak.",
        "degiskenler": ["Wide Push-up", "Diamond Push-up", "Archer Push-up", "Decline Push-up"],
        "gif_anahtar": "push up",
    },
    "Chest Dip": {
        "kategori": "Göğüs", "renk": "#e74c3c", "ikon": "bi-chevron-double-down",
        "ekipman": "Dip Bar",
        "birincil": ["Pectoralis Major (alt)"],
        "ikincil": ["Triceps", "Ön Deltoid"],
        "mekanik": "Bileşik",
        "teknik": "Gövdeyi öne eğ (~30°) — göğüs odaklı olur. Dik gövde = tricep dip. Tam aşağı in.",
        "hatalar": "Gövdeyi dik tutmak (tricep olur), omuzları öne almak.",
        "degiskenler": ["Weighted Dip", "Machine Dip", "Bench Dip"],
        "gif_anahtar": "chest dip",
    },

    # ── SIRTI ────────────────────────────────────────────────────────────────
    "Conventional Deadlift": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-bar-chart-fill",
        "ekipman": "Barbell",
        "birincil": ["Erector Spinae", "Gluteus Maximus", "Hamstrings"],
        "ikincil": ["Latissimus Dorsi", "Trapezius", "Quadriceps", "Core"],
        "mekanik": "Bileşik — full body",
        "teknik": "Bar bacaklara yakın. Kalçadan menteşe (hinge), bel nötr. Topukla itiş, kalça tam açılımı. Aktif lats ('çekiç kırmak gibi').",
        "hatalar": "Beli bükmek, barı bacaklardan uzaklaştırmak, omuzları öne almak.",
        "degiskenler": ["Sumo Deadlift", "Romanian Deadlift", "Trap Bar DL", "Deficit DL"],
        "gif_anahtar": "deadlift",
    },
    "Sumo Deadlift": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-bar-chart-fill",
        "ekipman": "Barbell",
        "birincil": ["Gluteus Maximus", "Adduktorlar"],
        "ikincil": ["Hamstrings", "Quadriceps", "Erektör"],
        "mekanik": "Bileşik",
        "teknik": "Geniş duruş, ayaklar dışa (~45°). Kısa ROM — kalça ve adductor vurgusu artar.",
        "hatalar": "Diz içe dönmesi, omuzlar barın önünde başlamak.",
        "degiskenler": ["Conventional DL", "Trap Bar DL"],
        "gif_anahtar": "sumo deadlift",
    },
    "Romanian Deadlift": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-down",
        "ekipman": "Barbell veya Dumbbell",
        "birincil": ["Hamstrings (uzama gerilimi)", "Erector Spinae"],
        "ikincil": ["Gluteus Maximus", "Trapezius"],
        "mekanik": "Bileşik",
        "teknik": "Diz hafifçe bükülü, sabit. Kalçadan menteşe ile barı bacak boyunca indir. Hamstrings'de derin strech hissi.",
        "hatalar": "Beli bükmek, dizi çok bükmek (squat olur), bar bacaklardan uzaklaşmak.",
        "degiskenler": ["Stiff-Leg DL", "Single-Leg RDL", "Good Morning"],
        "gif_anahtar": "romanian deadlift",
    },
    "Pull-up": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-up",
        "ekipman": "Pullup Bar",
        "birincil": ["Latissimus Dorsi"],
        "ikincil": ["Biceps Brachii", "Teres Major", "Orta Trapezius"],
        "mekanik": "Bileşik",
        "teknik": "Pronated (overhand) tutuş. Kürek kemiklerini deprese et (aşağı çek) önce. Göğsü bara götür. Tam uzanma ile in.",
        "hatalar": "Kıpırdama (kipping), kürek kemiği kullanmamak, yarım ROM.",
        "degiskenler": ["Chin-up (supinated)", "Wide-Grip", "Close-Grip", "Weighted Pull-up", "Neutral Grip"],
        "gif_anahtar": "pull-up",
    },
    "Chin-up": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-up",
        "ekipman": "Pullup Bar",
        "birincil": ["Latissimus Dorsi", "Biceps Brachii"],
        "ikincil": ["Teres Major", "Orta Trapezius"],
        "mekanik": "Bileşik",
        "teknik": "Supinated (underhand) tutuş — biceps aktivasyonu daha yüksek. Göğsü bara götür.",
        "hatalar": "Aynı pull-up hataları geçerli.",
        "degiskenler": ["Pull-up", "Neutral Grip Pull-up"],
        "gif_anahtar": "chin up",
    },
    "Lat Pulldown": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-down",
        "ekipman": "Kablo + Lat Pulldown Makinesi",
        "birincil": ["Latissimus Dorsi"],
        "ikincil": ["Biceps", "Teres Major", "Orta Trapezius"],
        "mekanik": "Bileşik",
        "teknik": "Hafif geriye eğil (10-15°). Barı göğsüne çek, dirsekleri cebe indir. Kürek kemiklerini sıkıştır.",
        "hatalar": "Aşırı geriye eğilmek (row olur), barı yüze çekmek, tam uzanmamak.",
        "degiskenler": ["Wide Grip", "Close Grip", "Reverse Grip", "V-Bar Pulldown", "Straight-Arm Pulldown"],
        "gif_anahtar": "lat pulldown",
    },
    "Straight-Arm Lat Pulldown": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-down",
        "ekipman": "Kablo",
        "birincil": ["Latissimus Dorsi (saf izolasyon)"],
        "ikincil": ["Teres Major", "Triceps uzun baş (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Kollar düz (hafif dirsek bükümü), kalçadan öne eğil, barı aşağı-geri çek. Lat'ları sıkıştır.",
        "hatalar": "Dirsekleri bükmek, gövdeyi sallamak.",
        "degiskenler": ["Lat Pulldown", "Pull-up"],
        "gif_anahtar": "straight arm pulldown",
    },
    "Bent-Over Barbell Row": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-left-right",
        "ekipman": "Barbell",
        "birincil": ["Latissimus Dorsi", "Rhomboids", "Orta Trapezius"],
        "ikincil": ["Biceps", "Erektör Spina", "Posterior Deltoid"],
        "mekanik": "Bileşik",
        "teknik": "45° gövde açısı. Barı göbeğe (lat vurgulu) veya sternum'a (orta sırt vurgulu) çek. Kürek kemiklerini sıkıştır.",
        "hatalar": "Beli bükmek, gövde çok dik/yatay, momentum.",
        "degiskenler": ["Pendlay Row (zemin), Yates Row (dik gövde)", "Dumbbell Row"],
        "gif_anahtar": "barbell row",
    },
    "Dumbbell Row (One-Arm)": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-left-right",
        "ekipman": "Dumbbell + Bench",
        "birincil": ["Latissimus Dorsi"],
        "ikincil": ["Rhomboids", "Biceps", "Posterior Deltoid"],
        "mekanik": "Bileşik (tek taraflı)",
        "teknik": "Dümbell'ı kalça cebine çek. Dirsek gövde boyunca. Kürek kemiği tam retraksiyon.",
        "hatalar": "Rotasyon (gövde dönmesi), dirsek çok geniş açıda.",
        "degiskenler": ["Chest-Supported Row", "Meadows Row", "Cable Row"],
        "gif_anahtar": "dumbbell row",
    },
    "Seated Cable Row": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-left-right",
        "ekipman": "Kablo + Row İstasyonu",
        "birincil": ["Orta Trapezius", "Rhomboids", "Latissimus Dorsi"],
        "ikincil": ["Biceps", "Posterior Deltoid"],
        "mekanik": "Bileşik",
        "teknik": "Hafif öne eğil (strech), sonra dik otur ve çek. Son pozisyonda kürek kemiklerini 1-2 sn sıkıştır.",
        "hatalar": "Gövdeyi çok geri sallamak (bel yük alır), kürek sıkıştırmamak.",
        "degiskenler": ["V-Bar Row", "Wide Grip Row", "Single-Arm Cable Row"],
        "gif_anahtar": "cable row",
    },
    "T-Bar Row": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-left-right",
        "ekipman": "T-Bar Makinesi",
        "birincil": ["Orta Sırt — Rhomboids + Trapezius"],
        "ikincil": ["Latissimus Dorsi", "Biceps"],
        "mekanik": "Bileşik",
        "teknik": "Göğsü desteğe koy (chest-supported) veya serbest duruş. Barı sternum'a çek. Kürek sıkıştır.",
        "hatalar": "Aşırı ağırlık (momentum), gövde dönmesi.",
        "degiskenler": ["Chest-Supported T-Bar", "Landmine Row"],
        "gif_anahtar": "t-bar row",
    },
    "Face Pull": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-left-right",
        "ekipman": "Kablo + Rope",
        "birincil": ["Posterior Deltoid", "Orta Trapezius", "Rotator Cuff"],
        "ikincil": ["Rhomboids", "Biceps (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Rope'u yüz hizasına çek, dirsekler omuz üstü. Son pozisyonda dışa döndür (external rotation). Hafif ağırlık, yüksek tekrar.",
        "hatalar": "Ağır gitmek, external rotation yapmamak, dirseği düşürmek.",
        "degiskenler": ["Band Face Pull", "Prone Y-T-W"],
        "gif_anahtar": "face pull",
    },
    "Barbell Shrug": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-up",
        "ekipman": "Barbell",
        "birincil": ["Trapezius Üst Lif"],
        "ikincil": ["Levator Scapulae"],
        "mekanik": "İzolasyon",
        "teknik": "Omuzları direkt yukarı kaldır (döndürme yok). Üstte 1 sn bekle. Kontrollü in.",
        "hatalar": "Omuzları döndürmek ('rolling'), boynu öne uzatmak.",
        "degiskenler": ["DB Shrug", "Cable Shrug", "Smith Machine Shrug"],
        "gif_anahtar": "barbell shrug",
    },
    "Back Extension": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-clockwise",
        "ekipman": "Hyperextension Bench",
        "birincil": ["Erector Spinae"],
        "ikincil": ["Gluteus Maximus", "Hamstrings"],
        "mekanik": "İzolasyon",
        "teknik": "Kalça minderde. Beli nötrden tam uzanmaya getir. Ağırlıklı versiyonda göğse plaka tut.",
        "hatalar": "Fazla hiperekstansiyon (lomber baskı), boyun hizası bozulması.",
        "degiskenler": ["Reverse Hyperextension", "Good Morning", "45° Back Extension"],
        "gif_anahtar": "back extension",
    },
    "Good Morning": {
        "kategori": "Sırt", "renk": "#3498db", "ikon": "bi-arrow-clockwise",
        "ekipman": "Barbell",
        "birincil": ["Erector Spinae", "Hamstrings"],
        "ikincil": ["Gluteus Maximus"],
        "mekanik": "Bileşik",
        "teknik": "Bar boyunda, omuzda (squat pozisyonu). Kalçadan menteşe ile gövdeyi eğ. Bel nötr.",
        "hatalar": "Dizi bükmek, beli yuvarlamamak veya aşırı eğmek.",
        "degiskenler": ["Romanian Deadlift", "Back Extension"],
        "gif_anahtar": "good morning exercise",
    },

    # ── OMUZ ─────────────────────────────────────────────────────────────────
    "Barbell Overhead Press": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrow-up",
        "ekipman": "Barbell",
        "birincil": ["Anterior Deltoid", "Medial Deltoid"],
        "ikincil": ["Triceps", "Trapezius Üst", "Core (stabilizatör)"],
        "mekanik": "Bileşik",
        "teknik": "Barı çeneden hafif önden başlat. Baş barın yolundan çekil. Üstte tam uzanma. Core sıkı.",
        "hatalar": "Beli fazla hiper-ekstansiyona sokmak, barı başın arkasından itmek (servikal stres).",
        "degiskenler": ["Seated BB Press", "Push Press", "Z-Press", "Log Press"],
        "gif_anahtar": "overhead press",
    },
    "Dumbbell Shoulder Press": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrow-up",
        "ekipman": "Dumbbell",
        "birincil": ["Anterior Deltoid", "Medial Deltoid"],
        "ikincil": ["Triceps"],
        "mekanik": "Bileşik",
        "teknik": "Başlangıç: dirsekler 90°, avuçlar öne. Üstte tam uzanma. Her iki taraf bağımsız çalışır.",
        "hatalar": "Ağırlıkları birbiriyle çarpmak, tam uzanmamak.",
        "degiskenler": ["Arnold Press", "Seated DB Press", "Single-Arm Press"],
        "gif_anahtar": "dumbbell shoulder press",
    },
    "Arnold Press": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrow-clockwise",
        "ekipman": "Dumbbell",
        "birincil": ["Deltoid (tüm 3 baş)"],
        "ikincil": ["Triceps"],
        "mekanik": "Bileşik",
        "teknik": "Başta avuçlar içe, iter. Döndürerek avuçları dışa çevir (supination → pronation). En fazla deltoid aktivasyonu.",
        "hatalar": "Dönüşü unutmak (normal DB press olur).",
        "degiskenler": ["DB Shoulder Press", "Overhead Press"],
        "gif_anahtar": "arnold press",
    },
    "Lateral Raise": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrows-expand",
        "ekipman": "Dumbbell",
        "birincil": ["Medial Deltoid (izolasyon)"],
        "ikincil": ["Supraspinatus (yardımcı)"],
        "mekanik": "İzolasyon",
        "teknik": "Hafif öne eğil (10°). Kolları yanlara kaldır, dirsekler hafif bükülü. Başparmak biraz aşağı (pinky up değil — supraspinatus sıkışması önler).",
        "hatalar": "Çok ağır gitmek (trapezius devralır), tam range yapmamak, momentum.",
        "degiskenler": ["Cable Lateral Raise (sabit gerilim)", "Machine Lateral Raise", "Leaning Lateral Raise"],
        "gif_anahtar": "lateral raise",
    },
    "Cable Lateral Raise": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrows-expand",
        "ekipman": "Kablo",
        "birincil": ["Medial Deltoid"],
        "ikincil": [],
        "mekanik": "İzolasyon",
        "teknik": "Alt kablo pozisyonu. Dumbbell'a göre sabit gerilim avantajı — alt pozisyonda da gerilim var.",
        "hatalar": "Gövde eğmek, momentum.",
        "degiskenler": ["DB Lateral Raise", "Machine Lateral Raise"],
        "gif_anahtar": "cable lateral raise",
    },
    "Rear Delt Fly": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrows-expand",
        "ekipman": "Dumbbell veya Kablo",
        "birincil": ["Posterior Deltoid"],
        "ikincil": ["Orta Trapezius", "Rhomboids"],
        "mekanik": "İzolasyon",
        "teknik": "Otur, gövde ileriye eğ (veya prone). Kolları yanlara aç, dirsekler hafif bükülü. Arka deltoid sıkıştır.",
        "hatalar": "Ağır gitmek (trapezius devralır), tam ROM yapmamak.",
        "degiskenler": ["Cable Rear Delt Fly", "Reverse Pec Deck", "Face Pull"],
        "gif_anahtar": "rear delt fly",
    },
    "Front Raise": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrow-up",
        "ekipman": "Dumbbell veya Plaka",
        "birincil": ["Anterior Deltoid"],
        "ikincil": ["Medial Deltoid (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Kolları öne kaldır, omuz hizasına kadar. Daha fazla: bench press/overhead press zaten çalıştırıyor.",
        "hatalar": "Aşırı kullanmak (ön deltoid genellikle aşırı dominant).",
        "degiskenler": ["Plate Front Raise", "Cable Front Raise"],
        "gif_anahtar": "front raise",
    },
    "Upright Row": {
        "kategori": "Omuz", "renk": "#9b59b6", "ikon": "bi-arrow-up",
        "ekipman": "Barbell veya Dumbbell",
        "birincil": ["Medial Deltoid", "Üst Trapezius"],
        "ikincil": ["Biceps"],
        "mekanik": "Bileşik",
        "teknik": "Barı dar tutuş. Dirsekler omuz yüksekliğine çık (daha fazla değil — impingement). Geniş tutuş daha az riskli.",
        "hatalar": "Dirsekli omuzun üstüne çıkarmak (rotator cuff sıkışması).",
        "degiskenler": ["Cable Upright Row", "DB Upright Row"],
        "gif_anahtar": "upright row",
    },

    # ── BİCEPS ───────────────────────────────────────────────────────────────
    "Barbell Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Barbell / EZ-Bar",
        "birincil": ["Biceps Brachii"],
        "ikincil": ["Brachialis", "Brachioradialis"],
        "mekanik": "İzolasyon",
        "teknik": "Dirsekler gövde yanında sabit. Tam curl: avuç dönmeli. Kontrollü eksantrik (2-3 sn iniş).",
        "hatalar": "Dirsekleri öne/dışa atmak, gövde sallanması, kısa ROM.",
        "degiskenler": ["EZ-Bar Curl", "Dumbbell Curl", "Cable Curl", "Reverse Curl"],
        "gif_anahtar": "barbell curl",
    },
    "Dumbbell Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Dumbbell",
        "birincil": ["Biceps Brachii"],
        "ikincil": ["Brachialis"],
        "mekanik": "İzolasyon",
        "teknik": "Alternatif veya aynı anda. Supinate et (avucu döndür) — biceps tam aktive olur. Dirsek sabit.",
        "hatalar": "Supinasyon yapmamak, kısa ROM.",
        "degiskenler": ["Hammer Curl", "Incline Curl", "Concentration Curl"],
        "gif_anahtar": "dumbbell curl",
    },
    "Hammer Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Dumbbell",
        "birincil": ["Brachialis", "Brachioradialis"],
        "ikincil": ["Biceps Brachii"],
        "mekanik": "İzolasyon",
        "teknik": "Nötral tutuş (avuç içe). Brachialis'i izole eder — kol kalınlığı için kritik.",
        "hatalar": "Bilek bükülmesi, momentum.",
        "degiskenler": ["Cross-Body Hammer Curl", "Cable Hammer Curl", "Rope Curl"],
        "gif_anahtar": "hammer curl",
    },
    "Preacher Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "EZ-Bar / Dumbbell + Preacher Bench",
        "birincil": ["Biceps Brachii — Uzun Baş"],
        "ikincil": ["Brachialis"],
        "mekanik": "İzolasyon",
        "teknik": "Kollar desteğe sabit. Momentum engellenmiş — saf biceps çalışması. Tam in, tam curl.",
        "hatalar": "Dirsekleri destekten kaldırmak, tam ROM yapmamak.",
        "degiskenler": ["Spider Curl", "Cable Preacher Curl"],
        "gif_anahtar": "preacher curl",
    },
    "Concentration Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Dumbbell",
        "birincil": ["Biceps Brachii — Kısa Baş (peak)"],
        "ikincil": ["Brachialis"],
        "mekanik": "İzolasyon",
        "teknik": "Otur, dirsek iç uylukta. Tek kol. En yüksek peak kontraksiyon. Yavaş eksantrik.",
        "hatalar": "Gövde dönmesi, kısa ROM.",
        "degiskenler": ["Preacher Curl", "Cable Curl"],
        "gif_anahtar": "concentration curl",
    },
    "Incline Dumbbell Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Dumbbell + İncline Bench",
        "birincil": ["Biceps Brachii — Uzun Baş (tam uzama gerilimi)"],
        "ikincil": ["Brachialis"],
        "mekanik": "İzolasyon",
        "teknik": "45-60° incline'da uzan. Kollar sarkık — uzun baş tam uzar. Yavaş eksantrik.",
        "hatalar": "Dirsekleri ileri atmak, hız yapmak.",
        "degiskenler": ["Preacher Curl", "Overhead Cable Curl"],
        "gif_anahtar": "incline dumbbell curl",
    },
    "Cable Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Kablo",
        "birincil": ["Biceps Brachii"],
        "ikincil": ["Brachialis"],
        "mekanik": "İzolasyon",
        "teknik": "Alt kablo sabit gerilim avantajı. Tüm ROM boyunca gerilim. Peak'te 1 sn tut.",
        "hatalar": "Momentum, dirsek kaçması.",
        "degiskenler": ["Rope Cable Curl", "Single-Arm Cable Curl"],
        "gif_anahtar": "cable curl",
    },
    "Reverse Curl": {
        "kategori": "Biceps", "renk": "#c0392b", "ikon": "bi-hand-thumbs-up",
        "ekipman": "Barbell / Dumbbell",
        "birincil": ["Brachioradialis", "Extensor Carpi"],
        "ikincil": ["Biceps (minimal)", "Brachialis"],
        "mekanik": "İzolasyon",
        "teknik": "Overhand tutuş. Ön kolun üst bölümünü ve brachioradialis'i çalıştırır.",
        "hatalar": "Bilek düşürmek, momentum.",
        "degiskenler": ["Hammer Curl", "EZ-Bar Reverse Curl"],
        "gif_anahtar": "reverse curl",
    },

    # ── TRİCEPS ──────────────────────────────────────────────────────────────
    "Tricep Pushdown": {
        "kategori": "Triceps", "renk": "#8e44ad", "ikon": "bi-chevron-bar-right",
        "ekipman": "Kablo + Rope/V-Bar",
        "birincil": ["Triceps — Lateral Baş"],
        "ikincil": ["Triceps — Medial Baş"],
        "mekanik": "İzolasyon",
        "teknik": "Dirsekler gövde yanında sabit. Tam uzanma (kol tam açılmalı). Rope: sona dışa aç. Peak 1 sn.",
        "hatalar": "Dirsekleri öne/yana atmak, tam uzanmamak, gövde sallanması.",
        "degiskenler": ["Rope Pushdown", "V-Bar Pushdown", "Reverse Grip Pushdown"],
        "gif_anahtar": "tricep pushdown",
    },
    "Skull Crusher": {
        "kategori": "Triceps", "renk": "#8e44ad", "ikon": "bi-chevron-bar-right",
        "ekipman": "Barbell / EZ-Bar + Bench",
        "birincil": ["Triceps — Uzun Baş", "Triceps — Lateral Baş"],
        "ikincil": ["Triceps — Medial Baş"],
        "mekanik": "İzolasyon",
        "teknik": "Düz veya hafif incline bench. Barı alın/kafa hizasına indir (yüze değil!). Dirsekler sabittir.",
        "hatalar": "Dirsekleri dışa açmak, tam indirmemek, ağır gitmek.",
        "degiskenler": ["JM Press", "Dumbbell Skull Crusher", "Ez-Bar Skullcrusher"],
        "gif_anahtar": "skull crusher",
    },
    "Overhead Tricep Extension": {
        "kategori": "Triceps", "renk": "#8e44ad", "ikon": "bi-chevron-bar-right",
        "ekipman": "Dumbbell / Kablo",
        "birincil": ["Triceps — Uzun Baş (tam uzama)"],
        "ikincil": ["Triceps — Lateral Baş"],
        "mekanik": "İzolasyon",
        "teknik": "Kolu dik tut. Ön kolu sadece hareket ettirir. Uzun baş tam uzar — en kritik egzersiz.",
        "hatalar": "Dirsekleri dışa açmak, kısa ROM.",
        "degiskenler": ["Cable Overhead Extension", "Rope Overhead Extension", "Lying Extension"],
        "gif_anahtar": "overhead tricep extension",
    },
    "Close-Grip Bench Press": {
        "kategori": "Triceps", "renk": "#8e44ad", "ikon": "bi-chevron-bar-right",
        "ekipman": "Barbell + Bench",
        "birincil": ["Triceps Brachii (tüm başlar)"],
        "ikincil": ["Pectoralis Major (iç)", "Ön Deltoid"],
        "mekanik": "Bileşik",
        "teknik": "Omuz genişliği dar (ama çok dar değil — bilek stresi). Dirsekler 45° açı.",
        "hatalar": "Tutuşu çok dar almak, dirsekleri geniş açmak.",
        "degiskenler": ["Skull Crusher", "Tricep Dip", "Diamond Push-up"],
        "gif_anahtar": "close grip bench press",
    },
    "Tricep Dip": {
        "kategori": "Triceps", "renk": "#8e44ad", "ikon": "bi-chevron-double-down",
        "ekipman": "Dip Bar",
        "birincil": ["Triceps Brachii (tüm başlar)"],
        "ikincil": ["Pectoralis Minor", "Ön Deltoid"],
        "mekanik": "Bileşik",
        "teknik": "Gövde dik (tricep odaklı). Dirsekler gövde yanında. Omuz yüksekliğine in.",
        "hatalar": "Gövdeyi öne eğmek (göğüs dip olur), omuzları öne almak.",
        "degiskenler": ["Weighted Dip", "Bench Dip (daha az etkili)", "Machine Dip"],
        "gif_anahtar": "tricep dip",
    },

    # ── BACAK ────────────────────────────────────────────────────────────────
    "Barbell Back Squat": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-lightning-fill",
        "ekipman": "Barbell + Squat Rack",
        "birincil": ["Quadriceps", "Gluteus Maximus"],
        "ikincil": ["Hamstrings", "Erektör Spina", "Core"],
        "mekanik": "Bileşik — full leg",
        "teknik": "Bar alttrapezde (low bar) veya üst trapezde (high bar). Diz parmak hizasında. Kalça aşağı-geri. Core sıkı, bel nötr.",
        "hatalar": "Diz içe dönmesi (valgus), bel yuvarlama, topuk kalkması.",
        "degiskenler": ["Front Squat", "Goblet Squat", "Box Squat", "Safety Bar Squat"],
        "gif_anahtar": "barbell squat",
    },
    "Front Squat": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-lightning-fill",
        "ekipman": "Barbell",
        "birincil": ["Quadriceps (daha fazla vurgu)", "Gluteus Maximus"],
        "ikincil": ["Erektör Spina", "Core"],
        "mekanik": "Bileşik",
        "teknik": "Bar göğüste (clean grip veya çapraz). Gövde çok dik kalır — quad vurgusu artar. Bilek flexibilitesi gerekir.",
        "hatalar": "Bar düşmesi (bilek/omuz sertliği), gövde öne düşme.",
        "degiskenler": ["Goblet Squat", "Hack Squat", "Barbell Back Squat"],
        "gif_anahtar": "front squat",
    },
    "Hack Squat Machine": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-lightning-fill",
        "ekipman": "Hack Squat Makinesi",
        "birincil": ["Quadriceps"],
        "ikincil": ["Gluteus Maximus"],
        "mekanik": "Bileşik",
        "teknik": "Ayaklar düşük platform = quad vurgusu. Derin ROM. Stabilizasyon makine tarafından sağlanır.",
        "hatalar": "ROM kısmak, ayakları çok yukarı koymak (glute olur).",
        "degiskenler": ["Leg Press", "Belt Squat"],
        "gif_anahtar": "hack squat",
    },
    "Leg Press": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-lightning-fill",
        "ekipman": "Leg Press Makinesi",
        "birincil": ["Quadriceps", "Gluteus Maximus"],
        "ikincil": ["Hamstrings"],
        "mekanik": "Bileşik",
        "teknik": "Ayak pozisyonu: düşük dar = quad, yüksek geniş = glute/hamstring. Tam ROM, dizleri göğse. Dizi kilitleme!",
        "hatalar": "Dizi kilitleme (eklem hasarı), ROM kısmak, bel platformdan kalkması.",
        "degiskenler": ["Single-Leg Press", "High Foot Press", "Narrow Stance Press"],
        "gif_anahtar": "leg press",
    },
    "Bulgarian Split Squat": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-lightning-fill",
        "ekipman": "Bench + Dumbbell/Barbell",
        "birincil": ["Quadriceps (ön bacak)", "Gluteus Maximus"],
        "ikincil": ["Hamstrings", "Hip Flexors"],
        "mekanik": "Bileşik (tek taraflı)",
        "teknik": "Arka ayak bench üstünde. Ön dizi parmaklar hizasında. Derin ROM. Dengesizlik stabilizatörleri aktive eder.",
        "hatalar": "Ön dizi fazla öne geçirmek, arka topuğu bastırmak.",
        "degiskenler": ["DB BSS", "BB BSS", "Barbell in rack"],
        "gif_anahtar": "bulgarian split squat",
    },
    "Goblet Squat": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-lightning-fill",
        "ekipman": "Dumbbell / Kettlebell",
        "birincil": ["Quadriceps", "Gluteus Maximus"],
        "ikincil": ["Core", "Erektör"],
        "mekanik": "Bileşik",
        "teknik": "Dumbbell göğüs önünde tutulur. Dik gövde, derin squat. Başlangıç için ideal teknik öğreticisi.",
        "hatalar": "Ağırlık dışarı kayması, topuk kalkması.",
        "degiskenler": ["Barbell Squat", "Front Squat"],
        "gif_anahtar": "goblet squat",
    },
    "Leg Extension": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-arrow-right",
        "ekipman": "Leg Extension Makinesi",
        "birincil": ["Quadriceps (saf izolasyon)"],
        "ikincil": [],
        "mekanik": "İzolasyon",
        "teknik": "Kontrollü extension, üstte 1 sn sık. VMO için tam kısalma (son 30°) kritik.",
        "hatalar": "Kalçayı kaldırmak, çok ağır gitmek (patellar tendon stresi).",
        "degiskenler": ["Single-Leg Extension", "Seated Leg Extension"],
        "gif_anahtar": "leg extension",
    },
    "Lying Leg Curl": {
        "kategori": "Bacak", "renk": "#27ae60", "ikon": "bi-arrow-left",
        "ekipman": "Leg Curl Makinesi",
        "birincil": ["Hamstrings (diz fleksiyonu)"],
        "ikincil": ["Gastrocnemius (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Kalçalar makineye sabit. Tam curl, üstte sık. Kontrollü in.",
        "hatalar": "Kalçayı kaldırmak, kısa ROM.",
        "degiskenler": ["Seated Leg Curl", "Standing Leg Curl", "Nordic Curl"],
        "gif_anahtar": "leg curl",
    },
    "Seated Leg Curl": {
        "kategori": "Bacak", "renk": "#27ae60", "ikon": "bi-arrow-left",
        "ekipman": "Seated Leg Curl Makinesi",
        "birincil": ["Biceps Femoris — Uzun Baş"],
        "ikincil": ["Semitendinosus", "Semimembranosus"],
        "mekanik": "İzolasyon",
        "teknik": "Ayak bileği plantar fleks (fleks değil dorsifleks). Kalça bükülü pozisyon biceps femoris uzun başını daha iyi uzatır.",
        "hatalar": "Kalçayı makineyle sabitlememek, ROM kısmak.",
        "degiskenler": ["Lying Leg Curl", "Nordic Curl"],
        "gif_anahtar": "seated leg curl",
    },
    "Nordic Hamstring Curl": {
        "kategori": "Bacak", "renk": "#27ae60", "ikon": "bi-arrow-down",
        "ekipman": "Partner / Nordic Bench",
        "birincil": ["Hamstrings (eksantrik)"],
        "ikincil": ["Gluteus Maximus"],
        "mekanik": "Bileşik",
        "teknik": "Ayak tutulur. Gövde öne kontrollü indirilir (eksantrik). En etkili hamstring yaralanma önleyicisi.",
        "hatalar": "Çok hızlı inmek, bel bükülmesi.",
        "degiskenler": ["Glute-Ham Raise (GHR)", "Slider Leg Curl"],
        "gif_anahtar": "nordic hamstring curl",
    },
    "Hip Thrust": {
        "kategori": "Bacak", "renk": "#27ae60", "ikon": "bi-arrow-up",
        "ekipman": "Barbell + Bench",
        "birincil": ["Gluteus Maximus (en yüksek EMG aktivasyonu)"],
        "ikincil": ["Hamstrings", "Core"],
        "mekanik": "Bileşik",
        "teknik": "Üst sırt bench kenarında. Barbell kalça kemiğinde. Kalçayı tam yukarı it, üstte 1 sn tut ve sıkıştır.",
        "hatalar": "Beli hiper-ekstansiyona sokmak, üstte sıkıştırmamak, ayak pozisyonu yanlış.",
        "degiskenler": ["Glute Bridge", "Single-Leg Hip Thrust", "Banded Hip Thrust"],
        "gif_anahtar": "hip thrust",
    },
    "Romanian Deadlift (RDL)": {
        "kategori": "Bacak", "renk": "#27ae60", "ikon": "bi-arrow-down",
        "ekipman": "Barbell / Dumbbell",
        "birincil": ["Hamstrings", "Erektör Spina"],
        "ikincil": ["Gluteus Maximus", "Trapezius"],
        "mekanik": "Bileşik",
        "teknik": "Diz hafif bükülü, sabit. Kalça menteşe. Bel nötr. Hamstrings'de derin strech hissi — çok kritik.",
        "hatalar": "Beli bükmek, bar bacaklardan uzaklaşmak, dizi çok bükmek.",
        "degiskenler": ["Stiff-Leg DL", "Single-Leg RDL", "Cable Pull-Through"],
        "gif_anahtar": "romanian deadlift",
    },
    "Standing Calf Raise": {
        "kategori": "Bacak", "renk": "#16a085", "ikon": "bi-arrow-up",
        "ekipman": "Smith Machine / Calf Raise Makinesi / Ayak Kenarı",
        "birincil": ["Gastrocnemius"],
        "ikincil": ["Soleus (yardımcı)"],
        "mekanik": "İzolasyon",
        "teknik": "Diz düz. Tam ROM: topuk zemine değsin, ayak ucu en yukarı. Üstte 1-2 sn tut.",
        "hatalar": "Kısa ROM (zıplama), çok hızlı tempo, tek tarafı atlamak.",
        "degiskenler": ["Single-Leg Calf Raise", "Donkey Calf Raise", "Leg Press Calf Raise"],
        "gif_anahtar": "standing calf raise",
    },
    "Seated Calf Raise": {
        "kategori": "Bacak", "renk": "#16a085", "ikon": "bi-arrow-up",
        "ekipman": "Seated Calf Raise Makinesi",
        "birincil": ["Soleus (diz bükülü — gastrocnemius devre dışı)"],
        "ikincil": ["Gastrocnemius (minimal)"],
        "mekanik": "İzolasyon",
        "teknik": "Diz 90°'de bükülü. Soleus izolasyonu için şart. Tam ROM, yavaş tempo.",
        "hatalar": "Dizi bükmemek (gastrocnemius baskın olur).",
        "degiskenler": ["Standing Calf Raise"],
        "gif_anahtar": "seated calf raise",
    },
    "Lunge": {
        "kategori": "Bacak", "renk": "#f39c12", "ikon": "bi-person-walking",
        "ekipman": "Vücut Ağırlığı / Dumbbell",
        "birincil": ["Quadriceps (ön bacak)", "Gluteus Maximus"],
        "ikincil": ["Hamstrings", "Core"],
        "mekanik": "Bileşik (tek taraflı)",
        "teknik": "Adım at, ön diz 90°. Arka diz neredeyse yere değsin. Gövde dik.",
        "hatalar": "Ön dizi fazla öne geçirmek, gövde öne düşmesi.",
        "degiskenler": ["Reverse Lunge", "Walking Lunge", "Lateral Lunge", "Deficit Lunge"],
        "gif_anahtar": "lunge",
    },

    # ── CORE ─────────────────────────────────────────────────────────────────
    "Plank": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-pause-circle",
        "ekipman": "Vücut Ağırlığı",
        "birincil": ["Transversus Abdominis", "Rectus Abdominis"],
        "ikincil": ["Erektör Spina", "Glute", "Omuz stabilizatörler"],
        "mekanik": "İzometrik",
        "teknik": "Dirsek veya el üstünde. Vücut düz tahta gibi. Kalça ne düşmeli ne kalkmalı. Nötr omurga.",
        "hatalar": "Kalça sarkması/kalkması, boyun öne uzanması, nefes tutmak.",
        "degiskenler": ["Side Plank", "RKC Plank", "Weighted Plank", "Plank Row"],
        "gif_anahtar": "plank",
    },
    "Ab Wheel Rollout": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-circle",
        "ekipman": "Ab Wheel",
        "birincil": ["Rectus Abdominis", "Latissimus Dorsi"],
        "ikincil": ["Oblique", "Hip Flexors"],
        "mekanik": "Dinamik bileşik",
        "teknik": "Diz üstünden başla, öne yuvarla, bel sarkmamalı. Geri dön. İleri seviye: ayakta.",
        "hatalar": "Beli bükmek, kolları tam uzatmamak.",
        "degiskenler": ["TRX Rollout", "Barbell Rollout", "Kneeling RKC"],
        "gif_anahtar": "ab wheel rollout",
    },
    "Cable Crunch": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-arrow-down-right",
        "ekipman": "Kablo + Rope",
        "birincil": ["Rectus Abdominis (yüklü)"],
        "ikincil": ["Oblique"],
        "mekanik": "Bileşik (yüklü crunch)",
        "teknik": "Diz çök, rope kafada. Kalçayı sabit tut, sadece gövde flex. Göbeği bacaklara götür.",
        "hatalar": "Kalçayla çekmek (hip flexion olur), boyun kuvvetiyle çekmek.",
        "degiskenler": ["Machine Crunch", "Decline Crunch", "Weighted Sit-up"],
        "gif_anahtar": "cable crunch",
    },
    "Hanging Leg Raise": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-arrow-up",
        "ekipman": "Pull-up Bar",
        "birincil": ["Alt Rectus Abdominis", "Hip Flexors"],
        "ikincil": ["Serratus Anterior", "Oblique"],
        "mekanik": "Dinamik",
        "teknik": "Bar'a asıl. Diz veya düz bacak kaldır. Pelvis posterior tilt et (kuyruğu içe tük) — alt karın aktive.",
        "hatalar": "Sallanmak (momentum), bacakları düşürmek yerine bırakmak.",
        "degiskenler": ["Captain's Chair", "TRX Leg Raise", "Decline Leg Raise"],
        "gif_anahtar": "hanging leg raise",
    },
    "Russian Twist": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-arrow-clockwise",
        "ekipman": "Vücut / Plaka / Dumbbell",
        "birincil": ["Obliquus Externus", "Obliquus Internus"],
        "ikincil": ["Rectus Abdominis"],
        "mekanik": "Rotasyonel",
        "teknik": "Otur, gövde 45°, bacaklar yukarı. Ağırlığı yanlara çevir. Kontrollü rotasyon.",
        "hatalar": "Sadece kollarla çevirmek (gövde sabit kalıyor), çok hızlı.",
        "degiskenler": ["Landmine Rotation", "Cable Wood Chop"],
        "gif_anahtar": "russian twist",
    },
    "Pallof Press": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-shield-check",
        "ekipman": "Kablo veya Bant",
        "birincil": ["Transversus Abdominis", "Oblique (anti-rotasyon)"],
        "ikincil": ["Erektör Spina", "Glute"],
        "mekanik": "İzometrik (anti-rotasyon)",
        "teknik": "Kabloya yan dur. Elleri göğüste. İt ve geri çek — rotasyona direnç. Fonksiyonel core stabilitesi.",
        "hatalar": "Gövdeyi döndürmek (direnç kaybı), nefes tutmak.",
        "degiskenler": ["Half-Kneeling Pallof Press", "Standing Pallof Press"],
        "gif_anahtar": "pallof press",
    },
    "Dead Bug": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-circle",
        "ekipman": "Vücut Ağırlığı",
        "birincil": ["Transversus Abdominis"],
        "ikincil": ["Hip Flexors (koordinasyon)", "Erektör (stabilizatör)"],
        "mekanik": "Koordinasyon + stabilizasyon",
        "teknik": "Sırt üstü. Kollar yukarı, diz 90°. Karşılıklı kol-bacak aç, beli yere bas. Yavaş, kontrollü.",
        "hatalar": "Beli kaldırmak, çok hızlı hareket etmek.",
        "degiskenler": ["Bird-Dog", "Hollow Hold"],
        "gif_anahtar": "dead bug exercise",
    },
    "Side Plank": {
        "kategori": "Core", "renk": "#1abc9c", "ikon": "bi-pause-circle",
        "ekipman": "Vücut Ağırlığı",
        "birincil": ["Obliquus Externus/Internus", "Quadratus Lumborum"],
        "ikincil": ["Hip Abductor", "Glute"],
        "mekanik": "İzometrik",
        "teknik": "Yan yat, dirsek veya el üstünde. Kalçayı yukarı tut, omurga düz. Zirveye küçük kalça yükseltme ekle.",
        "hatalar": "Kalça sarkması, omurga rotasyonu.",
        "degiskenler": ["Star Side Plank", "Copenhagen Plank"],
        "gif_anahtar": "side plank",
    },

    # ── FONKSİYONEL / OLİMPİK ────────────────────────────────────────────────
    "Farmer's Walk": {
        "kategori": "Fonksiyonel", "renk": "#795548", "ikon": "bi-person-walking",
        "ekipman": "Dumbbell / Kettlebell / Farmer Handles",
        "birincil": ["Trapezius", "Forearm Flexors", "Core"],
        "ikincil": ["Erektör Spina", "Glute", "Quadriceps"],
        "mekanik": "Full body taşıma",
        "teknik": "Dik duruş. Adım küçük-hızlı. Omuzları geri, kürek kemiklerini sıkıştır.",
        "hatalar": "Gövde öne eğmesi, omuzları öne almak.",
        "degiskenler": ["Suitcase Carry", "Overhead Carry", "Yoke Walk"],
        "gif_anahtar": "farmers walk",
    },
    "Kettlebell Swing": {
        "kategori": "Fonksiyonel", "renk": "#795548", "ikon": "bi-arrow-clockwise",
        "ekipman": "Kettlebell",
        "birincil": ["Gluteus Maximus", "Hamstrings"],
        "ikincil": ["Erektör Spina", "Core", "Deltoid"],
        "mekanik": "Balistik bileşik",
        "teknik": "Kalça menteşe ile swing. Kol sadece taşır, güç kalçadan. Üstte kalça tam kapanır.",
        "hatalar": "Squatting (diz bükülüyor), kollarla kaldırmak.",
        "degiskenler": ["American Swing", "Single-Arm Swing", "Double KB Swing"],
        "gif_anahtar": "kettlebell swing",
    },
    "Push Press": {
        "kategori": "Fonksiyonel", "renk": "#795548", "ikon": "bi-arrow-up",
        "ekipman": "Barbell",
        "birincil": ["Deltoid", "Triceps"],
        "ikincil": ["Quadriceps", "Glute", "Core"],
        "mekanik": "Balistik bileşik",
        "teknik": "Hafif dip (mini squat) ile momentum, sonra kollar itiş. Daha fazla ağırlık = daha çok güç.",
        "hatalar": "Çok derin dip, barı serbest bırakmak.",
        "degiskenler": ["Push Jerk", "Overhead Press", "Thruster"],
        "gif_anahtar": "push press",
    },
    "Barbell Hip Hinge": {
        "kategori": "Fonksiyonel", "renk": "#795548", "ikon": "bi-arrow-clockwise",
        "ekipman": "Barbell",
        "birincil": ["Gluteus Maximus", "Hamstrings", "Erektör"],
        "ikincil": ["Core"],
        "mekanik": "Temel hareket paterni",
        "teknik": "Kalçadan menteşe — tüm deadlift ve RDL hareketlerinin temeli. Bel nötr.",
        "hatalar": "Beli bükmek, dizi çok bükmek.",
        "degiskenler": ["RDL", "Good Morning", "Cable Pull-Through"],
        "gif_anahtar": "hip hinge",
    },
}

# Kas grubu ikon ve renk haritası (template'de kullanmak için)
KAS_IKON_MAP = {
    "Göğüs":     ("bi-heart-pulse-fill", "#e74c3c"),
    "Sırt":      ("bi-rulers", "#3498db"),
    "Omuz":      ("bi-arrow-up-circle-fill", "#9b59b6"),
    "Biceps":    ("bi-hand-thumbs-up-fill", "#c0392b"),
    "Triceps":   ("bi-chevron-bar-right", "#8e44ad"),
    "Bacak":     ("bi-lightning-charge-fill", "#f39c12"),
    "Core":      ("bi-circle-fill", "#1abc9c"),
    "Fonksiyonel": ("bi-person-walking", "#795548"),
}

# Egzersiz GIF anahtar haritası (JS'e gönderilecek)
EGZERSIZ_GIF_MAP = {eg: v.get("gif_anahtar", "") for eg, v in EGZERSIZ_ANSIKLOPEDISI.items()}


# ══════════════════════════════════════════════════════════════════════════════
#  EGZERSIZ VERİTABANI (program için)
# ══════════════════════════════════════════════════════════════════════════════

EGZERSIZ_DB = {
    eg: {
        "kaslar": v["birincil"] + v["ikincil"],
        "ekipman": ["salon"],
        "seviye": ["baslangic", "orta", "ileri"],
        "tip": "primer" if v["mekanik"].startswith("Bileşik") else "izolasyon",
    }
    for eg, v in EGZERSIZ_ANSIKLOPEDISI.items()
}


# ══════════════════════════════════════════════════════════════════════════════
#  EKİPMAN ALTERNATİFLERİ  (salon → ev → vücut ağırlığı)
# ══════════════════════════════════════════════════════════════════════════════

EKIPMAN_ALTERN = {
    "Barbell Back Squat":        {"ev": "Goblet Squat",                  "vucutagirligi": "Bodyweight Squat"},
    "Front Squat":               {"ev": "Goblet Squat",                  "vucutagirligi": "Bodyweight Squat"},
    "Conventional Deadlift":     {"ev": "Romanian Deadlift (RDL)",       "vucutagirligi": "Single-Leg RDL"},
    "Barbell Bench Press":       {"ev": "Dumbbell Bench Press",          "vucutagirligi": "Push-up"},
    "Incline Barbell Press":     {"ev": "Incline Dumbbell Press",        "vucutagirligi": "Incline Push-up"},
    "Barbell Overhead Press":    {"ev": "Dumbbell Shoulder Press",       "vucutagirligi": "Pike Push-up"},
    "Bent-Over Barbell Row":     {"ev": "Dumbbell Row (One-Arm)",        "vucutagirligi": "Inverted Row"},
    "Pull-up":                   {"ev": "Pull-up",                       "vucutagirligi": "Pull-up"},
    "Lat Pulldown":              {"ev": "Dumbbell Row (One-Arm)",        "vucutagirligi": "Inverted Row"},
    "Leg Press":                 {"ev": "Bulgarian Split Squat",         "vucutagirligi": "Lunge"},
    "Hack Squat Machine":        {"ev": "Bulgarian Split Squat",         "vucutagirligi": "Bulgarian Split Squat"},
    "Hip Thrust":                {"ev": "Hip Thrust",                    "vucutagirligi": "Glute Bridge"},
    "Cable Fly (Mid)":           {"ev": "Dumbbell Fly",                  "vucutagirligi": "Push-up"},
    "Seated Cable Row":          {"ev": "Dumbbell Row (One-Arm)",        "vucutagirligi": "Inverted Row"},
    "Tricep Pushdown":           {"ev": "Overhead Tricep Extension",     "vucutagirligi": "Diamond Push-up"},
    "Skull Crusher":             {"ev": "Overhead Tricep Extension",     "vucutagirligi": "Diamond Push-up"},
    "Close-Grip Bench Press":    {"ev": "Overhead Tricep Extension",     "vucutagirligi": "Diamond Push-up"},
    "Leg Extension":             {"ev": "Bulgarian Split Squat",         "vucutagirligi": "Wall Sit"},
    "Lying Leg Curl":            {"ev": "Romanian Deadlift (RDL)",       "vucutagirligi": "Nordic Hamstring Curl"},
    "Seated Leg Curl":           {"ev": "Romanian Deadlift (RDL)",       "vucutagirligi": "Nordic Hamstring Curl"},
    "Cable Crunch":              {"ev": "Ab Wheel Rollout",              "vucutagirligi": "Plank"},
    "Arnold Press":              {"ev": "Arnold Press",                  "vucutagirligi": "Pike Push-up"},
    "Face Pull":                 {"ev": "Band Pull-Apart",               "vucutagirligi": "Band Pull-Apart"},
    "Pallof Press":              {"ev": "Dead Bug",                      "vucutagirligi": "Dead Bug"},
    "Good Morning":              {"ev": "Romanian Deadlift (RDL)",       "vucutagirligi": "Hip Hinge (Vücut)"},
}

# ══════════════════════════════════════════════════════════════════════════════
#  A/B HAFTALIK VARİYASYON  (çift haftalarda B egzersizi)
# ══════════════════════════════════════════════════════════════════════════════

AB_VARYANT = {
    "Barbell Back Squat":        "Bulgarian Split Squat",
    "Barbell Bench Press":       "Incline Dumbbell Press",
    "Conventional Deadlift":     "Romanian Deadlift (RDL)",
    "Bent-Over Barbell Row":     "Seated Cable Row",
    "Pull-up":                   "Lat Pulldown",
    "Dumbbell Shoulder Press":   "Barbell Overhead Press",
    "Barbell Overhead Press":    "Arnold Press",
    "Lying Leg Curl":            "Seated Leg Curl",
    "Leg Press":                 "Hack Squat Machine",
    "Hip Thrust":                "Romanian Deadlift (RDL)",
    "Cable Fly (Mid)":           "Dumbbell Fly",
    "Tricep Pushdown":           "Overhead Tricep Extension",
    "Barbell Curl":              "Incline Dumbbell Curl",
    "Goblet Squat":              "Lunge",
    "Plank":                     "Dead Bug",
    "Kettlebell Swing":          "Romanian Deadlift (RDL)",
}

# ══════════════════════════════════════════════════════════════════════════════
#  SEVİYE ALTERNATİFLERİ  (başlangıç için ileri egzersizleri basitleştir)
# ══════════════════════════════════════════════════════════════════════════════

SEVIYE_ALTERN = {
    "baslangic": {
        "Conventional Deadlift":  "Romanian Deadlift (RDL)",
        "Pull-up":                "Lat Pulldown",
        "Ab Wheel Rollout":       "Plank",
        "Nordic Hamstring Curl":  "Lying Leg Curl",
        "Bulgarian Split Squat":  "Lunge",
        "Pallof Press":           "Dead Bug",
        "Good Morning":           "Romanian Deadlift (RDL)",
        "Push Press":             "Dumbbell Shoulder Press",
    }
}

# ══════════════════════════════════════════════════════════════════════════════
#  SET/TEKRAR ŞEMASİ  (seviyeye göre compound hareketler için)
# ══════════════════════════════════════════════════════════════════════════════

SEMA = {
    "hipertrofi": {
        "baslangic": ("3×10-12", "90 sn",  "Kontrollü tempo, tekniğe odaklan"),
        "orta":      ("4×8-10",  "90 sn",  "Progressive overload"),
        "ileri":     ("4×6-8",   "2 dk",   "RIR 1-2, neredeyse başarısızlık"),
    },
    "yakma": {
        "baslangic": ("3×12",    "75 sn",  "Kontrollü eccentric, form önce"),
        "orta":      ("4×12",    "45 sn",  "Süperset yapılabilir"),
        "ileri":     ("4×15",    "30 sn",  "Maks hız, metabolik baskı"),
    },
    "kardiyo": {
        "baslangic": ("3×12",    "60 sn",  "Tempoyu koru, nefes kontrolü"),
        "orta":      ("3×15",    "45 sn",  "Devre tarzı, kısa mola"),
        "ileri":     ("4×20",    "20 sn",  "HIIT yapısı, patlayıcı tempo"),
    },
    "powerbuilding": {
        "baslangic": ("3×8",     "2 dk",   "Teknikle kuvveti birleştir"),
        "orta":      ("4×6",     "2-3 dk", "Güç + hacim hibrid"),
        "ileri":     ("5×4-5",   "3 dk",   "Ağır güç seti + hacim"),
    },
}


class FitnessZekasi:

    @staticmethod
    def vki_kategori(vki):
        if vki < 16.0:   return "Ciddi Zayıf",   "#c0392b"
        elif vki < 18.5: return "Zayıf",          "#3498db"
        elif vki < 25.0: return "Normal (İdeal)", "#27ae60"
        elif vki < 30.0: return "Fazla Kilolu",   "#f39c12"
        elif vki < 35.0: return "Obez (Sınıf I)", "#e74c3c"
        else:            return "Obez (Sınıf II+)","#8e44ad"

    @staticmethod
    def bmr_hesapla(kilo, boy, yas, cinsiyet):
        if cinsiyet == "Erkek":
            return 10 * kilo + 6.25 * boy - 5 * yas + 5
        else:
            return 10 * kilo + 6.25 * boy - 5 * yas - 161

    @staticmethod
    def tdee_hesapla(bmr, aktivite):
        carpan = {
            "Hareketsiz (Masa başı)":        1.2,
            "Az Aktif (1-2 gün/hafta)":      1.375,
            "Orta Aktif (3-5 gün/hafta)":    1.55,
            "Çok Aktif (6-7 gün/hafta)":     1.725,
            "Profesyonel Sporcu":             1.9,
        }
        return bmr * carpan.get(aktivite, 1.375)

    @staticmethod
    def vucut_yag_tahmini(vki, yas, cinsiyet):
        sex = 1 if cinsiyet == "Erkek" else 0
        bf = (1.20 * vki) + (0.23 * yas) - (10.8 * sex) - 5.4
        return round(max(3, min(60, bf)), 1)

    @staticmethod
    def yag_kategorisi(bf, cinsiyet):
        if cinsiyet == "Erkek":
            if bf < 6:    return "Esansiyel Yağ", "#c0392b"
            elif bf < 14: return "Sporcu",         "#27ae60"
            elif bf < 18: return "Fitness",        "#2ecc71"
            elif bf < 25: return "Ortalama",       "#f39c12"
            else:         return "Obez",           "#e74c3c"
        else:
            if bf < 14:   return "Esansiyel Yağ", "#c0392b"
            elif bf < 21: return "Sporcu",         "#27ae60"
            elif bf < 25: return "Fitness",        "#2ecc71"
            elif bf < 32: return "Ortalama",       "#f39c12"
            else:         return "Obez",           "#e74c3c"

    @staticmethod
    def ffmi_hesapla(kilo, boy, bf_yuzde):
        yag_kilo = kilo * (bf_yuzde / 100)
        kas_kilo = kilo - yag_kilo
        boy_m = boy / 100
        ffmi = kas_kilo / (boy_m ** 2)
        duzeltilmis = ffmi + 6.1 * (1.8 - boy_m)
        return round(ffmi, 1), round(duzeltilmis, 1), round(kas_kilo, 1)

    @staticmethod
    def ffmi_yorum(ffmi, cinsiyet):
        if cinsiyet == "Erkek":
            if ffmi < 17:   return "Zayıf — başlangıç", "#888"
            elif ffmi < 20: return "Ortalama",           "#f39c12"
            elif ffmi < 22: return "Atletik",            "#27ae60"
            elif ffmi < 24: return "Gelişmiş",           "#2ecc71"
            elif ffmi < 26: return "İleri Düzey",        "#3498db"
            else:           return "Elite / Üst Sınır",  "#9b59b6"
        else:
            if ffmi < 14:   return "Zayıf",              "#888"
            elif ffmi < 17: return "Ortalama",            "#f39c12"
            elif ffmi < 19: return "Atletik",             "#27ae60"
            elif ffmi < 21: return "İleri Düzey",         "#2ecc71"
            else:           return "Elite",               "#9b59b6"

    @staticmethod
    def ideal_agirlik(boy, cinsiyet):
        boy_m = boy / 100
        return round(18.5 * (boy_m ** 2), 1), round(24.9 * (boy_m ** 2), 1)

    @staticmethod
    def kalori_hedefi(tdee, hedef):
        h = hedef
        if h == "Kilo Ver":                 return round(tdee - 400), "Kalori Açığı (-400 kal)"
        elif h == "Hızlı Kilo Ver":         return round(tdee - 700), "Agresif Açık (-700 kal)"
        elif h == "Kas Yap":                return round(tdee + 250), "Lean Bulk (+250 kal)"
        elif h == "Hızlı Kas Yap":          return round(tdee + 500), "Dirty Bulk (+500 kal)"
        elif h == "Kuvvet Kazan":           return round(tdee + 200), "Güç Surplus (+200 kal)"
        elif h == "Vücut Geliştirme":       return round(tdee + 300), "Hipertrofi Fazı (+300 kal)"
        elif h == "Güç + Hipertrofi":       return round(tdee + 200), "Powerbuilding (+200 kal)"
        elif h == "Kardiyo & Dayanıklılık": return round(tdee - 100), "İdame/Hafif Açık (-100 kal)"
        else:                               return round(tdee), "İdame"

    @staticmethod
    def makro_hesapla(kalori, hedef, kilo):
        h = hedef
        if h in ("Kas Yap", "Hızlı Kas Yap", "Vücut Geliştirme", "Güç + Hipertrofi"):
            protein_g = round(kilo * 2.2); yag_g = round(kilo * 1.0)
        elif h == "Kuvvet Kazan":
            protein_g = round(kilo * 2.0); yag_g = round(kilo * 1.1)
        elif h in ("Kilo Ver", "Hızlı Kilo Ver"):
            protein_g = round(kilo * 2.5); yag_g = round(kilo * 0.8)
        elif h == "Kardiyo & Dayanıklılık":
            protein_g = round(kilo * 1.6); yag_g = round(kilo * 0.8)
        else:
            protein_g = round(kilo * 1.8); yag_g = round(kilo * 0.9)
        protein_kal = protein_g * 4; yag_kal = yag_g * 9
        karb_g = round(max(0, kalori - protein_kal - yag_kal) / 4)
        return protein_g, karb_g, yag_g

    @staticmethod
    def su_ihtiyaci(kilo, aktivite):
        baz = kilo * 0.033
        if aktivite in ("Çok Aktif (6-7 gün/hafta)", "Profesyonel Sporcu"): baz += 0.75
        elif aktivite == "Orta Aktif (3-5 gün/hafta)": baz += 0.5
        return round(baz, 1)

    @staticmethod
    def _ekipman_kodu(ekipman):
        e = ekipman.lower()
        if "salon" in e or "tam" in e: return "salon"
        if "ev" in e or "dumbbell" in e: return "ev"
        return "vucutagirligi"

    @staticmethod
    def _seviye_kodu(seviye):
        s = seviye.lower()
        if "başl" in s: return "baslangic"
        if "orta" in s: return "orta"
        return "ileri"

    @staticmethod
    def _gun_kodlari(gun_sayisi):
        g = str(gun_sayisi)
        if "3" in g: return 3
        if "4" in g: return 4
        return 5

    @staticmethod
    def _egzersiz_sec(ad, ekp, sev="orta"):
        if sev == "baslangic":
            ad = SEVIYE_ALTERN["baslangic"].get(ad, ad)
        if ekp == "salon":
            return ad
        alt = EKIPMAN_ALTERN.get(ad, {})
        return alt.get(ekp, ad)

    @staticmethod
    def _ab_sec(ad, hafta, ekp, sev="orta"):
        if hafta % 2 == 0:
            ad = AB_VARYANT.get(ad, ad)
        return FitnessZekasi._egzersiz_sec(ad, ekp, sev)

    @staticmethod
    def _uygula_filtro(splits, hafta, ekp, sev, sema_turu=None):
        sr, din = None, None
        if sema_turu and sema_turu in SEMA:
            sr, din, _ = SEMA[sema_turu][sev]
        for g in splits:
            processed = []
            for e in g["egzersizler"]:
                nome = FitnessZekasi._ab_sec(e[0], hafta, ekp, sev)
                if sr is not None:
                    tip = EGZERSIZ_DB.get(nome, EGZERSIZ_DB.get(e[0], {})).get("tip", "")
                    if tip == "primer":
                        e = (nome, sr, din) + e[3:]
                    else:
                        e = (nome,) + e[1:]
                else:
                    e = (nome,) + e[1:]
                processed.append(e)
            g["egzersizler"] = processed
        return splits

    @staticmethod
    def program_olustur(hedef, seviye_str, ekipman_str, gun_sayisi_str, hafta):
        sev = FitnessZekasi._seviye_kodu(seviye_str)
        ekp = FitnessZekasi._ekipman_kodu(ekipman_str)
        gun = FitnessZekasi._gun_kodlari(gun_sayisi_str)
        deload = (hafta % 5 == 0 and sev in ("orta", "ileri") and hafta > 4)
        if deload:
            return FitnessZekasi._deload_programi(hafta)
        h = hedef
        if h in ("Kilo Ver", "Hızlı Kilo Ver"):
            return FitnessZekasi._kilo_verme_programi(sev, ekp, gun, hafta)
        elif h in ("Kas Yap", "Hızlı Kas Yap", "Vücut Geliştirme"):
            return FitnessZekasi._hipertrofi_programi(sev, ekp, gun, hafta, h)
        elif h == "Kuvvet Kazan":
            return FitnessZekasi._kuvvet_programi(sev, ekp, gun, hafta)
        elif h == "Güç + Hipertrofi":
            return FitnessZekasi._powerbuilding_programi(sev, ekp, gun, hafta)
        elif h == "Kardiyo & Dayanıklılık":
            return FitnessZekasi._kardiyo_programi(sev, ekp, gun, hafta)
        else:
            return FitnessZekasi._fitkal_programi(sev, ekp, gun, hafta)

    @staticmethod
    def _kilo_verme_programi(sev, ekp, gun, hafta):
        faz = "Yakma Fazı" if hafta <= 8 else "İleri Yakma"
        if gun <= 3:
            splits = [{"gun_adi": f"Full Body {['A','B','C'][i]} — Metabolik Antrenman", "egzersizler": [
                ("Goblet Squat" if ekp != "salon" else "Barbell Back Squat", "4 × 15", "45 sn", "Quadriceps, Glute", "Hızlı tempo"),
                ("Dumbbell Bench Press" if ekp != "salon" else "Barbell Bench Press", "4 × 12", "45 sn", "Göğüs, Triceps", "Kontrollü eccentric"),
                ("Dumbbell Row (One-Arm)" if ekp == "ev" else "Bent-Over Barbell Row", "4 × 12", "45 sn", "Sırt, Biceps", "Kürek sıkıştır"),
                ("Dumbbell Shoulder Press", "3 × 12", "45 sn", "Deltoid", "Tam ROM"),
                ("Romanian Deadlift (RDL)", "3 × 12", "60 sn", "Hamstrings, Glute", "Kalçadan menteşe"),
                ("Plank", "3 × 45 sn", "30 sn", "Core", "Kalça düz"),
                ("Burpee" if sev != "baslangic" else "Kettlebell Swing", "3 × 15", "30 sn", "Full Body + Kardiyo", "Maks hız"),
            ]} for i in range(gun)]
        else:
            gA = [
                ("Barbell Back Squat", "4 × 12", "60 sn", "Quadriceps, Glute", "Progressive overload"),
                ("Romanian Deadlift (RDL)", "4 × 12", "60 sn", "Hamstrings, Erektör", "Kalçadan menteşe"),
                ("Bulgarian Split Squat", "3 × 10/taraf", "60 sn", "Quad, Glute, Denge", ""),
                ("Leg Extension", "3 × 15", "45 sn", "Quadriceps izolasyon", ""),
                ("Lying Leg Curl", "3 × 15", "45 sn", "Hamstrings", ""),
                ("Standing Calf Raise", "4 × 20", "30 sn", "Baldır", "Tam ROM"),
            ]
            gB = [
                ("Barbell Bench Press", "4 × 12", "60 sn", "Göğüs, Triceps", ""),
                ("Bent-Over Barbell Row", "4 × 12", "60 sn", "Lat, Orta Sırt", ""),
                ("Dumbbell Shoulder Press", "3 × 12", "60 sn", "Deltoid", ""),
                ("Lateral Raise", "3 × 15", "45 sn", "Medial Deltoid", ""),
                ("Tricep Pushdown", "3 × 15", "45 sn", "Triceps", ""),
                ("Barbell Curl", "3 × 15", "45 sn", "Biceps", ""),
                ("Cable Crunch", "3 × 20", "30 sn", "Core", ""),
            ]
            splits = [
                {"gun_adi": "Pazartesi — Alt Vücut (Güç+Hacim)", "egzersizler": gA},
                {"gun_adi": "Salı — Üst Vücut (Güç+Hacim)", "egzersizler": gB},
                {"gun_adi": "Çarşamba — HIIT Kardiyo (30 dk)", "egzersizler": [
                    ("Kettlebell Swing", "4 × 20", "30 sn", "Full Body, Posterior Chain", "Kalçadan it"),
                    ("Push Press", "4 × 10", "45 sn", "Omuz, Triceps, Core", ""),
                    ("Goblet Squat", "4 × 15", "30 sn", "Quadriceps, Glute", ""),
                    ("Farmer's Walk", "4 × 30 adım", "45 sn", "Trap, Core, Grip", ""),
                ]},
                {"gun_adi": "Perşembe — Alt Vücut B", "egzersizler": gA},
                {"gun_adi": "Cuma — Üst Vücut B + Core", "egzersizler": gB},
            ][:gun]
        splits = FitnessZekasi._uygula_filtro(splits, hafta, ekp, sev, "yakma")
        return {
            "ad": f"Yağ Yakma — {faz} (Hafta {hafta})",
            "gunler": f"Haftada {gun} gün · Kısa mola · Yüksek tekrar",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for g in splits for e in g["egzersizler"]],
            "dinlenme": "Dinlenme günleri: tempolu yürüyüş 30-45 dk",
            "tavsiye": "Kalori açığını diyetle yarat, antrenmanla kasını koru. Progressive overload zorunlu.",
            "kardiyo": "Haftada 2-3 gün LISS (40-50 dk) + haftada 1 HIIT",
            "uyku_oneri": "7-9 saat. Kortizol yağ yakmayı engeller.",
        }

    @staticmethod
    def _hipertrofi_programi(sev, ekp, gun, hafta, hedef_str):
        blok = (hafta - 1) // 4 + 1
        if gun <= 3:
            liste = [
                ("Barbell Back Squat", "4 × 8-10", "90 sn", "Quadriceps, Glute", "Progressive overload"),
                ("Barbell Bench Press", "4 × 8-10", "90 sn", "Göğüs, Triceps", "Tam ROM"),
                ("Bent-Over Barbell Row", "4 × 8-10", "90 sn", "Lat, Orta Sırt", "Kürek sıkıştır"),
                ("Romanian Deadlift (RDL)", "3 × 10-12", "90 sn", "Hamstrings, Glute", "Kontrollü"),
                ("Dumbbell Shoulder Press", "3 × 10-12", "60 sn", "Deltoid", ""),
                ("Barbell Curl + Tricep Pushdown", "3 × 12-15", "45 sn", "Biceps + Triceps", "Süperset"),
                ("Plank", "3 × 45 sn", "30 sn", "Core", ""),
            ]
            splits = [{"gun_adi": f"Full Body {['A','B','C'][i]} — Blok {blok}", "egzersizler": liste} for i in range(gun)]
        elif gun == 4:
            ust_A = [
                ("Barbell Bench Press", "4 × 6-8", "2 dk", "Göğüs, Triceps, Ön Delt", "Güç odaklı"),
                ("Bent-Over Barbell Row", "4 × 6-8", "2 dk", "Lat, Biceps", "Ağır"),
                ("Barbell Overhead Press", "3 × 8-10", "90 sn", "Deltoid", ""),
                ("Incline Dumbbell Press", "3 × 10-12", "60 sn", "Üst Göğüs", "Pump"),
                ("Lat Pulldown", "3 × 10-12", "60 sn", "Lat", ""),
                ("Cable Fly (Mid)", "3 × 12-15", "45 sn", "Göğüs izolasyon", ""),
                ("Barbell Curl + Tricep Pushdown", "3 × 12", "45 sn", "Kol", "Süperset"),
            ]
            alt_A = [
                ("Barbell Back Squat", "4 × 6-8", "2-3 dk", "Quadriceps, Glute", "Ağır — güç seti"),
                ("Romanian Deadlift (RDL)", "4 × 8-10", "90 sn", "Hamstrings, Glute", ""),
                ("Leg Press", "3 × 10-12", "90 sn", "Quadriceps, Glute", "Pump"),
                ("Lying Leg Curl", "3 × 12-15", "60 sn", "Hamstrings", ""),
                ("Hip Thrust", "3 × 12-15", "60 sn", "Gluteus Maximus", "Sıkıştır"),
                ("Standing Calf Raise + Seated Calf Raise", "4+4 × 15", "30 sn", "Gastrocnemius + Soleus", ""),
            ]
            ust_B = [
                ("Incline Dumbbell Press", "4 × 10-12", "90 sn", "Üst Göğüs", "Pump odaklı"),
                ("Lat Pulldown", "4 × 10-12", "90 sn", "Lat", ""),
                ("Arnold Press", "3 × 10-12", "60 sn", "Deltoid tüm başlar", ""),
                ("Cable Fly (Mid)", "3 × 12-15", "60 sn", "Göğüs izolasyon", "Strech"),
                ("Face Pull", "3 × 15-20", "45 sn", "Arka Delt, Rotator Cuff", "Zorunlu"),
                ("Lateral Raise", "3 × 15-20", "30 sn", "Medial Deltoid", ""),
                ("Hammer Curl + Skull Crusher", "3 × 12", "45 sn", "Brachialis + Triceps", "Süperset"),
            ]
            alt_B = [
                ("Conventional Deadlift", "4 × 5", "3 dk", "Full Posterior Chain", ""),
                ("Bulgarian Split Squat", "3 × 10/taraf", "90 sn", "Quadriceps, Glute", ""),
                ("Hip Thrust", "4 × 12-15", "60 sn", "Gluteus Maximus", ""),
                ("Leg Extension + Seated Leg Curl", "3 × 15", "45 sn", "Quad + Hamstring", "Süperset"),
                ("Standing Calf Raise", "5 × 15-20", "30 sn", "Baldır", ""),
                ("Ab Wheel Rollout", "3 × 10-15", "45 sn", "Core", ""),
            ]
            splits = [
                {"gun_adi": "Pazartesi — Üst Vücut A (Güç)", "egzersizler": ust_A},
                {"gun_adi": "Salı — Alt Vücut A (Güç)", "egzersizler": alt_A},
                {"gun_adi": "Perşembe — Üst Vücut B (Hacim)", "egzersizler": ust_B},
                {"gun_adi": "Cuma — Alt Vücut B (Hacim)", "egzersizler": alt_B},
            ]
        else:
            push = [
                ("Barbell Bench Press", "4 × 6-8", "2 dk", "Orta Göğüs", "Güç seti"),
                ("Incline Dumbbell Press", "4 × 10-12", "90 sn", "Üst Göğüs", "Pump"),
                ("Barbell Overhead Press", "4 × 8-10", "90 sn", "Deltoid", ""),
                ("Cable Fly (Mid)", "3 × 12-15", "60 sn", "Göğüs Strech", ""),
                ("Lateral Raise", "4 × 15-20", "45 sn", "Medial Deltoid", "Hafif"),
                ("Tricep Pushdown + Overhead Tricep Extension", "3 × 12-15", "45 sn", "Triceps", ""),
            ]
            pull = [
                ("Conventional Deadlift", "3 × 5", "3 dk", "Full Posterior Chain", "Ağır"),
                ("Pull-up", "4 × 8-10", "90 sn", "Lat", ""),
                ("Bent-Over Barbell Row", "4 × 8-10", "90 sn", "Orta Sırt", ""),
                ("Seated Cable Row", "3 × 10-12", "60 sn", "Lat + Orta Sırt", ""),
                ("Face Pull", "3 × 15-20", "45 sn", "Arka Delt, Rotator Cuff", "Omuz sağlığı"),
                ("Barbell Curl + Hammer Curl", "3 × 12-15", "45 sn", "Biceps, Brachialis", ""),
            ]
            legs = [
                ("Barbell Back Squat", "4 × 6-8", "2-3 dk", "Quadriceps, Glute", "Ağır"),
                ("Romanian Deadlift (RDL)", "4 × 10-12", "90 sn", "Hamstrings, Glute", ""),
                ("Leg Press", "3 × 12-15", "90 sn", "Quadriceps, Glute", ""),
                ("Bulgarian Split Squat", "3 × 10/taraf", "90 sn", "Quad, Glute", ""),
                ("Lying Leg Curl + Leg Extension", "3 × 15", "60 sn", "İzolasyon", "Süperset"),
                ("Hip Thrust", "3 × 15", "60 sn", "Gluteus Maximus", ""),
                ("Standing Calf Raise + Seated Calf Raise", "5 × 15-20", "30 sn", "Baldır", ""),
                ("Ab Wheel Rollout + Side Plank", "3 tur", "30 sn", "Core", ""),
            ]
            splits = [
                {"gun_adi": "Pazartesi — Push (Göğüs/Omuz/Triceps)", "egzersizler": push},
                {"gun_adi": "Salı — Pull (Sırt/Biceps/Arka Delt)", "egzersizler": pull},
                {"gun_adi": "Çarşamba — Legs (Bacak/Core)", "egzersizler": legs},
                {"gun_adi": "Perşembe — Push B", "egzersizler": push},
                {"gun_adi": "Cuma — Pull B", "egzersizler": pull},
                {"gun_adi": "Cumartesi — Legs B", "egzersizler": legs},
            ][:gun]
        splits = FitnessZekasi._uygula_filtro(splits, hafta, ekp, sev, "hipertrofi")
        return {
            "ad": f"{'Vücut Geliştirme' if hedef_str=='Vücut Geliştirme' else 'Kas Hipertrofisi'} — Blok {blok} (Hafta {hafta})",
            "gunler": f"{'Upper/Lower 4 gün' if gun==4 else ('PPL '+str(gun)+' gün' if gun>=5 else 'Full Body 3 gün')}",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for g in splits for e in g["egzersizler"]],
            "dinlenme": "60-90 sn hacim setleri, 2-3 dk güç setleri. Haftada 1-2 tam dinlenme.",
            "tavsiye": f"Blok {blok}: Progressive overload öncelikli. RIR 1-2 hedefle (neredeyse başarısızlık). Protein + uyku olmadan kas büyümez.",
            "kardiyo": "Haftada 1-2 × 20-30 dk LISS",
            "uyku_oneri": "8-9 saat. GH derine uyku fazında salgılanır.",
        }

    @staticmethod
    def _kuvvet_programi(sev, ekp, gun, hafta):
        blok = (hafta - 1) // 4 + 1
        yuzde = [75, 80, 85, 90][min((hafta - 1) % 4, 3)]
        temel = [
            ("Barbell Back Squat", f"5 × 3-5  @{yuzde}% 1RM", "3-4 dk", "Quadriceps, Glute, Core", "Ağır — teknik önce"),
            ("Barbell Bench Press", f"5 × 3-5  @{yuzde}% 1RM", "3-4 dk", "Göğüs, Triceps", "Güçlü taban"),
            ("Conventional Deadlift", f"3 × 3  @{yuzde}% 1RM", "4-5 dk", "Full Posterior Chain", "Haftanın en ağır seti"),
            ("Barbell Overhead Press", "4 × 5", "2-3 dk", "Deltoid, Triceps", "Yardımcı güç hareketi"),
            ("Bent-Over Barbell Row", "4 × 6", "2 dk", "Sırt güçlendirici", ""),
            ("Close-Grip Bench Press", "3 × 6-8", "2 dk", "Triceps — bench yardımcı", ""),
            ("Romanian Deadlift (RDL)", "3 × 8", "2 dk", "Hamstring yardımcı", ""),
            ("Face Pull", "3 × 15-20", "45 sn", "Rotator Cuff — zorunlu", "Omuz sağlığı"),
        ]
        gunler = {
            3: ["Pazartesi — Squat Ağırlıklı", "Çarşamba — Bench Ağırlıklı", "Cuma — Deadlift Ağırlıklı"],
            4: ["Pazartesi — Squat", "Salı — Bench", "Perşembe — Deadlift Yardımcı", "Cuma — OHP"],
            5: ["Pazartesi — Max Effort Squat", "Salı — Max Effort Bench", "Perşembe — Dynamic Effort DL", "Cuma — DE Bench", "Cumartesi — Yardımcı"],
        }
        splits = [{"gun_adi": gunler.get(gun, gunler[3])[i], "egzersizler": temel} for i in range(min(gun, len(gunler.get(gun, gunler[3]))))]
        splits = FitnessZekasi._uygula_filtro(splits, hafta, ekp, sev)
        return {
            "ad": f"Kuvvet Periodizasyon — Blok {blok} ({yuzde}% 1RM, Hafta {hafta})",
            "gunler": f"Haftada {gun} gün · Yüksek yoğunluk · Uzun mola",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for e in temel],
            "dinlenme": "3-5 dakika ağır setler arası.",
            "tavsiye": f"Bu hafta %{yuzde} 1RM. Kuvvet = CNS uyarlanması. Her 4. haftada deload zorunlu. RPE 8-9 hedefle.",
            "kardiyo": "Haftada 1-2 × 20 dk hafif yürüyüş",
            "uyku_oneri": "8+ saat. CNS toparlanması kritik.",
        }

    @staticmethod
    def _powerbuilding_programi(sev, ekp, gun, hafta):
        blok = (hafta - 1) // 4 + 1
        splits = [
            {"gun_adi": "Pazartesi — Squat Güç + Bacak Hacim", "egzersizler": [
                ("Barbell Back Squat", "4 × 4-6 (ağır)", "3 dk", "Quadriceps, Glute", "Güç seti"),
                ("Leg Press", "3 × 10-12", "90 sn", "Quadriceps", "Hacim pump"),
                ("Romanian Deadlift (RDL)", "3 × 10", "90 sn", "Hamstrings, Glute", ""),
                ("Bulgarian Split Squat", "3 × 10/taraf", "90 sn", "Quad, Glute", ""),
                ("Lying Leg Curl + Leg Extension", "3 × 12-15", "60 sn", "İzolasyon", "Süperset"),
                ("Standing Calf Raise", "4 × 15-20", "30 sn", "Baldır", ""),
            ]},
            {"gun_adi": "Salı — Bench Güç + Göğüs Hacim", "egzersizler": [
                ("Barbell Bench Press", "4 × 4-6 (ağır)", "3 dk", "Göğüs, Triceps", "Güç seti"),
                ("Incline Dumbbell Press", "3 × 10-12", "90 sn", "Üst Göğüs", "Hacim"),
                ("Cable Fly (Mid)", "3 × 12-15", "60 sn", "Göğüs izolasyon", ""),
                ("Barbell Overhead Press", "3 × 8-10", "90 sn", "Deltoid", ""),
                ("Lateral Raise", "3 × 15-20", "45 sn", "Medial Deltoid", ""),
                ("Tricep Pushdown + Skull Crusher", "3 × 12", "45 sn", "Triceps", "Süperset"),
            ]},
            {"gun_adi": "Perşembe — Deadlift Güç + Sırt Hacim", "egzersizler": [
                ("Conventional Deadlift", "3 × 3-5 (ağır)", "4 dk", "Full Posterior Chain", "Güç seti"),
                ("Pull-up", "4 × 8-10", "90 sn", "Lat", "Hacim"),
                ("Bent-Over Barbell Row", "4 × 8-10", "90 sn", "Orta Sırt", ""),
                ("Seated Cable Row", "3 × 10-12", "60 sn", "Lat + Orta Sırt", ""),
                ("Face Pull", "3 × 15-20", "45 sn", "Arka Delt, Rotator Cuff", "Zorunlu"),
                ("Barbell Curl + Hammer Curl", "3 × 12", "45 sn", "Biceps, Brachialis", ""),
            ]},
            {"gun_adi": "Cuma — Yardımcı + Zayıf Noktalar + Core", "egzersizler": [
                ("Close-Grip Bench Press", "3 × 8", "90 sn", "Triceps güçlendirici", ""),
                ("Hip Thrust", "3 × 12", "60 sn", "Gluteus Maximus", ""),
                ("Good Morning", "3 × 10", "60 sn", "Erektör + Hamstring", ""),
                ("Rear Delt Fly", "3 × 15", "45 sn", "Arka Deltoid", ""),
                ("Ab Wheel Rollout + Pallof Press + Side Plank", "3 tur", "30 sn", "Core", ""),
            ]},
        ]
        splits = FitnessZekasi._uygula_filtro(splits, hafta, ekp, sev, "powerbuilding")
        return {
            "ad": f"Powerbuilding — Blok {blok} (Hafta {hafta})",
            "gunler": f"Haftada {min(gun,4)} gün · Güç + Hacim Hibrid",
            "splits": splits[:min(gun, 4)],
            "program_liste": [(e[0], e[1], e[4]) for g in splits for e in g["egzersizler"]],
            "dinlenme": "Güç setleri: 3-4 dk. Hacim setleri: 60-90 sn.",
            "tavsiye": "Bileşik hareketlerde güç artışı + izolasyonla estetik. Her 4 haftada deload.",
            "kardiyo": "Haftada 1-2 × 20-30 dk orta yoğunluk",
            "uyku_oneri": "8 saat — güç + büyüme için kritik.",
        }

    @staticmethod
    def _kardiyo_programi(sev, ekp, gun, hafta):
        faz = "Temel" if hafta <= 6 else "İleri"
        devre = [
            ("Kettlebell Swing", f"3 × {'15' if sev=='baslangic' else '20'}", "30 sn", "Posterior Chain + Kardiyovasküler", "Kalçadan it"),
            ("Push Press", "3 × 10", "30 sn", "Omuz, Triceps, Core", "Dip + patlat"),
            ("Goblet Squat", "3 × 15", "20 sn", "Quadriceps, Glute", "Derin"),
            ("Farmer's Walk", "3 × 30 adım", "45 sn", "Trap, Core, Grip", "Dik dur"),
            ("Plank", "3 × 45 sn", "20 sn", "Core stabilizasyon", ""),
            ("Lunge", "3 × 12", "45 sn", "Quadriceps, Glute", "Tempo kontrol"),
        ]
        splits = [{"gun_adi": f"Gün {i+1} — Dayanıklılık Devresi ({faz})", "egzersizler": devre} for i in range(min(gun, 5))]
        splits = FitnessZekasi._uygula_filtro(splits, hafta, ekp, sev, "kardiyo")
        return {
            "ad": f"Kardiyo & Dayanıklılık — {faz} (Hafta {hafta})",
            "gunler": f"Haftada {gun} gün · Devre antrenmanı + LISS",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for e in devre],
            "dinlenme": "Devreler arası 30-45 sn, tam devre arası 2 dk.",
            "tavsiye": "HIIT 20-30 dk. LISS 40-60 dk × 2/hafta. Zone 2 kardiyo VO2max için.",
            "kardiyo": "Her gün: HIIT ↔ LISS ↔ aktif dinlenme",
            "uyku_oneri": "7-8 saat. Kardiyovasküler toparlanma uyku sırasında.",
        }

    @staticmethod
    def _fitkal_programi(sev, ekp, gun, hafta):
        liste = [
            ("Barbell Back Squat" if ekp == "salon" else "Goblet Squat", "3 × 12", "60 sn", "Bacak", ""),
            ("Barbell Bench Press" if ekp == "salon" else "Dumbbell Bench Press", "3 × 12", "60 sn", "Göğüs", ""),
            ("Bent-Over Barbell Row" if ekp == "salon" else "Dumbbell Row (One-Arm)", "3 × 12", "60 sn", "Sırt", ""),
            ("Dumbbell Shoulder Press", "3 × 12", "60 sn", "Omuz", ""),
            ("Romanian Deadlift (RDL)", "3 × 12", "60 sn", "Arka Zincir", ""),
            ("Plank + Ab Wheel Rollout", "3 tur", "30 sn", "Core", ""),
            ("Lateral Raise + Face Pull", "3 × 15", "30 sn", "Omuz dengesi", ""),
        ]
        splits = [{"gun_adi": f"Full Body {['A','B','C'][i%3]} — Genel Fitness", "egzersizler": liste} for i in range(gun)]
        splits = FitnessZekasi._uygula_filtro(splits, hafta, ekp, sev, "hipertrofi")
        return {
            "ad": f"Fit Kal — Genel Sağlık (Hafta {hafta})",
            "gunler": f"Haftada {gun} gün Full Body",
            "splits": splits,
            "program_liste": [(e[0], e[1], e[4]) for e in liste],
            "dinlenme": "60-90 sn setler arası.",
            "tavsiye": "Progressive overload ile her antrenman biraz daha zorlaştır. Antrenman sonrası 10 dk stretching.",
            "kardiyo": "Haftada 2-3 × 30 dk yürüyüş",
            "uyku_oneri": "7-8 saat.",
        }

    @staticmethod
    def _deload_programi(hafta):
        return {
            "ad": f"⚡ Deload Haftası (Hafta {hafta}) — Toparlanma",
            "gunler": "3 gün · %50-60 ağırlık · Teknik odak",
            "splits": [{"gun_adi": "Deload — Full Body Hafif (Teknik)", "egzersizler": [
                ("Barbell Back Squat", "3 × 5  @60% 1RM", "2 dk", "Quadriceps, Glute", "Sadece teknik"),
                ("Barbell Bench Press", "3 × 5  @60% 1RM", "2 dk", "Göğüs, Triceps", "Kontrollü"),
                ("Conventional Deadlift", "2 × 3  @60% 1RM", "2 dk", "Full Chain", "Form"),
                ("Bent-Over Barbell Row", "3 × 8 hafif", "90 sn", "Sırt", ""),
                ("Face Pull", "3 × 20", "45 sn", "Omuz sağlığı", ""),
                ("Plank + Dead Bug + Bird-Dog", "3 tur", "—", "Core + Mobilite", ""),
            ]}],
            "program_liste": [("Deload — Tüm hareketler %60", "3×5", "Sadece form")],
            "dinlenme": "Maksimum uyku ve beslenme kalitesi",
            "tavsiye": "Deload ZORUNLU. Adaptasyon dinlenirken olur. CNS, tendon, ligament bu haftada onarılır.",
            "kardiyo": "Sadece yürüyüş, yoga veya stretching",
            "uyku_oneri": "Bu hafta 9+ saat hedefle.",
        }

    @staticmethod
    def analiz_et(boy, kilo, yas, cinsiyet, seviye, hedef, aktivite,
                  baslangic_tarihi=None, ekipman=None, gun_sayisi=None):
        boy  = max(100, min(250, float(boy)))
        kilo = max(30,  min(300, float(kilo)))
        yas  = max(10,  min(100, int(yas)))
        ekipman    = ekipman    or "Spor Salonu (Tam Ekipman)"
        gun_sayisi = gun_sayisi or "3 Gün/Hafta"

        metre_boy = boy / 100
        vki = round(kilo / (metre_boy ** 2), 1)
        vki_kategori, vki_renk = FitnessZekasi.vki_kategori(vki)
        bmr  = round(FitnessZekasi.bmr_hesapla(kilo, boy, yas, cinsiyet))
        tdee = round(FitnessZekasi.tdee_hesapla(bmr, aktivite))
        hedef_kalori, kalori_aciklamasi = FitnessZekasi.kalori_hedefi(tdee, hedef)
        protein_g, karb_g, yag_g = FitnessZekasi.makro_hesapla(hedef_kalori, hedef, kilo)
        su = FitnessZekasi.su_ihtiyaci(kilo, aktivite)
        ideal_alt, ideal_ust = FitnessZekasi.ideal_agirlik(boy, cinsiyet)

        bf = FitnessZekasi.vucut_yag_tahmini(vki, yas, cinsiyet)
        bf_kategori, bf_renk = FitnessZekasi.yag_kategorisi(bf, cinsiyet)
        ffmi, ffmi_duz, kas_kilo = FitnessZekasi.ffmi_hesapla(kilo, boy, bf)
        ffmi_kategori, ffmi_renk = FitnessZekasi.ffmi_yorum(ffmi_duz, cinsiyet)

        hafta_sayisi = 1
        if baslangic_tarihi:
            try:
                basla = datetime.datetime.strptime(baslangic_tarihi, "%Y-%m-%d")
                hafta_sayisi = max(1, ((datetime.datetime.now() - basla).days // 7) + 1)
            except Exception:
                pass

        prog = FitnessZekasi.program_olustur(hedef, seviye, ekipman, gun_sayisi, hafta_sayisi)

        if vki < 18.5:
            vki_tavsiye = f"Kilonu artırman gerekiyor. Hedef: {ideal_alt}–{ideal_ust} kg."
        elif vki < 25:
            vki_tavsiye = f"Harika! İdeal aralıktasın ({ideal_alt}–{ideal_ust} kg)."
        elif vki < 30:
            vki_tavsiye = f"İdeale ulaşmak için yaklaşık {round(kilo-ideal_ust,1)} kg vermelisin."
        else:
            vki_tavsiye = f"Sağlıklı hedef: {round(kilo-ideal_ust,1)} kg azaltma. Doktorana danış."

        supps = []
        if hedef in ("Kas Yap", "Hızlı Kas Yap", "Vücut Geliştirme", "Güç + Hipertrofi", "Kuvvet Kazan"):
            supps = ["Kreatin Monohidrat (3-5g/gün) — kanıtlanmış güç + kütle artışı",
                     f"Whey Protein — {protein_g}g/gün proteine ulaşmak için",
                     "Kafein (100-200mg, antrenmandan 30-45 dk önce)"]
        elif hedef in ("Kilo Ver", "Hızlı Kilo Ver"):
            supps = [f"Whey Protein — kas korumak için günlük {protein_g}g şart",
                     "Kafein — termojenik + enerji",
                     "Omega-3 (2-3g/gün) — inflamasyon kontrolü"]
        elif hedef == "Kardiyo & Dayanıklılık":
            supps = ["Elektrolit (Na, K, Mg) — dayanıklılık performansı",
                     "Beta-Alanin (3-6g/gün) — dayanıklılık kapasitesi",
                     "Kafein (antrenmandan önce)"]

        return {
            "vki": vki, "vki_kategori": vki_kategori, "vki_renk": vki_renk, "vki_tavsiye": vki_tavsiye,
            "ideal_alt": ideal_alt, "ideal_ust": ideal_ust,
            "bmr": bmr, "tdee": tdee, "hedef_kalori": hedef_kalori, "kalori_aciklamasi": kalori_aciklamasi,
            "protein_g": protein_g, "karb_g": karb_g, "yag_g": yag_g, "su_lt": su,
            "hafta": hafta_sayisi,
            "bf_yuzde": bf, "bf_kategori": bf_kategori, "bf_renk": bf_renk,
            "ffmi": ffmi, "ffmi_duzeltilmis": ffmi_duz, "ffmi_kategori": ffmi_kategori, "ffmi_renk": ffmi_renk,
            "kas_kilo": kas_kilo, "yag_kilo": round(kilo * bf / 100, 1),
            "program_adi": prog["ad"],
            "program_gunler": prog["gunler"],
            "program_liste": prog["program_liste"],
            "program_splits": prog.get("splits", []),
            "program_dinlenme": prog.get("dinlenme", ""),
            "program_kardiyo": prog.get("kardiyo", ""),
            "program_uyku": prog.get("uyku_oneri", ""),
            "tavsiye": prog["tavsiye"],
            "hedef": hedef, "seviye": seviye, "ekipman": ekipman, "gun_sayisi": gun_sayisi,
            "supplementler": supps,
            "kas_anatomisi": KAS_ANATOMISI,
            "egzersiz_ansiklopedisi": EGZERSIZ_ANSIKLOPEDISI,
            "kas_ikon_map": KAS_IKON_MAP,
        }

    @staticmethod
    def ilerleme_analizi(gecmis_listesi):
        if len(gecmis_listesi) < 2:
            return None
        son = gecmis_listesi[-1]; ilk = gecmis_listesi[0]
        kilo_fark = round(son.get("kilo", 0) - ilk.get("kilo", 0), 1)
        vki_fark  = round(son.get("vki", 0)  - ilk.get("vki", 0), 1)
        gun_fark  = 0
        try:
            gun_fark = (datetime.datetime.strptime(son["tarih"], "%Y-%m-%d") -
                        datetime.datetime.strptime(ilk["tarih"], "%Y-%m-%d")).days
        except Exception:
            pass
        return {
            "kilo_fark": kilo_fark, "vki_fark": vki_fark, "gun_fark": gun_fark,
            "kayit_sayisi": len(gecmis_listesi),
            "yonelim": "artıyor" if kilo_fark > 0 else ("azalıyor" if kilo_fark < 0 else "sabit"),
        }

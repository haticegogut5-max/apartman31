# Daire 31 (Apartment 31)

Birinci şahıs, psikolojik gözetleme-korku oyunu. Tarayıcıda çalışır (WebGL, **three.js r128**, derleme adımı yok).
Oyuncu, 1990'lar Rusya'sında bakımsız 6 katlı bir apartmanın **gece bekçisi**dir. Silah yok, dövüş yok: gözlem, kanıt toplama ve rapor kararları var.
Tasarım belgesi: `docs/GDD_original_main.pdf` (özgün) + `docs/GDD_Revision2.pdf` (paranormal tırmanış ve siluet kuralları; çelişkide Revision 2 geçerli).

## Durum
- Oynanabilir: **Gece 1–7**. Yok: Gece 8–10, üç son (A/B/C), kaydet/yükle, duraklatma menüsü ayarları.
- Dil: Türkçe + İngilizce (`L` tuşu / buton). Metinler `TX` tablosunda.
- Çalıştırma: `python3 -m http.server 8000` → http://localhost:8000/index.html (three.js CDN'den gelir: `cdnjs ... three.js/r128/three.min.js`).

## Oynanış / özellikler
- **Vardiya döngüsü:** kameraları kontrol et (3 CCTV beslemesi) → telefonu aç → devriye (3 zaman kartı, her gece) → sakinlerle konuş → ipuçlarını **deftere** yaz (Tab / 📓) → **vardiya raporu**nda hangi gözlemleri bildireceğini seç.
- **Geceler:** 1 yeni vardiya + telefon uyarısı · 2 kamerada siluet + gizli kayıt dolabı · 3 dört sakinle kapı kapı tanıklık · 4 31 numaralı daire (45 sn zaman sınırı, 3 nesne) · 5 bodrum arşivi · 6 telefondaki kadın (diyalog seçimi) · 7 beşinci kat (servis geçidi).
- **Sakinler:** Viktor (yaşlı adam, 28), Galina (30), Lena (29), Nadya (27). Kapı açılır, sakin eşikte durur, alt baloncukta konuşur, kapı kapanır. Daire içleri kapıdan görünür (girilemez).
- **Korku sistemi:** geceye göre sabit **siyah siluet bütçesi** (0/1/2) ve yerleşim kuralları (GDD Rev.2); korku tepkisi (kamera sarsıntısı, FOV, titreme, kalp atışı); rastgele ambiyans olayları (vuruş, ayak sesi, ışık söner, kapı aralanır, fısıltı); rahatlık ayarları (sarsıntı / titreme / FOV efekti) başlık ekranında.
- **Kontroller:** W A S D + fare (sürükle) · E etkileşim · Tab defter · L dil · Esc duraklat · Telefon: sol başparmak yürü, sağ başparmak bak, E ve 📓 düğmeleri.

## Teknoloji ve kütüphaneler
- **three.js r128** (CDN) — tek harici kütüphane. Ses: WebAudio ile sentez (ses dosyası yok).
- Dokular çoğunlukla **canvas ile prosedürel** üretilir (duvar kâğıdı, zemin, kapı, tablo). Geometri: `BoxGeometry` ağırlıklı.
- Malzemeler: `MeshPhongMaterial` (ortam) + `MeshStandardMaterial` (GLB karakter). Işıklar: ~7 `PointLight`. Gölge kapalı.
- **Özel post-process:** sahne `WebGLRenderTarget`'a çizilir, sonra tam ekran `ShaderMaterial` ile grain, vinyet, lens bozulması, kromatik sapma, hafif blur.
- **Kamera beslemeleri (CCTV):** ikinci kamerayla sahne çizilir, 2D canvas'a kopyalanır, siyah-beyaza çevrilir.
- Karakter verisi: Python araçları (`tools/`, numpy + Pillow) GLB'lerden ağ/doku paketler → `js/model_galina.js`, `js/models_chars.js` (base64 ikili biçim).

## Dosya haritası
| Dosya | İçerik |
|---|---|
| `index.html` | HTML iskeleti, CSS, UI katmanları, script etiketleri |
| `js/game.js` | Tüm oyun mantığı (533 satır; bölümler aşağıda) |
| `js/model_galina.js` | `window.GAL`: orijinal `textured_mesh.glb` (tam çözünürlük ağ + 6 parça grubu + renk/metal-pürüzlülük JPEG'leri) |
| `js/models_chars.js` | `window.MODELS`: Lena (`m2`) ve Nadya (`m3`) vertex-color ağları (`m1` eski, kullanılmıyor) |
| `tools/*.py` | GLB → paket dönüştürücüler (`gal.py`, `bake.py`, `proc.py`, `glbv.py`) |
| `tools/smoke_test.js` | Tarayıcısız yükleme testi (`node tools/smoke_test.js`) |
| `assets/source_models/` | 4 orijinal GLB (`textured_mesh`, `white_mesh`, `white_mesh_1`, `white_mesh__1_`) |
| `assets/reference/` | Hedef görseller (`TARGET_*`), mevcut hatalı görüntüler (`ingame_*`), hata kayıtları (`bug_*.mp4`) |
| `docs/` | GDD PDF'leri, gölge planı tablosu, bu README, bilinen sorunlar, Claude Code başlangıç istemi |

## `js/game.js` bölümleri (satır no)
40 3D sahne/geometri · 107 etkileşimler (`IT` listesi) · 139 CCTV · 162 ses · 165 UI · 180 girdi · 196 dokunmatik · 204 korku olayları · 225 insanlar+diyalog (`speak`, `emerge`) · 246 beşinci kat · 268 siluet bütçesi + korku tepkisi · 278–398 **görsel "yama" katmanları** (cinematic / reference-match / reference target / tone correction; sonraki blok öncekini ezer) · 398 daireler, merdiven, `person2` · 437 `person3` · 473–496 GLB karakterler · 496 ana döngü (`frame`).

## Oyun durum kodu (`S.stage`)
Gece N için aşamalar: N1: 0–5, N2: 10–12, N3: 20–22, N4: 30–32, N5: 40–44, N6: 50–52, N7: 60–66. Bitiş ekranları: 6, 16, 26, 36, 46, 56, 76. Rapor aşamaları: 5, 12, 22, 32, 44, 52, 66 (devriye 3/3 gerekir).

# Bilinen sorunlar ve istenen düzeltmeler

**Önemli not:** Bu oyun, tarayıcısı olmayan bir ortamda yazıldı. Hiçbir görsel değişiklik gerçek tarayıcıda otomatik doğrulanmadı; yalnızca kod okuma, sahte (stub) yükleme testi (`tools/smoke_test.js`) ve senin ekran görüntülerinle kontrol edildi. Aşağıdaki "doğrulanmadı" ifadeleri bunu gösterir.

## P0 — Önce bunlar
1. **GLB karakter (Galina) dokusu doğrulanmadı.** Kod `js/model_galina.js`'teki renk (JPEG 2048²) ve metal/pürüzlülük (JPEG 2048²) dokularını `Image` ile yükleyip 6 parçalı `MeshStandardMaterial`'e bağlıyor. Başlık ekranında `GLB NPC: ...` satırı yükleme durumunu yazar (`yüklendi`/`HATA`). Gerçek tarayıcıda görünmeli ve görsel olarak doğrulanmalı. *İstenen:* dokular doğru yüklensin, cilt/saç/kazak/etek/çorap/ayakkabı ayrı PBR hissi versin, bulanık ölçekleme olmasın.
2. **Karakter yüzleri kötü, yamuk, okunmuyor** (kullanıcının asıl şikayeti). Nedenler: (a) Lena/Nadya `white_mesh*.glb` dokusuz; ben **vertex color** ile boyadım ve ağı 12 mm ızgarayla sadeleştirdim → yüzde çok az köşe var, yüz/saç sınırı konuma göre kaba kuralla boyandı. (b) Kaynak ağlar yapay zekâ üretimi; yüzleri zaten kaba. (c) Viktor (yaşlı erkek) hâlâ ilkel şekillerden (`person3`) ve referansla alakasız; elimizde erkek GLB yok. *İstenen:* referans görsellere (`assets/reference/character_refs/TARGET_*`) birebir benzeyen 4 karakter: 3 kadın + 1 yaşlı adam (kel, gri kirli sakal, koyu kareli flanel gömlek), 1990'lar Moskova/Sovyet giyim.
3. **Işık/okunabilirlik tutarsız.** Koridor zaman zaman fazla turuncu-kırmızı, zaman zaman çok karanlık; kapıdaki karakterin yüzü seçilmiyor. *İstenen:* korku atmosferi kalsın ama yüz ve kıyafet net okunsun; nötr yumuşak dolgu ışığı; kırmızı renk sapması azalsın. (Kodda `fillL` nötr dolgu ışığı ve nötre yakın post-process tonu eklendi, **doğrulanmadı**.)
4. **Yürürken "geri ışınlanma"/takılma.** Kök neden bulunamadı. Kodda oyuncu konumunu geri yazan bir yer yok (konum yalnızca hareket ve gece geçişlerinde değişir); kayıtta (`assets/reference/bug_walk_snapback_stutter.mp4`) kare düşmesi + telafi izi var. Adaptif piksel oranı eklendi (kare süresi yüksekse çözünürlük düşer). *İstenen:* hatayı kayıttan yeniden üret, gerçek nedeni bul (çarpışma mı, takılma mı, joystick mi), düzelt.

## P1 — Grafik kalitesi
5. **Dünya hâlâ basit/kutu gibi.** Duvar, kapı, mobilya `BoxGeometry`; dokular canvas ile prosedürel. Hedef: `assets/reference/TARGET_reference_corridor_PT_style.png` (koyu kırmızı-turuncu çiçekli duvar kâğıdı, krem/beyaz panelli eski kapılar + üstte vasistas, koyu parlak ahşap zemin, küçük portre, dar klostrofobik koridor, sıcak loş ışık, hafif grain). *İstenen:* gerçek model/doku (ücretsiz CC0: Poly Haven, ambientCG) veya çok daha iyi prosedürel doku; kare ışık lekesi yok; gerçekçi yumuşak ışık düşüşü ve temas gölgeleri.
6. **Duvar kâğıdı deseni** ölçeği ve tekrarı hâlâ yapay (büyük kutu duvarlara aynı doku `repeat` ile sarılıyor, UV ölçeği yüzeye göre değil).
7. **Daire içleri** (kapı arkası) çok basit; girilemez.
8. **Merdiven boşluğu** (lobinin sağı) sadece görsel; 5. kata çıkış Gece 7'de teleportla yapılıyor; bodrum da teleport.

## P1 — Performans
9. Telefonda ağır: ~7 `PointLight` + per-pixel Phong/Standard + tam ekran post-process; sayfa 4,4 MB (base64 modeller). Gölgeler kapalı. *İstenen:* ölç, mobil için kalite seviyesi, modelleri ayrı ikili dosya olarak yükle.

## P2 — Eksik oyun içeriği
10. Gece 8–10, üç son (A/B/C), kaydet/yükle, duraklatma menüsünde ayarlar (şu an yalnız başlık ekranında), sakin diyaloglarının çeşitliliği.
11. Siluet zamanlaması belgeden farklı: `SIL_FIRST=45`, `SIL_GAP=60` sn (GDD: 180/300).
12. Yerelleştirme: çoğu metin `TX` içinde ama tabela canvas yazıları iki dilli sabit.
13. Çarpışma: görünmez sınırlar (`ok(x,z)`), nesnelerle çarpışma yok (masa dışında).
14. Hedef işaret topları (altın küreler) yakından ekranı kaplayabiliyor.

## P3 — Kod kalitesi
15. **Yama katmanlı kod:** görseller defalarca üst üste atanıyor; ölü kod: `person` / `person2` / `person3` (üç sürüm), `spawnFig`, `wT` / `wpT` / `wpT2` / `wpT3` (dört duvar dokusu), `drT` / `drT2` / `drT3`, post-process shader'ı dört kez yeniden yazılıyor. Tek `game.js` dosyası (533 satır, uzun satırlar). Test yok.
16. CCTV: ikinci kamerayla ana renderer'a çizip `getImageData` ile gri tonlama (her karede, yavaş).
17. Ses tamamen sentetik (WebAudio), gerçek ses dosyası yok.

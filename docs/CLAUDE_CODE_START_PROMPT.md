Merhaba. Bu klasörde "Daire 31" adlı, three.js r128 ile yazılmış, tarayıcıda çalışan birinci şahıs psikolojik korku oyunu var. Proje başka bir ortamda tarayıcı olmadan geliştirildi, yani hiçbir görsel değişiklik gerçek tarayıcıda doğrulanmadı. Senin ilk görevin bunu doğrulamak.

AŞAMA 0 — Önce incele, hiçbir şeyi değiştirme
1. docs/README.md, docs/KNOWN_ISSUES.md oku. docs/GDD_original_main.pdf ve docs/GDD_Revision2.pdf tasarım belgeleridir (çelişkide Revision 2 geçerli).
2. index.html ve js/game.js'i baştan sona oku (533 satır; bölümler README'de). tools/ altındaki Python scriptlerine ve js/model_galina.js / js/models_chars.js başlık satırlarına bak (dosyalar büyük base64'tür, içini okuma).
3. assets/reference/ altındaki görselleri aç ve incele: TARGET_reference_corridor_PT_style.png = hedef koridor görünümü; character_refs/TARGET_* = hedef karakterler; ingame_*.png = şu anki hatalı hâller; bug_*.mp4 = hata kayıtları.
4. Bana en fazla 10 satırlık özet ve düzeltme planı yaz, sonra devam et.

ÇALIŞMA KURALLARI
- `git init` yap, her düzeltmeyi ayrı commit yap.
- Oyunu çalıştırmak için: `python3 -m http.server 8000` ile sun, Playwright (Chromium, WebGL açık; gerekirse `--use-gl=swiftshader` veya `--use-angle=swiftshader`) ile aç. Konsol hatalarını ve ekran görüntülerini otomatik topla. three.js CDN'e erişemiyorsan r128 sürümünü js/vendor/three.min.js olarak indirip index.html'i buna çevir (sürümü değiştirme).
- Her adımdan sonra oyunu çalıştır, ekran görüntüsü al, hedef görselle karşılaştır ve sonucu yaz. Bir şeyi görmeden "düzeldi" deme; göremediysen açıkça "doğrulanamadı" yaz.
- Oynanışı, hikâyeyi, oda numaralarını, kapıları ve seviye yapısını değiştirme. Büyük yeniden yazımdan önce planı yaz ve bana sor.
- Karakterlere animasyon, iskelet, yürüme EKLEME: sakinler kapı eşiğinde statik poz ile durur.
- Telefonda da çalışmalı (dokunmatik joystick). Performansı ölç ve rapor et.
- Uydurma yer tutucu karakter/model yapma. Eksik varlık varsa (ör. yaşlı erkek GLB) bana sor.

SIRA (en önemliden)
1. Test düzeneği + konsolda hata yok. Başlık ekranındaki "GLB NPC: ..." satırına bak: Galina'nın GLB dokuları gerçekten yükleniyor mu? Yüklenmiyorsa nedenini bul ve düzelt.
2. Galina (GLB) kapı eşiğinde net görünsün: yüz okunur, kıyafet dokuları görünür, parçalara ayrı PBR hissi, bulanık ölçekleme yok, kapıya/duvara/zemine girme yok, gerçekçi insan ölçeği. Işık: korku atmosferi kalsın ama karakter okunsun; turuncu/kırmızı renk sapması azalsın; nötr yumuşak dolgu ışığı.
3. Lena ve Nadya (assets/source_models/white_mesh*.glb): vertex-color yerine uygun doku (UV + elle/projeksiyonla boyama) ya da daha iyi yüz. Viktor'u (yaşlı adam) character_refs/TARGET_old_man_bald_plaid_shirt.jpeg'e benzet. Erkek GLB yoksa bana sor.
4. Koridoru TARGET_reference_corridor_PT_style.png'ye yaklaştır: koyu kırmızı çiçekli duvar kâğıdı (doğru ölçek), krem panelli kapılar, vasistas, parlak koyu ahşap zemin, portreler, yumuşak ışık düşüşü, kare ışık lekesi yok, hafif grain.
5. Yürürken geri ışınlanma/takılma: assets/reference/bug_walk_snapback_stutter.mp4'ten yeniden üret, gerçek nedeni bul, düzelt.
6. Performans/mobil: kare süresini ölç, kalite seviyeleri, modelleri ayrı dosyaya al.
7. Kod temizliği: ölü kod (person/person2, spawnFig, eski dokular, tekrarlanan shader atamaları) temizle, game.js'i modüllere böl; her adımdan sonra tools/smoke_test.js ve tarayıcı testi geçsin.

Her adımın sonunda şunu yaz: ne yaptın, neyi çalıştırdın, hangi ekran görüntüsünü aldın, neyi doğrulayamadın.

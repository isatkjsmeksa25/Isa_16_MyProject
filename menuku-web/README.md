# MenuKu Web / PWA

MenuKu versi web dan PWA, terpisah dari aplikasi Kivy.

## Struktur

```text
public/          # file statis yang dilihat pengguna
  index.html
  style.css
  app.js
  manifest.webmanifest
  service-worker.js
  icons/
api/
  index.py       # endpoint Python untuk rekomendasi
python/          # salinan logic Python dari MenuKu
requirements.txt
```

## Cara Menjalankan Lokal

```powershell
python api/index.py
```

Buka:

```text
http://localhost:8000
```

## Deploy ke Vercel

1. Push folder `menuku-web` ke GitHub.
2. Buka [vercel.com](https://vercel.com).
3. Pilih **Add New → Project**.
4. Import repository GitHub.
5. Set root directory ke `menuku-web`.
6. Framework preset: **Other**.
7. Klik **Deploy**.

Vercel akan otomatis:
- serve file statis di `public/`
- menjalankan endpoint Python di `api/index.py`

## PWA / Install

Setelah dibuka di browser (Chrome/Edge/Safari), pengguna bisa memilih:

- **Install app**, atau
- **Add to Home Screen**

Aplikasi akan muncul seperti aplikasi biasa di HP atau laptop.

## Catatan

- Folder ini terpisah dari aplikasi Kivy.
- File Python disalin ke `python/` supaya Vercel bisa membacanya.
- Logic rekomendasi tetap Python.

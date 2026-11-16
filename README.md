# Isa_16_MyProject

# MenuKu

MenuKu adalah aplikasi rekomendasi menu makanan berdasarkan bahan yang tersedia. Aplikasi ini dibuat dengan Python dan Kivy.

> **Status proyek:** Fase pengembangan selesai untuk versi Windows. Android dan iOS memerlukan alat build tambahan.

## Tujuan

Membantu pengguna menemukan ide masakan dari bahan-bahan yang ada di dapur.

## Fitur Utama

- Memasukkan daftar bahan, termasuk beberapa bahan sekaligus.
- Normalisasi nama bahan dan alias (`cabe` -> `cabai`, `brambang` -> `bawang merah`, dan lain-lain).
- Pengecekan keamanan bahan berisiko, misalnya siput, ikan buntal, jamur liar, dan hewan liar.
- Rekomendasi resep katalog berdasarkan bahan yang tersedia.
- Rekomendasi alternatif berbasis template jika katalog tidak cocok.
- Menampilkan bahan yang cocok dan bahan yang kurang.
- Langkah memasak ditampilkan di popup detail resep.
- Tombol Menu Acak untuk memilih resep secara acak.
- Penghapusan bahan dan pembaruan rekomendasi otomatis.
- Tes otomatis dengan `unittest`.

## Teknologi

- **Bahasa pemrograman:** Python 3
- **Framework UI:** Kivy
- **Pengujian:** `unittest`
- **Packaging Windows:** PyInstaller
- **Android:** Buildozer (membutuhkan Linux/WSL)

## Cara Menjalankan dari Source Code

1. Pastikan Python 3 sudah terpasang.
2. Buat virtual environment:

   ```powershell
   python -m venv .venv
   ```

3. Aktifkan virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Instal dependensi:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Jalankan aplikasi:

   ```powershell
   .\.venv\Scripts\python.exe main.py
   ```

## Cara Membuat File `.exe` Windows

```powershell
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\pyinstaller --noconsole --onefile main.py
```

Hasilnya tersedia di:

```text
dist\main.exe
```

File `.exe` bisa dijalankan tanpa Python terpasang.

## Cara Menjalankan Pengujian

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -t . -v
```

Saat ini 78 tes lulus.

## Struktur Proyek

```text
recipe_data.py             # katalog 25 resep
ingredients.py             # normalisasi dan alias bahan
food_safety.py             # keamanan bahan berisiko
recommendation.py          # mesin rekomendasi katalog
recipe_templates.py        # template alternatif
template_recommendation.py # rekomendasi fallback berbasis template
main.py                    # UI Kivy
tests/                     # unit test
```

## Batasan

- Versi Windows sudah bisa dijalankan langsung.
- Android membutuhkan Buildozer dan WSL/Linux.
- iOS membutuhkan macOS, Xcode, dan Apple Developer account.
- Rekomendasi bersifat ide masak, bukan jaminan keamanan pangan.

## Lisensi

Proyek ini menggunakan MIT License. Lihat [LICENSE](LICENSE).

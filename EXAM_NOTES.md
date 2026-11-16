# Catatan Ujian MenuKu

## Satu Menit Perkenalan

“MenuKu adalah aplikasi rekomendasi menu masakan berdasarkan bahan yang tersedia. Aplikasi ini dibuat dengan Python dan Kivy. Pengguna memasukkan bahan, lalu aplikasi mencocokkan dengan katalog 25 resep dan beberapa template alternatif. Aplikasi juga memeriksa keamanan bahan, misalnya siput, ikan buntal, jamur liar, dan hewan liar.”

## Cara Menjelaskan Fitur Utama

1. **Input bahan** — pengguna mengetik bahan seperti `nasi, telur, bawang putih`.
2. **Normalisasi** — aplikasi mengubah nama bahan seperti `cabe -> cabai`.
3. **Keamanan** — bahan berisiko tidak dipakai untuk rekomendasi.
4. **Rekomendasi katalog** — minimal satu bahan utama cocok.
5. **Rekomendasi alternatif** — template dipakai jika katalog tidak cocok.
6. **Detail resep** — tombol `Lihat Detail Masakan` menampilkan langkah memasak.
7. **Menu Acak** — memilih rekomendasi secara acak.
8. **Tests** — 78 unit test, semua lulus.

## Cara Demo ke Guru

1. Buka `dist\main.exe`.
2. Masukkan `nasi, telur, bawang putih`.
3. Klik `Tambah`.
4. Klik `Cari Resep`.
5. Klik `Lihat Detail Masakan`.
6. Klik `Tutup`.
7. Klik `Menu Acak`.
8. Coba input `keong, fugu` untuk menunjukkan peringatan keamanan.
9. Coba input `brambang, tahu, tempe, kecap` untuk menunjukkan alternatif.

## Kalau Ditanya “Kenapa Python?”

“Python mudah dipelajari dan cocok untuk proyek ini karena datanya sederhana. UI-nya dibuat dengan Kivy sehingga bisa dijalankan di desktop dan Android nanti.”

## Kalau Ditanya “Kenapa belum Android/iPhone?”

“Android butuh Buildozer dan Linux/WSL. iPhone butuh macOS dan Xcode. Jadi untuk versi ini saya fokus ke Windows dulu.”

## Kalau Ditanya “Apa kelemahan aplikasi?”

“Aplikasinya masih terbatas pada bahan yang ada di katalog dan keamanan bahan bersifat konservatif, bukan jaminan aman.”

## Ringkasan untuk Diucapkan Saat Ujian

“Aplikasi ini membantu pengguna memasak dari bahan yang tersedia. Saya membuat normalisasi bahan, filter keamanan, mesin rekomendasi, dan tampilan hasil. Semua fungsi utama diuji dengan 78 unit test. Untuk distribusi Windows, saya mengemasnya menjadi file .exe dengan PyInstaller.”

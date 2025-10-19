# Presensi PMC — Panduan Deploy di Render

## Langkah 1 — Upload ke GitHub
1. Buka [https://github.com](https://github.com) dan login.
2. Buat repository baru, misalnya `presensi-pmc`.
3. Upload seluruh isi folder proyek ini (termasuk file `render.yaml`).
4. Klik **Commit changes**.

## Langkah 2 — Deploy ke Render
1. Buka [https://render.com](https://render.com) dan login pakai GitHub.
2. Klik **New + → Web Service**.
3. Pilih repository `presensi-pmc` yang baru kamu buat.
4. Render otomatis mendeteksi file `render.yaml`.
5. Klik **Create Web Service** dan tunggu proses build.

## Langkah 3 — Akses Aplikasi
Setelah deploy selesai, Render akan memberi URL seperti:
```
https://presensi-pmc.onrender.com
```
Buka URL tersebut di HP kamu, dan aplikasi siap digunakan!

### Tips
- Render menggunakan domain HTTPS gratis.
- Kamera dan GPS bisa langsung digunakan via browser HP.
- Untuk kinerja stabil, buka aplikasi minimal sekali setiap 15 menit agar tidak tertidur (sleep mode).

Selamat mencoba 🚀

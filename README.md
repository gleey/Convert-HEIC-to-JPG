# Convert HEIC to JPG

Script Python sederhana untuk mengonversi gambar berformat HEIC/HEIF ke JPG dengan kualitas maksimum, serta otomatis menghapus file HEIC asli setelah berhasil dikonversi.

## Fitur Utama

- **Kualitas Maksimum:** Menggunakan opsi `quality=100` dan menonaktifkan chroma subsampling (`subsampling=0`) agar hasil JPG sedekat mungkin dengan gambar asli.
- **Auto-Cleanup:** Menghapus file asli `.HEIC` / `.HEIF` setelah sukses dikonversi atau jika file `.jpg` dengan nama yang sama sudah ada di folder tersebut.
- **Penanganan Batasan JPEG EXIF:** Jika metadata EXIF pada file HEIC melebihi batas ukuran JPEG (65.535 bytes), script secara otomatis menyimpan gambar tanpa EXIF untuk mencegah kegagalan konversi, namun tetap menjaga kualitas gambar asli.

## Prasyarat

Pastikan Anda telah menginstal Python 3 di sistem Anda.

## Instalasi Library yang Dibutuhkan

Pasang library `pillow` dan `pillow-heif` terlebih dahulu menggunakan `pip`:

```bash
pip install pillow pillow-heif
```

## Cara Penggunaan

Jalankan script dengan menentukan path folder foto yang ingin dikonversi sebagai argumen:

```bash
python convert.py "/path/ke/folder/foto"
```

> **Catatan:** Jika argumen path folder tidak diisi, script akan berjalan pada folder aktif saat ini (working directory).

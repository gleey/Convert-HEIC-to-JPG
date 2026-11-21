# Convert HEIC to JPG

Script Python sederhana untuk mengonversi gambar berformat HEIC/HEIF ke JPG dengan kualitas maksimum, serta otomatis menghapus file HEIC asli setelah berhasil dikonversi.

## Fitur Utama

- **Kualitas Maksimum:** Menggunakan opsi `quality=100` dan menonaktifkan chroma subsampling (`subsampling=0`) agar hasil JPG sedekat mungkin dengan gambar asli.
- **Auto-Cleanup:** Menghapus file asli `.HEIC` / `.HEIF` setelah sukses dikonversi atau jika file `.jpg` dengan nama yang sama sudah ada di folder tersebut.
- **Penanganan Batasan JPEG EXIF:** Jika metadata EXIF pada file HEIC melebihi batas ukuran JPEG (65.535 bytes), script secara otomatis menyimpan gambar tanpa EXIF untuk mencegah kegagalan konversi, namun tetap menjaga kualitas gambar asli.

## Prasyarat

Pastikan Anda telah menginstal Python 3 di sistem Anda.

## Instalasi Library yang Dibutuhkan

Pasang library yang diperlukan dalam virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Cara Penggunaan

### GUI dengan drag-and-drop

Jalankan tanpa argumen:

```bash
.venv/bin/python convert.py
```

Kemudian seret foto atau folder berisi HEIC/HEIF ke jendela, atau gunakan tombol
**Pilih Foto** dan **Pilih Folder**.

### Mode command-line

Jalankan dengan menentukan path folder foto sebagai argumen:

```bash
.venv/bin/python convert.py "/path/ke/folder/foto"
```

> **Catatan:** Jika argumen tidak diberikan, aplikasi membuka GUI. Untuk mode CLI,
> folder yang diberikan beserta subfoldernya dipindai secara rekursif.

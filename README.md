# Convert HEIC to JPG

Script Python sederhana untuk mengonversi gambar berformat HEIC/HEIF ke JPG dengan kualitas maksimum, serta otomatis menghapus file HEIC asli setelah berhasil dikonversi.

## Fitur Utama

- **Kualitas Maksimum:** Menggunakan opsi `quality=100` dan menonaktifkan chroma subsampling (`subsampling=0`) agar hasil JPG sedekat mungkin dengan gambar asli.
- **Auto-Cleanup:** Menghapus file asli `.HEIC` / `.HEIF` setelah sukses dikonversi atau jika file `.jpg` dengan nama yang sama sudah ada di folder tersebut.
- **Penanganan Batasan JPEG EXIF:** Jika metadata EXIF pada file HEIC melebihi batas ukuran JPEG (65.535 bytes), script secara otomatis menyimpan gambar tanpa EXIF untuk mencegah kegagalan konversi, namun tetap menjaga kualitas gambar asli.

## Prasyarat

Pastikan Anda telah menginstal Python 3 di sistem Anda.

## Menggunakan aplikasi tanpa Python

Unduh build untuk OS Anda dari halaman
[Releases](https://github.com/gleey/Convert-HEIC-to-JPG/releases/latest).
Python dan library tidak perlu dipasang. Konversi berjalan di komputer Anda;
foto tidak diunggah ke server.

- **Windows x64:** jalankan `Convert-HEIC-to-JPG-windows-x64.exe`.
- **Linux x64:** ekstrak `Convert-HEIC-to-JPG-linux-x64.tar.gz`, lalu jalankan:

  ```bash
  chmod +x Convert-HEIC-to-JPG-linux-x64
  ./Convert-HEIC-to-JPG-linux-x64
  ```

  Build Linux dibuat di Ubuntu 22.04; distro yang lebih lama mungkin tidak
  memiliki versi library sistem yang kompatibel.

Jika belum ada file di halaman Releases, berarti belum ada build yang diterbitkan.
Build dapat dibuat dari tab **Actions** dengan menjalankan workflow
**Build desktop apps**; file Windows dan Linux tersedia sebagai artifact. Untuk
menerbitkan keduanya agar tersedia di Releases, buat dan push tag versi,
misalnya `v1.0.0`.

Menjalankan `convert.py` langsung dari hasil clone tetap memerlukan Python dan
library di bawah ini. File `.exe` adalah hasil build terpisah, bukan bagian dari
clone source code.

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

## Membuat build lokal

Build lokal hanya perlu dilakukan oleh pengembang, bukan pengguna aplikasi hasil
rilis. Gunakan Python 3.12 pada OS target.

### Windows (PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-build.txt
.\.venv\Scripts\pyinstaller --noconfirm --clean --onefile --windowed `
  --name Convert-HEIC-to-JPG-windows-x64 --collect-all pillow_heif `
  --collect-all tkinterdnd2 convert.py
```

### Linux (Bash)
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-build.txt
.venv/bin/pyinstaller --noconfirm --clean --onefile --windowed \
  --name Convert-HEIC-to-JPG-linux-x64 --collect-all pillow_heif \
  --collect-all tkinterdnd2 convert.py
tar -C dist -czf dist/Convert-HEIC-to-JPG-linux-x64.tar.gz \
  Convert-HEIC-to-JPG-linux-x64
```

File hasil build akan berada di `dist`. Setiap sistem operasi memerlukan build
tersendiri; workflow di GitHub Actions membangun versi Windows dan Linux.

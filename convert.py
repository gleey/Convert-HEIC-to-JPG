#!/usr/bin/env python3
"""
Convert semua file HEIC dalam folder ke JPG dengan kualitas maksimum.

Cara pakai:
    python convert_heic_to_jpg.py /path/ke/folder/foto

Jika argumen path tidak diisi, script akan memakai folder saat ini.

Catatan penting:
- JPG adalah format lossy, jadi "tanpa perubahan kualitas" secara harfiah
  tidak mungkin. Script ini menggunakan quality=100 dan subsampling=0
  (chroma subsampling dimatikan) supaya hasilnya sedekat mungkin dengan
  gambar asli.
- Metadata EXIF ikut tersalin jika tidak melewati batas.
- File asli (.heic) akan dihapus. Hasil JPG disimpan di folder yang sama
  dengan nama file yang sama, ekstensi berbeda.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    print("Library yang dibutuhkan belum terpasang.")
    print("Install dulu dengan:")
    print("    pip install pillow-heif pillow")
    sys.exit(1)

pillow_heif.register_heif_opener()


def convert_folder(folder: Path):
    heic_files = sorted(
        [f for f in folder.iterdir() if f.suffix.lower() in (".heic", ".heif")]
    )

    if not heic_files:
        print(f"Tidak ada file HEIC/HEIF ditemukan di: {folder}")
        return

    print(f"Ditemukan {len(heic_files)} file HEIC/HEIF. Memulai konversi...\n")

    berhasil = 0
    gagal = 0

    for i, heic_path in enumerate(heic_files, start=1):
        jpg_path = heic_path.with_suffix(".jpg")

        if jpg_path.exists():
            heic_path.unlink()
            print(f"[{i}/{len(heic_files)}] Lewati (sudah ada), HEIC dihapus: {jpg_path.name}")
            continue

        try:
            img = Image.open(heic_path)
            rgb_img = img.convert("RGB")

            # Ambil metadata EXIF asli jika ada
            exif_data = img.info.get("exif")

            # JPEG punya batas EXIF maks 65535 bytes
            # Jika EXIF terlalu besar, simpan tanpa EXIF
            save_kwargs = {
                "quality": 100,       # kualitas maksimum
                "subsampling": 0,     # matikan chroma subsampling
            }

            exif_stripped = False
            if exif_data and len(exif_data) <= 65535:
                save_kwargs["exif"] = exif_data
            elif exif_data:
                exif_stripped = True

            rgb_img.save(jpg_path, "JPEG", **save_kwargs)

            status = "OK"
            if exif_stripped:
                status = "OK (EXIF dihapus, terlalu besar untuk JPEG)"
            # Hapus file HEIC asli setelah berhasil convert
            heic_path.unlink()

            print(f"[{i}/{len(heic_files)}] {status}: {heic_path.name} -> {jpg_path.name}")
            berhasil += 1

        except Exception as e:
            print(f"[{i}/{len(heic_files)}] GAGAL: {heic_path.name} ({e})")
            gagal += 1

    print(f"\nSelesai. Berhasil: {berhasil}, Gagal: {gagal}, Total: {len(heic_files)}")


if __name__ == "__main__":
    target_folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    if not target_folder.is_dir():
        print(f"Folder tidak ditemukan: {target_folder}")
        sys.exit(1)

    convert_folder(target_folder)
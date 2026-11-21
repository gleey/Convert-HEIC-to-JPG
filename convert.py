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
import threading
from pathlib import Path
from urllib.parse import unquote, urlparse

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    print("Library yang dibutuhkan belum terpasang.")
    print("Install dulu dengan:")
    print("    pip install pillow-heif pillow")
    sys.exit(1)

pillow_heif.register_heif_opener()


SUPPORTED_EXTENSIONS = (".heic", ".heif")


def convert_file(heic_path: Path):
    heic_path = Path(heic_path)
    jpg_path = heic_path.with_suffix(".jpg")

    if jpg_path.exists():
        heic_path.unlink()
        return True, f"Lewati (JPG sudah ada), HEIC dihapus: {jpg_path.name}"

    try:
        with Image.open(heic_path) as img:
            rgb_img = img.convert("RGB")
            exif_data = img.info.get("exif")
            save_kwargs = {"quality": 100, "subsampling": 0}
            exif_stripped = False

            if exif_data and len(exif_data) <= 65535:
                save_kwargs["exif"] = exif_data
            elif exif_data:
                exif_stripped = True

            rgb_img.save(jpg_path, "JPEG", **save_kwargs)

        heic_path.unlink()
        status = "OK"
        if exif_stripped:
            status += " (EXIF dihapus, terlalu besar)"
        return True, f"{status}: {heic_path.name} -> {jpg_path.name}"
    except Exception as exc:
        if jpg_path.exists():
            try:
                jpg_path.unlink()
            except OSError:
                pass
        return False, f"GAGAL: {heic_path.name} ({exc})"


def convert_folder(folder: Path):
    heic_files = sorted([
        file for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ])

    if not heic_files:
        print(f"Tidak ada file HEIC/HEIF ditemukan di: {folder}")
        return 0, 0

    print(f"Ditemukan {len(heic_files)} file HEIC/HEIF. Memulai konversi...\n")

    berhasil = 0
    gagal = 0

    for i, heic_path in enumerate(heic_files, start=1):
        success, message = convert_file(heic_path)
        print(f"[{i}/{len(heic_files)}] {message}")
        berhasil += success
        gagal += not success

    print(f"\nSelesai. Berhasil: {berhasil}, Gagal: {gagal}, Total: {len(heic_files)}")
    return berhasil, gagal


def parse_dropped_paths(data):
    paths = []
    remaining = data.strip()

    while remaining:
        if remaining.startswith("{"):
            end = remaining.find("}")
            if end == -1:
                break
            path = remaining[1:end]
            remaining = remaining[end + 1:].strip()
        else:
            parts = remaining.split(None, 1)
            path = parts[0]
            remaining = parts[1].strip() if len(parts) > 1 else ""

        if path.startswith("file://"):
            path = urlparse(path).path
            path = unquote(path)
        paths.append(path)
    return paths


def launch_gui():
    dnd_files = None
    try:
        from tkinterdnd2 import DND_FILES, Tk
        dnd_files = DND_FILES
    except ImportError:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
        root = tk.Tk()
    else:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
        root = Tk()

    root.title("HEIC/HEIF to JPG")
    root.geometry("620x420")
    root.minsize(520, 360)

    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")

    main = ttk.Frame(root, padding=20)
    main.pack(fill="both", expand=True)

    drop_frame = ttk.LabelFrame(main, text="Drag & drop", padding=15)
    drop_frame.pack(fill="x")

    drop_label = tk.Label(
        drop_frame,
        text="Seret foto HEIC/HEIF atau folder ke sini",
        height=5,
        relief="ridge",
        borderwidth=2,
        bg="#eef4ff",
        fg="#245",
        font=("Segoe UI", 12),
    )
    drop_label.pack(fill="x")

    button_frame = ttk.Frame(main)
    button_frame.pack(fill="x", pady=(12, 8))

    status = tk.StringVar(value="Siap")
    running = {"value": False}

    log = tk.Text(main, height=10, wrap="word", state="disabled")
    log.pack(fill="both", expand=True)

    def append_log(text):
        log.configure(state="normal")
        log.insert("end", text + "\n")
        log.see("end")
        log.configure(state="disabled")

    def process_paths(paths):
        if running["value"]:
            messagebox.showwarning("Sedang berjalan", "Konversi sebelumnya masih berlangsung.")
            return

        files = []
        folders = []
        for raw_path in paths:
            path = Path(raw_path).expanduser()
            if path.is_dir():
                folders.append(path)
            elif path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)

        for folder in folders:
            files.extend(
                file for file in folder.rglob("*")
                if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
            )

        files = sorted(set(files))
        if not files:
            status.set("Tidak ada file HEIC/HEIF yang dipilih")
            append_log("Tidak ada file HEIC/HEIF yang dipilih.")
            return

        log.configure(state="normal")
        log.delete("1.0", "end")
        log.configure(state="disabled")
        running["value"] = True
        status.set(f"Mengonversi {len(files)} file...")

        def worker():
            berhasil = 0
            gagal = 0
            for index, file in enumerate(files, start=1):
                root.after(0, status.set, f"Mengonversi {index}/{len(files)}: {file.name}")
                success, message = convert_file(file)
                berhasil += success
                gagal += not success
                root.after(0, append_log, message)

            root.after(0, status.set, f"Selesai - berhasil: {berhasil}, gagal: {gagal}")
            root.after(0, lambda: running.update(value=False))

        threading.Thread(target=worker, daemon=True).start()

    def choose_files():
        paths = filedialog.askopenfilenames(
            title="Pilih foto HEIC/HEIF",
            filetypes=[("HEIC/HEIF", "*.heic *.HEIC *.heif *.HEIF")],
        )
        if paths:
            process_paths(paths)

    def choose_folder():
        folder = filedialog.askdirectory(title="Pilih folder foto")
        if folder:
            process_paths([folder])

    ttk.Button(button_frame, text="Pilih Foto", command=choose_files).pack(side="left")
    ttk.Button(button_frame, text="Pilih Folder", command=choose_folder).pack(
        side="left", padx=(8, 0)
    )
    ttk.Label(main, textvariable=status).pack(anchor="w", pady=(4, 4))

    if dnd_files is not None:
        drop_label.drop_target_register(dnd_files)
        drop_label.dnd_bind("<<Drop>>", lambda event: process_paths(parse_dropped_paths(event.data)))

    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        launch_gui()
        sys.exit(0)

    target_folder = Path(sys.argv[1])

    if not target_folder.is_dir():
        print(f"Folder tidak ditemukan: {target_folder}")
        sys.exit(1)

    convert_folder(target_folder)
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading

from compressor.engine import compress_image
from compressor.utils import scan_folder


class AppLayout(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Compressor Pro")
        self.geometry("900x600")
        self.minsize(900, 600)

        self.selected_file = None
        self.selected_files = []
        self.selected_folder = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.show_single_mode()

    # ---------------- SIDEBAR ---------------- #
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(
            self.sidebar,
            text="Image\nCompressor",
            font=ctk.CTkFont(size=20, weight="bold"),
            justify="left"
        ).pack(pady=(20, 10), padx=20, anchor="w")

        ctk.CTkButton(self.sidebar, text="Single Image",
                      command=self.show_single_mode).pack(padx=20, pady=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Multiple Images",
                      command=self.show_multi_mode).pack(padx=20, pady=10, fill="x")

        ctk.CTkButton(self.sidebar, text="Folder",
                      command=self.show_folder_mode).pack(padx=20, pady=10, fill="x")

    # ---------------- MAIN ---------------- #
    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.pack_propagate(False)

    def clear_main(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    # ================= SINGLE ================= #
    def show_single_mode(self):
        self.clear_main()

        ctk.CTkLabel(self.main_frame, text="Single Image Compression",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(30, 20))

        self.single_label = ctk.CTkLabel(self.main_frame, text="No file selected")
        self.single_label.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Browse Image",
                      command=self.browse_single).pack(pady=10)

        self.single_size = ctk.CTkEntry(self.main_frame,
                                        placeholder_text="Target size (KB)")
        self.single_size.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Compress",
                      command=self.compress_single).pack(pady=20)

        self.single_status = ctk.CTkLabel(self.main_frame, text="")
        self.single_status.pack()

    def browse_single(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")]
        )
        if path:
            self.selected_file = Path(path)
            self.single_label.configure(text=self.selected_file.name)

    def compress_single(self):
        if not self.selected_file:
            self.single_status.configure(text="❌ No image selected")
            return

        try:
            target_kb = int(self.single_size.get())
        except ValueError:
            self.single_status.configure(text="❌ Invalid size")
            return

        out_dir = self.selected_file.parent / "compressed"
        out_dir.mkdir(exist_ok=True)

        output = out_dir / f"{self.selected_file.stem}_compressed.jpg"
        ok, size = compress_image(self.selected_file, output, target_kb)

        self.single_status.configure(
            text=f"✅ Done: {round(size,2)} KB" if ok else f"⚠ Saved: {round(size,2)} KB",
            text_color="lightgreen" if ok else "orange"
        )

    # ================= MULTI ================= #
    def show_multi_mode(self):
        self.clear_main()

        ctk.CTkLabel(self.main_frame, text="Multiple Images Compression",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(30, 20))

        self.multi_label = ctk.CTkLabel(self.main_frame, text="No images selected")
        self.multi_label.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Select Images",
                      command=self.browse_multi).pack(pady=10)

        self.multi_size = ctk.CTkEntry(self.main_frame,
                                       placeholder_text="Target size (KB)")
        self.multi_size.pack(pady=10)

        self.multi_progress = ctk.CTkProgressBar(self.main_frame, width=300)
        self.multi_progress.pack(pady=20)
        self.multi_progress.set(0)

        ctk.CTkButton(self.main_frame, text="Start Compression",
                      command=self.start_multi).pack(pady=10)

        self.multi_status = ctk.CTkLabel(self.main_frame, text="")
        self.multi_status.pack()

    def browse_multi(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")]
        )
        if files:
            self.selected_files = [Path(f) for f in files]
            self.multi_label.configure(text=f"{len(self.selected_files)} images selected")

    def start_multi(self):
        if not self.selected_files:
            self.multi_status.configure(text="❌ No images selected")
            return

        try:
            target_kb = int(self.multi_size.get())
        except ValueError:
            self.multi_status.configure(text="❌ Invalid size")
            return

        self.multi_progress.set(0)
        self.multi_status.configure(text="Processing...")

        threading.Thread(
            target=self.run_batch,
            args=(self.selected_files, target_kb, self.multi_progress),
            daemon=True
        ).start()

    # ================= FOLDER ================= #
    def show_folder_mode(self):
        self.clear_main()

        ctk.CTkLabel(self.main_frame, text="Folder Compression",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(30, 20))

        self.folder_label = ctk.CTkLabel(self.main_frame, text="No folder selected")
        self.folder_label.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Select Folder",
                      command=self.browse_folder).pack(pady=10)

        self.folder_size = ctk.CTkEntry(self.main_frame,
                                        placeholder_text="Target size (KB)")
        self.folder_size.pack(pady=10)

        self.folder_progress = ctk.CTkProgressBar(self.main_frame, width=300)
        self.folder_progress.pack(pady=20)
        self.folder_progress.set(0)

        ctk.CTkButton(self.main_frame, text="Start Compression",
                      command=self.start_folder).pack(pady=10)

        self.folder_status = ctk.CTkLabel(self.main_frame, text="")
        self.folder_status.pack()

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_folder = Path(path)
            self.folder_label.configure(text=self.selected_folder.name)

    def start_folder(self):
        if not self.selected_folder:
            self.folder_status.configure(text="❌ No folder selected")
            return

        try:
            target_kb = int(self.folder_size.get())
        except ValueError:
            self.folder_status.configure(text="❌ Invalid size")
            return

        files = scan_folder(self.selected_folder)
        if not files:
            self.folder_status.configure(text="⚠ No images found")
            return

        self.folder_progress.set(0)
        self.folder_status.configure(text=f"Processing {len(files)} images...")

        threading.Thread(
            target=self.run_batch,
            args=(files, target_kb, self.folder_progress),
            daemon=True
        ).start()

    # ================= SHARED BATCH ================= #
    def run_batch(self, files, target_kb, progress_bar):
        out_dir = files[0].parent / "compressed"
        out_dir.mkdir(exist_ok=True)

        total = len(files)

        for idx, file in enumerate(files, start=1):
            compress_image(
                file,
                out_dir / f"{file.stem}_compressed.jpg",
                target_kb
            )
            self.after(0, progress_bar.set, idx / total)

        self.after(0, lambda: messagebox.showinfo(
            "Completed",
            f"{total} images compressed successfully!"
        ))

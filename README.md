
# 🖼️ Image Compressor Pro

**Image Compressor Pro** adalah aplikasi desktop berbasis Python untuk mengompres gambar dengan cepat dan aman.  
Dirancang untuk kebutuhan **single image, batch image, dan folder compression**, bahkan untuk **ribuan gambar sekaligus** tanpa crash.

Aplikasi ini cocok untuk:
- Upload marketplace (Shopee, Tokopedia, Shopify, dll)
- Website / e-commerce
- Optimasi storage
- Kerja batch image skala besar

---

## ✨ Fitur Utama

- ✅ Compress 1 gambar
- ✅ Compress banyak gambar sekaligus
- ✅ Compress 1 folder (recursive)
- ✅ Target ukuran file (KB)
- ✅ Smart quality & resize fallback
- ✅ UI modern & ringan
- ✅ Progress bar & notifikasi selesai
- ✅ Aman untuk 3000+ gambar

---

## 🖥️ Preview

- Tampilan modern (dark mode)
- Navigasi sederhana
- Feedback jelas saat proses berjalan

---

## ⚙️ Teknologi

- **Python 3.9+**
- **Pillow** – image processing
- **CustomTkinter** – modern UI
- **Threading** – batch processing tanpa freeze

---

## 📁 Struktur Project

```

image-compressor/
│
├── app.py
├── compressor/
│   ├── engine.py        # Logic compress utama
│   └── utils.py         # Batch & folder helper
│
├── ui/
│   └── layout.py        # UI layout & interaction
│
├── assets/
├── requirements.txt
├── README.md
└── .gitignore

````

---

## ⬇️ Download (Windows EXE)

Untuk pengguna Windows, tersedia versi **EXE (portable)** yang bisa langsung dijalankan tanpa install Python.

👉 **Download di halaman GitHub Releases:**
https://github.com/Libra2694/image-compressor-pro/releases

## ▶️ Cara Menjalankan Aplikasi (source code)
### 🔹 Opsi 1 — Jalankan Langsung (Tanpa Virtual Env)

> Cocok untuk testing cepat

Pastikan Python sudah terinstall:

```bash
python --version
````

Install dependency:

```bash
pip install -r requirements.txt
```

Jalankan aplikasi:

```bash
python app.py
```

---

### 🔹 Opsi 2 — Jalankan dengan Virtual Environment (Direkomendasikan)

> Lebih aman, rapi, dan profesional

#### 1️⃣ Buat virtual environment

```bash
python -m venv env
```

#### 2️⃣ Aktifkan virtual environment

**Windows**

```bash
env\Scripts\activate
```

**Mac / Linux**

```bash
source env/bin/activate
```

Jika berhasil, terminal akan menampilkan `(env)`.

#### 3️⃣ Install dependency di env

```bash
pip install -r requirements.txt
```

#### 4️⃣ Jalankan aplikasi

```bash
python app.py
```

---

## 📦 Output Hasil Compress

Hasil gambar akan otomatis disimpan ke folder:

```
compressed/
```

yang berada di:

* folder gambar asli (Single / Multiple)
* folder yang dipilih (Folder mode)

Semua output disimpan dalam format **JPEG** untuk hasil kompresi terbaik.

---

## 🧪 Format Gambar yang Didukung

* JPG / JPEG
* PNG
* WEBP

---

## ⚠️ Catatan Penting

* Beberapa gambar resolusi ekstrem mungkin tidak bisa mencapai ukuran target.
* Dalam kondisi tersebut, aplikasi akan menyimpan versi terbaik **tanpa crash**.
* Proses batch tetap berjalan walaupun ada satu file bermasalah.

---

## 🛠️ Rencana Pengembangan

* Drag & Drop support
* Preset marketplace (Shopee / Tokopedia / Shopify)
* Build EXE / Portable app
* Preview before & after
* CLI version

---

## 📄 Lisensi

MIT License
Bebas digunakan, dimodifikasi, dan didistribusikan.

---

## 🙌 Author

Dibuat untuk kebutuhan kompresi gambar skala besar dengan workflow yang aman dan efisien.


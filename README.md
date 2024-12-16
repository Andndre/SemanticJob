# SemanticLoker

Proyek ini adalah aplikasi web yang menampilkan informasi lowongan pekerjaan dari berbagai sumber menggunakan teknologi **Semantic Web**. Aplikasi ini terdiri dari dua bagian utama: backend yang dibangun dengan **Flask** dan frontend yang dibangun dengan **React** dan **Vite**.

## Fitur Utama
- **Web Scraping**: Mengambil data lowongan pekerjaan dari berbagai situs web.
- **Semantic Web**: Data disimpan dalam format RDF dan dikelola di GraphDB.
- **SPARQL Query**: Mengambil data lowongan pekerjaan dari GraphDB untuk ditampilkan melalui endpoint Flask.
- **React**: Library untuk membangun antarmuka pengguna.
- **TypeScript**: Superset JavaScript yang menambahkan tipe statis.
- **Vite**: Bundler modern yang cepat dengan dukungan HMR (Hot Module Replacement).
- **Tailwind CSS**: Framework CSS untuk styling yang cepat dan efisien.

## Prasyarat
Pastikan Anda telah menginstal:
- **Python 3.8** atau lebih baru
- **Node.js** (versi terbaru direkomendasikan)
- **npm** atau **yarn**
- **GraphDB** (jalankan di `http://localhost:7200` atau sesuaikan URL repository di file `.env`)

## Instalasi

### Backend (Flask)

1. Clone repository ini.
    ```bash
    git clone https://github.com/Andndre/SemanticJob.git
    cd SemanticJob/backend
    ```

2. Install dependencies.
    ```bash
    pip install -r requirements.txt
    ```

3. Buat file [.env](http://_vscodecontentref_/0) untuk konfigurasi endpoint GraphDB:
    ```plaintext
    GRAPHDB_ENDPOINT=http://localhost:7200/repositories/lokerku
    ```

4. Jalankan **GraphDB** dan pastikan repository `lokerku` sudah dibuat.

### Frontend (React Vite)

1. Pindah ke direktori frontend.
    ```bash
    cd ../frontend
    ```

2. Install dependencies.
    ```bash
    npm install
    # atau
    yarn install
    ```

## Menjalankan Aplikasi

### Backend

1. **Jalankan** skrip [save.py](http://_vscodecontentref_/1) untuk scraping data dan mengunggahnya ke GraphDB.
    ```bash
    python save.py
    ```

    Setelah skrip selesai, data akan tersedia di GraphDB di repository `lokerku`.

2. **Jalankan** aplikasi Flask ([app.py](http://_vscodecontentref_/2)) untuk menampilkan lowongan pekerjaan.
    ```bash
    python app.py
    ```

3. **Akses** aplikasi melalui browser di `http://localhost:5000/`.

### Frontend

1. Jalankan aplikasi dalam mode pengembangan.
    ```bash
    npm run dev
    # atau
    yarn dev
    ```

2. Buka aplikasi di browser pada `http://localhost:3000`.

## Struktur Proyek

### Backend
- **[save.py](http://_vscodecontentref_/3)**: Skrip untuk scraping data dan mengunggahnya ke GraphDB.
- **[app.py](http://_vscodecontentref_/4)**: Aplikasi Flask untuk menampilkan data lowongan pekerjaan.

### Frontend
- **[src](http://_vscodecontentref_/5)**: Direktori utama untuk kode sumber aplikasi.
  - **[App.tsx](http://_vscodecontentref_/6)**: Komponen utama aplikasi.
  - **`types.ts`**: Definisi tipe TypeScript untuk aplikasi.
  - **[index.css](http://_vscodecontentref_/7)**: File CSS utama yang menggunakan Tailwind CSS.
  - **`main.tsx`**: Entry point aplikasi.
- **[public](http://_vscodecontentref_/8)**: Direktori untuk aset publik.
- **[index.html](http://_vscodecontentref_/9)**: Template HTML utama.

## Penggunaan

- **Pencarian Lowongan Pekerjaan**: Gunakan form pencarian di halaman utama untuk mencari lowongan pekerjaan berdasarkan kata kunci.
- **Navigasi**: Gunakan navigasi di bagian atas untuk berpindah antara halaman Home, Jobs, dan About.

## Lisensi
Proyek ini menggunakan lisensi [MIT](https://opensource.org/licenses/MIT).
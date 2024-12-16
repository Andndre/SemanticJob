# Lowongan Kerja Semantic Web

Proyek ini adalah aplikasi berbasis **Flask** yang menggunakan **Semantic Web** untuk menampilkan informasi lowongan pekerjaan dari berbagai sumber. Data diambil melalui web scraping, disimpan dalam format RDF, dan diunggah ke **GraphDB** untuk query SPARQL.

---

## Fitur Utama
- **Web Scraping**: Mengambil data lowongan pekerjaan dari berbagai situs web.
- **Semantic Web**: Data disimpan dalam format RDF dan dikelola di GraphDB.
- **SPARQL Query**: Mengambil data lowongan pekerjaan dari GraphDB untuk ditampilkan melalui endpoint Flask.

---

## Prasyarat
Pastikan Anda telah menginstal:
- **Python 3.8** atau lebih baru
- **GraphDB** (jalankan di `http://localhost:7200` atau sesuaikan URL repository di file `.env`)

---

## Instalasi

1. Clone repository ini.
    ```bash
    git clone hhttps://github.com/Andndre/SemanticJob.git
    cd SemanticJob
    ```

2. Install dependencies.
    ```bash
    pip install -r requirements.txt
    ```

3. Buat file `.env` untuk konfigurasi endpoint GraphDB:
    ```plaintext
    GRAPHDB_ENDPOINT=http://localhost:7200/repositories/lokerku
    ```

4. Jalankan **GraphDB** dan pastikan repository `lokerku` sudah dibuat.

---

## Tutorial Singkat

1. **Jalankan** skrip `save.py` untuk scraping data dan mengunggahnya ke GraphDB.
    ```bash
    python save.py
    ```

    Setelah skrip selesai, data akan tersedia di GraphDB di repository `lokerku`.

2. **Jalankan** aplikasi Flask (`app.py`) untuk menampilkan lowongan pekerjaan.
    ```bash
    python app.py
    ```

3. **Akses** aplikasi melalui browser di `http://localhost:5000/`.

---

## Struktur File
- **`save.py`**: Skrip untuk scraping data dan mengunggahnya ke GraphDB.
- **`app.py`**: Aplikasi Flask untuk menampilkan data lowongan pekerjaan.

---

## Penggunaan

- Buka endpoint utama di `http://localhost:5000/` untuk melihat daftar lowongan pekerjaan.
- Endpoint menggunakan query SPARQL untuk mengambil data langsung dari GraphDB.

---

## Lisensi
Proyek ini menggunakan lisensi [MIT](https://opensource.org/licenses/MIT).

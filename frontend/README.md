# SemanticLoker Frontend

Proyek ini adalah aplikasi frontend berbasis **React** dan **TypeScript** yang menggunakan **Vite** sebagai bundler. Aplikasi ini menampilkan informasi lowongan pekerjaan yang diambil dari backend Flask dan GraphDB.

## Fitur Utama
- **React**: Library untuk membangun antarmuka pengguna.
- **TypeScript**: Superset JavaScript yang menambahkan tipe statis.
- **Vite**: Bundler modern yang cepat dengan dukungan HMR (Hot Module Replacement).
- **Tailwind CSS**: Framework CSS untuk styling yang cepat dan efisien.

## Prasyarat
Pastikan Anda telah menginstal:
- **Node.js** (versi terbaru direkomendasikan)
- **npm** atau **yarn**

## Instalasi

1. Clone repository ini.
    ```bash
    git clone https://github.com/Andndre/SemanticJob.git
    cd SemanticJob/frontend
    ```

2. Install dependencies.
    ```bash
    npm install
    # atau
    yarn install
    ```

3. Jalankan aplikasi dalam mode pengembangan.
    ```bash
    npm run dev
    # atau
    yarn dev
    ```

4. Buka aplikasi di browser pada `http://localhost:3000`.

## Struktur Proyek
- **[src](http://_vscodecontentref_/0)**: Direktori utama untuk kode sumber aplikasi.
  - **[App.tsx](http://_vscodecontentref_/1)**: Komponen utama aplikasi.
  - **`types.ts`**: Definisi tipe TypeScript untuk aplikasi.
  - **[index.css](http://_vscodecontentref_/2)**: File CSS utama yang menggunakan Tailwind CSS.
  - **`main.tsx`**: Entry point aplikasi.
- **[public](http://_vscodecontentref_/3)**: Direktori untuk aset publik.
- **[index.html](http://_vscodecontentref_/4)**: Template HTML utama.

## Konfigurasi
- **`vite.config.ts`**: Konfigurasi untuk Vite.
- **`tailwind.config.js`**: Konfigurasi untuk Tailwind CSS.
- **`tsconfig.json`**: Konfigurasi untuk TypeScript.

## Penggunaan

- **Pencarian Lowongan Pekerjaan**: Gunakan form pencarian di halaman utama untuk mencari lowongan pekerjaan berdasarkan kata kunci.
- **Navigasi**: Gunakan navigasi di bagian atas untuk berpindah antara halaman Home, Jobs, dan About.

## Lisensi
Proyek ini menggunakan lisensi [MIT](https://opensource.org/licenses/MIT).

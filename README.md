# KIT KP Monitor API (Backend)

Proyek backend FastAPI untuk memonitor kegiatan Kerja Praktik (KP) mahasiswa, meliputi absensi wajah (Face Recognition), pencatatan tugas harian, pelaporan harian, dan pelaporan mingguan.

## Persyaratan
- Docker
- Docker Compose

## Cara Menjalankan (Docker)
1. **Clone repositori** atau pastikan Anda berada di root folder `backend`.
2. **Setup file env**:
   Buat file `.env` dari contoh `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Pastikan konfigurasi `DATABASE_URL`, `JWT_SECRET_KEY`, dan lainnya sudah sesuai.
3. **Build & Jalankan**:
   Gunakan docker-compose untuk menjalankan database PostgreSQL (opsional jika sudah ada *external db*) dan aplikasi FastAPI:
   ```bash
   docker-compose up -d --build
   ```
4. **Migrasi Database**:
   Agar tabel di database terbuat (jika menggunakan postgres kosong), jalankan perintah alembic di dalam container:
   ```bash
   docker exec -it kit_kp_api alembic upgrade head
   ```
5. Aplikasi akan berjalan di `http://localhost:8000`.
6. Buka `http://localhost:8000/docs` untuk melihat dokumentasi API Swagger.
7. Alternatif dokumentasi: Anda bisa memuat file `swagger.yaml` di root backend ini ke [Swagger Editor](https://editor.swagger.io/) atau Postman.

## Struktur Direktori Utama
- `app/api`: Definisi rute dan endpoint REST API (Users, Attendance, Task, Report).
- `app/core`: Konfigurasi *security*, *dependency injection*, dan *settings*.
- `app/db`: Pengaturan *database connection* dan migrasi (Alembic).
- `app/models`: Definisi model ORM SQLAlchemy (termasuk FaceVector & struktur laporan).
- `app/repositories`: Logika akses ke *database* (*Data Access Layer*).
- `app/schemas`: Skema Pydantic untuk validasi input (Request) dan output (Response).
- `app/services`: Logika bisnis (pengolahan absensi wajah, filter tugas, laporan).
- `app/utils`: Modul utilitas (*file upload*, *face recognition*).
- `/uploads`: Folder default (didalam Docker container) untuk menyimpan file statis (foto avatar, bukti tugas, laporan pdf). Direktori ini diekspos melalui endpoint `/uploads`.


## Face Recognition
Proyek ini menggunakan pustaka `face-recognition` (C++ dlib) untuk mengubah wajah mahasiswa menjadi representasi vektor 128 dimensi. Vektor ini disimpan di database dan digunakan untuk mencocokkan wajah saat mahasiswa datang/pulang tanpa perlu melatih model dari awal.

## Alur Kerja API
Semua endpoint (kecuali registrasi/login) dilindungi oleh JWT.
- Header Request harus berisi `Authorization: Bearer <token>`.
- Payload dan response dari setiap endpoint didokumentasikan di OpenAPI (Swagger UI).

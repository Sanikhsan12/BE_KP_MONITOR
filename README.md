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
4. Aplikasi akan berjalan di `http://localhost:8000`.
5. Buka `http://localhost:8000/docs` untuk melihat dokumentasi API Swagger.

## Struktur Direktori Utama
- `app/api`: Definisi rute dan endpoint REST API.
- `app/core`: Konfigurasi *security*, *dependency injection*, dan *settings*.
- `app/db`: Pengaturan *database connection* dan migrasi (Alembic).
- `app/models`: Definisi model ORM SQLAlchemy.
- `app/repositories`: Logika akses ke *database* (*Data Access Layer*).
- `app/schemas`: Skema Pydantic untuk validasi input (Request) dan output (Response).
- `app/services`: Logika bisnis.
- `app/utils`: Modul utilitas (*file upload*, *face recognition*, dll).
- `/uploads`: Folder default untuk menyimpan file statis (foto & pdf). Direktori ini diekspos melalui `StaticFiles` di FastAPI.

## Face Recognition
Proyek ini menggunakan pustaka `face-recognition` (C++ dlib) untuk mengubah wajah mahasiswa menjadi representasi vektor 128 dimensi. Vektor ini disimpan di database dan digunakan untuk mencocokkan wajah saat mahasiswa datang/pulang tanpa perlu melatih model dari awal.

## Alur Kerja API
Semua endpoint (kecuali registrasi/login) dilindungi oleh JWT.
- Header Request harus berisi `Authorization: Bearer <token>`.
- Payload dan response dari setiap endpoint didokumentasikan di OpenAPI (Swagger UI).

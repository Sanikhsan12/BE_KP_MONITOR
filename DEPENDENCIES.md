# Dokumentasi Dependensi (`requirements.txt`)

Berikut adalah daftar pustaka (library) utama yang digunakan dalam backend **KIT KP Monitor API** beserta fungsinya:

## 1. Web Framework & Server
- **`fastapi==0.115.0`**: Framework web modern yang cepat (berkinerja tinggi) untuk membangun API dengan Python 3.8+ berdasarkan *standard Python type hints*. FastAPI otomatis membuat dokumentasi (Swagger/OpenAPI) dari kodenya.
- **`uvicorn[standard]==0.30.6`**: ASGI *web server implementation* untuk Python. Berfungsi sebagai server yang menjalankan aplikasi FastAPI dengan performa tinggi.
- **`python-multipart==0.0.9`**: Digunakan oleh FastAPI untuk memparsing form-data (*multipart/form-data*), sangat esensial untuk menerima *file upload* (gambar, PDF).

## 2. Database & ORM
- **`sqlalchemy==2.0.35`**: Object Relational Mapper (ORM) Python untuk berinteraksi dengan SQL databases secara *pythonic*.
- **`asyncpg==0.29.0`**: Driver antarmuka database asinkron yang sangat cepat untuk PostgreSQL. Digunakan bersama SQLAlchemy agar *query* bersifat non-blocking (async).
- **`alembic==1.13.2`**: *Database migration tool* untuk SQLAlchemy. Berfungsi mencatat dan mengaplikasikan perubahan skema database secara bertahap (*version control* untuk database).

## 3. Data Validation & Configuration
- **`pydantic==2.9.2`**: Library untuk validasi data dan pengelolaan pengaturan (settings) menggunakan anotasi tipe Python. Digunakan luas dalam `schemas`.
- **`pydantic-settings==2.5.2`**: Modul tambahan Pydantic khusus untuk membaca konfigurasi aplikasi dari environment variable atau file `.env`.
- **`python-dotenv==1.0.1`**: Library pembantu untuk memuat variabel dari file `.env` ke environment system, sehingga dapat diakses oleh kode.

## 4. Security & Autentikasi
- **`python-jose[cryptography]==3.3.0`**: Digunakan untuk men-generate (sign) dan memverifikasi (verify) JSON Web Tokens (JWT) dalam fitur *login* dan perlindungan endpoint (auth).
- **`passlib[bcrypt]==1.7.4`**: Library *password hashing*. Dalam sistem ini memakai *bcrypt* untuk menyimpan kata sandi mahasiswa/mentor dengan aman di database.

## 5. Machine Learning & Face Recognition
- **`face-recognition==1.3.0`**: *Wrapper* yang ramah pengguna dari library C++ `dlib`. Digunakan untuk mengekstraksi wajah dari sebuah gambar, dan mengubahnya menjadi array/vektor matematika (128 dimensi) yang unik per wajah. Vektor ini yang kemudian dibandingkan (*compare*) untuk absensi.
- **`Pillow==10.4.0`**: Library *imaging* Python. Digunakan sebagai *dependency* untuk membuka dan memproses file gambar sebelum diproses oleh `face-recognition`.

# FlowForge

Platform workflow automation sederhana yang memungkinkan tim untuk mendefinisikan, menjalankan, dan memonitor workflow otomatis.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Infrastructure**: Docker, Docker Compose

## Cara Menjalankan

### Prasyarat
- Docker Desktop
- Git

### Langkah-langkah

1. Clone repository
   git clone <repo-url>
   cd flowforge

2. Jalankan dengan Docker
   docker-compose up --build

3. Akses aplikasi
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Fitur

- Register & Login dengan JWT Authentication
- Buat, lihat, dan hapus workflow
- DAG Engine untuk menjalankan workflow berdasarkan dependency antar step
- Multi-tenant (setiap user punya data terpisah)
- Dashboard monitoring sederhana

## Arsitektur
# 🐳 Docker Containerization & Local Development

This directory provides centralized Docker multi-stage container build specifications and Docker Compose orchestration for CloudPulse.

---

## 📦 Container Specifications

- **`Dockerfile.backend`:**
  - Base: `python:3.12-slim`
  - Two-stage build isolating build dependencies from runtime image
  - Runs as non-root user `appuser` (UID 10001)
  - Automatic Alembic migration execution on container boot
- **`Dockerfile.frontend`:**
  - Base: `node:20-alpine` (builder) and `nginx:1.25-alpine` (runtime)
  - Production static bundle served via Nginx reverse proxy
  - Runs as non-root user `nginx` (UID 101)

---

## 🚀 Running with Docker Compose
```bash
docker compose up --build -d
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/docs`
- Database: `localhost:5432`

# 💻 CloudPulse Application Layer

The CloudPulse application is built as a cloud-native microservice architecture comprising two primary components:

---

## 🏗️ Architecture

- **Backend API (`backend/`):**
  - **Framework:** Python 3.12 + FastAPI 0.115
  - **ORM & Migrations:** SQLAlchemy 2.0 & Alembic 1.14
  - **Database:** PostgreSQL 16 (Psycopg 3 async engine)
  - **Tests:** Pytest 8.3 test suite with in-memory SQLite isolation (12 tests)
  - **Telemetry:** Prometheus FastAPI instrumentator exporting `/metrics`

- **Frontend Dashboard (`frontend/`):**
  - **Framework:** React 18 + Vite 5
  - **Styling:** Responsive modern CSS design system
  - **Web Server:** Hardened Nginx 1.25 Alpine reverse proxy

---

## 🚀 Running Application Locally
See the root [`README.md`](../README.md) for full instructions.

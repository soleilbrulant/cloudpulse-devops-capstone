# 📊 CloudPulse DevOps Capstone Presentation

> **File:** `demo/PRESENTATION.md`  
> **Topic:** End-to-End Enterprise DevOps & DevSecOps Platform  
> **Course:** DevOps Engineering Masterclass — Session 21 Final Capstone

---

## Slide 1: Title Slide
# CloudPulse — Multi-Cloud Asset & Infrastructure Management
### Automated CI/CD, DevSecOps, IaC on AWS EKS, Helm, Prometheus & ArgoCD GitOps
- **Presenter:** DevOps Student
- **Repository:** [github.com/soleilbrulant/cloudpulse-devops-capstone](https://github.com/soleilbrulant/cloudpulse-devops-capstone)
- **Date:** October 2026

---

## Slide 2: Executive Summary & Problem Statement
- **The Challenge:** Modern engineering teams deploy across heterogeneous cloud platforms (AWS, GCP, Azure), leading to fragmented visibility, untracked orphan assets, configuration drift, and unbudgeted cloud spend.
- **The Solution:** CloudPulse provides a centralized, automated control plane to register, track, monitor, and cost-attribute multi-cloud assets in real time.
- **DevOps Objective:** Design and implement a zero-touch, resilient, secure delivery pipeline from code commit to AWS production with automated monitoring and GitOps continuous reconciliation.

---

## Slide 3: End-to-End Architecture Overview
```
Developer Commit
      ↓
GitHub Repository (Trigger Webhook)
      ↓
CI Pipeline (GitHub Actions)
  ├── 1. Automated Testing (Pytest - 12 Tests, SQLite in-memory)
  ├── 2. Frontend Build (Vite 5 Production Bundle)
  ├── 3. DevSecOps Quality Gates:
  │      ├── SAST Code Analysis (Bandit)
  │      ├── Secret Scanning (Gitleaks)
  │      └── Container Vulnerability Scan (Aqua Trivy: CRITICAL/HIGH = Exit 1)
  └── 4. Container Build & Push (GitHub Container Registry - GHCR)
      ↓
Infrastructure as Code (Terraform)
  ├── AWS Custom VPC (10.0.0.0/16, Multi-AZ Subnets)
  └── Amazon EKS Managed Kubernetes Cluster + t3.medium Worker Nodes
      ↓
Continuous Deployment & GitOps (ArgoCD + Helm)
  ├── Reconciles Helm Chart from Git Repository
  ├── Deploys Backend API, React Frontend, PostgreSQL 16 StatefulSet
  ├── Horizontal Pod Autoscaler (HPA) & Ingress Routing
  └── Probes: Liveness (/health) & Readiness (/ready)
      ↓
Observability & Telemetry
  ├── Prometheus Operator (Scrapes /metrics every 15s)
  └── Grafana (Real-time Dashboards for Latency, RPS, Error Rates, CPU/Mem)
```

---

## Slide 4: Application Architecture & Core Microservices
- **FastAPI Core Service (Python 3.12):**
  - High-concurrency async REST API.
  - Pydantic v2 data models for input validation.
  - SQLAlchemy 2.0 ORM with Psycopg 3 connection pooling.
  - Alembic automatic database migrations on container startup.
- **PostgreSQL 16 Database:**
  - ACID-compliant relational persistence.
  - Deployed as a Kubernetes StatefulSet with 5Gi PersistentVolumeClaim (`volumeClaimTemplates`).
- **React 18 Single Page Application:**
  - Modern, responsive asset dashboard built with Vite 5.
  - Real-time cloud spend aggregation by provider (AWS/GCP/Azure) and lifecycle state.

---

## Slide 5: Containerization & Docker Hardening
- **Backend Dockerfile:**
  - Multi-stage build based on official `python:3.12-slim`.
  - Hardened non-root user `appuser` (UID 10001).
  - Minimal container footprint (<180MB).
  - Explicit healthcheck instruction.
- **Frontend Dockerfile:**
  - Stage 1: `node:20-alpine` builds static production assets.
  - Stage 2: `nginx:1.25-alpine` serves static files and reverse-proxies `/api` calls.
  - Runs as non-root `nginx` user (UID 101) with unprivileged port configurations.
- **Docker Compose:**
  - Single-command developer environment (`docker compose up --build -d`) with isolated bridge network and Postgres health dependency.

---

## Slide 6: Infrastructure as Code with Terraform
- **Cloud Provider:** Amazon Web Services (AWS).
- **Network Topology:**
  - Modular VPC (`10.0.0.0/16`).
  - 2 Public Subnets across Availability Zones (`ap-south-1a`, `ap-south-1b`).
  - Internet Gateway and automated route table association.
- **Compute Plane:**
  - Amazon EKS Cluster (`cloudpulse-eks-prod`, Kubernetes v1.28).
  - Managed Node Group (`t3.medium`, autoscaling from 2 to 4 nodes).
  - IAM Roles for Service Accounts (IRSA) and security group isolation.
- **Reproducibility:**
  - Parameterized via `variables.tf` and `terraform.tfvars`.
  - Clean lifecycle teardown via `terraform destroy`.

---

## Slide 7: Kubernetes Orchestration & Helm Packaging
- **Kubernetes Resources Included:**
  - **Namespace:** `cloudpulse` for workload isolation.
  - **ConfigMap:** Decoupled runtime configuration (`APP_ENV`, `LOG_LEVEL`).
  - **Secret:** Encrypted database credentials (`DATABASE_URL`).
  - **StatefulSet & PVC:** 5Gi persistent disk for PostgreSQL database reliability.
  - **Deployments:** 2 replicas for frontend and backend with non-root security contexts.
  - **Services:** ClusterIP services with proper port mapping.
  - **Ingress Controller:** NGINX Ingress routing `/api` to backend and `/` to frontend.
  - **Probes:** Custom `/health` (liveness) and `/ready` (database readiness probe).
  - **HPA:** Horizontal Pod Autoscaler targeting 70% CPU utilization (2 to 6 replicas).
- **Helm Modularization:**
  - Parameterized `values-dev.yaml` and `values-prod.yaml` for multi-environment deployments.
  - Validated with `helm lint` in CI pipeline.

---

## Slide 8: CI/CD Pipeline (GitHub Actions)
- **Trigger Strategy:** Runs on every `push` and `pull_request` to `main`.
- **Workflow Stages:**
  1. **Test Job:** Python 3.12 environment, runs all 12 Pytest tests in <0.5s; builds Vite frontend bundle.
  2. **DevSecOps Security Gate:** Trivy container scans for CRITICAL and HIGH CVEs (`exit-code: 1`).
  3. **Build & Publish Job:** Docker multi-platform build, authenticates to GHCR, tags with Git commit SHA and `latest`.
  4. **Validation & Deployment Gate:** Validates Helm chart syntax, template hydration, and deploys manifests.

---

## Slide 9: DevSecOps "Shift-Left" Implementation
- **SAST (Static Application Security Testing):**
  - Bandit scanning Python backend code for SQL injection, insecure imports, and dangerous functions.
- **Secret Scanning:**
  - Automated scanning with Gitleaks to eliminate accidental API keys, tokens, or plaintext passwords in Git history.
- **SCA (Software Composition Analysis):**
  - Dependency scanning with Trivy and `pip-audit` to detect known CVEs in libraries.
- **Container Hardening:**
  - Multi-stage image build strips compilers and development headers.
  - Enforced `runAsNonRoot: true` in Kubernetes Pod security contexts.
  - Strict security gate: Builds fail immediately if vulnerabilities exceed threshold.

---

## Slide 10: Production Observability & Monitoring
- **Application Telemetry:**
  - Native Prometheus instrumentation via `prometheus-fastapi-instrumentator`.
  - Exposes request counts, latency histograms, and system stats at `/metrics`.
- **Prometheus Operator:**
  - Declarative `ServiceMonitor` resource targets `cloudpulse-backend` every 15 seconds.
- **Grafana Visualization:**
  - Production dashboard with 4 core golden signals:
    - HTTP Request Rate (RPS).
    - Latency (P50, P95, P99).
    - Error Rates (HTTP 4xx and 5xx).
    - CPU and Memory Utilization per Pod.

---

## Slide 11: GitOps Workflow with ArgoCD
- **Single Source of Truth:** The Git repository declaratively specifies all desired state.
- **Continuous Synchronization:**
  - ArgoCD monitors the Helm chart at `helm/cloudpulse`.
  - Automated sync and self-healing: any manual `kubectl edit` in the cluster is automatically detected and reconciled back to the Git definition.
- **Zero-Downtime Rollouts:**
  - Rolling updates guarantee zero dropped connections during new version rollouts.

---

## Slide 12: Troubleshooting Challenge — Incident 1
- **Failure:** Container fails to launch, entering `ImagePullBackOff`.
- **Investigation:**
  - `kubectl get pods -n cloudpulse` shows `0/1 ImagePullBackOff`.
  - `kubectl describe pod` reveals `rpc error: code = NotFound: image tag non-existent-tag-v999 does not exist`.
- **Root Cause:** Typos in deployment manifest image tag.
- **Resolution:** Updated deployment spec with verified GHCR tag `latest` and `IfNotPresent` pull policy.
- **Verification:** Pod transitioned to `1/1 Running` and passed readiness checks.

---

## Slide 13: Troubleshooting Challenge — Incident 2
- **Failure:** External HTTP requests fail with `502 Bad Gateway` / Connection Refused.
- **Investigation:**
  - `curl -I http://cloudpulse-broken-service:8080` yields Connection Refused.
  - `kubectl get endpoints` shows `<none>` for the service.
  - `kubectl describe svc` revealed selector `app=label-selector-that-matches-no-pod` and targetPort `8080`.
- **Root Cause:** Service label selector did not match Pod template labels (`app=cloudpulse-backend`), and targetPort did not match Uvicorn port (8000).
- **Resolution:** Corrected selector and targetPort in `troubleshooting/fixed-service.yaml`.
- **Verification:** Endpoints populated immediately (`10.244.1.28:8000`), `/health` returned `200 OK`.

---

## Slide 14: Lessons Learned & Engineering Best Practices
1. **Shift-Left Security Saves Time:** Detecting vulnerabilities in container base images in CI prevents emergency hotfixes in production.
2. **Immutable Infrastructure with Terraform:** Declarative VPC and EKS provisioning eliminates configuration drift and "works on my machine" issues.
3. **Observability Enables Proactive Incident Response:** Combining custom readiness probes with Prometheus metrics ensures traffic is only routed to pods with verified database connectivity.
4. **GitOps Enforces Operational Discipline:** Managing Kubernetes manifests strictly via Git prevents undocumented manual cluster mutations.

---

## Slide 15: Q&A & Demonstration Links
- **Demo Video (Google Drive):** [👉 **Watch on Google Drive**](https://drive.google.com/file/d/1MjWNdOOhW2WfD3lgkewCFqb2unRxYm1R/view?usp=sharing)
- **Local Video in Repo:** [`cloudpulse_capstone_demo.mp4`](./cloudpulse_capstone_demo.mp4)
- **Repository:** [github.com/soleilbrulant/cloudpulse-devops-capstone](https://github.com/soleilbrulant/cloudpulse-devops-capstone)
- **Documentation:** See `README.md` and `SUBMISSION.md`
- **Thank you!**

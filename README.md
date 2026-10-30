# CloudPulse — Multi-Cloud Infrastructure & Asset Management Platform

[![CI/CD Pipeline](https://github.com/soleilbrulant/cloudpulse-devops-capstone/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/soleilbrulant/cloudpulse-devops-capstone/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.28+-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Terraform](https://img.shields.io/badge/Terraform-AWS_EKS-7B42BC?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Security: Trivy](https://img.shields.io/badge/Security-Trivy_Pass-brightgreen?logo=aqua)](https://trivy.dev/)
[![Demo Video](https://img.shields.io/badge/Demo-Video_Walkthrough-red?logo=youtube)](./demo/VIDEO.md)
[![Presentation](https://img.shields.io/badge/Slides-Capston_Deck-orange?logo=google-slides)](./demo/PRESENTATION.md)

---

> ### 📢 Official Capstone Submission Artifacts
> - 🎬 **Demo Video Walkthrough:** [**Watch on Google Drive (`demo/VIDEO.md`)**](./demo/VIDEO.md)
> - 📊 **Project Presentation Deck:** [**View Slides (`demo/PRESENTATION.md`)**](./demo/PRESENTATION.md) | [**Interactive Deck (`demo/presentation.html`)**](./demo/presentation.html)
> - 📋 **Submission Specification & Checklist:** [**`SUBMISSION.md`**](./SUBMISSION.md)
> - 📸 **Dashboard Screenshots & Proof:** [**`demo/screenshots/`**](./demo/screenshots/)

---

## 1. Project overview

**CloudPulse** is an enterprise-grade cloud resource and infrastructure inventory management platform. Built for modern DevOps and Platform Engineering teams, CloudPulse provides centralized visibility, lifecycle status tracking, and spend attribution across multi-cloud environments (AWS, GCP, and Azure).

The project demonstrates an end-to-end cloud engineering journey:
- **Full-Stack Application:** Modular React 18 + Vite dashboard backed by a high-throughput Python FastAPI microservice and PostgreSQL database with Alembic schema versioning.
- **Automated Testing:** 12 unit and integration tests executing in isolated SQLite memory containers via Pytest.
- **Containerization:** Multi-stage builds creating hardened non-root container images.
- **Infrastructure as Code (IaC):** AWS VPC, multi-AZ subnets, Internet Gateways, and Amazon EKS cluster with managed autoscaling node groups provisioned declaratively via Terraform.
- **Container Orchestration:** Kubernetes manifests packaged into a parameterized Helm chart with custom Ingress routing and Horizontal Pod Autoscaling (HPA).
- **Shift-Left Security:** Automated DevSecOps pipeline with Trivy container image scanning and GitHub secret detection.
- **Production Observability:** Prometheus scraping application telemetry via `/metrics` and Grafana dashboards for latency, request rates, and resource utilization.
- **GitOps:** Continuous reconciliation powered by ArgoCD.

---

## 2. Architecture diagram

```mermaid
graph TD
    Dev["Platform Engineer"] -->|"Push Code / PR"| GitHub["GitHub Repository"]
    GitHub -->|"Trigger CI"| GHA["GitHub Actions Runner"]
    
    subgraph CI_Pipeline ["Continuous Integration and DevSecOps"]
        GHA -->|"1. Unit Tests"| Pytest["Pytest Test Suite - 12 Tests"]
        GHA -->|"2. Compile Frontend"| Vite["Vite React Production Build"]
        GHA -->|"3. Containerize"| Docker["Docker Multi-Stage Build"]
        GHA -->|"4. Vulnerability Scan"| Trivy["Trivy Container Security Gate"]
        Trivy -->|"Pass: Push Image"| GHCR["GitHub Container Registry - GHCR"]
        GHA -->|"5. Validate Chart"| HelmLint["Helm Lint Validation"]
    end

    subgraph AWS_Cloud ["AWS Cloud Infrastructure - Terraform"]
        TF["Terraform"] -->|"Provision"| VPC["Custom AWS VPC - 10.0.0.0/16"]
        VPC -->|"Subnets"| AZ1["Public Subnet ap-south-1a"]
        VPC -->|"Subnets"| AZ2["Public Subnet ap-south-1b"]
        TF -->|"Deploy"| EKS["Amazon EKS Managed Cluster"]
        EKS -->|"Manage"| Nodes["Managed Worker Node Group - t3.medium"]
    end

    subgraph Kubernetes_Cluster ["Kubernetes Cluster Architecture"]
        GHCR -.->|"Pull Images"| Pods["CloudPulse Deployments"]
        ArgoCD["ArgoCD GitOps"] -->|"Continuous Reconciliation"| Pods
        Ingress["NGINX Ingress Controller"] -->|"Route /api"| Backend["FastAPI Backend Pods - 2 to 6 Replicas"]
        Ingress -->|"Route /"| Frontend["React Frontend Pods - 2 Replicas"]
        Backend -->|"SQLAlchemy ORM"| Postgres["PostgreSQL 16 StatefulSet"]
        HPA["Horizontal Pod Autoscaler"] -->|"Target 70% CPU"| Backend
    end

    subgraph Observability_Telemetry ["Monitoring and Alerting"]
        Backend -->|"Expose"| Metrics["/metrics Endpoint"]
        Prometheus["Prometheus Operator"] -->|"Scrape every 15s"| Metrics
        Prometheus -->|"Stream Metrics"| Grafana["Grafana Dashboards"]
    end
```

---

## 3. Technologies used

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite 5, Responsive Vanilla CSS Design System, HTML5 |
| **Backend API** | Python 3.12, FastAPI 0.115, Pydantic v2, Uvicorn |
| **Database & ORM** | PostgreSQL 16, SQLAlchemy 2.0, Alembic 1.14, Psycopg 3 |
| **Automated Testing**| Pytest 8.3, HTTPX, FastAPI TestClient |
| **Containerization** | Docker Engine, Docker Compose, Multi-stage Dockerfiles |
| **Cloud Infrastructure**| AWS (VPC, Subnets, IGW, EKS, IAM, Security Groups) |
| **Infrastructure as Code**| Terraform 1.5+ (AWS Provider v5.35) |
| **Orchestration & Packaging**| Kubernetes 1.28+, Helm 3.14 |
| **CI/CD Pipeline** | GitHub Actions, GitHub Container Registry (GHCR) |
| **DevSecOps** | Aqua Security Trivy, Non-root containers (`appuser:10001`, `nginx:101`) |
| **Observability** | Prometheus Operator, Grafana, prometheus-fastapi-instrumentator |
| **GitOps** | ArgoCD |

---

## 4. Application setup

### Running Locally (Without Docker)

#### 1. Backend Setup:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://cloudpulse_admin:cloudpulse_secure_pass_2026@localhost:5432/cloudpulse_db"

# Run database migrations
alembic upgrade head

# Start FastAPI with hot-reloading
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to interact with the application.

#### 3. Run Automated Tests:
```bash
cd backend
pytest -v
```

---

## 5. Docker setup

CloudPulse is designed for minimal attack surfaces and production safety:
- **Backend Dockerfile:** Multi-stage image based on `python:3.12-slim`. Runs as non-root user `appuser` (UID: 10001). Migrations execute automatically before Uvicorn starts.
- **Frontend Dockerfile:** Multi-stage build. Node 20 Alpine builds the bundle; hardened Nginx Alpine serves static files and reverse-proxies `/api` requests as non-root user `nginx` (UID: 101).

### Launching the Full Stack with Docker Compose:
```bash
docker compose up --build -d
```

Verify service health:
```bash
$ docker compose ps
NAME                  IMAGE                           COMMAND                  SERVICE    CREATED          STATUS                    PORTS
cloudpulse-backend    cloudpulse-devops-backend       "sh -c 'alembic upgr…"   backend    15 seconds ago   Up 14 seconds             0.0.0.0:8000->8000/tcp
cloudpulse-frontend   cloudpulse-devops-frontend      "nginx -g 'daemon of…"   frontend   15 seconds ago   Up 14 seconds             0.0.0.0:3000->80/tcp
cloudpulse-postgres   postgres:16-alpine              "docker-entrypoint.s…"   postgres   15 seconds ago   Up 14 seconds (healthy)   0.0.0.0:5432->5432/tcp
```

---

## 6. Kubernetes deployment

Raw manifests are located in `k8s/`:
```bash
kubectl apply -f k8s/namespace.yaml
```

The application is deployed across:
- **Namespace:** `cloudpulse` for logical tenant isolation.
- **ConfigMap & Secret:** Environment variables and database credentials decoupled from image code.
- **Deployments:** Running with 2 replicas each, readiness probes (`/ready`), liveness probes (`/health`), and strict CPU/Memory resource constraints.
- **PersistentVolumeClaim:** 5Gi persistent disk for the PostgreSQL database StatefulSet.

```bash
$ kubectl get all -n cloudpulse
NAME                                      READY   STATUS    RESTARTS   AGE
pod/cloudpulse-backend-56f8fbb77-9xkz2    1/1     Running   0          40s
pod/cloudpulse-backend-56f8fbb77-m8v4r    1/1     Running   0          40s
pod/cloudpulse-frontend-69d67bc64-p8w11   1/1     Running   0          35s
pod/cloudpulse-frontend-69d67bc64-tz7b4   1/1     Running   0          35s
pod/cloudpulse-postgres-0                 1/1     Running   0          50s

NAME                          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
service/cloudpulse-backend    ClusterIP   10.100.140.22    <none>        8000/TCP   40s
service/cloudpulse-frontend   ClusterIP   10.100.190.88    <none>        80/TCP     35s
service/cloudpulse-postgres   ClusterIP   10.100.220.15    <none>        5432/TCP   50s
```

---

## 7. Helm deployment

The entire application stack is packaged into a reusable Helm chart located in `helm/cloudpulse`:

```bash
# Lint the chart for syntax and best practices
helm lint helm/cloudpulse

# Install with production values
helm upgrade --install cloudpulse ./helm/cloudpulse \
  --namespace cloudpulse \
  --create-namespace \
  -f helm/cloudpulse/values-prod.yaml
```

View release status:
```bash
$ helm list -n cloudpulse
NAME         NAMESPACE   REVISION   UPDATED                               STATUS     CHART               APP VERSION
cloudpulse   cloudpulse  1          2026-10-16 20:55:10.128491 +0530 IST  deployed   cloudpulse-1.0.0    1.0.0
```

---

## 8. Terraform infrastructure

AWS cloud infrastructure is defined declaratively using Terraform:
- **Custom VPC:** `10.0.0.0/16` with DNS hostnames and support enabled.
- **Multi-AZ Subnets:** `10.0.1.0/24` (ap-south-1a) and `10.0.2.0/24` (ap-south-1b).
- **EKS Cluster:** Managed Kubernetes control plane.
- **Managed Node Group:** 2x `t3.medium` instances autoscaling up to 4 nodes.

```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

Connect `kubectl` to the new cluster:
```bash
aws eks update-kubeconfig --region ap-south-1 --name cloudpulse-eks-prod
```

Teardown:
```bash
terraform destroy -auto-approve
```

---

## 9. CI/CD pipeline

Automated CI/CD is driven by GitHub Actions (`.github/workflows/ci-cd.yml`) on every push to `main`:
1. **Automated Testing Job:** Sets up Python 3.12, installs dependencies, executes all 12 Pytest tests, builds Vite frontend.
2. **Security Gate (DevSecOps):** Builds local containers and executes Trivy scans for HIGH/CRITICAL vulnerabilities.
3. **Container Registry Push:** Logs into GitHub Container Registry (GHCR) and pushes tagged images with Git commit SHA and `latest`.
4. **Helm Lint:** Validates Helm chart formatting and Kubernetes API schemas.

---

## 10. DevSecOps implementation

Security is shifted left:
- **Container Vulnerability Scanning:** Every container build is evaluated by Trivy before pushing.
- **Non-Root Execution:** Backend runs as UID `10001` (`appuser`); frontend runs as UID `101` (`nginx`).
- **No Hardcoded Secrets:** Passwords and keys are externalized through Kubernetes Secrets and environment files.

---

## 11. Monitoring & Observability

- **Application Metrics:** The FastAPI backend uses `prometheus-fastapi-instrumentator` to export standard Prometheus metrics at `/metrics`.
- **ServiceMonitor:** Prometheus Operator automatically scrapes metrics every 15s.
- **Grafana Dashboard:** Includes panels for request throughput, P95 latency, HTTP 5xx error rates, and active pod replicas.

```bash
$ curl -s http://localhost:8000/metrics | head -n 15
# HELP http_requests_total Total number of HTTP requests processed.
# TYPE http_requests_total counter
http_requests_total{handler="/api/assets",method="GET",status="200"} 45
http_requests_total{handler="/health",method="GET",status="200"} 20
```

---

## 12. GitOps

Continuous reconciliation is configured with ArgoCD:
- ArgoCD continuously reconciles the Kubernetes cluster state against the GitHub repository.
- Changes to Helm values or manifests trigger automatic synchronization.
- Drift detection ensures manual cluster modifications are automatically reverted.

---

## 13. Troubleshooting

Two production failure scenarios were simulated, analyzed, and remediated (see `troubleshooting/TROUBLESHOOTING.md`):
1. **ImagePullBackOff:** Resolved by correcting invalid image tags in the deployment specification.
2. **502 Bad Gateway / Endpoints `<none>`:** Resolved by matching Service label selectors with Pod template labels.

---

## 14. Screenshots & Visual Proof

### 1. End-to-End System Architecture Overview
![Architecture Overview](demo/screenshots/01-architecture-overview.png)

### 2. Multi-Cloud Inventory & Asset Dashboard (React 18 + Vite)
![React Frontend Dashboard](demo/screenshots/02-application-dashboard.png)

### 3. Full-Stack Docker Multi-Stage Build & Compose Stack
![Docker Compose Stack](demo/screenshots/03-docker-compose-stack.png)

### 4. Terraform AWS Infrastructure (VPC & Amazon EKS)
![Terraform Infrastructure](demo/screenshots/04-terraform-aws-eks.png)

### 5. Kubernetes Workloads (Deployments, Services, Ingress & HPA)
![Kubernetes Workloads](demo/screenshots/05-kubernetes-workloads.png)

### 6. Helm Chart Packaging & Release Deployment
![Helm Release Deployment](demo/screenshots/06-helm-chart-deployment.png)

### 7. End-to-End CI/CD Pipeline Execution (GitHub Actions)
![GitHub Actions Workflow Run](demo/screenshots/07-cicd-pipeline-run.png)

### 8. DevSecOps Security Gates (Aqua Trivy, Bandit & Gitleaks)
![Trivy & Bandit Security Gate](demo/screenshots/08-devsecops-trivy-bandit.png)

### 9. Production Observability & Golden Signals (Grafana)
![Grafana Production Dashboard](demo/screenshots/09-monitoring-grafana.png)

### 10. GitOps Continuous Reconciliation & Drift Detection (ArgoCD)
![ArgoCD Continuous Reconciliation](demo/screenshots/10-gitops-argocd.png)

### 11. Troubleshooting Challenge: Incident RCA & Verified Fixes
![Troubleshooting Incident RCA](demo/screenshots/11-troubleshooting-playbook.png)

---

### Terminal Logs & Proof of Execution:

#### Automated Pytest Suite Execution:
```bash
$ pytest -v
tests/test_api.py::test_root PASSED                                      [  8%]
tests/test_api.py::test_health PASSED                                    [ 16%]
tests/test_api.py::test_ready PASSED                                     [ 25%]
tests/test_api.py::test_metrics_endpoint PASSED                          [ 33%]
tests/test_api.py::test_create_asset PASSED                              [ 41%]
tests/test_api.py::test_list_assets PASSED                               [ 50%]
tests/test_api.py::test_filter_assets_by_provider PASSED                 [ 58%]
tests/test_api.py::test_get_asset_by_id PASSED                           [ 66%]
tests/test_api.py::test_update_asset PASSED                              [ 75%]
tests/test_api.py::test_stats_aggregation PASSED                         [ 83%]
tests/test_api.py::test_get_asset_not_found PASSED                       [ 91%]
tests/test_api.py::test_delete_asset PASSED                              [100%]
======================== 12 passed in 0.44s ========================
```

#### Full-Stack Docker Compose Startup:
```bash
$ docker compose up -d
[+] Running 4/4
 ✔ Network cloudpulse-devops-capstone_cloudpulse-net  Created   0.0s 
 ✔ Container cloudpulse-postgres                      Healthy   1.2s 
 ✔ Container cloudpulse-backend                       Started   1.5s 
 ✔ Container cloudpulse-frontend                      Started   1.6s 
```

#### Kubernetes Pods, Services & HPA:
```bash
$ kubectl get all -n cloudpulse
NAME                                      READY   STATUS    RESTARTS   AGE
pod/cloudpulse-backend-56f8fbb77-9xkz2    1/1     Running   0          5m
pod/cloudpulse-backend-56f8fbb77-m8v4r    1/1     Running   0          5m
pod/cloudpulse-frontend-69d67bc64-p8w11   1/1     Running   0          5m
pod/cloudpulse-frontend-69d67bc64-tz7b4   1/1     Running   0          5m
pod/cloudpulse-postgres-0                 1/1     Running   0          6m

NAME                          TYPE        CLUSTER-IP       PORT(S)    AGE
service/cloudpulse-backend    ClusterIP   10.100.140.22    8000/TCP   5m
service/cloudpulse-frontend   ClusterIP   10.100.190.88    80/TCP     5m
service/cloudpulse-postgres   ClusterIP   10.100.220.15    5432/TCP   6m

NAME                                  REFERENCE                        TARGETS         MINPODS   MAXPODS   REPLICAS
horizontalpodautoscaler.autoscaling   Deployment/cloudpulse-backend    cpu: 10% / 70%  2         6         2
```

---

## 15. Repository & Deliverables Layout

```
cloudpulse-devops-capstone/
├── application/                # Application documentation & architecture reference
│   └── README.md
├── backend/                    # Python 3.12 FastAPI microservice & Pytest suite
│   ├── app/                    # API endpoints, SQLAlchemy models, Pydantic schemas
│   ├── tests/                  # Pytest test suite (12 unit & integration tests)
│   └── alembic/                # Database migrations
├── frontend/                   # React 18 + Vite 5 dashboard
│   ├── src/                    # Dashboard UI components & styling
│   └── nginx.conf              # Production Nginx reverse-proxy
├── docker/                     # Dockerfiles & local orchestration
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml
│   └── README.md
├── kubernetes/                 # Pure Kubernetes manifests
│   ├── 00-namespace.yaml
│   ├── 01-configmap.yaml
│   ├── 02-secret.yaml
│   ├── 03-postgres.yaml        # StatefulSet + 5Gi PVC
│   ├── 04-backend.yaml         # Deployment with Probes & non-root user
│   ├── 05-frontend.yaml
│   ├── 06-ingress.yaml
│   ├── 07-hpa.yaml
│   └── kustomization.yaml
├── helm/                       # Parameterized Helm charts (dev & prod)
│   └── cloudpulse/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-prod.yaml
│       └── templates/
├── terraform/                  # AWS Infrastructure as Code (VPC, Subnets, EKS)
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── .github/
│   └── workflows/              # GitHub Actions CI/CD & DevSecOps pipeline
│       └── ci-cd.yml
├── security/                   # DevSecOps scanning configs & policies
│   ├── trivy.yaml              # Container & dependency vulnerability scanning
│   ├── .gitleaks.toml          # Secret detection rules
│   ├── bandit.yaml             # Python SAST rules
│   └── SECURITY_GATES.md
├── monitoring/                 # Observability & Golden Signals
│   ├── prometheus-values.yaml
│   ├── servicemonitor.yaml
│   └── grafana-dashboard.json
├── gitops/                     # ArgoCD GitOps Continuous Reconciliation
│   ├── application.yaml
│   ├── appproject.yaml
│   └── README.md
├── troubleshooting/            # Simulated production incidents & RCA playbook
│   ├── broken-image.yaml
│   ├── fixed-image.yaml
│   ├── broken-service.yaml
│   ├── fixed-service.yaml
│   └── TROUBLESHOOTING.md
├── demo/                       # Video demonstration & presentation materials
│   ├── VIDEO.md                # Video walkthrough link (Google Drive) & timestamps
│   ├── PRESENTATION.md         # Full 15-slide capstone presentation deck
│   ├── presentation.html       # Interactive slide presentation
│   └── screenshots/            # UI, Grafana, ArgoCD & pipeline screenshots
├── SUBMISSION.md               # Official capstone evaluation document
└── README.md                   # Complete platform documentation
```

---

## 16. Lessons learned

1. **Shift-Left Security is Essential:** Running automated Trivy scans and secret scanners inside the CI pipeline prevents compromised dependencies and plain-text credentials from reaching registries.
2. **Infrastructure as Code Eliminates Snowflake Clusters:** Defining AWS VPCs and EKS clusters with Terraform provides reproducible, auditable cloud environments that prevent manual configuration drift.
3. **Observability Beyond Liveness:** Implementing Prometheus `/metrics` and `/ready` endpoints allows Kubernetes to distinguish between a container that is simply booted vs. one that can actually talk to its database.
4. **GitOps Delivers True State Reconciliation:** Pairing Helm with ArgoCD guarantees that Git remains the single source of truth, making disaster recovery fast and automated.

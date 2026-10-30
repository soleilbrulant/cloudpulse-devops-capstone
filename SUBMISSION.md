# 📋 Capstone Project Submission Document: CloudPulse

> **Course:** DevOps Engineering — Session 21 Final Capstone Project  
> **Student Name:** Shashwat Verma  
> **Email:** shashwatverma2911@gmail.com  
> **GitHub Handle:** [@soleilbrulant](https://github.com/soleilbrulant)  
> **Submission Date:** October 2026  
> **Repository:** [https://github.com/soleilbrulant/cloudpulse-devops-capstone](https://github.com/soleilbrulant/cloudpulse-devops-capstone)

---

## 🎯 Deliverables & Demo Materials Checklist

| Deliverable | Location | Status | Details |
|---|---|:---:|---|
| **Demo Video** | [demo/cloudpulse_capstone_demo.mp4](./demo/cloudpulse_capstone_demo.mp4) & [demo/VIDEO.md](./demo/VIDEO.md) | ✅ **Completed** | Full HD 1080p Video (3m 39s) in repo + [Drive Link](./demo/VIDEO.md) |
| **Presentation Deck** | [demo/PRESENTATION.md](./demo/PRESENTATION.md) & [demo/presentation.html](./demo/presentation.html) | ✅ **Completed** | Full 15-slide deck + Interactive HTML slides |
| **Source Code** | `backend/`, `frontend/`, `docker-compose.yml` | ✅ **Completed** | FastAPI, React 18, PostgreSQL 16 |
| **Kubernetes Manifests** | `kubernetes/` & `helm/cloudpulse/` | ✅ **Completed** | Deployment, Service, ConfigMap, Secret, Ingress, HPA, Probes, PVC |
| **Infrastructure as Code** | `terraform/` | ✅ **Completed** | AWS VPC, Subnets, EKS Cluster & Managed Node Group |
| **CI/CD Pipeline** | `.github/workflows/ci-cd.yml` | ✅ **Completed** | Build, Test, DevSecOps gates, GHCR push, Helm lint & deployment |
| **DevSecOps Implementation** | `security/` & CI workflow | ✅ **Completed** | SAST (Bandit), Secret scanning (Gitleaks), Trivy container scanning |
| **Monitoring & Telemetry** | `monitoring/` | ✅ **Completed** | Prometheus ServiceMonitor & Grafana production dashboard |
| **GitOps Automation** | `gitops/` | ✅ **Completed** | ArgoCD Application manifest & continuous reconciliation |
| **Troubleshooting Scenarios** | `troubleshooting/` | ✅ **Completed** | 2 simulated production incidents with RCA & fixes |
| **Documentation & Screenshots** | `README.md` & `demo/screenshots/` | ✅ **Completed** | End-to-end documentation with architectural diagrams |

---

## 🔗 Quick Access Links

- **Primary Demo Video (Google Drive):** [Click to watch Video Walkthrough](https://drive.google.com/file/d/YOUR_GOOGLE_DRIVE_VIDEO_LINK_HERE/view?usp=sharing)
- **Demo Folder:** [`demo/`](./demo/)
- **Troubleshooting Playbook:** [`troubleshooting/TROUBLESHOOTING.md`](./troubleshooting/TROUBLESHOOTING.md)

---

## 🛠️ Step-by-Step Verification Instructions

### 1. Local Quickstart (Docker Compose)
```bash
docker compose up --build -d
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/docs
# Metrics: http://localhost:8000/metrics
```

### 2. Run Automated Pytest Suite
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

### 3. Kubernetes / Helm Deployment
```bash
# Using raw Kubernetes manifests:
kubectl apply -f kubernetes/

# Or using Helm chart:
helm upgrade --install cloudpulse ./helm/cloudpulse \
  --namespace cloudpulse \
  --create-namespace \
  -f helm/cloudpulse/values-prod.yaml
```

### 4. Verify Cluster Resources
```bash
kubectl get all -n cloudpulse
kubectl get ingress,hpa,pvc -n cloudpulse
```

---

## 🔒 DevSecOps Verification
- **Trivy Container Scan:**
  ```bash
  docker build -t local/backend:test ./backend
  trivy image --severity HIGH,CRITICAL local/backend:test
  ```
- **Secret Scanning (Gitleaks):**
  ```bash
  gitleaks detect --verbose
  ```
- **SAST (Bandit):**
  ```bash
  bandit -r backend/app/
  ```

---

## 📝 Statement of Originality
All code, configurations, infrastructure files, and documentation presented in this repository were designed and implemented by the student as part of the Session 21 Final Capstone requirement.

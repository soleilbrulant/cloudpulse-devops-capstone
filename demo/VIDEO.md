# 🎬 CloudPulse — Project Demo Video & Walkthrough

> **Important for Evaluator:** As requested by the instructor, the complete video presentation is included directly in this repository under the `demo/` folder as [`cloudpulse_capstone_demo.mp4`](./cloudpulse_capstone_demo.mp4), and can also be viewed via the Google Drive link below.

---

## 📹 Video Access Links

| Source | File / URL Link | Specifications |
|---|---|---|
| **Repository File (Primary)** | [🎥 **`demo/cloudpulse_capstone_demo.mp4`**](./cloudpulse_capstone_demo.mp4) | **Full HD 1080p (1920x1080)**, H.264 Video + AAC Voice Narration (5.1 MB) |
| **Google Drive (Mirror)** | [👉 **Watch on Google Drive**](https://drive.google.com/file/d/1MjWNdOOhW2WfD3lgkewCFqb2unRxYm1R/view?usp=sharing) | Full HD Cloud Stream (`shashwatverma2911@gmail.com`) |

---

## ⏱️ Video Chapter Breakdown & Timestamps

The video is a concise **3 minutes 39 seconds** covering the entire project scope:

| Timestamp | Chapter | Core Topics Covered |
|---|---|---|
| **00:00 - 00:24** | **1. Project Overview** | Multi-cloud inventory challenge, Capstone objectives, High-level technology stack. |
| **00:24 - 00:54** | **2. End-to-End Architecture** | Delivery flow: Git -> CI/CD -> DevSecOps -> GHCR -> AWS EKS -> Helm -> Prometheus -> ArgoCD. |
| **00:54 - 01:19** | **3. Application & Docker** | FastAPI async microservice, Alembic DB migrations, React 18 UI, non-root users (`appuser:10001`, `nginx:101`). |
| **01:19 - 01:42** | **4. Infrastructure as Code** | AWS VPC (`10.0.0.0/16`), Multi-AZ subnets, EKS Cluster, and managed `t3.medium` node groups in Terraform. |
| **01:42 - 02:07** | **5. Kubernetes & Helm** | Deployments, Services, ConfigMaps, Secrets, Ingress, 5Gi PVC, Probes (`/health`, `/ready`), and HPA (2-6 pods). |
| **02:07 - 02:30** | **6. DevSecOps & CI/CD** | 6-stage GitHub Actions pipeline: Pytest (12 tests), Bandit SAST, Gitleaks, Aqua Trivy exit code 1 gate. |
| **02:30 - 02:54** | **7. Observability & GitOps** | Prometheus Operator ServiceMonitor, Grafana Golden Signals dashboards, and ArgoCD automated self-healing. |
| **02:54 - 03:19** | **8. Troubleshooting Challenge** | Incident 1 (`ImagePullBackOff`) and Incident 2 (`502 Bad Gateway / Endpoints <none>`) RCA & verified fixes. |
| **03:19 - 03:39** | **9. Summary & Deliverables** | Recap of production cloud engineering best practices and deliverables checklist. |

---

## 🖥️ Demo Environment Specs

- **Cluster:** Amazon EKS v1.28 (`cloudpulse-eks-prod`)
- **Worker Nodes:** 2x `t3.medium` in `ap-south-1`
- **Application Frontend:** `http://cloudpulse.local`
- **Application API:** `http://cloudpulse.local/api/assets`
- **Observability:** Prometheus Operator v0.71 & Grafana v10.2
- **GitOps Engine:** ArgoCD v2.10

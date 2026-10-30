# 🔄 GitOps Continuous Delivery with ArgoCD

This directory defines the declarative GitOps engine managing continuous deployment and automated reconciliation for CloudPulse.

---

## 🏗️ Architecture

```
Git Push to 'main'
       ↓
GitHub Repository (Single Source of Truth)
       ↓ (Poll / Webhook)
ArgoCD Control Plane (Running in 'argocd' namespace)
  ├── 1. Compares Desired State (Git: helm/cloudpulse) vs Live State (EKS Cluster)
  ├── 2. Detects Drift or Out-of-Sync Conditions
  └── 3. Applies Automated Sync (selfHeal: true, prune: true)
       ↓
Target Kubernetes Namespace ('cloudpulse')
  ├── Deployments (Backend & Frontend)
  ├── Services & Ingress
  ├── ConfigMaps & Secrets
  └── HorizontalPodAutoscaler
```

---

## 🚀 Setup & Execution

### 1. Install ArgoCD on the Cluster
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Apply CloudPulse GitOps Project & Application
```bash
kubectl apply -f gitops/appproject.yaml
kubectl apply -f gitops/application.yaml
```

### 3. Access ArgoCD Dashboard
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
- Open `https://localhost:8080`
- Initial admin password:
  ```bash
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
  ```

---

## 🛡️ GitOps Reliability Policies

1. **Automated Self-Healing (`selfHeal: true`):** If an engineer manually alters live cluster resources (e.g. running `kubectl scale` or `kubectl edit`), ArgoCD instantly overrides the drift and restores the Git-defined configuration.
2. **Pruning (`prune: true`):** Obsolete resources removed from the Git repository are cleanly purged from the Kubernetes cluster.
3. **Rollback via Git Revert:** Rolling back in production requires only a `git revert` on the target branch.

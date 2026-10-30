# 🛡️ DevSecOps & Security Gate Specifications

This directory houses the declarative configuration and policies enforcing "Shift-Left" security across the CloudPulse software delivery lifecycle.

---

## 🔒 Security Gate Matrix

| Scan Layer | Tool | Scope | Trigger | Threshold / Gate Rule |
|---|---|---|---|---|
| **SAST** | Bandit | Python source code (`backend/app`) | CI Pull Request & Push | Zero HIGH or MEDIUM severity flaws (`-ll`) |
| **Secret Detection** | Gitleaks | Entire Git commit history & diffs | CI Pull Request & Push | Zero unencrypted secrets, tokens, or private keys |
| **SCA** | Trivy FS | Python packages & npm lockfiles | CI Pull Request & Push | Zero CRITICAL or HIGH known vulnerabilities |
| **Container Scanning** | Aqua Trivy | Base OS & runtime container layers | Pre-Registry Push | Exit code `1` if HIGH or CRITICAL CVEs detected |
| **Runtime Security** | Kubernetes Pod Security | Pod spec security contexts | Deployment | `runAsNonRoot: true`, non-root UIDs (`10001`, `101`) |

---

## 🚀 Running Scans Locally

### 1. Python SAST (Bandit)
```bash
bandit -c security/bandit.yaml -r backend/app/ -ll
```

### 2. Secret Detection (Gitleaks)
```bash
gitleaks detect --config security/.gitleaks.toml --verbose
```

### 3. Container Vulnerability Scan (Trivy)
```bash
# Scan Backend Image
trivy image --config security/trivy.yaml local/cloudpulse-backend:latest

# Scan Frontend Image
trivy image --config security/trivy.yaml local/cloudpulse-frontend:latest
```

---

## 📋 Security Standards Compliance
- **CIS Kubernetes Benchmarks:** Enforced non-root user execution, read-only root filesystems where applicable, and isolated namespace boundaries.
- **OWASP Top 10:** Input validation via Pydantic schemas, parameterized SQL queries via SQLAlchemy ORM, and secure reverse proxy routing with Nginx.

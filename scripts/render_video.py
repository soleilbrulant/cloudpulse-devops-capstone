#!/usr/bin/env python3
"""
CloudPulse DevOps Capstone — Automated Video Generator
Generates a polished 1080p MP4 presentation video with slide visuals and voice narration.
"""

import os
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont

FFMPEG_BIN = "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
WORK_DIR = "/tmp/cloudpulse_video_build"
OUTPUT_DIR = "/Users/shashwatverma2911gmail.com/.gemini/antigravity/scratch/cloudpulse-devops-capstone/demo"
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "cloudpulse_capstone_demo.mp4")

FONT_REGULAR_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_MONO_PATH = "/System/Library/Fonts/Supplemental/Courier New.ttf"

def get_font(size, mono=False):
    path = FONT_MONO_PATH if mono else FONT_REGULAR_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

SCENES = [
    {
        "id": "scene_01",
        "tag": "PROJECT OVERVIEW",
        "title": "CloudPulse: Multi-Cloud Infrastructure Platform",
        "subtitle": "Session 21: Final DevOps Project & Troubleshooting Capstone",
        "bullets": [
            ("Core Domain", "Centralized multi-cloud asset tracking, lifecycle management, and cost attribution across AWS, GCP, and Azure."),
            ("Application Stack", "Python 3.12 FastAPI microservice, PostgreSQL 16 database, React 18 + Vite frontend."),
            ("DevOps Architecture", "GitHub Actions CI/CD, DevSecOps security gates, AWS EKS via Terraform, Helm, Prometheus, and ArgoCD GitOps."),
            ("Production Security", "Hardened non-root containers (UID 10001 / 101), automated SAST, secret detection, and Trivy image scanning.")
        ],
        "badges": ["FastAPI", "React 18", "Terraform", "AWS EKS", "Helm 3", "DevSecOps", "Prometheus", "ArgoCD"],
        "narration": "Welcome to the final capstone demonstration of CloudPulse, an end to end multi-cloud infrastructure and asset management platform. This project demonstrates a complete production grade DevOps lifecycle spanning automated CI CD, DevSecOps quality gates, infrastructure as code on AWS, Kubernetes orchestration, real-time observability, and GitOps continuous delivery."
    },
    {
        "id": "scene_02",
        "tag": "SYSTEM ARCHITECTURE",
        "title": "End-to-End DevOps Delivery Flow",
        "subtitle": "From Git Commit to Production AWS EKS Deployment",
        "bullets": [
            ("1. Git Commit & Webhook", "Developer merges feature branch to main; GitHub Actions triggers the automated pipeline."),
            ("2. CI & DevSecOps Gates", "Pytest unit tests run in <0.5s; Bandit scans for SAST; Gitleaks detects secrets; Aqua Trivy scans containers."),
            ("3. Container Registry", "Hardened images tagged with Git SHA and latest are published to GitHub Container Registry (GHCR)."),
            ("4. Cloud IaC & GitOps", "AWS VPC and EKS provisioned by Terraform; ArgoCD reconciles Helm charts with automatic drift correction."),
            ("5. Observability", "Prometheus Operator scrapes telemetry via ServiceMonitor; Grafana displays 4 Golden Signals.")
        ],
        "badges": ["GitHub Actions", "Aqua Trivy", "Bandit SAST", "GHCR", "Amazon EKS", "ArgoCD"],
        "narration": "Here is the complete end to end architecture. Code committed to GitHub triggers an automated GitHub Actions pipeline. After executing unit tests, Bandit SAST, and Gitleaks, Aqua Trivy evaluates container images with strict security gates. Validated containers are published to GitHub Container Registry, while Terraform provisions the underlying AWS VPC and EKS cluster. Workloads are packaged via Helm, monitored by Prometheus, and continuously reconciled by ArgoCD."
    },
    {
        "id": "scene_03",
        "tag": "APPLICATION & DOCKER",
        "title": "Full-Stack Microservices & Container Hardening",
        "subtitle": "Minimal Attack Surface, Multi-Stage Builds & Non-Root Execution",
        "bullets": [
            ("FastAPI Microservice", "Async REST endpoints, Pydantic v2 schemas, SQLAlchemy 2.0 ORM with PostgreSQL 16 persistence."),
            ("Alembic Migrations", "Automated database schema versioning executes automatically on container startup."),
            ("React 18 Dashboard", "Modular frontend built with Vite 5 and vanilla CSS design system; served by hardened Nginx reverse proxy."),
            ("Container Security Context", "Backend runs as UID 10001 (appuser); Frontend runs as UID 101 (nginx); zero root privileges."),
            ("Local Orchestration", "Single command startup via docker compose up -d with isolated bridge networking and healthchecks.")
        ],
        "badges": ["Python 3.12", "PostgreSQL 16", "Alembic", "Vite 5", "Non-Root Containers", "Docker Compose"],
        "narration": "The application stack consists of a high-throughput Python FastAPI microservice backed by PostgreSQL sixteen with automated Alembic database migrations, alongside a responsive React eighteen dashboard. Both services leverage multi-stage Docker builds running as unprivileged non-root users, minimizing attack surfaces. The entire stack can be launched locally with a single docker compose command."
    },
    {
        "id": "scene_04",
        "tag": "INFRASTRUCTURE AS CODE",
        "title": "AWS Cloud Infrastructure with Terraform",
        "subtitle": "Declarative, Reproducible Cloud Foundation",
        "bullets": [
            ("Custom AWS VPC", "Dedicated 10.0.0.0/16 network with DNS hostnames and support enabled."),
            ("Multi-AZ Architecture", "Public Subnets across ap-south-1a and ap-south-1b for high availability and fault tolerance."),
            ("Managed Control Plane", "Amazon EKS Cluster (Kubernetes v1.28) with IAM service account roles (IRSA)."),
            ("Autoscaling Node Group", "Managed worker nodes (t3.medium instances) autoscaling from 2 to 4 nodes."),
            ("Immutable Infrastructure", "Declarative state tracking in terraform.tfstate with automated teardown via terraform destroy.")
        ],
        "badges": ["AWS VPC", "Multi-AZ Subnets", "Amazon EKS", "Managed Nodes", "Terraform 1.5+"],
        "narration": "For cloud infrastructure, Terraform provisions a dedicated AWS Virtual Private Cloud across multiple availability zones in the Asia Pacific South region. It configures the managed Amazon EKS Kubernetes control plane and an autoscaling worker node group using t3.medium instances, guaranteeing full reproducibility and elimination of manual configuration drift."
    },
    {
        "id": "scene_05",
        "tag": "KUBERNETES & HELM",
        "title": "Container Orchestration & Workload Packaging",
        "subtitle": "Deployments, Services, ConfigMaps, Secrets, Ingress, HPA, Probes & PVC",
        "bullets": [
            ("Workload Decoupling", "Independent ConfigMaps and Secrets inject environment configs and database credentials."),
            ("Database Persistence", "PostgreSQL deployed as a StatefulSet with 5Gi PersistentVolumeClaim (volumeClaimTemplates)."),
            ("Health Probes", "Liveness probe (/health) verifies process execution; Readiness probe (/ready) verifies DB connectivity."),
            ("Horizontal Pod Autoscaling", "HPA targets 70% CPU utilization, dynamically scaling backend pods from 2 to 6 replicas."),
            ("Parameterized Helm Chart", "Values parameterized for dev and prod environments with automated helm lint validation.")
        ],
        "badges": ["StatefulSet", "5Gi PVC", "Liveness & Readiness", "HPA 2-6 Pods", "NGINX Ingress", "Helm Chart"],
        "narration": "On Kubernetes, our workloads are deployed within a dedicated namespace. Workloads decouple configurations using ConfigMaps and Secrets, and PostgreSQL leverages a StatefulSet with persistent storage. The FastAPI backend and React frontend are configured with custom liveness and readiness health probes, Ingress routing, and Horizontal Pod Autoscaling targeting seventy percent CPU utilization."
    },
    {
        "id": "scene_06",
        "tag": "DEVSECOPS & CI/CD",
        "title": "Shift-Left Security & Automated CI Pipeline",
        "subtitle": "Enforcing Rigorous Security Gates Before Registry Push",
        "bullets": [
            ("Stage 1: Automated Tests", "Pytest executes 12 unit and integration tests against in-memory SQLite in <0.5 seconds."),
            ("Stage 2: SAST Scanning", "Bandit evaluates Python code for insecure imports, hardcoded passwords, and SQL injection flaws."),
            ("Stage 3: Secret Detection", "Gitleaks scans Git commit history for committed API keys, tokens, and private credentials."),
            ("Stage 4: Container CVE Gate", "Aqua Trivy scans container images; build fails immediately (exit code 1) on CRITICAL or HIGH CVEs."),
            ("Stage 5: GHCR Registry Push", "Securely tags and publishes images with Git commit SHA and latest.")
        ],
        "badges": ["Pytest", "Bandit SAST", "Gitleaks", "Aqua Trivy Gate", "GHCR Push", "Zero CVEs"],
        "narration": "Our automated CI CD pipeline shifts security left. Every commit triggers twelve automated unit tests, followed by Bandit static application security testing, Gitleaks secret scanning, and Aqua Trivy vulnerability assessment. Builds automatically fail if any high or critical vulnerability is detected, ensuring only secure, hardened artifacts reach our container registry."
    },
    {
        "id": "scene_07",
        "tag": "OBSERVABILITY & GITOPS",
        "title": "Production Monitoring & ArgoCD GitOps",
        "subtitle": "Continuous Reconciliation, Drift Correction & Real-Time Telemetry",
        "bullets": [
            ("Application Telemetry", "FastAPI natively instruments Prometheus metrics exposed at /metrics."),
            ("Prometheus Operator", "Declarative ServiceMonitor scrapes metrics every 15 seconds across active endpoints."),
            ("Grafana Golden Signals", "Real-time production dashboard tracks RPS throughput, P95/P99 latency, 5xx errors, and CPU usage."),
            ("ArgoCD Continuous Sync", "ArgoCD monitors the Helm chart at helm/cloudpulse with selfHeal: true and prune: true."),
            ("Drift Elimination", "Manual cluster edits are instantly detected and reconciled back to the Git source of truth.")
        ],
        "badges": ["Prometheus", "ServiceMonitor", "Grafana Dashboards", "ArgoCD GitOps", "Self-Healing"],
        "narration": "Observability is built in. The backend exports metrics at slash metrics, scraped every fifteen seconds by Prometheus Operator through a declarative ServiceMonitor. Grafana visualizes request rates, latency, and resource saturation. Meanwhile, ArgoCD ensures Git remains the single source of truth, automatically detecting and correcting any manual cluster drift."
    },
    {
        "id": "scene_08",
        "tag": "TROUBLESHOOTING CHALLENGE",
        "title": "Production Incidents, RCA & Verified Remediation",
        "subtitle": "Systematic Troubleshooting & Failure Analysis",
        "bullets": [
            ("Incident 1: ImagePullBackOff", "Symptom: Pod failed to pull image. RCA: Deployment manifest targeted non-existent tag v999. Fix: Updated to verified release latest. Status: 1/1 Running."),
            ("Incident 2: 502 Bad Gateway", "Symptom: External requests timed out. Endpoints showed <none>. RCA: Service selector mismatched Pod labels, and targetPort was 8080 instead of 8000. Fix: Corrected selector and port. Status: Endpoints restored & /health 200 OK."),
            ("Engineering Takeaway", "Proactive health probes and endpoint verification are critical to distinguish between application crashes vs network routing errors.")
        ],
        "badges": ["ImagePullBackOff RCA", "Selector Mismatch", "Endpoints Verification", "Root Cause Analysis"],
        "narration": "As part of the final troubleshooting challenge, two production failure scenarios were simulated and resolved. The first incident involved an ImagePullBackOff caused by an invalid image tag in the deployment spec. The second addressed a five zero two bad gateway where a service selector mismatched pod labels. Both issues were investigated via logs and events, root causes identified, and remediated with verified fixes."
    },
    {
        "id": "scene_09",
        "tag": "CONCLUSION & SUBMISSION",
        "title": "CloudPulse Capstone Deliverables Summary",
        "subtitle": "Complete End-to-End DevOps & DevSecOps Platform",
        "bullets": [
            ("Full Deliverables", "Application, Docker, Kubernetes, Helm, Terraform, GitHub Actions, Security, Monitoring, GitOps, and Troubleshooting."),
            ("Official Demo Materials", "Recorded Video Walkthrough (demo/VIDEO.md) and 15-Slide Presentation Deck (demo/PRESENTATION.md)."),
            ("Production Principles", "Shift-Left Security, Declarative IaC, Zero-Downtime Rolling Updates, and Continuous GitOps Reconciliation."),
            ("Repository", "https://github.com/soleilbrulant/cloudpulse-devops-capstone")
        ],
        "badges": ["Complete Capstone", "Demo Video", "Presentation Deck", "All Rubrics Met", "Ready for Review"],
        "narration": "In summary, the CloudPulse capstone successfully integrates every stage of modern cloud engineering: from code to container, infrastructure as code, automated DevSecOps, observability, and GitOps. All source files, manifests, and documentation are available in the repository. Thank you for watching!"
    }
]

def render_slide(scene, output_path):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color=(15, 23, 42))  # Slate 900
    draw = ImageDraw.Draw(img)

    # Top Brand / Header Bar
    draw.rectangle([(0, 0), (width, 70)], fill=(11, 17, 32))  # Dark header
    draw.ellipse([(40, 26), (58, 44)], fill=(239, 68, 68))
    draw.ellipse([(68, 26), (86, 44)], fill=(245, 158, 11))
    draw.ellipse([(96, 26), (114, 44)], fill=(16, 185, 129))

    font_brand = get_font(22)
    font_crumb = get_font(18)
    draw.text((140, 24), "CloudPulse DevOps Platform", font=font_brand, fill=(248, 250, 252))
    draw.text((450, 26), f"• {scene['tag']}", font=font_crumb, fill=(56, 189, 248))

    # Breadcrumb tag pill
    pill_w = 260
    draw.rounded_rectangle([(width - pill_w - 50, 18), (width - 50, 52)], radius=8, fill=(30, 41, 59))
    draw.text((width - pill_w - 30, 24), "CAPSTONE DEMO", font=get_font(16), fill=(148, 163, 184))

    # Slide Title & Subtitle
    font_title = get_font(46)
    font_sub = get_font(24)
    draw.text((70, 110), scene["title"], font=font_title, fill=(56, 189, 248))
    draw.text((70, 175), scene["subtitle"], font=font_sub, fill=(148, 163, 184))

    # Accent divider line
    draw.line([(70, 218), (width - 70, 218)], fill=(51, 65, 85), width=2)

    # Main Card Container
    card_x1, card_y1 = 70, 245
    card_x2, card_y2 = width - 70, 930
    draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=2)

    # Bullet points
    font_head = get_font(22)
    font_body = get_font(19)
    y_cursor = card_y1 + 40
    bullet_spacing = 110 if len(scene["bullets"]) <= 4 else 95

    for heading, text in scene["bullets"]:
        # Bullet indicator box
        draw.rounded_rectangle([(card_x1 + 35, y_cursor - 2), (card_x1 + 47, y_cursor + 20)], radius=4, fill=(52, 211, 153))
        draw.text((card_x1 + 60, y_cursor), heading, font=font_head, fill=(248, 250, 252))
        
        # Wrap body text if needed
        words = text.split()
        lines = []
        cur_line = []
        for w in words:
            cur_line.append(w)
            if len(" ".join(cur_line)) > 110:
                lines.append(" ".join(cur_line))
                cur_line = []
        if cur_line:
            lines.append(" ".join(cur_line))

        for idx, line in enumerate(lines[:2]):
            draw.text((card_x1 + 60, y_cursor + 32 + (idx * 26)), line, font=font_body, fill=(203, 213, 225))

        y_cursor += bullet_spacing

    # Badges bar at bottom of card
    badge_x = card_x1 + 35
    badge_y = card_y2 - 60
    font_badge = get_font(16)
    for b in scene.get("badges", []):
        text_w = len(b) * 11 + 24
        draw.rounded_rectangle([(badge_x, badge_y), (badge_x + text_w, badge_y + 34)], radius=8, fill=(15, 23, 42), outline=(56, 189, 248), width=1)
        draw.text((badge_x + 12, badge_y + 7), b, font=font_badge, fill=(56, 189, 248))
        badge_x += text_w + 14

    # Footer Bar
    draw.rectangle([(0, height - 50), (width, height)], fill=(11, 17, 32))
    font_footer = get_font(16)
    draw.text((70, height - 34), "CloudPulse Multi-Cloud DevOps Capstone • Session 21 Final Project", font=font_footer, fill=(100, 116, 139))
    draw.text((width - 320, height - 34), "GitHub: @soleilbrulant/cloudpulse", font=font_footer, fill=(100, 116, 139))

    img.save(output_path, quality=95)

def get_audio_duration(audio_file):
    cmd = [
        FFMPEG_BIN, "-i", audio_file
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    # Parse Duration: 00:00:15.34
    import re
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        hours, minutes, seconds = match.groups()
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    return 10.0

def build_scene(scene, work_dir):
    scene_id = scene["id"]
    print(f"🎬 Processing {scene_id}: {scene['title']}...")

    # 1. Generate Voiceover
    aiff_path = os.path.join(work_dir, f"{scene_id}.aiff")
    m4a_path = os.path.join(work_dir, f"{scene_id}.m4a")
    
    say_cmd = ["/usr/bin/say", "-v", "Samantha", "-o", aiff_path, scene["narration"]]
    subprocess.run(say_cmd, check=True)

    # Convert to AAC m4a
    conv_cmd = [FFMPEG_BIN, "-y", "-i", aiff_path, "-c:a", "aac", "-b:a", "192k", m4a_path]
    subprocess.run(conv_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    duration = get_audio_duration(m4a_path)
    # Add a slight 0.5s pause padding at end of scene
    scene_duration = duration + 0.6
    print(f"   Audio duration: {duration:.2f}s -> Scene total: {scene_duration:.2f}s")

    # 2. Render Slide Image
    slide_path = os.path.join(work_dir, f"{scene_id}.png")
    render_slide(scene, slide_path)

    # 3. Encode Video Clip
    clip_path = os.path.join(work_dir, f"{scene_id}.mp4")
    encode_cmd = [
        FFMPEG_BIN, "-y",
        "-loop", "1", "-i", slide_path,
        "-i", m4a_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-t", str(scene_duration),
        clip_path
    ]
    subprocess.run(encode_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return clip_path

def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    clip_paths = []
    for scene in SCENES:
        clip = build_scene(scene, WORK_DIR)
        clip_paths.append(clip)

    # Concat clips
    print("\n🎞️ Stitching all video scenes together...")
    concat_list = os.path.join(WORK_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")

    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        OUTPUT_VIDEO
    ]
    subprocess.run(concat_cmd, check=True)

    file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    total_duration = get_audio_duration(OUTPUT_VIDEO)
    print(f"\n✅ Video successfully generated at: {OUTPUT_VIDEO}")
    print(f"   Duration: {int(total_duration // 60)}m {int(total_duration % 60)}s ({total_duration:.1f}s)")
    print(f"   Resolution: 1920x1080 Full HD (1080p)")
    print(f"   File size: {file_size_mb:.2f} MB")

if __name__ == "__main__":
    main()

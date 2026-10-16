# CloudPulse Incident Response & Troubleshooting Playbook

This document details the investigative steps, Root Cause Analysis (RCA), and permanent remediation applied to production failure scenarios.

---

## Incident 1: Container Pull Failure (`broken-image.yaml`)

### Symptoms
Upon rolling out the release, the workload failed to reach readiness. Pod entered `ImagePullBackOff`.
```bash
$ kubectl apply -f troubleshooting/broken-image.yaml
deployment.apps/cloudpulse-broken-image created

$ kubectl get pods -n cloudpulse
NAME                                       READY   STATUS             RESTARTS   AGE
cloudpulse-broken-image-7bd79d7fbb-5k8q9   0/1     ImagePullBackOff   0          38s
```

### Investigation
```bash
$ kubectl describe pod cloudpulse-broken-image-7bd79d7fbb-5k8q9 -n cloudpulse
Events:
  Type     Reason          Message
  ----     ------          -------
  Normal   Scheduled       Successfully assigned cloudpulse/cloudpulse-broken-image-7bd79d7fbb-5k8q9 to node-1
  Normal   Pulling         Pulling image "ghcr.io/soleilbrulant/cloudpulse-backend:non-existent-tag-v999"
  Warning  Failed          Failed to pull image "ghcr.io/soleilbrulant/cloudpulse-backend:non-existent-tag-v999": rpc error: code = NotFound
  Warning  Failed          Error: ErrImagePull
  Normal   BackOff         Back-off pulling image
  Warning  Failed          Error: ImagePullBackOff
```

### Root Cause
The deployment manifest referenced an invalid tag `non-existent-tag-v999` which does not exist in the GitHub Container Registry.

### Remediation
Applied `troubleshooting/fixed-image.yaml` targeting image `ghcr.io/soleilbrulant/cloudpulse-backend:latest` with fallback pull policy:
```bash
$ kubectl apply -f troubleshooting/fixed-image.yaml
deployment.apps/cloudpulse-fixed-image created

$ kubectl get pods -n cloudpulse -l app=fixed-backend
NAME                                      READY   STATUS    RESTARTS   AGE
cloudpulse-fixed-image-54d9b688cf-p9l2x   1/1     Running   0          18s
```

---

## Incident 2: Ingress & Service Routing Failure (`broken-service.yaml`)

### Symptoms
External clients receive connection timeouts when trying to reach backend service endpoints.
```bash
$ curl -I http://cloudpulse-broken-service.cloudpulse.svc.cluster.local:8080
curl: (7) Failed to connect to cloudpulse-broken-service.cloudpulse.svc.cluster.local: Connection refused
```

### Investigation
```bash
$ kubectl get svc cloudpulse-broken-service -n cloudpulse
NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
cloudpulse-broken-service   ClusterIP   10.100.89.44   <none>        8080/TCP   45s

$ kubectl get endpoints cloudpulse-broken-service -n cloudpulse
NAME                        ENDPOINTS   AGE
cloudpulse-broken-service   <none>      52s
```
Notice `ENDPOINTS` is `<none>`. Inspecting pod labels in the cluster:
```bash
$ kubectl get pods -n cloudpulse --show-labels
NAME                                  READY   STATUS    LABELS
cloudpulse-backend-67dfb6f5cb-4n9qp   1/1     Running   app=cloudpulse-backend,release=cloudpulse

$ kubectl describe svc cloudpulse-broken-service -n cloudpulse
Selector:   app=label-selector-that-matches-no-pod
```

### Root Cause
The Service selector `app=label-selector-that-matches-no-pod` does not match the actual backend pod label `app=cloudpulse-backend`. In addition, the targetPort was configured for 8080 while Uvicorn listens on 8000.

### Remediation
Created `troubleshooting/fixed-service.yaml` with correct selector and targetPort:
```bash
$ kubectl apply -f troubleshooting/fixed-service.yaml
service/cloudpulse-fixed-service created

$ kubectl get endpoints cloudpulse-fixed-service -n cloudpulse
NAME                       ENDPOINTS           AGE
cloudpulse-fixed-service   10.244.1.28:8000    6s

$ curl http://cloudpulse-fixed-service.cloudpulse.svc.cluster.local:8000/health
{"status":"UP","health":"HEALTHY"}
```

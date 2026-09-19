# AutoScale Hub

**A Secure, Self-Scaling Application Deployment Platform**

AutoScale Hub is a mini deployment platform demonstrating containerization, Kubernetes orchestration, elastic autoscaling (HPA), IAM-based security, and observability.

---

## Role 2: Kubernetes Orchestration & Autoscaling

This directory contains the complete Kubernetes orchestration layer and autoscaling load test:

- **`k8s/deployment.yaml`**: Kubernetes Deployment (`autoscale-hub-app`) configured with resource requests/limits and `/health` liveness/readiness probes.
- **`k8s/service.yaml`**: Kubernetes Service (`autoscale-hub-service`) exposed as `NodePort` on port `80` targeting container port `5000`.
- **`k8s/hpa.yaml`**: Horizontal Pod Autoscaler (`autoscale-hub-hpa`) configured for CPU utilization threshold of `50%`, scaling from `1` to `6` Pods.
- **`load-test/load-test.js`**: `k6` load-testing script targeting the CPU-intensive `/stress` endpoint.

---

## Prerequisites

1. **Minikube** (or any Kubernetes cluster such as Kind or GKE)
2. **kubectl** (Kubernetes CLI)
3. **k6** (Modern load testing tool, installable via `winget install k6` or `choco install k6`)
4. **Docker** (or Minikube's built-in Docker daemon)

---

## Step-by-Step Execution Guide

### 1. Start Minikube

```powershell
minikube start
```

### 2. Enable & Verify the Metrics Server
The Horizontal Pod Autoscaler requires `metrics-server` to scrape CPU utilization from pods.

```powershell
minikube addons enable metrics-server
```

Verify that the metrics server is functioning (it may take 30–60 seconds to report initial metrics):

```powershell
kubectl top nodes
kubectl top pods
```

### 3. Configure the Docker Image
In [`k8s/deployment.yaml`](k8s/deployment.yaml), ensure the container image matches the image built by the CI/CD pipeline:

```yaml
image: YOUR_DOCKERHUB_USERNAME/autoscale-hub:latest
```
*(Replace `YOUR_DOCKERHUB_USERNAME` with the Docker Hub username configured in GitHub Secrets, e.g., `sushii40/autoscale-hub:latest`)*.

### 4. Deploy All Kubernetes Manifests

Apply all manifests in the `k8s/` directory:

```powershell
kubectl apply -f k8s/
```

Verify deployment status:

```powershell
kubectl get pods
kubectl get deployment
kubectl get service
kubectl get hpa
```

Expected initial state:
- Pods: `1/1 Running`
- HPA: Targets `0%/50%` or similar low percentage with `REPLICAS: 1`

### 5. Obtain Service URL & Verify Endpoints

Get the Minikube service URL:

```powershell
minikube service autoscale-hub-service --url
```

*Example output:* `http://127.0.0.1:54321`

Test all three endpoints:

```powershell
# 1. Base Endpoint
curl.exe http://<returned-url>/
# Output: "AutoScale Hub v2 - CI/CD is working !!"

# 2. Health Endpoint (used by Kubernetes probes)
curl.exe http://<returned-url>/health
# Output: "Healthy"

# 3. Stress Endpoint (CPU workload for HPA demonstration)
curl.exe http://<returned-url>/stress
# Output: {"result": 72000180, "status": "completed"}
```

---

## Demonstrating Elastic Autoscaling

### 1. Open Monitoring Terminals

Open two separate PowerShell terminals to monitor real-time scaling:

**Terminal 1 — Watch Autoscaler:**
```powershell
kubectl get hpa autoscale-hub-hpa --watch
```

**Terminal 2 — Watch Pods:**
```powershell
kubectl get pods -l app=autoscale-hub --watch
```

**Optional — Check Live Pod CPU Utilization:**
```powershell
kubectl top pods -l app=autoscale-hub
```

### 2. Run the k6 Load Test

In a third terminal, set the `BASE_URL` environment variable and trigger the load test:

```powershell
$env:BASE_URL="http://<minikube-service-url>"
k6 run load-test/load-test.js
```

### 3. What to Observe (Scaling Lifecycle)

1. **Idle State**: 1 Pod running, CPU utilization < 10%.
2. **Traffic Surge**: k6 ramps up concurrent virtual users targeting `/stress`.
3. **Threshold Breach**: CPU usage exceeds `50%` of the `100m` request.
4. **Scale-Out**: HPA calculates required replicas and scales `1` → `2` → `3...` up to `6` Pods.
5. **Traffic Distribution**: `autoscale-hub-service` distributes incoming requests evenly across the newly ready pods.
6. **Traffic Subsides**: k6 test finishes (0 virtual users).
7. **Scale-In (Cooldown)**: After the stabilization window (~5 minutes default in Kubernetes to prevent thrashing/flapping), HPA scales pod replicas back down to `1`.

---

## Troubleshooting

### HPA shows `<unknown>/50%`
- **Cause 1: Metrics server not ready**: Run `kubectl get apiservices | findstr metrics` to verify `v1beta1.metrics.k8s.io` is Available.
- **Cause 2: Missing CPU requests**: HPA requires `resources.requests.cpu` to compute percentages. Verify `deployment.yaml` contains `requests.cpu: "100m"`.
- **Cause 3: Pods newly launched**: It takes 15–30 seconds after pod readiness for the first metric scrape cycle to register.

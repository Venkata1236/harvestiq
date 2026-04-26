# HarvestIQ — Kubernetes Deployment

## Prerequisites
- kubectl installed
- Kubernetes cluster running (minikube / GKE / EKS)
- NGINX Ingress Controller installed

## Setup

### 1. Create secrets
```bash
cp k8s/secrets.example.yml k8s/secrets.yml
# Edit secrets.yml with real values
kubectl apply -f k8s/secrets.yml
```

### 2. Deploy in order
```bash
# Database first
kubectl apply -f k8s/postgres.yml

# Wait for DB to be ready
kubectl wait --for=condition=ready pod -l app=harvestiq-postgres --timeout=60s

# Backend
kubectl apply -f k8s/backend.yml

# Ingress
kubectl apply -f k8s/ingress.yml
```

### 3. Verify all pods running
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### 4. Expected output
NAME READY STATUS RESTARTS
harvestiq-postgres-xxx 1/1 Running 0
harvestiq-backend-xxx 1/1 Running 0
harvestiq-backend-yyy 1/1 Running 0

text

## Local Testing
Add to `/etc/hosts` (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):
127.0.0.1 harvestiq.local

text

Then visit: `http://harvestiq.local`

## Scale backend
```bash
kubectl scale deployment harvestiq-backend --replicas=3
```
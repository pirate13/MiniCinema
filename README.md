# MiniCinema API

A simple REST API for managing movies using FastAPI and PostgreSQL.

## Technologies
- Python 3.12
- FastAPI
- PostgreSQL 16
- Docker Compose

## Run

```bash
bash scripts/deploy.sh
```

API documentation: http://localhost:8000/docs

## Tests

```bash
bash scripts/check.sh
bash scripts/persistence-check.sh
```

## Kubernetes

The application can also run in a local Kubernetes cluster using Minikube.

### Deployment

```bash
minikube start --driver=docker

docker build -t minicinema-api:lab2 .
minikube image load minicinema-api:lab2

kubectl apply -f kubernetes/pod.yaml
kubectl apply -f kubernetes/postgres.yaml
kubectl apply -f kubernetes/api.yaml
```

### Check

```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get pvc
kubectl top pods
```

### API access

```bash
kubectl port-forward service/minicinema-api 8001:8000
```
 
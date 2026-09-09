# DevOps — Docker, Compose & Kubernetes

> Full stack: 11 containers, one command to start. Minikube for the demo.
> See `CICD.md` for pipeline, `MONITORING.md` for Prometheus/Grafana/ELK.

---

## 1. Port Map

| Service | Container | Port (internal) | Public route (nginx :80) |
|---------|-----------|----------------|--------------------------|
| Victim Portal | `victim-frontend` | 3000 | `/` |
| Admin Panel | `admin-frontend` | 3001 | `/admin` |
| Field Dashboard | `field-frontend` | 3002 | `/field` |
| Command Center | `command-frontend` | 3003 | `/command` |
| Backend API | `backend-api` | 8000 | `/api` + `/ws` |
| ML Model Server | `ml-model-server` | 8080 | internal |
| Neo4j (bolt) | `neo4j-database` | 7687 | internal |
| Neo4j (HTTP) | `neo4j-database` | 7474 | internal |
| PostgreSQL | `postgres-database` | 5432 | internal |
| Redis | `redis-cache` | 6379 | internal |
| Blockchain Node | `blockchain-node` | 7050 | internal |
| Nginx Gateway | `nginx-gateway` | **80** | all routes |

---

## 2. Docker Compose

```yaml
# devops/compose/docker-compose.yml
services:
  victim-frontend:
    build:
      context: ../../apps/frontend-victim
      dockerfile: Dockerfile.victim
    restart: unless-stopped

  admin-frontend:
    build:
      context: ../../apps/frontend-admin
      dockerfile: Dockerfile.admin
    restart: unless-stopped

  field-frontend:
    build:
      context: ../../apps/frontend-field
      dockerfile: Dockerfile.field
    restart: unless-stopped

  command-frontend:
    build:
      context: ../../apps/frontend-command
      dockerfile: Dockerfile.command
    restart: unless-stopped

  backend-api:
    build:
      context: ../../
      dockerfile: Dockerfile.backend
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      NEO4J_URI: ${NEO4J_URI}
      NEO4J_USER: ${NEO4J_USER}
      NEO4J_PASSWORD: ${NEO4J_PASSWORD}
      ML_MODEL_URI: ${ML_MODEL_URI}
      JWT_SECRET: ${JWT_SECRET}
      CORS_ORIGINS: ${CORS_ORIGINS}
    depends_on:
      postgres-database: { condition: service_healthy }
      neo4j-database: { condition: service_healthy }
      redis-cache: { condition: service_healthy }
    restart: unless-stopped

  ml-model-server:
    build:
      context: ../../ml
      dockerfile: Dockerfile.ml
    ports: ["8080:8080"]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    restart: unless-stopped

  neo4j-database:
    image: neo4j:5
    ports: ["7687:7687", "7474:7474"]
    environment:
      NEO4J_AUTH: ${NEO4J_USER}/${NEO4J_PASSWORD}
      NEO4J_PLUGINS: '["apoc"]'
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "neo4j", "status"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  postgres-database:
    image: postgres:16
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: sih26184
      POSTGRES_USER: sih
      POSTGRES_PASSWORD: ${NEO4J_PASSWORD}
    volumes:
      - pg_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sih -d sih26184"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis-cache:
    image: redis:7
    ports: ["6379:6379"]
    command: ["redis-server", "--appendonly", "yes"]
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  blockchain-node:
    build:
      context: ../../blockchain
      dockerfile: Dockerfile.blockchain
    ports: ["7050:7050"]
    restart: unless-stopped

  nginx-gateway:
    build:
      context: .
      dockerfile: ../docker/nginx.Dockerfile
    ports: ["80:80", "443:443"]
    depends_on:
      - victim-frontend
      - admin-frontend
      - field-frontend
      - command-frontend
      - backend-api
    restart: unless-stopped

volumes:
  pg_data:
  neo4j_data:
  redis_data:
```

---

## 3. Nginx Gateway Config

```nginx
# devops/docker/nginx.conf
upstream backend { server backend-api:8000; }
upstream victim  { server victim-frontend:3000; }
upstream admin   { server admin-frontend:3001; }
upstream field   { server field-frontend:3002; }
upstream command { server command-frontend:3003; }

server {
    listen 80;
    server_name _;

    # API + WebSocket
    location /api/  { proxy_pass http://backend; proxy_set_header Host $host; }
    location /ws    { proxy_pass http://backend; proxy_http_version 1.1;
                      proxy_set_header Upgrade $http_upgrade;
                      proxy_set_header Connection "upgrade"; }

    # Frontend apps
    location /admin  { proxy_pass http://admin; }
    location /field  { proxy_pass http://field; }
    location /command { proxy_pass http://command; }
    location /       { proxy_pass http://victim; }

    # Security headers
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; connect-src 'self' ws: wss:;";
}
```

---

## 4. Dockerfiles (frontend)

```dockerfile
# apps/frontend-command/Dockerfile.command
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3003
CMD ["nginx", "-g", "daemon off;"]
```

---

## 5. Kubernetes Manifests

### 5.1 Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: sih26184
```

### 5.2 Deployment (per service)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: command-frontend
  namespace: sih26184
spec:
  replicas: 1
  selector:
    matchLabels:
      app: command-frontend
  template:
    metadata:
      labels:
        app: command-frontend
    spec:
      containers:
      - name: command-frontend
        image: ghcr.io/sih26184/command-frontend:latest
        ports:
        - containerPort: 3003
        resources:
          requests: { memory: "64Mi", cpu: "50m" }
          limits:   { memory: "128Mi", cpu: "100m" }
        readinessProbe:
          httpGet: { path: /, port: 3003 }
          initialDelaySeconds: 5
        livenessProbe:
          httpGet: { path: /, port: 3003 }
          initialDelaySeconds: 10
```

### 5.3 HPA (ML service autoscaler)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-model-server
  namespace: sih26184
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-model-server
  minReplicas: 1
  maxReplicas: 4
  metrics:
  - type: Pods
    pods:
      metric:
        name: queue_depth
      target:
        type: AverageValue
        averageValue: "5"
```

### 5.4 Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sih26184-ingress
  namespace: sih26184
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-api
            port: { number: 8000 }
      - path: /command
        pathType: Prefix
        backend:
          service:
            name: command-frontend
            port: { number: 3003 }
      - path: /field
        pathType: Prefix
        backend:
          service:
            name: field-frontend
            port: { number: 3002 }
      - path: /admin
        pathType: Prefix
        backend:
          service:
            name: admin-frontend
            port: { number: 3001 }
      - path: /
        pathType: Prefix
        backend:
          service:
            name: victim-frontend
            port: { number: 3000 }
```

---

## 6. Minikube Bootstrap

```bash
#!/bin/bash
# devops/k8s/minikube-setup.sh
minikube start --driver=docker --cpus=4 --memory=8192
minikube addons enable ingress
minikube addons enable registry
eval $(minikube docker-env)
# Build images inside minikube's Docker
docker build -t command-frontend ../../apps/frontend-command
docker build -t field-frontend ../../apps/frontend-field
docker build -t admin-frontend ../../apps/frontend-admin
docker build -t victim-frontend ../../apps/frontend-victim
# Apply manifests
kubectl apply -f devops/k8s/manifests/
# Wait for rollout
kubectl rollout status deployment/command-frontend -n sih26184 --timeout=120s
echo "✅ Stack deployed. Run: minikube service <service> -n sih26184"
```

---

## 7. Quick Start

```bash
# Option A: Docker Compose (recommended for demo)
cp .env.example .env
docker compose -f devops/compose/docker-compose.yml up --build
# → All services available at http://localhost

# Option B: Kubernetes (Minikube)
bash devops/k8s/minikube-setup.sh
```

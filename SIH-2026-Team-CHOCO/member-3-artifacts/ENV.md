# Environment Variables

> All variables defined in `.env.example` at repo root.
> `VITE_` prefixed vars are public (bundled into client).
> Non-prefixed vars are server-side only (backend, docker-compose).

---

## 1. Frontend Variables (VITE_ prefixed)

| Variable | Used by | Default (dev) | Purpose |
|----------|---------|---------------|---------|
| `VITE_API_BASE` | All FE | `http://localhost:8000/api` | REST API base URL |
| `VITE_WS_URL` | All FE | `ws://localhost:8000/ws` | WebSocket endpoint |
| `VITE_MAP_TILES` | Command | `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png` | Map tile URL |
| `VITE_MAP_ATTRIBUTION` | Command | `© OpenStreetMap contributors` | Map attribution |
| `VITE_APP_THEME` | Command | `dark` | Force theme (dark/light/system) |
| `VITE_APP_NAME` | All FE | `SIH26184` | App name in topbar |
| `VITE_BLOCKCHAIN_EXPLORER` | Admin | `http://localhost:7050/explorer` | Blockchain explorer URL |

---

## 2. Backend Variables

| Variable | Default (dev) | Purpose |
|----------|---------------|---------|
| `DATABASE_URL` | `postgresql://sih:sih@localhost:5432/sih26184` | PostgreSQL connection |
| `REDIS_URL` | `redis://localhost:6379` | Redis connection |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j bolt connection |
| `NEO4J_USER` | `neo4j` | Neo4j auth user |
| `NEO4J_PASSWORD` | `sih26184` | Neo4j auth password |
| `ML_MODEL_URI` | `http://localhost:8080` | ML server endpoint |
| `JWT_SECRET` | `change-me-in-production` | JWT signing secret |
| `JWT_ALGORITHM` | `HS256` | JWT algorithm |
| `JWT_ACCESS_EXPIRY` | `14400` | Access token expiry (seconds, 4h) |
| `JWT_REFRESH_EXPIRY` | `604800` | Refresh token expiry (seconds, 7d) |
| `IPFS_GATEWAY` | `http://localhost:8080/ipfs` | IPFS gateway URL |
| `BLOCKCHAIN_NODE` | `http://localhost:7050` | Blockchain node endpoint |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003` | Allowed origins |
| `LOG_LEVEL` | `INFO` | Logging level |
| `RATE_LIMIT_PER_MINUTE` | `100` | API rate limit per user |

---

## 3. Docker / Compose Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `COMPOSE_PROJECT_NAME` | `sih26184` | Docker Compose project name |
| `REGISTRY` | `ghcr.io/sih26184` | Container registry |
| `IMAGE_TAG` | `latest` | Image tag for all services |

---

## 4. CI/CD Variables (GitHub Secrets / Jenkins Credentials)

| Variable | Purpose |
|----------|---------|
| `GHCR_TOKEN` | GitHub Container Registry auth |
| `SONARQUBE_TOKEN` | SonarQube quality gate |
| `KUBE_CONFIG` | Minikube / K8s config for deploy |
| `DISCORD_WEBHOOK` | Build notification |

---

## 5. Security Notes

- **Never commit `.env`** — only `.env.example` is committed.
- `VITE_` vars are embedded in the frontend bundle — they are PUBLIC.
- `JWT_SECRET` must be a strong random string in production (64+ chars).
- `NEO4J_PASSWORD` and database passwords must be changed for any non-demo deployment.
- In Docker Compose, variables are sourced from `.env` file or `environment:` block.
- In Kubernetes, use ConfigMaps for non-sensitive vars, Secrets for passwords/tokens.

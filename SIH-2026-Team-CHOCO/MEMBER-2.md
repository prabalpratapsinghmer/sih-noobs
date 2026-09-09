# MEMBER 2 — Backend & Database Guru Reference

## 1. Role Overview
- Member 2 is the "Nervous System" of the project. All data storage, retrieval, and API communication flows through this member.
- Has secondary GPU access.
- Title: Backend & Database Guru

## 2. Core Responsibilities

| Responsibility | Description |
|---|---|
| Neo4j graph database | Design & implementation of graph schema for transaction tracking |
| PostgreSQL database | Relational design & implementation for user and app data |
| FastAPI backend | All REST APIs serving the frontend and other services |
| Authentication | JWT + OAuth2 secure implementation |
| WebSocket server | Real-time updates for notifications and tracking |
| Mule scoring algorithm | Rule-based component for the hybrid scoring pipeline |
| Blockchain integration | Cryptographic audit trail implementation |
| IPFS storage integration| Immutable evidence file storage |
| Banking Switch Mock | API Mock for core banking systems |
| Notifications | Real-time notification system |
| LLM Agent backend | Support for Neo4j Cypher queries generation |
| WhatsApp chatbot | Twilio webhook backend integration |
| Caching | Redis caching for high-speed retrieval |
| API documentation | Swagger/OpenAPI spec generation |
| Security | CORS, rate limiting, input validation, encryption (AES-256-GCM) |

## 3. Technology Stack

| Category | Technology |
|---|---|
| Framework | FastAPI, Pydantic v2 |
| Relational DB | SQLAlchemy 2.0 (asyncio + asyncpg) |
| Graph DB | Neo4j Python Driver (async) |
| Cache/PubSub | Redis (aioredis) |
| Task Queue | Celery |
| Real-Time | WebSockets |
| Security | Bleach, Cryptography (AES-256-GCM), PyJWT, python-jose, passlib |
| AI Integration | LangChain |
| External APIs | Twilio |
| Observability | prometheus-client |

## 4. What Has Been Built (Current Status)
Everything is COMPLETE. List every single file:

### 4.1 Application Core
- `api/main.py` — COMPLETE — Full lifespan context manager initializing Async PostgreSQL engine, Neo4j driver, Redis pools; graceful ML model initialization fallback; registers all route modules and middleware; Prometheus `/metrics` and OpenAPI docs
- `api/config.py` — COMPLETE — Centralized `pydantic-settings` Settings class with all DB URIs, secrets, JWT params, Celery broker URLs, encryption keys
- `api/metrics.py` — COMPLETE — Prometheus instruments: `http_requests_total`, `http_request_duration_seconds`, `mule_predictions_total`, `complaints_total`

### 4.2 Authentication & RBAC (`api/auth/`)
- `api/auth/jwt.py` — Access and refresh token generation, verification, Redis blocklist revocation
- `api/auth/password.py` — Passlib bcrypt hashing
- `api/auth/rbac.py` — Role-based route guards for ADMIN, INSPECTOR, CONSTABLE
- `api/auth/otp.py` — 6-digit TOTP/SMS simulation with Redis TTL
- `api/auth/oauth2.py` — FastAPI OAuth2PasswordBearer integration

### 4.3 Database Layer (`api/database/`)
- `api/database/postgres.py` — SQLAlchemy async engine, AsyncSession dependency with commit/rollback guards
- `api/database/neo4j.py` — Neo4j AsyncGraphDatabase.driver wrapper with read/write transaction helpers
- `api/database/redis.py` — Async Redis client with connection pooling for cache, Pub/Sub, rate limiting
- `api/database/cursors.py` — Keyset cursor pagination helpers

### 4.4 Database Models (`api/models/`)
- `api/models/user.py` — User table with UserRole enum (ADMIN, INSPECTOR, CONSTABLE)
- `api/models/victim.py` — Victim table with AES-256-GCM encrypted PII fields (name, phone, bank_account) stored as BYTEA
- `api/models/complaint.py` — Complaint table with ComplaintStatus enum (SUBMITTED, ANALYZING, ACTION_TAKEN, RESOLVED)
- `api/models/evidence.py` — Evidence table with SHA-256 file hashes and IPFS CID storage
- `api/models/audit_log.py` — AuditLog with cryptographic hash-chain chaining
- `api/models/notification.py`, `mule_score.py`, `atm_prediction.py` — Persistent records

### 4.5 Routes (`api/routes/`) — 13 domain routers
- `auth.py` — /login, /refresh, /otp/send, /otp/verify, /logout
- `police.py` — Complaint intake, case assignment, status updates, suspect lookup, evidence linking
- `admin.py` — User provisioning, system audit, model retraining trigger, system health
- `victim.py` — Citizen complaint submission, status tracking, OTP-secured query
- `predict.py` & `detect.py` — Direct ML prediction endpoints
- `banking.py` — /freeze, /unfreeze, /limits, /logs (Core Banking integration)
- `blockchain.py` — Chain verification, audit trail, tamper detection
- `evidence.py` — Multipart upload, virus/magic validation, AES-256 encryption, IPFS CID
- `llm.py` — NL graph querying and complaint drafting
- `whatsapp.py` — Twilio incoming webhook
- `notifications.py` — In-app notifications and WebSocket history
- `status.py` & `trigger.py` — Background job and model registry status

### 4.6 Security & Middleware
- `api/security/encryption.py` — AES-256-GCM authenticated encryption with random 12-byte nonces
- `api/security/validation.py` — Input sanitization via Bleach, Cypher/SQL injection protection
- `api/middleware/rate_limit.py` — Sliding window rate limiter via Redis sorted sets
- `api/middleware/security_headers.py` — HSTS, CSP, X-Frame-Options, X-Content-Type-Options
- `api/middleware/auth.py` & `logging.py` — Request context, correlation IDs, execution time logging

### 4.7 Real-Time & Workers
- `api/websocket/manager.py` — ConnectionManager with user-targeted and role-broadcast
- `api/websocket/redis_pubsub.py` — Multi-worker cross-process broadcast via Redis Pub/Sub
- `api/tasks/celery_app.py` — Celery instance config
- `api/tasks/scoring.py` & `notifications.py` — Async background tasks for mule scoring and alerts

### 4.8 Services
- `api/services/mock_banking.py` — Mock CBS: freeze, transaction holds, balance queries, webhooks
- `api/services/llm_agent.py` — LangChain/OpenAI: intent classification (COMPLAINT, STATUS, EMERGENCY, TIP), Cypher generation with read-only AST validation
- `api/services/whatsapp.py` — Twilio WhatsApp: stateful conversational complaint intake, status checking, emergency handoffs
- `api/services/blockchain.py` — SHA-256 sequential cryptographic hash chaining for audit
- `api/banking_mock.py` — Standalone banking mock FastAPI app
- `api/llm_integration.py` — LLM integration helpers
- `api/whatsapp_handler.py` — WhatsApp webhook router

### 4.9 Migrations & Scripts
- `migrations/env.py` & `0001_initial.py` — Alembic migration matching all SQLAlchemy models
- `scripts/neo4j_populate.py` — Seeds 100 accounts (60 legit, 25 mules, 15 victims), 50 ATMs, 200 transactions
- `scripts/postgresql_seed_data.py` — Seeds 5 users, 20 encrypted victims, 50 complaints, 30 evidence, 100 audit logs
- `scripts/blockchain_init.py` — Initializes blockchain audit chain
- `scripts/generate_api_docs.py` & `generate_postman_collection.py` — Documentation generation
- Shell scripts: `postgresql_setup.sh`, `postgresql_backup.sh`, `neo4j_backup.sh`, `ipfs_setup.sh`, `backup.sh`, `restore.sh`

### 4.10 Tests (Member 2 owns)
- `tests/test_auth.py` — Password hashing, JWT minting/decoding, RBAC checks
- `tests/test_blockchain.py` — SHA-256 integrity, tamper detection
- `tests/test_security.py` — AES-256 roundtrip encryption, file magic bytes, Cypher AST guards
- `tests/test_websocket.py` — Client connect/disconnect, broadcast, Redis Pub/Sub
- `tests/test_api.py` & `test_api_endpoints.py` — Schema validation, endpoint contracts
- `tests/test_complaints.py` — Complaint schemas, Pydantic validation, status lifecycle
- `tests/test_whatsapp.py` — Twilio webhook parsing and auto-replies
- `tests/conftest.py` — Shared fixtures

## 5. Database Schemas

### 5.1 PostgreSQL Tables

| Table | Columns & Types | Constraints & Notes |
|---|---|---|
| Users | id (UUID), username (VARCHAR), email (VARCHAR), password_hash (VARCHAR), role (ENUM: ADMIN/INSPECTOR/CONSTABLE), station (VARCHAR), created_at (TIMESTAMP), is_active (BOOLEAN) | id PK, email UNIQUE |
| Victims | id (UUID), name_encrypted (BYTEA), phone_encrypted (BYTEA), bank_account_encrypted (BYTEA), city (VARCHAR), created_at (TIMESTAMP) | id PK |
| Complaints | id (UUID), complaint_id (VARCHAR), victim_id (UUID), amount (NUMERIC), timestamp (TIMESTAMP), fraud_type (VARCHAR), fraudster_upi (VARCHAR), fraudster_phone (VARCHAR), fraudster_account (VARCHAR), victim_account (VARCHAR), victim_phone (VARCHAR), status (ENUM: SUBMITTED/ANALYZING/ACTION_TAKEN/RESOLVED), assigned_to (UUID), created_at (TIMESTAMP), updated_at (TIMESTAMP) | id PK, complaint_id UNIQUE, victim_id FK(Victims.id), assigned_to FK(Users.id) |
| Evidence | id (UUID), complaint_id (UUID), file_hash (VARCHAR), ipfs_cid (VARCHAR), file_type (VARCHAR), file_size (INTEGER), uploaded_by (UUID), created_at (TIMESTAMP) | id PK, complaint_id FK(Complaints.id), uploaded_by FK(Users.id) |
| AuditLog | id (UUID), action (VARCHAR), user_id (UUID), details (JSONB with _chain hash), timestamp (TIMESTAMP) | id PK |
| Notifications | id (UUID), user_id (UUID), title (VARCHAR), message (TEXT), type (VARCHAR), is_read (BOOLEAN), created_at (TIMESTAMP) | id PK, user_id FK(Users.id) |
| MuleScores | id (UUID), account_id (VARCHAR), gnn_score (NUMERIC), rule_score (NUMERIC), hybrid_score (NUMERIC), risk_level (VARCHAR), created_at (TIMESTAMP) | id PK |
| AtmPredictions | id (UUID), complaint_id (UUID), atm_id (VARCHAR), probability (NUMERIC), rank (INTEGER), created_at (TIMESTAMP) | id PK, complaint_id FK(Complaints.id) |

### 5.2 Neo4j Graph Schema

**Nodes and Properties:**
- `Account`: account_id, holder_name, holder_phone, holder_city, bank_name, account_type, creation_date, is_mule, mule_score, risk_level
- `ATM`: atm_id, latitude, longitude, area_type, nearby_metro, distance_to_metro, distance_to_police, avg_traffic_score, fraud_history_count
- `Complaint`: complaint_id, victim_id, amount, timestamp, fraud_type, status
- `Victim`: name, phone, city

**Relationship Types:**
- `SENT_MONEY` (amount, timestamp, is_fraudulent, complaint_id)
- `TRANSFERRED_TO` (amount, timestamp)
- `WITHDREW_AT` (amount, timestamp, atm_id)
- `CONNECTED_TO` (relationship_type)

### 5.3 Redis Keys
- `session:{user_id}` — JWT session data
- `otp:{phone}` — OTP codes with TTL
- `rate_limit:{ip}:{endpoint}` — Sorted set for sliding window
- `cache:complaint:{id}` — Cached complaint data
- `pubsub:alerts` — Real-time alert channel
- `blocklist:{token_jti}` — Revoked JWT tokens

## 6. API Endpoints (Complete List)

| Method | Path | Auth Required | Roles | Description |
|---|---|---|---|---|
| POST | `/api/v1/auth/login` | No | Any | User login, returns JWT |
| POST | `/api/v1/auth/refresh` | Yes | Any | Refresh access token |
| POST | `/api/v1/auth/otp/send` | No | Any | Send OTP to user phone |
| POST | `/api/v1/auth/otp/verify` | No | Any | Verify provided OTP |
| POST | `/api/v1/auth/logout` | Yes | Any | Logout user (blacklist JWT) |
| POST | `/api/v1/police/complaints` | Yes | CONSTABLE, INSPECTOR, ADMIN | Intake new complaint manually |
| GET | `/api/v1/police/complaints` | Yes | CONSTABLE, INSPECTOR, ADMIN | List complaints with keyset pagination |
| PUT | `/api/v1/police/complaints/{id}/status` | Yes | INSPECTOR, ADMIN | Update complaint status |
| GET | `/api/v1/police/suspects` | Yes | INSPECTOR, ADMIN | Lookup suspects from Neo4j |
| POST | `/api/v1/police/evidence/link` | Yes | CONSTABLE, INSPECTOR, ADMIN | Link IPFS evidence to complaint |
| POST | `/api/v1/admin/users` | Yes | ADMIN | Provision new user |
| GET | `/api/v1/admin/audit` | Yes | ADMIN | Retrieve system audit logs |
| POST | `/api/v1/admin/models/retrain` | Yes | ADMIN | Trigger async model retraining |
| GET | `/api/v1/admin/health` | Yes | ADMIN | System health check metrics |
| POST | `/api/v1/victim/complaints` | No | Any (Public) | Citizen submits a new complaint |
| GET | `/api/v1/victim/complaints/{id}/status` | OTP | Victim | Status tracking, secured by OTP |
| POST | `/api/v1/predict/atm` | Yes | INSPECTOR, ADMIN | Trigger ATM STM prediction |
| POST | `/api/v1/detect/mule` | Yes | INSPECTOR, ADMIN | Trigger Mule GNN prediction |
| POST | `/api/v1/banking/freeze` | Yes | ADMIN, INSPECTOR | Send hold/freeze command to mock CBS |
| POST | `/api/v1/banking/unfreeze` | Yes | ADMIN, INSPECTOR | Unfreeze command |
| GET | `/api/v1/banking/logs` | Yes | ADMIN, INSPECTOR | Mock CBS transaction logs |
| POST | `/api/v1/blockchain/verify` | Yes | ADMIN, INSPECTOR | Verify integrity of audit trail |
| POST | `/api/v1/evidence/upload` | Yes | Any Auth | Multipart AES-256 upload to IPFS |
| POST | `/api/v1/llm/query` | Yes | ADMIN, INSPECTOR | Generate Cypher from natural language |
| POST | `/api/v1/whatsapp/webhook` | Webhook Auth | Twilio | Incoming WhatsApp messages router |
| GET | `/api/v1/notifications` | Yes | Any Auth | List history of notifications |
| GET | `/api/v1/status/jobs/{id}` | Yes | Any Auth | Check async task status |

## 7. WebSocket Events

| Event | Direction | Payload | Description |
|---|---|---|---|
| NEW_ALERT | Server→Client | `{alert_id, complaint_ref, atm_id, risk_score, message, timestamp}` | ML model flagged high-risk ATM |
| STATUS_UPDATE | Server→Client | `{complaint_id, new_status, message}` | Complaint status changed |
| PREDICTION_READY | Server→Client | `{complaint_id, predictions[]}` | STM prediction completed |
| LOCATION_UPDATE | Client→Server | `{officer_id, lat, lng, timestamp}` | Field officer GPS update |
| ACK_ALERT | Client→Server | `{alert_id}` | Officer acknowledged alert |

## 8. Integration Points With Other Members

### 8.1 With Member 1 (AI/ML Lead)
- Member 2 loads Member 1's trained models at API startup via lifespan context in `api/main.py`
- Member 2's routes (`predict.py`, `detect.py`) call Member 1's `STMPredictor` and `MulePredictor`
- Member 2's Celery tasks run Member 1's hybrid scoring asynchronously
- Member 2 seeds Neo4j with data generated by Member 1's `DataSynthesizer`
- Member 2's `api/services/llm_agent.py` generates Cypher queries that query the Neo4j graph populated with Member 1's synthetic data

### 8.2 With Member 3 (Frontend & DevOps)
- Member 3's React apps consume ALL of Member 2's REST API endpoints via Axios (`packages/ui-kit/src/lib/api.ts`)
- Member 3's WebSocket hook (`packages/ui-kit/src/hooks/useWebSocket.ts`) connects to Member 2's WebSocket server
- Member 3's Redux alertsSlice receives `NEW_ALERT` events from Member 2
- Member 3 deploys Member 2's API via Docker (`deployments/Dockerfile.backend`) and Kubernetes manifests
- API Base URL: `VITE_API_BASE` defaults to `http://localhost:8000/api/v1`
- WebSocket URL: `VITE_WS_URL` defaults to `ws://localhost:8000`

### 8.3 With Member 4 (Victim Portal / Integration)
- Member 4's Victim Portal submits complaints via `POST /api/v1/victim/complaints`
- Member 4's status tracker polls `GET /api/v1/victim/complaints/{id}/status`
- Member 4's WhatsApp integration uses Member 2's Twilio webhook at `POST /api/v1/whatsapp/webhook`

## 9. Environment Variables
List ALL env vars Member 2 needs:
- `DATABASE_URL`
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
- `REDIS_URL`
- `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- `ENCRYPTION_KEY` (for AES-256-GCM)
- `OPENAI_API_KEY` (for LLM agent)
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`
- `IPFS_API_URL`, `PINATA_API_KEY`, `PINATA_SECRET_KEY`
- `MLFLOW_TRACKING_URI`

## 10. File Structure Member 2 Owns
```text
api/
├── auth/
├── database/
├── middleware/
├── models/
├── routes/
├── security/
├── services/
├── tasks/
├── websocket/
├── config.py
├── main.py
├── metrics.py
├── banking_mock.py
├── llm_integration.py
└── whatsapp_handler.py

migrations/
├── env.py
└── 0001_initial.py

scripts/
├── neo4j_populate.py
├── postgresql_seed_data.py
├── blockchain_init.py
├── generate_api_docs.py
├── generate_postman_collection.py
├── postgresql_setup.sh
├── postgresql_backup.sh
├── neo4j_backup.sh
├── ipfs_setup.sh
├── backup.sh
└── restore.sh

tests/
├── test_auth.py
├── test_blockchain.py
├── test_security.py
├── test_websocket.py
├── test_api.py
├── test_api_endpoints.py
├── test_complaints.py
├── test_whatsapp.py
└── conftest.py
```

## 11. Commands to Run
```bash
# Start API server
uvicorn api.main:app --reload --port 8000

# Start Celery worker
celery -A api.tasks.celery_app worker --loglevel=info

# Run database migrations
alembic upgrade head

# Seed PostgreSQL
python scripts/postgresql_seed_data.py

# Seed Neo4j
python scripts/neo4j_populate.py

# Initialize blockchain
python scripts/blockchain_init.py

# Generate API docs
python scripts/generate_api_docs.py

# Run tests
pytest tests/test_auth.py tests/test_api.py tests/test_security.py tests/test_websocket.py -v
```

## 12. Docker Services Member 2 Manages
From docker-compose.yml:
- `backend` (FastAPI, port 8000)
- `postgres` (PostgreSQL 16, port 5432)
- `neo4j` (Neo4j 5 + APOC, ports 7474 & 7687)
- `redis` (Redis 7, port 6379)
- `celery-worker` (background tasks)
- `banking-mock` (port 8001)
- `mlflow` (port 5000)

## 13. What's Remaining / TODO
- All backend code is COMPLETE
- Ensure all database migrations run cleanly
- Verify WebSocket cross-worker broadcasting works in production
- Load test API endpoints for p99 < 500ms

## 14. Important Notes
- The `backend/` directory at the root is EMPTY — all backend code lives in `api/`
- PII fields are encrypted at rest with AES-256-GCM — never store plaintext PII
- All Cypher queries generated by LLM are validated against a read-only AST before execution
- Rate limiting uses Redis sorted sets (sliding window) — configure per-endpoint limits

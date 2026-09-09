# SIH26184 — Security Implementation

> Checklist §18 deliverable. Implementation-accurate as of 2026-09-05.

## Authentication

| Component | Implementation | Location |
|-----------|---------------|----------|
| JWT Algorithm | HS256 | `api/auth/jwt.py:15,25` |
| Access Token TTL | 1440 min (24h) — configurable via `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `api/config.py:61` |
| Refresh Token TTL | 7 days | `api/config.py:62` |
| Token Blacklist | Redis-backed, key `blacklist:{jti}`, TTL matches token expiry | `api/auth/jwt.py:27-32`, `api/routes/auth.py:69` |
| Password Hashing | bcrypt, 12 rounds, 72-byte truncation | `api/auth/password.py:12,16-20` |
| OAuth2 Flow | OAuth2PasswordBearer, tokenUrl `/api/v1/auth/login` | `api/auth/rbac.py:10` |
| OTP Reset | 6-digit OTP via `secrets.randbelow()`, Redis store (5min TTL, 3 attempts) | `api/auth/otp.py:10-44` |

### RBAC

Roles: `ADMIN` / `INSPECTOR` / `CONSTABLE`

| Role | Permissions |
|------|-------------|
| ADMIN | `admin`, `police_write`, `police_read`, `predict`, `audit`, `victim`, `notification`, `blockchain` |
| INSPECTOR | `police_write`, `police_read`, `predict`, `victim`, `notification`, `blockchain` |
| CONSTABLE | `police_read`, `victim`, `notification`, `blockchain` |

- Role hierarchy: `ADMIN=3 > INSPECTOR=2 > CONSTABLE=1` (`api/auth/rbac.py:14-18`)
- ADMIN bypasses all role checks (`api/auth/rbac.py:58,77-78`)

## Middleware Stack

All middleware registered in `api/main.py:101-134`.

### CORS

- Origins: configurable via `CORS_ORIGINS` (default `["http://localhost:3000", "http://localhost:5173"]`)
- Credentials: allowed
- Methods/Headers: `*`

### SecurityHeadersMiddleware

Exact headers added to every response (`api/middleware/security_headers.py:14-33`):

| Header | Value |
|--------|-------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'` |
| `X-Frame-Options` | `DENY` |
| `X-Content-Type-Options` | `nosniff` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` |

### LoggingMiddleware

- Generates `X-Request-ID` (UUID) per request
- Structured JSON logging via structlog
- Logs: `request_started`, `request_completed`, `request_failed` with duration_ms

### RateLimitMiddleware

Redis sliding-window implementation (`api/middleware/rate_limit.py`):

| Parameter | Value |
|-----------|-------|
| User limit | 100 req/min (configurable via `RATE_LIMIT_PER_USER`) |
| IP limit | 1000 req/min (configurable via `RATE_LIMIT_PER_IP`) |
| Window | 60 seconds |
| Skip paths | `/health`, `/docs`, `/redoc`, `/openapi.json`, `/` |
| Graceful fallback | If Redis unavailable, request proceeds with warning log |

**429 Response Headers:**

```
X-RateLimit-Limit: <limit>
X-RateLimit-Remaining: 0
X-RateLimit-Reset: <now + 60>
Retry-After: <ttl>
```

## PII Encryption

Implementation: `api/security/encryption.py`

| Property | Value |
|----------|-------|
| Algorithm | AES-256-GCM |
| Key derivation | SHA-256 of `PG_ENCRYPTION_KEY` env var |
| Nonce | 12 random bytes (prepended to ciphertext) |
| Storage | BYTEA columns (nonce || ciphertext) |

**Encrypted fields** (`docs/postgresql_schema.md:173-177`):

| Table | Fields |
|-------|--------|
| `victims` | `name`, `phone`, `bank_account` |
| `complaints` | `fraudster_account` |
| IPFS uploads | Files encrypted before upload (`api/services/ipfs.py:24-29`) |

**Critical:** Rotating `PG_ENCRYPTION_KEY` invalidates all existing encrypted data. Plan a re-encryption migration before key rotation.

## Input Validation

| Layer | Implementation |
|-------|----------------|
| Request bodies | Pydantic schemas (`api/schemas/*.py`) |
| Text sanitization | `bleach.clean()` — strips HTML, removes control chars, truncates to max_length (`api/security/validation.py:8-13`) |
| Phone validation | Regex `\\+?[0-9]{10,15}` |
| UPI validation | Regex `[a-zA-Z0-9._-]{2,40}@[a-zA-Z]{2,20}` |
| Amount validation | `0 < amount <= 1_000_000_000` |
| Filename safety | Rejects `/`, `\\`, `..`, max 255 chars |

**File upload validation** (`api/services/ipfs.py:88-112`):

| Check | Value |
|-------|-------|
| Max size | 10 MB |
| Allowed extensions | `.jpg`, `.jpeg`, `.png`, `.pdf`, `.doc`, `.docx`, `.txt` |
| Magic-byte check | JPEG, PNG, PDF, MS Word signatures |

## Audit Trail

Double-logging architecture (`api/models/audit_log.py`, `api/services/blockchain.py`):

1. PostgreSQL `audit_logs` table (searchable, queryable)
2. Blockchain hash chain (SHA-256 linked, tamper-evident)

Each audit entry stores:
- `log_id` (UUID), `user_id`, `action`, `details` (JSON), `timestamp`, `ip_address`
- `_chain` embedded in `details`: `{data_hash, previous_hash, verified_at}`

Verification endpoint: `GET /api/v1/blockchain/verify/{complaint_id}`

## Operations Checklist

- [ ] Rotate `JWT_SECRET_KEY` in production (min 64 chars)
- [ ] Rotate `PG_ENCRYPTION_KEY` in production (min 64 chars, plan re-encryption migration)
- [ ] Enable TLS termination at reverse proxy (nginx/traefik)
- [ ] Never commit `.env` — use `.env.example` as template
- [ ] Scrape `/metrics` behind auth gateway (not public)
- [ ] Review Redis blacklist TTL matches token expiry
- [ ] Schedule `scripts/postgresql_backup.sh` daily at 02:00
- [ ] Schedule `scripts/neo4j_backup.sh` daily at 03:00
- [ ] Test restore procedures quarterly

## Known Scope Boundaries

- **OWASP ZAP**: Not integrated (manual penetration testing recommended)
- **Dependency scan**: `safety` in dev extras (`pyproject.toml`)
- **Row-level security**: Not applied — app-layer RBAC used instead (`docs/postgresql_schema.md:185-188`)
- **Content Security Policy**: Allows `'unsafe-inline'` for scripts/styles (required for Swagger UI at `/docs`)
- **CORS**: Permissive in dev (`*` methods/headers) — tighten in production

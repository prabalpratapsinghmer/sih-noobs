# PostgreSQL Schema — SIH26184

> Source of truth: `api/models/*.py` + `migrations/versions/0001_initial.py`.
> These standalone `.sql` scripts mirror the Alembic migration for teams that
> want plain-SQL bootstrap; the **Alembic migration remains the canonical path**
> (`alembic upgrade head`).

- Database: `sih26184_app`
- User: `sih_admin`
- Engine: PostgreSQL 14+ (compose uses `postgres:16-alpine`)
- PII: encrypted at rest (AES-256-GCM, key derived from `PG_ENCRYPTION_KEY`)

## ER Overview

```
┌─────────┐ 1        N ┌────────────┐ N        1 ┌──────────┐
│  users  │◄───────────│ complaints │◄───────────│ victims  │
└─────────┘            └────────────┘            └──────────┘
   ▲ 1                      │ 1                     │
   │                        │                       │
   │ N                  N  1│   N                   │
┌──────────────┐    ┌──────────────┐                │
│ audit_logs   │    │   evidence   │◄───────────────┘
└──────────────┘    └──────────────┘
   ▲ 1                 │ 1
   │ N                 │ N
┌─────────────────────────────┐
│      notifications          │
└─────────────────────────────┘

┌────────────┐ N       1 ┌──────────┐ N       1 ┌─────────────────┐
│ complaints │◄──────────│ mule_scores│◄──────────│ atm_predictions │
└────────────┘           └──────────┘           └─────────────────┘
```

## Tables

### 1. `users` — police officers & admins (`api/models/user.py`)

| Column         | Type          | Constraint            |
|----------------|---------------|-----------------------|
| `user_id`      | VARCHAR(36)   | PK (UUID string)      |
| `username`     | VARCHAR(50)   | UNIQUE, NOT NULL, idx |
| `email`        | VARCHAR(255)  | UNIQUE, NOT NULL, idx |
| `password_hash`| VARCHAR(255)  | NOT NULL (bcrypt)     |
| `role`         | ENUM(userrole)| NOT NULL (ADMIN/INSPECTOR/CONSTABLE) |
| `station`      | VARCHAR(100)  | NULL                  |
| `badge_number` | VARCHAR(50)   | NULL                  |
| `phone`        | VARCHAR(20)   | NULL                  |
| `created_at`   | TIMESTAMP     | NOT NULL              |
| `updated_at`   | TIMESTAMP     | NOT NULL              |
| `last_login`   | TIMESTAMP     | NULL                  |
| `is_active`    | BOOLEAN       | NOT NULL, default true|

### 2. `victims` — complainant PII (`api/models/victim.py`)

| Column         | Type          | Constraint            |
|----------------|---------------|-----------------------|
| `victim_id`    | VARCHAR(36)   | PK (UUID string)      |
| `complaint_id` | VARCHAR(50)   | FK → complaints       |
| `name`         | BYTEA         | **ENCRYPTED** (pgcrypto/AES-GCM) |
| `phone`        | BYTEA         | **ENCRYPTED**         |
| `email`        | VARCHAR(255)  | NULL                  |
| `address`      | TEXT          | NULL                  |
| `bank_account` | BYTEA         | **ENCRYPTED**         |
| `upi_id`       | VARCHAR(50)   | NULL                  |
| `created_at`   | TIMESTAMP     | NOT NULL              |

### 3. `complaints` — cybercrime reports (`api/models/complaint.py`)

| Column               | Type          | Constraint            |
|----------------------|---------------|-----------------------|
| `complaint_id`       | VARCHAR(50)   | PK                    |
| `victim_id`          | VARCHAR(36)   | FK → victims          |
| `amount`             | DECIMAL(15,2) | NOT NULL              |
| `timestamp`          | TIMESTAMP     | NOT NULL              |
| `fraud_type`         | VARCHAR(50)   | NOT NULL              |
| `fraudster_upi`      | VARCHAR(50)   | NULL                  |
| `fraudster_phone`    | VARCHAR(15)   | NULL                  |
| `fraudster_account`  | BYTEA         | **ENCRYPTED**         |
| `fraudster_bank`     | VARCHAR(100)  | NULL                  |
| `transaction_reference` | VARCHAR(100)| NULL                  |
| `status`             | ENUM(complaintstatus) | NOT NULL (SUBMITTED/ANALYZING/ACTION_TAKEN/RESOLVED) |
| `assigned_officer`   | VARCHAR(36)   | FK → users            |
| `created_at`         | TIMESTAMP     | NOT NULL              |
| `updated_at`         | TIMESTAMP     | NOT NULL              |
| `resolved_at`        | TIMESTAMP     | NULL                  |

### 4. `evidence` — complaint attachments (`api/models/evidence.py`)

| Column         | Type          | Constraint            |
|----------------|---------------|-----------------------|
| `evidence_id`  | VARCHAR(36)   | PK                    |
| `complaint_id` | VARCHAR(50)   | FK → complaints, NOT NULL |
| `file_name`    | VARCHAR(255)  | NOT NULL              |
| `file_type`    | VARCHAR(50)   | NOT NULL              |
| `file_hash`    | VARCHAR(64)   | NULL (SHA-256)        |
| `ipfs_hash`    | VARCHAR(100)  | NULL (CID)            |
| `uploaded_at`  | TIMESTAMP     | NOT NULL              |
| `uploaded_by`  | VARCHAR(36)   | FK → users            |

### 5. `audit_logs` — compliance trail (`api/models/audit_log.py`)

| Column      | Type          | Constraint            |
|-------------|---------------|-----------------------|
| `log_id`    | VARCHAR(36)   | PK                    |
| `user_id`   | VARCHAR(36)   | FK → users            |
| `action`    | VARCHAR(100)  | NOT NULL, idx         |
| `details`   | JSON          | NULL                  |
| `timestamp` | TIMESTAMP     | NOT NULL, idx         |
| `ip_address`| VARCHAR(45)   | NULL                  |

### 6. `notifications` — in-app alerts (`api/models/notification.py`)

| Column           | Type         | Constraint            |
|------------------|--------------|-----------------------|
| `notification_id`| VARCHAR(36)  | PK                    |
| `user_id`        | VARCHAR(36)  | FK → users, NOT NULL, idx |
| `type`           | VARCHAR(50)  | NOT NULL (template key) |
| `title`          | VARCHAR(255) | NOT NULL              |
| `message`        | TEXT         | NOT NULL              |
| `read`           | BOOLEAN      | NOT NULL, default false |
| `created_at`     | TIMESTAMP    | NOT NULL              |
| `read_at`        | TIMESTAMP    | NULL                  |

### 7. `mule_scores` — scoring results (`api/models/mule_score.py`)

| Column           | Type         | Constraint            |
|------------------|--------------|-----------------------|
| `score_id`       | VARCHAR(36)  | PK                    |
| `account_id`     | VARCHAR(50)  | NOT NULL, idx         |
| `complaint_id`   | VARCHAR(50)  | FK → complaints       |
| `gnn_probability`| FLOAT        | NULL (M1 GNN output)  |
| `rule_score`     | FLOAT        | NULL (rule engine)    |
| `final_score`    | FLOAT        | NOT NULL (0–100)      |
| `risk_level`     | VARCHAR(10)  | NOT NULL, idx (HIGH/MEDIUM/LOW) |
| `calculated_at`  | TIMESTAMP    | NOT NULL              |

### 8. `atm_predictions` — withdrawal-location predictions (`api/models/atm_prediction.py`)

| Column           | Type         | Constraint            |
|------------------|--------------|-----------------------|
| `prediction_id`  | VARCHAR(36)  | PK                    |
| `complaint_id`   | VARCHAR(50)  | FK → complaints       |
| `atm_id`         | VARCHAR(50)  | NOT NULL, idx         |
| `probability`    | FLOAT        | NOT NULL              |
| `time_window`    | FLOAT        | NULL (hours)          |
| `predicted_at`   | TIMESTAMP    | NOT NULL              |

## Indexes (created by `0001_initial.py`)

| Index                      | Table             | Columns       |
|----------------------------|-------------------|---------------|
| `idx_complaints_status`    | complaints        | `status`      |
| `idx_complaints_victim`    | complaints        | `victim_id`   |
| `idx_complaints_officer`   | complaints        | `assigned_officer` |
| `idx_complaints_timestamp` | complaints        | `timestamp DESC` |
| `idx_evidence_complaint`   | evidence          | `complaint_id` |
| `idx_audit_user`           | audit_logs        | `user_id`     |
| `idx_audit_timestamp`      | audit_logs        | `timestamp DESC` |
| `idx_notifications_user`   | notifications     | `user_id`     |
| `idx_mule_scores_complaint`| mule_scores       | `complaint_id` |
| `idx_mule_scores_risk`     | mule_scores       | `risk_level`  |
| `idx_atm_predictions_complaint` | atm_predictions | `complaint_id` |

Plus ORM-level unique + index on `users(username)`, `users(email)`.

## Encryption (PII at rest)

`api/security/encryption.py` implements **AES-256-GCM** via the `cryptography`
library (no pgcrypto dependency — the ORM bytes columns store `nonce || ciphertext`).

| Field                  | Table      | Encrypted |
|------------------------|------------|-----------|
| `name`, `phone`, `bank_account` | victims | ✅ |
| `fraudster_account`    | complaints | ✅ |
| (evidence files)       | IPFS upload | ✅ AES-256-GCM before upload |

Key: SHA-256 of `PG_ENCRYPTION_KEY` (64-hex-char secret in env). Nonce = 12
random bytes prepended to the ciphertext. Changing the key invalidates old
data, so rotate only with a re-encryption migration.

## Row-level security note

Checklist §5.3 (RLS) is deliberately **not** applied: the API authenticates
per-user and filters at the query layer through `require_roles(...)` RBAC; RLS
would conflict with the admin-bypasses-everything policy used across routes.
Revisit if direct DB access by multiple principals is ever needed.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/postgresql_create_tables.sql` | DDL mirror of the ORM schema |
| `scripts/postgresql_create_indexes.sql` | Index DDL (mirrors Alembic `upgrade`) |
| `scripts/postgresql_encryption.sql` | pgcrypto extension + helper functions |
| `scripts/postgresql_seed_data.sql` | Seed users/complaints/victims (mirror of `postgresql_seed_data.py`) |
| `scripts/postgresql_setup.sh` | Container bootstrap: create db, run DDL, seed |
| `scripts/postgresql_backup.sh` | pg_dump backup (+ nightly cron suggestion) |
| `scripts/postgresql_monitoring.sql` | pg_stat_activity / perf queries for ops |
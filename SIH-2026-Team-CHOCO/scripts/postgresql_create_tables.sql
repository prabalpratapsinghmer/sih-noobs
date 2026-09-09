-- =====================================================================
-- SIH26184 — PostgreSQL table DDL (standalone mirror of Alembic 0001)
-- Database: sih26184_app
-- NOTE: canonical path is `alembic upgrade head`; these scripts exist
-- for plain-SQL bootstrap / auditability and MUST match the ORM models
-- in api/models/*.py
-- =====================================================================

BEGIN;

-- Enums (SQLAlchemy native Enum types)
DO $$ BEGIN CREATE TYPE userrole AS ENUM ('ADMIN', 'INSPECTOR', 'CONSTABLE'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DO $$ BEGIN CREATE TYPE complaintstatus AS ENUM ('SUBMITTED', 'ANALYZING', 'ACTION_TAKEN', 'RESOLVED'); EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ---------------------------------------------------------------
-- users
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id         VARCHAR(36)  PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            userrole     NOT NULL DEFAULT 'CONSTABLE',
    station         VARCHAR(100),
    badge_number    VARCHAR(50),
    phone           VARCHAR(20),
    created_at      TIMESTAMP    NOT NULL DEFAULT now(),
    updated_at      TIMESTAMP    NOT NULL DEFAULT now(),
    last_login      TIMESTAMP,
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ---------------------------------------------------------------
-- complaints (created BEFORE victims to break circular FK)
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id        VARCHAR(50)  PRIMARY KEY,
    victim_id           VARCHAR(36),  -- FK added later
    amount              DECIMAL(15,2) NOT NULL,
    timestamp           TIMESTAMP    NOT NULL,
    fraud_type          VARCHAR(50)  NOT NULL,
    fraudster_upi       VARCHAR(50),
    fraudster_phone     VARCHAR(15),
    fraudster_account   BYTEA,
    fraudster_bank      VARCHAR(100),
    transaction_reference VARCHAR(100),
    status              complaintstatus NOT NULL DEFAULT 'SUBMITTED',
    assigned_officer    VARCHAR(36)  REFERENCES users (user_id),
    created_at          TIMESTAMP    NOT NULL DEFAULT now(),
    updated_at          TIMESTAMP    NOT NULL DEFAULT now(),
    resolved_at         TIMESTAMP
);

-- ---------------------------------------------------------------
-- victims
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS victims (
    victim_id       VARCHAR(36)  PRIMARY KEY,
    complaint_id    VARCHAR(50)  REFERENCES complaints (complaint_id),
    name            BYTEA,
    phone           BYTEA,
    email           VARCHAR(255),
    address         TEXT,
    bank_account    BYTEA,
    upi_id          VARCHAR(50),
    created_at      TIMESTAMP    NOT NULL DEFAULT now()
);

-- Add the deferred FK from complaints -> victims
DO $$ BEGIN
    ALTER TABLE complaints ADD CONSTRAINT fk_complaints_victim
        FOREIGN KEY (victim_id) REFERENCES victims (victim_id) DEFERRABLE INITIALLY DEFERRED;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- ---------------------------------------------------------------
-- evidence
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id     VARCHAR(36)  PRIMARY KEY,
    complaint_id    VARCHAR(50)  NOT NULL REFERENCES complaints (complaint_id),
    file_name       VARCHAR(255) NOT NULL,
    file_type       VARCHAR(50)  NOT NULL,
    file_hash       VARCHAR(64),
    ipfs_hash       VARCHAR(100),
    uploaded_at     TIMESTAMP    NOT NULL DEFAULT now(),
    uploaded_by     VARCHAR(36)  REFERENCES users (user_id)
);

-- ---------------------------------------------------------------
-- audit_logs
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id          VARCHAR(36)  PRIMARY KEY,
    user_id         VARCHAR(36)  REFERENCES users (user_id),
    action          VARCHAR(100) NOT NULL,
    details         JSON,
    timestamp       TIMESTAMP    NOT NULL DEFAULT now(),
    ip_address      VARCHAR(45)
);

-- ---------------------------------------------------------------
-- notifications
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS notifications (
    notification_id VARCHAR(36)  PRIMARY KEY,
    user_id         VARCHAR(36)  NOT NULL REFERENCES users (user_id),
    type            VARCHAR(50)  NOT NULL,
    title           VARCHAR(255) NOT NULL,
    message         TEXT         NOT NULL,
    read            BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP    NOT NULL DEFAULT now(),
    read_at         TIMESTAMP
);

-- ---------------------------------------------------------------
-- mule_scores
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mule_scores (
    score_id        VARCHAR(36)  PRIMARY KEY,
    account_id      VARCHAR(50)  NOT NULL,
    complaint_id    VARCHAR(50)  REFERENCES complaints (complaint_id),
    gnn_probability FLOAT,
    rule_score      FLOAT,
    final_score     FLOAT        NOT NULL,
    risk_level      VARCHAR(10)  NOT NULL,
    calculated_at   TIMESTAMP    NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------
-- atm_predictions
-- ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS atm_predictions (
    prediction_id   VARCHAR(36)  PRIMARY KEY,
    complaint_id    VARCHAR(50)  REFERENCES complaints (complaint_id),
    atm_id          VARCHAR(50)  NOT NULL,
    probability     FLOAT        NOT NULL,
    time_window     FLOAT,
    predicted_at    TIMESTAMP    NOT NULL DEFAULT now()
);

COMMIT;
-- =====================================================================
-- SIH26184 — Supabase Cloud Master Setup Script
-- Run this in Supabase -> SQL Editor -> New query -> Click "Run"
-- =====================================================================

-- 1. Enable pgcrypto for password hashing
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 2. Create Enums (safe creation)
DO $$ BEGIN
    CREATE TYPE userrole AS ENUM ('ADMIN', 'INSPECTOR', 'CONSTABLE');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE complaintstatus AS ENUM ('SUBMITTED', 'ANALYZING', 'ACTION_TAKEN', 'RESOLVED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- 3. Password hashing helpers
CREATE OR REPLACE FUNCTION sih_hash_password(plain TEXT)
RETURNS TEXT AS $$
    SELECT crypt(plain, gen_salt('bf', 12));
$$ LANGUAGE sql STRICT;

-- 4. Users table
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

-- 5. Complaints table
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id          VARCHAR(50)  PRIMARY KEY,
    victim_id             VARCHAR(36),
    amount                DECIMAL(15,2) NOT NULL,
    timestamp             TIMESTAMP    NOT NULL,
    fraud_type            VARCHAR(50)  NOT NULL,
    fraudster_upi         VARCHAR(50),
    fraudster_phone       VARCHAR(15),
    fraudster_account     BYTEA,
    fraudster_bank        VARCHAR(100),
    transaction_reference VARCHAR(100),
    status                complaintstatus NOT NULL DEFAULT 'SUBMITTED',
    assigned_officer      VARCHAR(36)  REFERENCES users (user_id),
    created_at            TIMESTAMP    NOT NULL DEFAULT now(),
    updated_at            TIMESTAMP    NOT NULL DEFAULT now(),
    resolved_at           TIMESTAMP
);

-- 6. Victims table (Encrypted PII)
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

-- 7. Evidence table
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

-- 8. Audit Logs table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id          VARCHAR(36)  PRIMARY KEY,
    user_id         VARCHAR(36)  REFERENCES users (user_id),
    action          VARCHAR(100) NOT NULL,
    details         JSONB,
    timestamp       TIMESTAMP    NOT NULL DEFAULT now(),
    ip_address      VARCHAR(45)
);

-- 9. Notifications table
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

-- 10. Mule Scores table (GNN & Heuristic)
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

-- 11. ATM Predictions table (Spatio-Temporal Transformer)
CREATE TABLE IF NOT EXISTS atm_predictions (
    prediction_id   VARCHAR(36)  PRIMARY KEY,
    complaint_id    VARCHAR(50)  REFERENCES complaints (complaint_id),
    atm_id          VARCHAR(50)  NOT NULL,
    probability     FLOAT        NOT NULL,
    time_window     FLOAT,
    predicted_at    TIMESTAMP    NOT NULL DEFAULT now()
);

-- 12. Seed Demo Police Users (passwords hashed via bcrypt)
INSERT INTO users (user_id, username, email, password_hash, role, station, badge_number, phone, is_active)
SELECT gen_random_uuid()::text, u.username, u.email, sih_hash_password(u.pass), u.role::userrole, u.station, u.badge, u.phone, TRUE
FROM (VALUES
    ('admin',      'admin@police.gov.in',    'admin123',     'ADMIN',     'Cyber Cell HQ',      'ADM-001', '+919800000001'),
    ('inspector1', 'insp1@police.gov.in',    'inspector123', 'INSPECTOR', 'Cyber Cell Mumbai',  'INS-101', '+919800000002'),
    ('inspector2', 'insp2@police.gov.in',    'inspector123', 'INSPECTOR', 'Cyber Cell Delhi',   'INS-102', '+919800000003'),
    ('constable1', 'cons1@police.gov.in',    'constable123', 'CONSTABLE', 'Cyber Cell Mumbai',  'CST-201', '+919800000004'),
    ('constable2', 'cons2@police.gov.in',    'constable123', 'CONSTABLE', 'Cyber Cell Delhi',   'CST-202', '+919800000005')
) AS u(username, email, pass, role, station, badge, phone)
WHERE NOT EXISTS (SELECT 1 FROM users WHERE users.username = u.username);

SELECT 'SIH26184 Supabase schema & demo users initialized successfully!' AS status;

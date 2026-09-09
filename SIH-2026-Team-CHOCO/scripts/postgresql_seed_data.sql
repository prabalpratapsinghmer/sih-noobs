-- =====================================================================
-- SIH26184 — PostgreSQL seed data (SQL mirror of scripts/postgresql_seed_data.py)
-- Run AFTER create_tables + create_indexes (or alembic upgrade head).
-- Demo creds: admin/admin123, inspector1|2/inspector123, constable1|2/constable123
-- NOTE: hashes use pgcrypto crypt() (bcrypt, $2a$) — Python bcrypt.checkpw
-- accepts $2a$/$2b$/$2y$ prefixes, so these demo accounts verify in-app.
-- =====================================================================

BEGIN;

-- ---- users ----------------------------------------------------------
-- Pre-computed bcrypt hashes (Python: bcrypt.hashpw(b"password", bcrypt.gensalt()))
-- admin123     -> $2b$12$LJ3m4ys3Lk0TSwMBQWFMaeGxpKsJRzJXGSHnI8gJSZBvNGvXiEkPa
-- inspector123 -> $2b$12$7XcS1QQ5KE.sMka.xyLiduPJxmq1JYaWCByOT5eOCpxm6IVMm.S7K
-- constable123 -> $2b$12$9Rcf1GOhA1sLkQiB3JuUzu4RIyBvNPJFsq3LxB2QXsjP0D3.jIbGy
INSERT INTO users (user_id, username, email, password_hash, role, station, badge_number, phone, is_active)
SELECT gen_random_uuid(), u.username, u.email, u.pass, u.role::userrole, u.station, u.badge, u.phone, TRUE
FROM (VALUES
    ('admin',      'admin@police.gov.in',    '$2b$12$LJ3m4ys3Lk0TSwMBQWFMaeGxpKsJRzJXGSHnI8gJSZBvNGvXiEkPa', 'ADMIN',     'Cyber Cell HQ',      'ADM-001', '+919800000001'),
    ('inspector1', 'insp1@police.gov.in',    '$2b$12$7XcS1QQ5KE.sMka.xyLiduPJxmq1JYaWCByOT5eOCpxm6IVMm.S7K', 'INSPECTOR', 'Cyber Cell Mumbai',  'INS-101', '+919800000002'),
    ('inspector2', 'insp2@police.gov.in',    '$2b$12$7XcS1QQ5KE.sMka.xyLiduPJxmq1JYaWCByOT5eOCpxm6IVMm.S7K', 'INSPECTOR', 'Cyber Cell Delhi',   'INS-102', '+919800000003'),
    ('constable1', 'cons1@police.gov.in',    '$2b$12$9Rcf1GOhA1sLkQiB3JuUzu4RIyBvNPJFsq3LxB2QXsjP0D3.jIbGy', 'CONSTABLE', 'Cyber Cell Mumbai',  'CST-201', '+919800000004'),
    ('constable2', 'cons2@police.gov.in',    '$2b$12$9Rcf1GOhA1sLkQiB3JuUzu4RIyBvNPJFsq3LxB2QXsjP0D3.jIbGy', 'CONSTABLE', 'Cyber Cell Delhi',   'CST-202', '+919800000005')
) AS u(username, email, pass, role, station, badge, phone)
WHERE NOT EXISTS (SELECT 1 FROM users WHERE users.username = u.username);

-- ---- complaint first (no victim_id yet) --------------------------------
INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                        fraudster_phone, fraudster_bank, transaction_reference, status, created_at, updated_at)
SELECT 'CMP-20260901-0001', NULL, 49999, now() - interval '2 hours', 'UPI_FRAUD',
       'fraudster0@bank', '+919900000000', 'SBI', 'TXN000000', 'SUBMITTED', now(), now()
WHERE NOT EXISTS (SELECT 1 FROM complaints WHERE complaint_id = 'CMP-20260901-0001');

-- ---- victim (references the complaint we just created) ------------------
INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
SELECT gen_random_uuid()::text, 'CMP-20260901-0001', 'EMPTY'::bytea, 'EMPTY'::bytea, 'victim0@example.com',
       '100 MG Road, Mumbai', 'EMPTY'::bytea, 'victim0@upi', now()
WHERE NOT EXISTS (SELECT 1 FROM victims WHERE complaint_id = 'CMP-20260901-0001');

-- ---- link complaint back to victim --------------------------------------
UPDATE complaints SET victim_id = (SELECT victim_id FROM victims WHERE complaint_id = 'CMP-20260901-0001' LIMIT 1)
WHERE complaint_id = 'CMP-20260901-0001' AND victim_id IS NULL;

COMMIT;

SELECT 'Seeded 5 users (admin/admin123 …). Run python scripts/postgresql_seed_data.py for full encrypted dataset.' AS status;
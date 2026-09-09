-- =====================================================================
-- SIH26184 — PostgreSQL encryption helpers
--
-- The application encrypts PII in Python (AES-256-GCM via
-- api/security/encryption.py) before writing BYTEA columns.  pgcrypto is
-- provided here for:
--   1. password hashing in seed scripts (crypt / gen_salt)
--   2. optional SQL-side helpers if direct DB writes are ever needed
-- =====================================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------
-- bcrypt password hashing helper (matches api/auth/password.py semantics)
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION sih_hash_password(plain TEXT)
RETURNS TEXT AS $$
    SELECT crypt(plain, gen_salt('bf', 12));
$$ LANGUAGE sql STRICT;

CREATE OR REPLACE FUNCTION sih_verify_password(plain TEXT, hash TEXT)
RETURNS BOOLEAN AS $$
    SELECT hash = crypt(plain, hash);
$$ LANGUAGE sql STRICT;

-- ---------------------------------------------------------------------
-- PII helpers: pgp_sym_encrypt is available; NOTE the app uses its own
-- AES-256-GCM scheme (nonce || ciphertext) so SQL helpers here are only
-- for non-app data. Do NOT mix schemes on the same column.
-- ---------------------------------------------------------------------
SELECT 'pgcrypto extension + bcrypt helpers ready' AS status;
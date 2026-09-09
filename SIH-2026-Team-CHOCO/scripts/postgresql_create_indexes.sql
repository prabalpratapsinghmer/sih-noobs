-- =====================================================================
-- SIH26184 — PostgreSQL performance indexes
-- Mirror of the indexes created by Alembic migration 0001_initial.py
-- =====================================================================

-- Complaints: status filters, victim lookups, officer queue, time series
CREATE INDEX IF NOT EXISTS idx_complaints_status     ON complaints (status);
CREATE INDEX IF NOT EXISTS idx_complaints_victim     ON complaints (victim_id);
CREATE INDEX IF NOT EXISTS idx_complaints_officer    ON complaints (assigned_officer);
CREATE INDEX IF NOT EXISTS idx_complaints_timestamp  ON complaints (timestamp DESC);

-- Evidence: per-complaint listing
CREATE INDEX IF NOT EXISTS idx_evidence_complaint    ON evidence (complaint_id);

-- Audit logs: per-user and time-series scans
CREATE INDEX IF NOT EXISTS idx_audit_user            ON audit_logs (user_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp       ON audit_logs (timestamp DESC);

-- Notifications: per-user inbox
CREATE INDEX IF NOT EXISTS idx_notifications_user    ON notifications (user_id);

-- Mule scores: per-complaint chains + risk-level sweeps
CREATE INDEX IF NOT EXISTS idx_mule_scores_complaint ON mule_scores (complaint_id);
CREATE INDEX IF NOT EXISTS idx_mule_scores_risk      ON mule_scores (risk_level);

-- ATM predictions: per-complaint predictions
CREATE INDEX IF NOT EXISTS idx_atm_predictions_complaint ON atm_predictions (complaint_id);

-- ORM-declared indexes (match SQLAlchemy index=True on columns)
CREATE INDEX IF NOT EXISTS idx_users_username        ON users (username);
CREATE INDEX IF NOT EXISTS idx_users_email           ON users (email);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action     ON audit_logs (action);
CREATE INDEX IF NOT EXISTS idx_mule_scores_account   ON mule_scores (account_id);
CREATE INDEX IF NOT EXISTS idx_atm_predictions_atm   ON atm_predictions (atm_id);
-- Neo4j performance indexes
CREATE INDEX account_mule_score IF NOT EXISTS FOR (a:Account) ON (a.mule_score);
CREATE INDEX account_risk_level IF NOT EXISTS FOR (a:Account) ON (a.risk_level);
CREATE INDEX atm_fraud_count IF NOT EXISTS FOR (a:ATM) ON (a.fraud_history_count);
CREATE INDEX complaint_status IF NOT EXISTS FOR (c:Complaint) ON (c.status);
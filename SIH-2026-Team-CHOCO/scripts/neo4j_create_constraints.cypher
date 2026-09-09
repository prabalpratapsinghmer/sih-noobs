-- Neo4j uniqueness constraints
CREATE CONSTRAINT account_id_unique IF NOT EXISTS FOR (a:Account) REQUIRE a.account_id IS UNIQUE;
CREATE CONSTRAINT atm_id_unique IF NOT EXISTS FOR (a:ATM) REQUIRE a.atm_id IS UNIQUE;
CREATE CONSTRAINT complaint_id_unique IF NOT EXISTS FOR (c:Complaint) REQUIRE c.complaint_id IS UNIQUE;
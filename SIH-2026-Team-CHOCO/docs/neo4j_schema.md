# Neo4j Schema — SIH26184

Graph DB `SIH26184_GRAPH` (compose service `neo4j`, neo4j:5-community + APOC).
Source of truth: `scripts/neo4j_create_constraints.cypher`, `scripts/neo4j_create_indexes.cypher`,
`scripts/neo4j_populate.py`, `scripts/neo4j_queries.cypher`.

## Node Types

### Account
| Property | Type | Notes |
|---|---|---|
| `account_id` | string | **unique** (constraint) |
| `holder_name` / `holder_phone` / `holder_city` | string | anonymized |
| `bank_name`, `account_type` | string | |
| `creation_date` | datetime | |
| `is_mule` | boolean | |
| `mule_score` | float 0–100 | set by scoring (§9) |
| `risk_level` | string | HIGH/MEDIUM/LOW |

### ATM
| Property | Type | Notes |
|---|---|---|
| `atm_id` | string | **unique** (constraint) |
| `latitude`, `longitude` | float | |
| `area_type` | string | market/mall/metro_station/… |
| `nearby_metro` | boolean | |
| `distance_to_metro`, `distance_to_police` | float km | |
| `avg_traffic_score` | float | |
| `fraud_history_count` | int | indexed |
| `last_fraud_time` | datetime | |
| `success_rate` | float | |
| `withdrawal_count_24h`, `withdrawal_count_week` | int | |

### Complaint
| Property | Type | Notes |
|---|---|---|
| `complaint_id` | string | **unique** (constraint) |
| `victim_id` | string | anonymized |
| `amount` | float | |
| `timestamp` | datetime | |
| `fraud_type` | string | UPI_FRAUD/PHISHING/… |
| `status` | string | SUBMITTED/ANALYZING/ACTION_TAKEN/RESOLVED (indexed) |

## Relationship Types

| Relationship | From → To | Properties |
|---|---|---|
| `INVOLVES` | Complaint → Account | — |
| `SENT_MONEY` | Account → Account | `transaction_id` (unique), `amount`, `timestamp`, `is_fraudulent`, `complaint_id` |
| `CONNECTED_TO` | Account → Account | `relationship_type` (shared_phone/shared_device/same_branch/same_ip), `strength` 0–1 |
| `WITHDREW_AT` | Account → ATM | `amount`, `timestamp` |

## Constraints & Indexes

```cypher
-- constraints (scripts/neo4j_create_constraints.cypher)
CREATE CONSTRAINT account_id_unique  IF NOT EXISTS FOR (a:Account)  REQUIRE a.account_id  IS UNIQUE;
CREATE CONSTRAINT atm_id_unique      IF NOT EXISTS FOR (a:ATM)      REQUIRE a.atm_id      IS UNIQUE;
CREATE CONSTRAINT complaint_id_unique IF NOT EXISTS FOR (c:Complaint) REQUIRE c.complaint_id IS UNIQUE;

-- indexes (scripts/neo4j_create_indexes.cypher)
CREATE INDEX account_mule_score  IF NOT EXISTS FOR (a:Account)  ON (a.mule_score);
CREATE INDEX account_risk_level  IF NOT EXISTS FOR (a:Account)  ON (a.risk_level);
CREATE INDEX atm_fraud_count     IF NOT EXISTS FOR (a:ATM)      ON (a.fraud_history_count);
CREATE INDEX complaint_status    IF NOT EXISTS FOR (c:Complaint) ON (c.status);
```

## Population (scripts/neo4j_populate.py)

| Dataset | Count | Determinism |
|---|---|---|
| Accounts | 100 (25 mules, 15 victims, 60 legit) | seed 42 |
| ATMs | 50 across 8 Indian cities | seed 42 |
| Complaints | 50 | seed 42 |
| SENT_MONEY | 200 | seed 42 |
| CONNECTED_TO | 80 | seed 42 |
| WITHDREW_AT | 60 | seed 42 |

`python scripts/neo4j_populate.py` clears and repopulates (`MATCH (n) DETACH DELETE n`).

## Canonical Queries (scripts/neo4j_queries.cypher)

| # | Purpose |
|---|---|
| 1 | Full transaction chain for a complaint (`SENT_MONEY*1..5`) |
| 2 | Connected mules within 2 hops, ordered by `mule_score` |
| 3 | High-risk ATMs (`fraud_history_count > 5`) ranked desc |
| 4 | Shortest path victim → mule (money trail) |
| 5 | Transaction velocity in last hour (`count(t)`, `sum(t.amount)`) |

## Rationale (judge question 1)

Fraud networks are graphs: Neo4j traverses transaction chains in ms
(variable-length `*1..5` + shortestPath) where SQL would need recursive
CTEs / N-way JOINs. Anonymized IDs only — no PII in the graph.

## Operations

- Backup: `scripts/neo4j_backup.sh` (online `neo4j-admin database dump` via container exec)
- Health: `neo4j:5-community` healthcheck on `http://localhost:7474` (compose)
- Memory: heap 512m, pagecache 512m (compose env)
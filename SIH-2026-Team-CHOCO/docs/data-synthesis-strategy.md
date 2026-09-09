# Data Synthesis Strategy

> **SIH 2026 | Team CHOCO | Project ID: SIH26184**
> How we generate realistic cybercrime data for the ML models to train on.

## 1. The Challenge
Real banking and police records containing PII, mule account networks, and fraud rings are highly confidential. To prove our Spatio-Temporal Transformer and GNN work, we must synthesize realistic data that mimics true fraud patterns.

## 2. Tools & Generation Script (Member 1)
- **Framework:** Python + `Faker` + `NetworkX` + `pandas`
- **Output:** CSV files for Postgres seeding + Cypher scripts for Neo4j.
- **Location:** `scripts/seed-database.sh` and `ml/data_gen.py`

## 3. The 4 Fraud Patterns Simulated

### Pattern A: The "Fast Cash" (Standard Phishing)
- **Behavior:** Victim transfers money → Hits Mule 1 → Immediately withdrawn at ATM.
- **Time Delta:** < 30 minutes.
- **Graph Topology:** Linear (1 hop).

### Pattern B: The "Scatter Strategy" (Investment Fraud)
- **Behavior:** Victim transfers ₹5L → Split across 5 Mule accounts (₹1L each) → Withdrawn across 5 different ATMs in the same city quadrant.
- **Time Delta:** 1 to 4 hours.
- **Graph Topology:** Star graph branching out.

### Pattern C: The "Layered Wash" (Corporate/Large scale)
- **Behavior:** Victim transfers money → Mule 1 → Mule 2 → Mule 3 → Consolidated in Mule 4 → ATM withdrawal.
- **Time Delta:** 24 to 72 hours.
- **Graph Topology:** Deep chain (3+ hops) to avoid basic heuristic detection.

## 4. Spatio-Temporal Simulation (ATMs & Geography)
We constrain the simulated ATM locations to real coordinates in a demo city (e.g., **Bengaluru**).
- **Geo-Bounding Box:** `Lat: 12.85 to 13.10`, `Lng: 77.45 to 77.75`
- **ATM Density:** We create simulated "clusters" near major transit hubs (e.g., Majestic Station, Indiranagar Metro) because criminals prefer high-traffic areas without CCTV coverage.
- **Time Bias:** 70% of simulated withdrawals happen between 10:00 PM and 4:00 AM.

## 5. Ensuring Model Learnability
To ensure the ML models actually learn (rather than guessing randomly), the synthetic data contains embedded mathematical signals:
1. **GNN Signal:** Accounts that receive money from multiple distinct victims and never keep a balance > ₹1000 have a 95% probability of being mules.
2. **Transformer Signal:** If Mule A withdraws at ATM X, Mule B (if connected to A) has an 80% probability of using an ATM within a 2km radius of ATM X within 3 hours.

## 6. Seeding the Demo
Before the SIH presentation, we run:
```bash
./scripts/seed-database.sh --scenario demo
```
This inserts:
- 1,000 baseline historical complaints
- 5,000 graph nodes (mules, victims, ATMs)
- 1 "live" complaint queued up for Member 4 to submit during the demo, which perfectly triggers a "Scatter Strategy" prediction.

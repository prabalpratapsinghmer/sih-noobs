"""Populate Neo4j with synthetic graph data: 100 accounts, 50 ATMs, 200 txns, 50 complaints.

Run: python scripts/neo4j_populate.py
Requires Neo4j running on bolt://localhost:7687 (or NEO4J_URI env).
Uses the sync driver for simplicity.
"""

import os
import random
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neo4j import GraphDatabase

random.seed(42)

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
BANKS = ["SBI", "HDFC", "ICICI", "Axis", "Kotak", "PNB", "Yes Bank", "IndusInd"]
AREA_TYPES = ["market", "residential", "metro_station", "mall", "highway", "airport", "college", "bank_branch"]
FRAUD_TYPES = ["UPI_FRAUD", "PHISHING", "CARD_SKIMMING", "OTP_FRAUD", "LOAN_SCAM", "INVESTMENT_SCAM", "JOB_SCAM"]


def make_accounts(driver, n=100):
    """Create 60 legit + 25 mules + 15 victims."""
    with driver.session() as s:
        for i in range(n):
            is_mule = i < 25
            is_victim = 25 <= i < 40
            city = random.choice(CITIES)
            score = random.uniform(70, 98) if is_mule else random.uniform(0, 20) if not is_victim else random.uniform(5, 30)
            level = "HIGH" if score >= 80 else ("MEDIUM" if score >= 50 else "LOW")
            s.run(
                """
                CREATE (:Account {
                    account_id: $aid, holder_name: $name, holder_phone: $phone,
                    holder_city: $city, bank_name: $bank, account_type: $atype,
                    creation_date: datetime($created), is_mule: $ismule,
                    mule_score: $score, risk_level: $level
                })
                """,
                aid=f"ACC-{i:03d}",
                name=f"Holder {i}",
                phone=f"+9198{i%100:02d}{i:05d}",
                city=city,
                bank=random.choice(BANKS),
                atype=random.choice(["SAVINGS", "CURRENT", "SALARY"]),
                created=(datetime.utcnow() - timedelta(days=random.randint(30, 2000))).isoformat(),
                ismule=is_mule,
                score=round(score, 1),
                level=level,
            )
        print(f"Created {n} accounts")


def make_atms(driver, n=50):
    """Create 50 ATM nodes across Indian cities with coords."""
    # city -> (lat_base, lon_base)
    coords = {
        "Mumbai": (19.0760, 72.8777), "Delhi": (28.6139, 77.2090),
        "Bangalore": (12.9716, 77.5946), "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639), "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567), "Ahmedabad": (23.0225, 72.5714),
    }
    with driver.session() as s:
        for i in range(n):
            city = random.choice(list(coords.keys()))
            lat, lon = coords[city]
            fraud_count = random.randint(0, 12)
            s.run(
                """
                CREATE (:ATM {
                    atm_id: $atm_id, latitude: $lat, longitude: $lon,
                    area_type: $area, nearby_metro: $metro, distance_to_metro: $d_metro,
                    distance_to_police: $d_police, avg_traffic_score: $traffic,
                    fraud_history_count: $fraud_count, last_fraud_time: $last_fraud,
                    success_rate: $success_rate, withdrawal_count_24h: $w24,
                    withdrawal_count_week: $wweek
                })
                """,
                atm_id=f"ATM-{city[:3].upper()}-{i:03d}",
                lat=round(lat + random.uniform(-0.15, 0.15), 5),
                lon=round(lon + random.uniform(-0.15, 0.15), 5),
                area=random.choice(AREA_TYPES),
                metro=random.random() < 0.6,
                d_metro=round(random.uniform(0.1, 5.0), 2),
                d_police=round(random.uniform(0.3, 8.0), 2),
                traffic=round(random.uniform(0.2, 1.0), 2),
                fraud_count=fraud_count,
                last_fraud=(datetime.utcnow() - timedelta(hours=random.randint(1, 2000))).isoformat()
                if fraud_count else None,
                success_rate=round(random.uniform(0.6, 0.99), 3),
                w24=random.randint(20, 500),
                wweek=random.randint(100, 3000),
            )
        print(f"Created {n} ATMs")


def make_complaints_and_txns(driver, n_complaints=50, n_txns=200, n_conn=80):
    """Create complaint nodes + SENT_MONEY + CONNECTED_TO + WITHDREW_AT relationships."""
    with driver.session() as s:
        for i in range(n_complaints):
            victim_idx = 25 + (i % 15)          # victims are idx 25-39
            mule_idx = i % 25                    # mules are idx 0-24
            cid = f"CMP-2026090{i % 9}1-{i:04d}"
            s.run(
                """
                MERGE (c:Complaint {complaint_id: $cid})
                SET c.victim_id = $victim_id, c.amount = $amount,
                    c.timestamp = datetime($ts), c.fraud_type = $ftype, c.status = 'SUBMITTED'
                WITH c
                MATCH (v:Account {account_id: $victim_acc})
                MATCH (m:Account {account_id: $mule_acc})
                MERGE (c)-[:INVOLVES]->(v)
                MERGE (c)-[:INVOLVES]->(m)
                """,
                cid=cid,
                victim_id=f"VIC-{i}",
                amount=random.choice([9999, 49999, 99000, 199000, 499000, 15000, 75000]),
                ts=(datetime.utcnow() - timedelta(days=i % 30, hours=random.randint(1, 12))).isoformat(),
                ftype=random.choice(FRAUD_TYPES),
                victim_acc=f"ACC-{victim_idx:03d}",
                mule_acc=f"ACC-{mule_idx:03d}",
            )

        # SENT_MONEY chains: mules send to other accounts
        txn_ids = set()
        for i in range(n_txns):
            src = random.randint(0, 30)          # mix of mules + some legit upstream
            dst = random.randint(0, 40)
            if src == dst:
                dst = (dst + 1) % 41
            tid = f"TXN-{i:04d}"
            while tid in txn_ids:
                tid = f"TXN-{i:04d}-{random.randint(0,9)}"
            txn_ids.add(tid)
            amount = random.choice([9999, 19999, 49000, 99000, 199000, 499000, 25000, 5000, 100000])
            s.run(
                """
                MATCH (a:Account {account_id: $src})
                MATCH (b:Account {account_id: $dst})
                CREATE (a)-[:SENT_MONEY {
                    transaction_id: $tid, amount: $amount, timestamp: datetime($ts),
                    is_fraudulent: $fraud, complaint_id: $cid
                }]->(b)
                """,
                src=f"ACC-{src:03d}", dst=f"ACC-{dst:03d}", tid=tid, amount=amount,
                ts=(datetime.utcnow() - timedelta(hours=random.randint(0, 72),
                                                  minutes=random.randint(0, 59))).isoformat(),
                fraud=src < 25,
                cid=f"CMP-2026090{i % 9}1-{i % 50:04d}",
            )

        # CONNECTED_TO mule networks
        for _ in range(n_conn):
            a = random.randint(0, 24)
            b = random.randint(0, 24)
            if a == b:
                continue
            s.run(
                """
                MATCH (x:Account {account_id: $a})
                MATCH (y:Account {account_id: $b})
                MERGE (x)-[:CONNECTED_TO {relationship_type: $rtype, strength: $strength}]->(y)
                """,
                a=f"ACC-{a:03d}", b=f"ACC-{b:03d}",
                rtype=random.choice(["shared_phone", "shared_device", "same_branch", "same_ip"]),
                strength=round(random.uniform(0.3, 1.0), 2),
            )

        # WITHDREW_AT: mules withdraw at ATMs
        for _ in range(60):
            acc = random.randint(0, 24)
            atm = random.randint(0, 49)
            s.run(
                """
                MATCH (a:Account {account_id: $acc})
                MATCH (t:ATM {atm_id: $atm})
                CREATE (a)-[:WITHDREW_AT {amount: $amount, timestamp: datetime($ts)}]->(t)
                """,
                acc=f"ACC-{acc:03d}",
                atm=f"ATM-MUM-{atm:03d}" if atm < 10 else f"ATM-DEL-{atm:03d}" if atm < 20 else f"ATM-BLR-{atm:03d}",
                amount=random.choice([5000, 10000, 20000, 50000]),
                ts=(datetime.utcnow() - timedelta(hours=random.randint(0, 48))).isoformat(),
            )

        print(f"Created {n_complaints} complaints, {n_txns} SENT_MONEY, {n_conn} CONNECTED_TO, 60 WITHDREW_AT")


def clear_db(driver):
    with driver.session() as s:
        s.run("MATCH (n) DETACH DELETE n")
        print("Cleared database")


def main():
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        driver.verify_connectivity()
    except Exception as e:
        print(f"Cannot connect to Neo4j at {URI}: {e}")
        print("Start it with: docker compose up -d neo4j")
        sys.exit(1)

    clear_db(driver)
    make_accounts(driver)
    make_atms(driver)
    make_complaints_and_txns(driver)
    driver.close()
    print("Neo4j population complete ✓")


if __name__ == "__main__":
    main()

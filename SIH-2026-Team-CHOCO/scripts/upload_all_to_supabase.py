"""Upload all enterprise data and evidence files to Supabase Cloud.

Performs:
1. Evidence files upload to Supabase Storage 'evidence' bucket
2. 50 realistic complaints seeding
3. 50 encrypted victim records (AES-256-GCM)
4. 25 evidence registry records linked to cloud storage
5. 100 system audit logs
6. 20 GNN Mule scores
7. 20 Spatio-Temporal ATM withdrawal predictions
"""

import os
import sys
import uuid
import random
import json
import httpx
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.config import get_settings
from api.security.encryption import encrypt_pii

settings = get_settings()

BANKS = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Kotak Mahindra Bank"]
FRAUD_TYPES = ["UPI_FRAUD", "DIGITAL_ARREST", "TASK_SCAM", "ELECTRICITY_BILL", "LOAN_APP_FRAUD", "PHISHING", "INVESTMENT_SCAM"]
STATUSES = ["SUBMITTED", "ANALYZING", "ACTION_TAKEN", "RESOLVED"]


def upload_storage_evidence():
    """Upload sample evidence files to Supabase Storage 'evidence' bucket."""
    print("==> 1. Uploading evidence documents to Supabase Storage...")
    headers = {
        "apikey": settings.supabase_service_role_key or settings.supabase_key,
        "Authorization": f"Bearer {settings.supabase_service_role_key or settings.supabase_key}",
    }

    evidence_files = [
        ("fir_sample_test.pdf", b"%PDF-1.4 Mock Cyber Crime First Information Report (FIR) - SIH26184", "application/pdf"),
        ("bank_statement_axis.pdf", b"%PDF-1.4 Official Bank Account Transaction Statement - Suspect Mule Account 9182371920", "application/pdf"),
        ("digital_arrest_evidence.pdf", b"%PDF-1.4 Skype call recording transcripts, fake arrest warrant and fake CBI seizure notice", "application/pdf"),
        ("whatsapp_chat_evidence.png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR Mock WhatsApp extortion chat screenshot", "image/png"),
        ("imps_transaction_slip.pdf", b"%PDF-1.4 Immediate Payment Service (IMPS) remittance slip Rs. 1,80,000", "application/pdf"),
        ("mule_network_topology.json", json.dumps({"network_id": "NET-MULE-009", "nodes": 14, "hops": 3}).encode(), "application/json"),
    ]

    uploaded = []
    for filename, content, content_type in evidence_files:
        url = f"{settings.supabase_url}/storage/v1/object/evidence/{filename}"
        files = {"file": (filename, content, content_type)}
        r = httpx.post(url, headers=headers, files=files, timeout=10)
        if r.status_code in (200, 201):
            print(f"  [OK] Uploaded: {filename} -> storage/evidence/{filename}")
            uploaded.append(filename)
        elif "Duplicate" in r.text or "already exists" in r.text or r.status_code == 400:
            print(f"  [EXISTS] Already exists: {filename}")
            uploaded.append(filename)
        else:
            print(f"  [!] Upload failed {filename}: {r.status_code} - {r.text[:80]}")

    return uploaded


def generate_seed_sql():
    """Generate SQL statements for complaints, victims, evidence, audit logs, mule scores, ATM predictions."""
    print("==> 2. Generating comprehensive database seed SQL...")
    random.seed(42)

    # Use fixed officer IDs matching our seeded users
    officer_usernames = ["admin", "inspector1", "inspector2", "constable1", "constable2"]

    lines = [
        "-- Auto-generated comprehensive dataset for SIH26184 Supabase Cloud",
        "BEGIN;",
    ]

    # Map officers
    lines.append("""
        CREATE TEMP TABLE temp_officers AS
        SELECT user_id, username FROM users;
    """)

    # 1. Complaints and Victims
    complaint_ids = []
    for i in range(1, 51):
        cid = f"CMP-20260905-{i:04d}"
        vid = str(uuid.uuid4())
        complaint_ids.append(cid)
        amount = random.choice([15000, 28500, 45000, 85000, 120000, 180000, 350000, 500000, 950000])
        ftype = random.choice(FRAUD_TYPES)
        status = random.choice(STATUSES)
        fbank = random.choice(BANKS)
        fupi = f"scammer{i % 12}@ok{fbank.split()[0].lower()}"
        fphone = f"+9198{random.randint(10000000, 99999999)}"
        txref = f"TXN26184{i:06d}"
        days_ago = random.randint(0, 14)
        ts = (datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(1, 18))).strftime("%Y-%m-%d %H:%M:%S")

        # Encrypted PII
        vname_hex = encrypt_pii(f"Citizen Victim {i}").hex()
        vphone_hex = encrypt_pii(f"+9199{random.randint(10000000, 99999999)}").hex()
        vbank_hex = encrypt_pii(f"{fbank}-{random.randint(1000000000, 9999999999)}").hex()
        vaccount_hex = encrypt_pii(f"ACC{random.randint(1000000, 9999999)}").hex()

        # Insert complaint
        lines.append(f"""
            INSERT INTO complaints (complaint_id, victim_id, amount, timestamp, fraud_type, fraudster_upi,
                                    fraudster_phone, fraudster_account, fraudster_bank, transaction_reference,
                                    status, assigned_officer, created_at, updated_at)
            SELECT '{cid}', '{vid}', {amount}, '{ts}'::timestamp, '{ftype}', '{fupi}',
                   '{fphone}', '\\x{vaccount_hex}'::bytea, '{fbank}', '{txref}',
                   '{status}'::complaintstatus, user_id, '{ts}'::timestamp, '{ts}'::timestamp
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (complaint_id) DO NOTHING;
        """)

        # Insert victim
        lines.append(f"""
            INSERT INTO victims (victim_id, complaint_id, name, phone, email, address, bank_account, upi_id, created_at)
            VALUES ('{vid}', '{cid}', '\\x{vname_hex}'::bytea, '\\x{vphone_hex}'::bytea,
                    'victim{i}@example.gov.in', '{i * 12} Cyber Park, Mumbai', '\\x{vbank_hex}'::bytea,
                    'victim{i}@upi', '{ts}'::timestamp)
            ON CONFLICT (victim_id) DO NOTHING;
        """)

    # 2. Evidence
    evidence_names = [
        ("fir_sample_test.pdf", "application/pdf"),
        ("bank_statement_axis.pdf", "application/pdf"),
        ("digital_arrest_evidence.pdf", "application/pdf"),
        ("whatsapp_chat_evidence.png", "image/png"),
        ("imps_transaction_slip.pdf", "application/pdf"),
        ("mule_network_topology.json", "application/json"),
    ]

    for i in range(1, 26):
        eid = str(uuid.uuid4())
        cid = random.choice(complaint_ids)
        fname, ftype = random.choice(evidence_names)
        fhash = uuid.uuid4().hex
        lines.append(f"""
            INSERT INTO evidence (evidence_id, complaint_id, file_name, file_type, file_hash, ipfs_hash, uploaded_at, uploaded_by)
            SELECT '{eid}', '{cid}', '{fname}', '{ftype}', '{fhash}', 'bafy{uuid.uuid4().hex[:24]}', now() - interval '{i} hours', user_id
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (evidence_id) DO NOTHING;
        """)

    # 3. Audit Logs
    actions = [
        "COMPLAINT_CREATED", "STATUS_UPDATED", "EVIDENCE_UPLOADED",
        "MULE_SUSPECT_IDENTIFIED", "BANK_FREEZE_NOTICE_ISSUED", "ATM_DISPATCH_TRIGGERED", "CASE_RESOLVED"
    ]
    for i in range(1, 101):
        lid = str(uuid.uuid4())
        action = random.choice(actions)
        cid = random.choice(complaint_ids)
        ip = f"10.40.{i % 10}.{i % 200 + 1}"
        details_json = json.dumps({"complaint_id": cid, "action": action, "severity": "HIGH" if "FREEZE" in action else "INFO"})
        lines.append(f"""
            INSERT INTO audit_logs (log_id, user_id, action, details, timestamp, ip_address)
            SELECT '{lid}', user_id, '{action}', '{details_json}'::jsonb, now() - interval '{i} hours', '{ip}'
            FROM temp_officers ORDER BY random() LIMIT 1
            ON CONFLICT (log_id) DO NOTHING;
        """)

    # 4. Mule Scores
    risk_levels = [("HIGH", 0.88, 0.92, 0.90), ("HIGH", 0.94, 0.85, 0.91), ("MEDIUM", 0.65, 0.70, 0.67), ("LOW", 0.15, 0.20, 0.17)]
    for i in range(1, 26):
        sid = str(uuid.uuid4())
        acc = f"MULE_ACC_{1000 + i}"
        cid = random.choice(complaint_ids)
        level, gnn, rule, final = random.choice(risk_levels)
        lines.append(f"""
            INSERT INTO mule_scores (score_id, account_id, complaint_id, gnn_probability, rule_score, final_score, risk_level, calculated_at)
            VALUES ('{sid}', '{acc}', '{cid}', {gnn}, {rule}, {final}, '{level}', now() - interval '{i * 2} hours')
            ON CONFLICT (score_id) DO NOTHING;
        """)

    # 5. ATM Predictions
    atm_ids = [f"ATM_MUM_ANDHERI_{i:02d}" for i in range(1, 6)] + [f"ATM_DEL_CP_{i:02d}" for i in range(1, 6)]
    for i in range(1, 26):
        pid = str(uuid.uuid4())
        cid = random.choice(complaint_ids)
        atm = random.choice(atm_ids)
        prob = round(random.uniform(0.72, 0.96), 3)
        window = round(random.uniform(1.5, 4.0), 1)
        lines.append(f"""
            INSERT INTO atm_predictions (prediction_id, complaint_id, atm_id, probability, time_window, predicted_at)
            VALUES ('{pid}', '{cid}', '{atm}', {prob}, {window}, now() - interval '{i * 3} hours')
            ON CONFLICT (prediction_id) DO NOTHING;
        """)

    lines.append("DROP TABLE temp_officers;")
    lines.append("COMMIT;")
    return "\n".join(lines)


def main():
    upload_storage_evidence()
    sql = generate_seed_sql()
    out_path = os.path.join(os.path.dirname(__file__), "supabase_full_seed.sql")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sql)
    print(f"==> 3. Wrote complete seed script to {out_path} ({len(sql)} bytes)")


if __name__ == "__main__":
    main()

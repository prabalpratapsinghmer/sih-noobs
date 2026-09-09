"""Mule scoring: rule-based + hybrid scoring (GNN probability × 0.7 + rule × 0.3)."""

import contextlib
from datetime import UTC, datetime

from api.database.neo4j import execute_query, execute_write


# --- Rule: transaction velocity (25 pts) ---
async def rule_transaction_velocity(account_id: str) -> float:
    query = """
    MATCH (a:Account {account_id: $account_id})-[t:SENT_MONEY]->(:Account)
    WHERE t.timestamp > datetime() - duration('PT1H')
    RETURN count(t) AS txn_count
    """
    rows = await execute_query(query, {"account_id": account_id})
    count = rows[0]["txn_count"] if rows else 0
    if count > 5:
        return 25.0
    return min(count / 5 * 25, 25.0)


# --- Rule: rapid outflow (20 pts) ---
async def rule_rapid_outflow(account_id: str) -> float:
    query = """
    MATCH (a:Account {account_id: $account_id})-[t:SENT_MONEY]->(:Account)
    WITH t ORDER BY t.timestamp LIMIT 100
    RETURN min(t.timestamp) AS first_t, max(t.timestamp) AS last_t, count(t) AS n
    """
    rows = await execute_query(query, {"account_id": account_id})
    if not rows or rows[0]["n"] < 2:
        return 0.0
    first_v = datetime.fromtimestamp(rows[0]["first_t"].to_native().timestamp(), tz=UTC)
    last_v = datetime.fromtimestamp(rows[0]["last_t"].to_native().timestamp(), tz=UTC)
    span = (last_v - first_v).total_seconds() / 60.0
    if span < 30:
        return 20.0
    if span < 60:
        return 15.0
    if span < 120:
        return 10.0
    return 5.0


# --- Rule: connected complaints (20 pts) ---
async def rule_connected_complaints(account_id: str) -> float:
    query = """
    MATCH (a:Account {account_id: $account_id})-[:INVOLVES]-(c:Complaint)
    RETURN count(DISTINCT c) AS n
    """
    rows = await execute_query(query, {"account_id": account_id})
    n = rows[0]["n"] if rows else 0
    return min(n / 3 * 20, 20.0)


# --- Rule: suspicious timing 2-5 AM (15 pts) ---
async def rule_suspicious_timing(account_id: str) -> float:
    query = """
    MATCH (a:Account {account_id: $account_id})-[t:SENT_MONEY]->(:Account)
    RETURN t.timestamp AS ts
    """
    rows = await execute_query(query, {"account_id": account_id})
    if not rows:
        return 0.0
    suspicious = 0
    for row in rows:
        native = row["ts"].to_native()
        hour = native.hour
        if 2 <= hour < 5:
            suspicious += 1
    return min(suspicious * 3, 15.0)


# --- Rule: threshold amounts (10 pts) ---
THRESHOLDS = [99_000, 199_000, 499_000, 999_000]


def _near_threshold(amount: float) -> bool:
    return any(abs(amount - t) / t < 0.15 for t in THRESHOLDS)


async def rule_threshold_amounts(account_id: str) -> float:
    query = """
    MATCH (a:Account {account_id: $account_id})-[t:SENT_MONEY]->(:Account)
    RETURN t.amount AS amount
    """
    rows = await execute_query(query, {"account_id": account_id})
    if not rows:
        return 0.0
    hits = 0
    for row in rows:
        amt = float(row["amount"])
        if _near_threshold(amt):
            hits += 1
    return min(hits * 2.5, 10.0)


# --- Rule: outflow/inflow ratio (10 pts) ---
async def rule_outflow_inflow_ratio(account_id: str) -> float:
    query = """
    MATCH (a:Account {account_id: $account_id})
    OPTIONAL MATCH (a)-[out:SENT_MONEY]->(:Account)
    OPTIONAL MATCH (:Account)-[in:SENT_MONEY]->(a)
    RETURN sum(out.amount) AS out_sum, sum(in.amount) AS in_sum
    """
    rows = await execute_query(query, {"account_id": account_id})
    if not rows:
        return 0.0
    out_sum = float(rows[0]["out_sum"] or 0)
    in_sum = float(rows[0]["in_sum"] or 0)
    if in_sum == 0:
        return 0.0
    ratio = out_sum / in_sum
    if abs(ratio - 1.0) < 0.15:
        return 10.0
    if abs(ratio - 1.0) < 0.3:
        return 5.0
    return 0.0


async def compute_rule_score(account_id: str) -> float:
    """Compute full rule-based score (0-100)."""
    scores = await _gather_rules(account_id)
    return min(sum(scores), 100.0)


async def _gather_rules(account_id: str) -> list[float]:
    import asyncio

    return await asyncio.gather(
        rule_transaction_velocity(account_id),
        rule_rapid_outflow(account_id),
        rule_connected_complaints(account_id),
        rule_suspicious_timing(account_id),
        rule_threshold_amounts(account_id),
        rule_outflow_inflow_ratio(account_id),
    )


def hybrid_score(gnn_probability: float | None, rule_score: float) -> tuple[float, str]:
    """Apply hybrid formula and map risk level."""
    gnn_part = (gnn_probability or 0.0) * 100 * 0.7
    final = min(gnn_part + rule_score * 0.3, 100.0)
    level = "HIGH" if final >= 80 else ("MEDIUM" if final >= 50 else "LOW")
    return round(final, 2), level


async def score_account(account_id: str, complaint_id: str | None = None,
                        gnn_probability: float | None = None,
                        session=None) -> dict:
    """Score a single account; persist in PG mule_scores + Neo4j."""
    rule_score = await compute_rule_score(account_id)
    final_score, risk_level = hybrid_score(gnn_probability, rule_score)

    # Persist to PostgreSQL
    from sqlalchemy import insert

    from api.models.mule_score import MuleScore
    if session is not None:
        await session.execute(
            insert(MuleScore).values(
                account_id=account_id,
                complaint_id=complaint_id,
                gnn_probability=gnn_probability,
                rule_score=rule_score,
                final_score=final_score,
                risk_level=risk_level,
            )
        )

    # Update Neo4j node
    with contextlib.suppress(Exception):  # Neo4j may be unavailable
        await execute_write(
            """
            MATCH (a:Account {account_id: $account_id})
            SET a.mule_score = $score, a.risk_level = $level
            """,
            {"account_id": account_id, "score": final_score, "level": risk_level},
        )

    return {
        "account_id": account_id,
        "rule_score": round(rule_score, 2),
        "gnn_probability": gnn_probability,
        "final_score": final_score,
        "risk_level": risk_level,
    }


async def batch_score_chain(complaint_id: str, session=None) -> list[dict]:
    """Score all accounts in a complaint's transaction chain, sorted by score desc."""
    query = """
    MATCH (c:Complaint {complaint_id: $complaint_id})-[:INVOLVES]->(fraudster:Account)
    CALL {
        WITH fraudster
        MATCH (fraudster)-[:SENT_MONEY*1..5]->(m:Account)
        RETURN DISTINCT m
        UNION
        WITH fraudster
        RETURN fraudster AS m
    }
    RETURN DISTINCT m.account_id AS account_id
    """
    try:
        rows = await execute_query(query, {"complaint_id": complaint_id})
    except Exception:
        return []
    results = []
    for row in rows:
        res = await score_account(row["account_id"], complaint_id, session=session)
        results.append(res)
    results.sort(key=lambda r: r["final_score"], reverse=True)
    return results

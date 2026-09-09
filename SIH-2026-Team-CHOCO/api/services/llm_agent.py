"""LLM agent backend — safe Cypher execution with whitelist/blacklist."""

from typing import Any

import structlog

from api.database.neo4j import execute_query

logger = structlog.get_logger(__name__)

# Whitelist: only read-only Cypher keywords
ALLOWED_KEYWORDS = {"MATCH", "RETURN", "WHERE", "ORDER", "BY", "LIMIT", "SKIP", "AS", "WITH", "DISTINCT",
                    "AND", "OR", "NOT", "IN", "IS", "NULL", "CASE", "WHEN", "THEN", "ELSE", "END", "COUNT",
                    "SUM", "AVG", "MIN", "MAX", "COLLECT", "UNWIND", "TRUE", "FALSE", "CALL", "USING", "INDEX",
                    "PROFILE", "EXPLAIN", "SHORTESTPATH", "OPTIONAL"}

# Blacklist: mutation/risky keywords
BLOCKED_KEYWORDS = {"CREATE", "DELETE", "DETACH", "SET", "MERGE", "DROP", "REMOVE", "LOAD", "CSV",
                    "FOREACH", "CALL", "YIELD", "PROCEDURE", "ADMIN", "SHOW", "EXISTS"}

MAX_RESULT_ROWS = 100

# Pre-built query templates
TEMPLATES = {
    "transaction_chain": (
        "MATCH chain = (c:Complaint {{complaint_id: $complaint_id}})-[:INVOLVES]->(f:Account)"
        "MATCH chain2 = (f)-[:SENT_MONEY*1..5]->(m:Account) RETURN chain, chain2 LIMIT $limit"
    ),
    "connected_mules": (
        "MATCH (a:Account {{account_id: $account_id}})-[:SENT_MONEY|CONNECTED_TO*1..3]-(m:Account) "
        "WHERE m.is_mule = true RETURN DISTINCT m.account_id AS account_id, m.mule_score AS mule_score "
        "ORDER BY mule_score DESC LIMIT $limit"
    ),
    "high_risk_atms": (
        "MATCH (atm:ATM) WHERE atm.fraud_history_count > 5 "
        "RETURN atm.atm_id AS atm_id, atm.fraud_history_count AS fraud_count "
        "ORDER BY fraud_count DESC LIMIT $limit"
    ),
    "victim_to_mule_path": (
        "MATCH path = shortestPath((v:Account {{account_id: $victim_acc}})-[*]-(m:Account {{account_id: $mule_acc}})) "
        "RETURN path LIMIT 1"
    ),
    "account_summary": (
        "MATCH (a:Account {{account_id: $account_id}}) "
        "RETURN a.account_id AS account_id, a.holder_city AS city, a.bank_name AS bank, "
        "a.mule_score AS mule_score, a.risk_level AS risk_level LIMIT 1"
    ),
    "complaint_graph": (
        "MATCH (c:Complaint {{complaint_id: $complaint_id}})-[*1..3]-(n) "
        "RETURN DISTINCT labels(n) AS node_type, n LIMIT $limit"
    ),
    "account_transactions": (
        "MATCH (a:Account {{account_id: $account_id}})-[t:SENT_MONEY]->(b:Account) "
        "RETURN b.account_id AS to_account, t.amount AS amount, t.timestamp AS timestamp "
        "ORDER BY t.timestamp DESC LIMIT $limit"
    ),
    "atms_by_city": (
        "MATCH (atm:ATM) WHERE atm.area_type = $city "
        "RETURN atm.atm_id AS atm_id, atm.success_rate AS success_rate "
        "ORDER BY success_rate DESC LIMIT $limit"
    ),
    "fraud_velocity": (
        "MATCH (a:Account {{account_id: $account_id}})-[t:SENT_MONEY]->(b:Account) "
        "WHERE t.timestamp > datetime() - duration('PT1H') "
        "RETURN count(t) AS txn_count, sum(t.amount) AS total_amount LIMIT 1"
    ),
    "network_size": (
        "MATCH (a:Account {{account_id: $account_id}})-[:SENT_MONEY|CONNECTED_TO*1..2]-(n:Account) "
        "RETURN count(DISTINCT n) AS network_size, toFloat(a.mule_score) AS mule_score LIMIT $limit"
    ),
}


def validate_query(query: str) -> str | None:
    """Validate a Cypher query for safe execution. Returns error or None."""
    upper = query.upper().strip()

    # Must start with a whitelisted read keyword
    if not any(upper.startswith(k) for k in ("MATCH", "RETURN", "CALL {", "WITH", "UNWIND")):
        return "Query must start with MATCH/RETURN/WITH"

    # Block dangerous keywords
    for kw in BLOCKED_KEYWORDS:
        if kw in upper:
            return f"Cypher keyword '{kw}' is not allowed"

    # Reject semicolons (multiple statements)
    if ";" in upper:
        return "Multiple statements are not allowed"

    # AST-ish guard: ensure `:` protocol or auth tokens aren't smuggled — sufficient for demo
    if "://" in query:
        return "URL protocol strings not allowed"

    return None


async def execute_safe_query(query: str, parameters: dict | None = None) -> dict:
    """Validate + execute. Returns {ok, rows, error, truncated}."""
    error = validate_query(query)
    if error:
        return {"ok": False, "error": error, "rows": []}

    try:
        rows = await execute_query(query, parameters or {})
        truncated = len(rows) > MAX_RESULT_ROWS
        rows = rows[:MAX_RESULT_ROWS]
        # Convert Neo4j types to JSON-safe
        safe_rows = [_jsonable(r) for r in rows]
        return {"ok": True, "rows": safe_rows, "truncated": truncated}
    except Exception as e:
        logger.warning("llm_query_failed", error=str(e))
        return {"ok": False, "error": f"Query failed: {e}", "rows": []}


def _jsonable(obj: Any) -> Any:
    """Convert Neo4j driver types to plain JSON-able values (best-effort)."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[str(k)] = _jsonable(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_jsonable(x) for x in obj]
    if hasattr(obj, "_properties"):  # neo4j Node/Relationship
        return {str(k): _jsonable(v) for k, v in obj._properties.items()}
    if hasattr(obj, "to_native"):  # neo4j DateTime etc.
        return str(obj.to_native())
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


async def explain_results(rows: list[dict], question: str) -> str:
    """Natural-language-ish summary of query results (rule-based; real LLM as stretch)."""
    n = len(rows)
    if n == 0:
        return f"No results for '{question}'. Try broadening the query."
    keys = set()
    for r in rows:
        keys.update(r.keys())
    sample = rows[0]
    return (
        f"Query returned {n} row(s) for: {question}. "
        f"Fields: {', '.join(sorted(keys))}. "
        f"Sample row: {sample}"
    )

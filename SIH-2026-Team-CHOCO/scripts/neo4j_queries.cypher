# Neo4j common query templates

# 1. Get full transaction chain for a complaint
MATCH path = (victim:Account)<-[:INVOLVES]-(c:Complaint {complaint_id: $complaint_id})
              -[:INVOLVES]->(fraudster:Account)
MATCH chain = (fraudster)-[:SENT_MONEY*1..5]->(mule:Account)
RETURN path, chain

# 2. Find connected mules (2-hop)
MATCH (a:Account {account_id: $account_id})-[:SENT_MONEY|CONNECTED_TO*1..2]-(mule:Account)
WHERE mule.is_mule = true
RETURN mule ORDER BY mule.mule_score DESC

# 3. High-risk ATMs ranked by fraud history
MATCH (atm:ATM)
WHERE atm.fraud_history_count > 5
RETURN atm ORDER BY atm.fraud_history_count DESC LIMIT 20

# 4. Shortest path: victim → mule
MATCH path = shortestPath(
    (v:Account {account_id: $victim_acc})-[*]-(m:Account {account_id: $mule_acc})
)
RETURN path

# 5. Transaction velocity check (last hour)
MATCH (a:Account {account_id: $account_id})-[t:SENT_MONEY]->(b:Account)
WHERE t.timestamp > datetime() - duration('PT1H')
RETURN count(t) AS txn_count, sum(t.amount) AS total_amount
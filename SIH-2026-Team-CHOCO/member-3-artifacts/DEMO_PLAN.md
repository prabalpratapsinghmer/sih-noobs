# Demo Plan — 5-Minute Walkthrough

> Member 3 drives every UI on stage. Backend/ML parts are props seeded with demo data.
> Practice until smooth. Record a backup video. Run the full stack before judges arrive.

---

## 1. Demo Script (5 minutes)

| Time | Screen | What to say | What to show |
|------|--------|-------------|--------------|
| 0:00 | Victim Portal (M4) | "A victim files a complaint. Takes 2 minutes." | Submit complaint form, see confirmation |
| 0:30 | Backend | "The backend triggers the AI pipeline instantly." | (narrated, no screen change needed) |
| 0:45 | Command Center | "Within moments, the inspector sees the prediction." | Map updates with new high-risk ATM |
| 1:15 | Command Center — Graph | "The GNN traced the money trail: victim → mule → ATM." | Click complaint, show graph with nodes/edges |
| 1:45 | Command Center — LLM | "The inspector asks in plain English." | Type "Show mules linked to C1001" → see result |
| 2:15 | Command Center — Actions | "One click to trigger verification." | Click "Trigger Verification" → confirm → success toast |
| 2:30 | Field Dashboard | "The constable gets the alert immediately." | Show alert card with risk score, distance, ETA |
| 3:00 | Field Dashboard — Actions | "Navigate. Dispatch. Verify. Three taps." | Tap Navigate → Dispatch → Verify |
| 3:15 | Admin Panel | "System health at a glance." | Show health dashboard with gauges |
| 3:30 | Admin Panel — Audit | "Every action is auditable and blockchain-backed." | Show audit log with tx hashes |
| 3:45 | Admin Panel — Models | "ML performance tracked in real time." | Show accuracy/latency charts |
| 4:00 | Architecture diagram | "Six layers, microservices, production-ready." | Show architecture slide |
| 4:15 | DevOps | "One command to deploy. Kubernetes-ready." | Show `docker compose up` + Grafana dashboards |
| 4:30 | Summary | "Complaint to police action in under 10 minutes." | Key stats on screen |
| 5:00 | Q&A | — | — |

---

## 2. Pre-Demo Checklist

### Infrastructure (30 min before)
- [ ] Run `docker compose up --build` — all 11 containers healthy
- [ ] Verify nginx routes: `/`, `/admin`, `/field`, `/command`
- [ ] Verify WebSocket: open DevTools → WS tab → connection green
- [ ] Seed demo data: 5 complaints, 20 ATMs, 10 mules, 3 predictions
- [ ] Pre-fill: login as inspector (Command), constable (Field), admin (Admin)
- [ ] Verify Grafana dashboards load
- [ ] Test the decisive flow end-to-end once

### Backup (in case of failure)
- [ ] Recorded demo video (Loom or OBS)
- [ ] Screenshots of each key screen
- [ ] Static fallback: architecture diagram + stats
- [ ] If WiFi fails: PWA offline mode + cached data

---

## 3. Demo Data Seeds

### Complaints
```json
[
  { "id": "C1001", "fraud_type": "investment", "amount": 45000, "status": "predictions_ready" },
  { "id": "C1002", "fraud_type": "phishing", "amount": 12000, "status": "in_analysis" },
  { "id": "C1003", "fraud_type": "romance", "amount": 85000, "status": "action_taken" },
  { "id": "C1004", "fraud_type": "upi_fraud", "amount": 8500, "status": "resolved" },
  { "id": "C1005", "fraud_type": "tech_support", "amount": 32000, "status": "predictions_ready" }
]
```

### ATMs (20 points, spread across Bangalore)
Include: Koramangala (3), Indiranagar (2), Whitefield (2), Electronic City (2), Jayanagar (2), MG Road (2),HSR Layout (2), BTM Layout (2), Frazer Town (1), Rajajinagar (2).

Risk scores: 5 ATMs at 80+, 7 at 50–79, 8 at 20–49.

### Mules (10 accounts)
```json
[
  { "id": "mule-001", "score": 92, "connected_to": ["C1001", "C1003"] },
  { "id": "mule-002", "score": 78, "connected_to": ["C1001"] },
  { "id": "mule-003", "score": 65, "connected_to": ["C1002"] },
  ...
]
```

---

## 4. Talking Points for Judges

1. **"We built 3 responsive web interfaces for different personas."**
   Inspector (dense, dark), Constable (mobile, big buttons), Admin (operational).

2. **"The Command Center provides real-time intelligence."**
   Live heatmap + money-trail graph + natural-language LLM agent.

3. **"Our LLM lets officers ask complex questions in plain English."**
   No Cypher knowledge needed. LangChain handles the translation.

4. **"The Field Dashboard enables rapid response from anywhere."**
   Mobile-first, offline-capable, three taps to act.

5. **"Everything is containerized and production-ready."**
   Docker Compose for demo, Kubernetes for scale, Jenkins for CI/CD.

6. **"We monitor everything."**
   Prometheus + Grafana dashboards, ELK for logs.

7. **"Every action is auditable and blockchain-backed."**
   Tamper-proof trail for legal admissibility.

---

## 5. Anticipated Judge Questions

| Question | Answer |
|----------|--------|
| "How does the LLM know what to query?" | LangChain converts natural language to constrained Cypher queries. The LLM has context about the schema. |
| "What if the officer asks something vague?" | The agent returns a clarification prompt with suggestions. The UI renders these as chips. |
| "How do you ensure data privacy?" | JWT auth + role-based access; backend masks PII; evidence encrypted before IPFS; TLS in transit. |
| "How scalable is this?" | Kubernetes auto-scaling (HPA on ML queue), microservices architecture, Redis for caching. |
| "What about offline use?" | Field Dashboard has service worker + localStorage queue; Victim Portal is a PWA. |
| "How is evidence integrity maintained?" | File hashing (SHA-256) + IPFS CID + blockchain hash trail. Verifiable in the audit log. |
| "What if the ATM prediction is wrong?" | Top-3 predictions with probabilities; officers use judgment; system improves via feedback loop. |
| "How does the blockchain work?" | Only hashes stored on-chain (not full data). Saves cost and maintains privacy while proving integrity. |
| "Why not use Mapbox?" | Leaflet is free, no API key, good enough for 500+ markers. Mapbox is the upgrade path — code is wrapped for easy swap. |
| "How do you handle concurrent users?" | Redis pub/sub for WS broadcasting; JWT stateless auth; connection pooling in Postgres. |

---

## 6. Presentation Slide Outline

1. **Title slide:** Project name, team, problem statement.
2. **Problem:** 2–4 hour response time → money lost.
3. **Solution:** AI-powered prediction → < 10 min response.
4. **Architecture:** 6-layer diagram.
5. **Live demo:** (5-minute walkthrough).
6. **Tech stack:** React, FastAPI, PyTorch, Neo4j, Docker, K8s.
7. **Results:** Accuracy metrics, response time improvement.
8. **Innovation:** LLM agent, blockchain audit, multi-channel.
9. **Scalability:** Kubernetes auto-scale, microservices.
10. **Team & timeline:** 4 members, 10 days.

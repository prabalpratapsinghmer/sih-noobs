# Edge Cases & Fallback Strategies

> **SIH 2026 | Team CHOCO | Project ID: SIH26184**
> How the system survives failures during production and the live demo.

## 1. Machine Learning Server Fails / Times Out
**Scenario:** The GPU processing the Transformer/GNN takes too long or crashes.
**Fallback:**
- Backend API wraps the ML call in a 5-second timeout.
- If it times out, the backend queries Neo4j using a fallback heuristic Cypher query (e.g., "Find nearest ATM to last known mule") and returns a `risk_score` flagged with `is_heuristic: true`.
- UI renders the score in Orange (Warning) with a tooltip: "AI Model offline; showing heuristic estimation."

## 2. LLM Agent API (Gemini) Rate Limits or Fails
**Scenario:** Google Gemini API goes down or hits the free-tier rate limit during the demo.
**Fallback:**
- Member 2's backend implements an exact-match cache in Redis.
- If the API fails, it returns pre-canned demo responses for our specific demo queries.
- UI shows a `(Cached)` badge next to the AI response.

## 3. WebSocket Disconnection
**Scenario:** Shaky Wi-Fi causes the Command Center or Field Dashboard to lose the WebSocket connection.
**Fallback:**
- `socket.io-client` automatically attempts exponential backoff reconnection (1s, 2s, 4s, 8s).
- During disconnect, the UI displays a yellow "Reconnecting..." toast.
- The UI silently falls back to standard HTTP polling (`GET /api/v1/alerts`) every 5 seconds until WS restores.

## 4. Constable Goes Offline in the Field
**Scenario:** Officer in a patrol car enters a dead zone (no 4G/5G).
**Fallback:**
- Field Dashboard is a Progressive Web App (PWA) with a Service Worker.
- It serves the cached UI shell and the last known list of alert cards from IndexedDB/localStorage.
- Shows a red banner: "Offline Mode — Showing last known alerts."
- If the officer clicks "Dispatch", the action is queued locally and synced automatically when the network returns.

## 5. Map Clutter (Thousands of ATMs)
**Scenario:** A city has 5,000+ ATMs; rendering them all crashes the browser DOM.
**Fallback:**
- Member 3 implements `leaflet.markercluster`.
- At low zoom levels, ATMs are grouped into bubbles with numbers (e.g., "45").
- The color of the bubble represents the *highest* risk score of any ATM inside that cluster.

## 6. Blockchain Network Congestion
**Scenario:** The simulated blockchain takes too long to mine a block for the audit log.
**Fallback:**
- We don't block the main UI thread. Audit logging is an asynchronous background task.
- The PostgreSQL `audit_log` table acts as the immediate source of truth.
- A chron job / background worker syncs it to the hash chain.

## 7. Zero Evidence Uploaded
**Scenario:** A victim submits a complaint but attaches no screenshots of transactions.
**Fallback:**
- ML models are trained to accept `null` evidence arrays.
- Risk scores rely heavily on the textual description (NLP extraction) and the target bank account numbers to form the graph.

## 8. False Positives (Innocent ATM User)
**Scenario:** The system flags an ATM, police trigger facial recognition, but it's an innocent citizen.
**Fallback:**
- The system *never* automatically arrests. It only triggers "Step-Up Verification" (OTP to the registered phone + photo capture).
- If the OTP succeeds, the innocent user gets their cash. The ATM logs the event, and the AI model weights are adjusted via negative feedback.

## 9. Judges Ask to See a Random Query
**Scenario:** During Q&A, a judge types a completely random query into the LLM agent that we didn't prepare for.
**Fallback:**
- The LangChain agent is strictly scoped to the Neo4j schema.
- If asked "What is the weather?", the system prompt forces it to reply: "I am a police intelligence agent. I can only assist with cybercrime data, mule networks, and ATM risk scoring."

## 10. Complete Demo Catastrophe
**Scenario:** Minikube crashes, Docker fails, or ports conflict right as the timer starts.
**Fallback:**
- Member 3 has a `.env` flag: `VITE_DEMO_MODE=true`.
- When flipped, the React frontends bypass Axios entirely and serve hardcoded JSON payloads from a `mock/` folder. The UI looks 100% functional for the 5-minute pitch.

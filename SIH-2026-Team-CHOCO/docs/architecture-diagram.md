# Architecture Diagrams

> **SIH 2026 | Team CHOCO | Project ID: SIH26184**
> High-level system architecture and deployment flow.

## 1. System Context Diagram (C4 Model - Level 1)

```mermaid
graph TD
    V[Victim] -->|Submits Complaint| VP[Victim Portal]
    P[Police Inspector] -->|Monitors & Queries| CC[Command Center]
    C[Constable] -->|Receives Alerts| FD[Field Dashboard]
    A[Admin] -->|Monitors Health| AP[Admin Panel]

    VP -->|HTTPS / API| GW[API Gateway / Nginx]
    CC -->|HTTPS / WSS| GW
    FD -->|HTTPS / WSS| GW
    AP -->|HTTPS / API| GW

    GW --> BE[FastAPI Backend]

    BE -->|Triggers ML| ML[ML Model Server]
    BE -->|Reads/Writes| DB[(PostgreSQL)]
    BE -->|Queries Paths| Graph[(Neo4j)]
    BE -->|Caches| Cache[(Redis)]
    
    ML -.->|Predicts| BE
```

## 2. Machine Learning Pipeline (Level 2)

```mermaid
sequenceDiagram
    participant B as Backend
    participant M as ML Server (Port 8081)
    participant T as Spatio-Temporal Model
    participant G as GNN Model
    
    B->>M: POST /predict { complaint_data }
    parallel ML Tasks
        M->>T: Predict next ATM withdrawal
        T-->>M: [ATM #452, 92% risk, 2h window]
    and
        M->>G: Score linked bank accounts
        G-->>M: [Mule1: 95%, Mule2: 40%]
    end
    M-->>B: Return aggregated intelligence
    B->>B: Save to DB & Cache
    B->>B: Broadcast via WebSocket
```

## 3. Deployment Architecture (Kubernetes / Docker)

```mermaid
graph TB
    subgraph K8s Cluster [Minikube Cluster - sih-choco namespace]
        
        subgraph Ingress
            IG[Nginx Ingress Controller]
        end

        subgraph UI Pods
            VP_P[Victim Portal :3000]
            CC_P[Command Center :3001]
            FD_P[Field Dashboard :3002]
            AP_P[Admin Panel :3003]
        end

        subgraph Backend Pods
            BE_P[FastAPI Server :8000]
            ML_P[ML Server :8081]
        end

        subgraph Data Pods
            PG[(PostgreSQL :5432)]
            N4[(Neo4j :7687)]
            RD[(Redis :6379)]
        end
        
        subgraph Observability
            PR[Prometheus]
            GF[Grafana]
        end

        IG --> VP_P
        IG --> CC_P
        IG --> FD_P
        IG --> AP_P
        
        VP_P --> BE_P
        CC_P --> BE_P
        FD_P --> BE_P
        AP_P --> BE_P

        BE_P --> ML_P
        BE_P --> PG
        BE_P --> N4
        BE_P --> RD
    end
```

## 4. Blockchain Audit Flow

```mermaid
graph LR
    Action[Action Taken by Police] --> Hash[Generate SHA-256 Hash of Payload]
    Hash --> Block[Append to Immutable Chain]
    Block --> DB[Store Block in Postgres]
    DB --> Verify[Admin Panel Verifies Chain Integrity]
    Verify -- Valid --> Green[Chain Valid]
    Verify -- Tampered --> Red[Alert: Hash Mismatch]
```

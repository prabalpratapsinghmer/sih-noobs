# LLM Agent — Natural Language Query Interface

> Feature: `features/llm-agent/` in Command Center.
> Backend: Member 2's FastAPI endpoint that calls LangChain → LLM → Cypher → Neo4j.
> Frontend: chat interface, result rendering, quick prompts, structured query builder.

---

## 1. Flow

1. Inspector types a question in the chat input.
2. Question is sent to `POST /api/llm/query` with `{ question: string, context?: string }`.
3. Backend: LangChain extracts intent → generates Cypher → executes on Neo4j → formats response.
4. Response streams back (text chunks) → frontend renders progressively.
5. Structured result (table/chart/graph) is included in the final response.

---

## 2. API Contract

```
POST /api/llm/query
```

**Request:**
```json
{
  "question": "Show all high-risk ATMs in Indiranagar linked to investment fraud in the last 2 hours",
  "context": "C1001"  // optional: current complaint context
}
```

**Response (streamed SSE):**
```
data: {"type": "text", "content": "I found 3 high-risk ATMs in Indiranagar linked to investment fraud cases in the last 2 hours:"}
data: {"type": "table", "columns": ["ATM ID", "Risk Score", "Connected Cases", "Last Active"], "rows": [["ATM-0042", 82, 3, "2 hours ago"], ...]}
data: {"type": "chart", "chart_type": "bar", "data": [...]}
data: {"type": "suggestions", "items": ["Show mule accounts for ATM-0042", "Extend search to last 24 hours", "Show all fraud types in Indiranagar"]}
data: {"type": "done", "cypher_query": "MATCH (c:Complaint)-[:CONNECTED_TO]->(a:ATM) WHERE..."}
```

---

## 3. ChatThread Component

```tsx
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  result?: {
    type: 'text' | 'table' | 'chart' | 'graph';
    data: unknown;
  };
  suggestions?: string[];
  cypherQuery?: string;  // shown in expandable "View Query" section
}
```

Layout:
- Messages: user (right-aligned, accent bg), assistant (left-aligned, surface bg).
- Streaming: typewriter effect for text, progressive render for structured results.
- Scroll: auto-scroll to bottom on new message, but stop if user scrolls up.
- Loading: skeleton pulsing dots while waiting for first chunk.

---

## 4. ResultRenderer

Handles the structured results that come with the assistant's response:

| `type` | Renders | Library |
|--------|---------|---------|
| `text` | Markdown-like formatted text | Simple HTML/markdown renderer |
| `table` | Sortable data table | `@sih/ui` DataTable |
| `chart` | Bar/line/pie chart | Recharts |
| `graph` | Mini force-directed graph | D3 (subset of graph feature) |

---

## 5. QuickPrompts

Pre-defined chips below the input for common queries:

```typescript
const QUICK_PROMPTS = [
  "Show high-risk ATMs in my jurisdiction",
  "List active mule accounts",
  "Complaints from the last 24 hours",
  "ATMs with most connected complaints",
  "Show mules connected to complaint C1001",
  "What fraud types are trending this week?",
];
```

---

## 6. QueryBuilder (Visual Alternative)

For inspectors who don't want to type. A form-based query builder:

```
[Entity: Complaint ▼] [Attribute: fraud_type ▼] [Operator: = ▼] [Value: investment ▼]
[AND]
[Entity: ATM ▼] [Attribute: area ▼] [Operator: = ▼] [Value: Indiranagar ▼]
[AND]
[Entity: ATM ▼] [Attribute: risk_score ▼] [Operator: > ▼] [Value: 70 ▼]
[Time: last 2 hours ▼]
[Run Query ▼]
```

Translates to a natural-language question and sends to the same `/api/llm/query` endpoint.

---

## 7. Chat Persistence

- Messages stored in `localStorage` per inspector (keyed by `user_id`).
- "Clear chat" button wipes localStorage for that user.
- "Save as template" sends the question to `POST /api/llm/templates` for reuse.

---

## 8. Error Handling

| Scenario | Behavior |
|----------|----------|
| LLM returns clarification | Render the clarification question as an assistant message + suggestion chips |
| LLM can't understand | "I'm not sure what you mean. Try rephrasing or use the Query Builder." + suggestions |
| Backend error (500) | "Something went wrong. Try again in a moment." + retry button |
| Timeout (> 5s) | "This query is taking longer than expected. It may be complex — try a simpler question." |
| Empty result | "No results found. Try broadening your search." |

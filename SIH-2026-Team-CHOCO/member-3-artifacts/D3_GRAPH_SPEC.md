# D3 Money-Trail Graph — Implementation Spec

> Feature: `features/graph/` in Command Center.
> Library: D3.js (v7) for force simulation + SVG rendering.
> Data: `GET /api/mules/{complaint_id}/graph` → `{ nodes: GraphNode[], edges: GraphEdge[] }`.

---

## 1. Node Types & Visual Encoding

| Type | Shape | Fill | Stroke | Special |
|------|-------|------|--------|---------|
| `victim` | Circle | `--accent` | white | Default size |
| `mule` | Circle | `--crit` | white | Ring width proportional to `mule_score` (0–100) |
| `atm` | Square (rotated 45°) | `--good` | white | Icon of cash machine |
| `upi` | Diamond | `--muted` | white | Smaller size |
| `phone` | Circle | `--muted` | white | Smaller size |
| `bank` | Rounded rect | `--accent-2` | white | Medium size |

**Size scale:**
- Victim: r=20
- Mule: r=18 + ring width = `mule_score / 10` (max 10px)
- ATM: r=22 (largest, anchor point)
- UPI/Phone/Bank: r=12

---

## 2. Edge Types & Visual Encoding

| Relationship | Color | Stroke width | Label |
|-------------|-------|--------------|-------|
| `SENT_MONEY_TO` | `--crit` (red) | 2px | Amount (₹) |
| `TRANSFERRED_TO` | `--warn` (amber) | 2px | Amount (₹) |
| `WITHDREW_AT` | `--good` (green) | 2px | Amount (₹) |
| `CONNECTED_TO` | `--muted` (gray) | 1px dashed | — |

Arrow markers on directed edges.

---

## 3. Force Simulation Config

```typescript
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(edges).id(d => d.id).distance(120))
  .force('charge', d3.forceManyBody().strength(-400))
  .force('center', d3.forceCenter(width / 2, height / 2))
  .force('collision', d3.forceCollide().radius(40))
  .force('x', d3.forceX(width / 2).strength(0.05))
  .force('y', d3.forceY(height / 2).strength(0.05));
```

---

## 4. Interactions

- **Drag:** drag any node to reposition; simulation re-heats gently.
- **Zoom/Pan:** `d3.zoom` with extent limits.
- **Select node:** click → highlight node + all connected edges + neighbors. Show `NodePanel` side panel.
- **Hover:** tooltip with node label + type + score (if mule).
- **Double-click node:** center graph on that node.
- **Reset:** button to restore default zoom + unselect.

---

## 5. NodePanel (Side Panel)

When a node is selected, a side panel slides in from the right:

```tsx
<NodePanel node={selectedNode} onClose={() => setSelected(null)} />
```

Content depends on node type:
- **Victim:** masked name, amount sent, connected mules list.
- **Mule:** `RiskPill`, risk factors (list), connected complaints, action buttons (Freeze).
- **ATM:** area, coordinates, connected mules, action buttons (Trigger Verification).
- **UPI/Phone/Bank:** label, connected nodes, relationships.

---

## 6. Layout File Structure

```
features/graph/
├── GraphView.tsx          # container: dropdown + graph + panel
├── MoneyGraph.tsx         # D3 SVG rendering
├── useGraphLayout.ts      # D3 force simulation hook
├── NodePanel.tsx          # side panel for selected node
├── GraphLegend.tsx        # type + edge legend
└── types.ts               # GraphNode, GraphEdge interfaces
```

---

## 7. Performance

- **Node cap:** 100+ nodes without lag (D3 SVG).
- **Zoom/Pan:** 60fps via `d3.zoom`.
- **Select highlight:** < 100ms (simple lookup by id).
- **Force reheat:** 300ms on new data (add node/edge).
- **Reduced motion:** if `prefers-reduced-motion`, skip force animation, use static layout.

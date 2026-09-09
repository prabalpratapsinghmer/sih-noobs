# Performance, Accessibility & UX Targets

> These are the numbers we hold ourselves to. Measurable, testable, enforceable in CI.
> See `DEVOPS.md` for infrastructure targets, `MONITORING.md` for runtime metrics.

---

## 1. Frontend Performance

| Metric | Target | How to measure |
|--------|--------|----------------|
| First Contentful Paint (FCP) | **< 1.5 s** | Lighthouse CI |
| Largest Contentful Paint (LCP) | **< 2.5 s** | Lighthouse CI |
| Time to Interactive (TTI) | **< 3 s** | Lighthouse CI |
| Total Blocking Time (TBT) | **< 200 ms** | Lighthouse CI |
| Cumulative Layout Shift (CLS) | **< 0.1** | Lighthouse CI |
| Lighthouse Performance | **≥ 90** all UIs | Lighthouse CI (budget gate) |
| Animation framerate | **60 fps** | Chrome DevTools Performance tab |
| Bundle size (per app, gzip) | **< 300 KB** initial | Vite build output |

---

## 2. Map Performance

| Metric | Target |
|--------|--------|
| ATM markers rendered | **500+** without lag |
| Heatmap update latency | **< 2 s** after new WS prediction |
| Zoom/pan FPS | **60 fps** |
| Cluster render time | **< 100 ms** for 500 markers |
| Marker click → popup | **< 50 ms** |

---

## 3. Graph Performance

| Metric | Target |
|--------|--------|
| Nodes rendered | **100+** without performance issues |
| Zoom/pan FPS | **60 fps** |
| Node selection highlight | **< 100 ms** |
| Force simulation settle | **< 3 s** after new data |
| Graph load from API | **< 1 s** |

---

## 4. LLM Agent Performance

| Metric | Target |
|--------|--------|
| Query → first response chunk | **< 2 s** |
| Full response complete | **< 5 s** (including LLM call) |
| Cypher query accuracy | **≥ 95%** correct generation |
| Clarification rate | **< 10%** of queries |
| Response rendering | **< 200 ms** after full response |

---

## 5. DevOps Performance

| Metric | Target |
|--------|--------|
| Full stack `compose up` | **< 2 min** |
| CI/CD pipeline (push → deploy) | **< 10 min** |
| Monitoring scrape cadence | **30 s** |
| K8s rollout (zero-downtime) | **< 60 s** |
| Service self-heal (restart) | **< 30 s** |
| Demo uptime | **99.9%** during presentation |

---

## 6. Accessibility (WCAG 2.1 AA)

| Requirement | Status |
|-------------|--------|
| Text contrast ≥ 4.5:1 (normal), ≥ 3:1 (large) | Required |
| Focus visible on all interactive elements | Required |
| Keyboard navigable throughout | Required |
| Screen reader compatible (roles, labels, aria-live) | Required |
| Risk conveyed by color + text + symbol (not color-only) | Required |
| `prefers-reduced-motion` respected | Required |
| Form labels associated with inputs | Required |
| Error messages linked to inputs via `aria-describedby` | Required |
| Modal focus trap + Escape close | Required |
| Touch targets ≥ 48×48px (Field Dashboard) | Required |

---

## 7. Testing Targets

| Type | Coverage | Tool |
|------|----------|------|
| Unit tests | **≥ 80%** lines | Vitest / Jest |
| Component tests | All shared `@sih/ui` components | React Testing Library |
| E2E tests | All critical user flows | Playwright |
| Lighthouse CI | **≥ 90** all 3 UIs | Lighthouse CI |
| Cross-browser | Chrome, Firefox, Edge, Safari | Playwright |

---

## 8. User Experience

| Requirement | Target |
|-------------|--------|
| Complaint → police action clock | **< 10 min** |
| Offline support (Field Dashboard) | Service worker + queue |
| PWA installable (Victim Portal) | Manifest + service worker |
| Multi-language support (Victim Portal) | 22 Indian languages (deferred) |
| Print-friendly (Admin audit logs) | `@media print` styles |

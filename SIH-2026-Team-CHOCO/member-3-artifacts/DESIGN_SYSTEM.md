# Design System — Tokens, Themes & Semantics

> All frontends consume this. Tokens are the single source of truth for colors, type, spacing, and risk semantics.
> See `COMPONENT_SPEC.md` for individual component contracts; see `UI_KIT_API.md` for the shared package surface.

---

## 1. Color Tokens

All colors are CSS custom properties. Every token is declared on bare `:root` first, then redefined for dark mode. No token lives only inside a dark block.

### 1.1 Light Theme (default)

```css
:root {
  /* Surface & background */
  --bg:           #eef2f7;   /* page ground */
  --surface:      #ffffff;   /* cards, panels */
  --surface-2:    #f6f8fc;   /* alt blocks, table headers */

  /* Text */
  --ink:          #1d2740;   /* headings, strong text */
  --body:         #3d4a63;   /* reading text */
  --muted:        #64728c;   /* labels, captions, timestamps */

  /* Borders */
  --line:         #d8e0ec;   /* hairline borders, dividers */
  --line-2:       #c3cfdf;   /* heavier borders, table rules */

  /* Accent (steel blue) */
  --accent:       #2a6cd8;   /* links, active states, primary CTA */
  --accent-2:     #1e4fa8;   /* hover / pressed accent */
  --accent-soft:  #e4ecfa;   /* light accent background */
  --onaccent:     #ffffff;   /* text on accent background */

  /* Semantic: good / low risk */
  --good:         #16815f;
  --good-soft:    #e3f4ed;

  /* Semantic: warn / medium risk */
  --warn:         #a8640a;
  --warn-soft:    #faf0dc;

  /* Semantic: crit / high risk */
  --crit:         #c02f45;
  --crit-soft:    #fbe7ea;

  /* Code panels (dark even in light theme) */
  --code-bg:      #0d1730;
  --code-ink:     #dbe6f7;
  --code-mut:     #6f84ad;
  --code-kw:      #7e9bff;   /* keywords */
  --code-str:     #ffd28a;   /* strings */
  --code-fn:      #5ee0c0;   /* functions */

  /* Danger / destructive */
  --danger:       #c02f45;
  --danger-hover: #a51f34;
  --danger-soft:  #fbe7ea;

  /* Shadow */
  --shadow: 0 1px 2px rgba(23,38,64,.06), 0 12px 32px -18px rgba(23,38,64,.22);
}
```

### 1.2 Dark Theme (via OS preference)

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:           #0a101d;
    --surface:      #121a2c;
    --surface-2:    #0e1626;

    --ink:          #e8eef8;
    --body:         #b4bfd3;
    --muted:        #7c8bab;

    --line:         #24304a;
    --line-2:       #31405f;

    --accent:       #5b97f2;
    --accent-2:     #8ab4f7;
    --accent-soft:  #16233f;
    --onaccent:     #081326;

    --good:         #3ecf9c;
    --good-soft:    #102920;
    --warn:         #e3a34b;
    --warn-soft:    #2b2213;
    --crit:         #f0697c;
    --crit-soft:    #2b151b;

    --code-bg:      #080e1c;
    --code-ink:     #cfdbf0;
    --code-mut:     #5c6f96;
    --code-kw:      #7493f7;
    --code-str:     #f4c173;
    --code-fn:      #4cd8b4;

    --danger:       #f0697c;
    --danger-hover: #ff8a99;
    --danger-soft:  #2b151b;

    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 16px 40px -20px rgba(0,0,0,.6);
  }
}
```

### 1.3 Dark Theme (via explicit toggle)

```css
:root[data-theme="dark"] {
  /* Identical values to the media query block above.
     Duplicate intentionally so the toggle wins regardless of OS. */
}
```

### 1.4 Theme Toggle

```typescript
// Toggle the data-theme attribute on <html>
type Theme = 'light' | 'dark' | 'system';

function setTheme(theme: Theme) {
  const root = document.documentElement;
  if (theme === 'system') {
    root.removeAttribute('data-theme');
  } else {
    root.setAttribute('data-theme', theme);
  }
  localStorage.setItem('theme', theme);
}
```

---

## 2. Typography

### 2.1 Faces

| Role | Font | Weight | Source |
|------|------|--------|--------|
| Headings + body | IBM Plex Sans | 400, 500, 600, 700 | Google Fonts |
| Code + data + labels | IBM Plex Mono | 400, 500, 600 | Google Fonts |

**Fallback stack:** `'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif`
**Mono fallback:** `'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, monospace`

### 2.2 Type Scale

| Role | Size | Weight | Line height | Letter spacing |
|------|------|--------|-------------|----------------|
| Page title (h1) | clamp(2rem, 4vw, 3.4rem) | 700 | 1.08 | -0.02em |
| Section title (h2) | clamp(1.4rem, 2.6vw, 1.9rem) | 700 | 1.2 | -0.01em |
| Subsection (h3) | 1.16rem | 600 | 1.3 | 0 |
| Card title (h4) | 0.95rem | 600 | 1.3 | 0 |
| Body | 16px | 400 | 1.68 | 0 |
| Small / caption | 0.9rem | 400 | 1.5 | 0 |
| Eyebrow / label | 12.5px | 600 | 1 | 0.1em |
| Table header | 10.5px | 500 | 1 | 0.14em |
| Code | 12.5px | 400 | 1.62 | 0 |
| Mono label | 11px | 500 | 1 | 0.08em |

### 2.3 Rules

- All h1/h2: `text-wrap: balance` (prevents orphaned words).
- Body text: max-width `70ch` (optimal reading width).
- Eyebrows: uppercase, letter-spaced, mono font.
- Tabular data: `font-variant-numeric: tabular-nums` on all `<td>` and `<th>` with numbers.

---

## 3. Spacing

### 3.1 Base Grid
4px base unit. All spacing is a multiple of 4:

| Token | Value | Common use |
|-------|-------|------------|
| `space-1` | 4px | Tight gaps (badge padding, icon offset) |
| `space-2` | 8px | Small gaps (button padding, tag spacing) |
| `space-3` | 12px | Card inner padding (compact) |
| `space-4` | 16px | Card inner padding, table cell padding |
| `space-5` | 20px | Card padding (standard) |
| `space-6` | 24px | Section gaps |
| `space-8` | 32px | Between major blocks |
| `space-10` | 40px | Section margins (medium) |
| `space-12` | 48px | Section margins (large) |
| `space-16` | 64px | Hero margins, page section breaks |

### 3.2 Layout

| Property | Value |
|----------|-------|
| Max content width | 1080px |
| Content padding (desktop) | 28px |
| Content padding (mobile) | 18px |
| Grid gap (card grids) | 16px |
| Table border-radius | 10px |
| Card border-radius | 10px |
| Pill border-radius | 999px |
| Small control radius | 6px |
| Focus ring radius | 4px |

---

## 4. Shadows

One shadow token for light theme, one for dark:

```css
/* Light */
--shadow: 0 1px 2px rgba(23,38,64,.06),
          0 12px 32px -18px rgba(23,38,64,.22);

/* Dark */
--shadow: 0 1px 2px rgba(0,0,0,.4),
          0 16px 40px -20px rgba(0,0,0,.6);
```

**Usage:** Apply to cards, modals, dropdowns, popups. Not to inline elements, text, or borders.

---

## 5. Risk Semantics

Risk is the most important visual signal in the system. It is **never color-only**.

### 5.1 Risk Levels

| Level | Color token | Pill class | Symbol | Usage |
|-------|------------|------------|--------|-------|
| Critical / High | `--crit` | `.pill.crit` | ▲ (triangle) | Risk score ≥ 70 |
| Medium / Warning | `--warn` | `.pill.warn` | ● (circle) | Risk score 40–69 |
| Low / Info | `--good` | `.pill.good` | ▼ (down arrow) | Risk score < 40 |

### 5.2 Risk Pill Component

```tsx
<RiskPill score={82} />  // renders: ▲ High · 82 (with red pill background)
```

### 5.3 Heatmap Mapping

| Risk range | Marker color | Cluster color |
|-----------|--------------|---------------|
| 70–100 | Red (`--crit`) | Red with count |
| 40–69 | Amber (`--warn`) | Amber with count |
| 0–39 | Green (`--good`) | Green with count |

### 5.4 Edge Stripe (Alert Cards)

The right edge of each alert card is a 4px stripe in the risk color. This provides a non-text, non-color-only indicator visible even in grayscale.

---

## 6. Component Tokens (Tailwind)

The Tailwind preset maps CSS tokens to Tailwind utilities:

```typescript
// tailwind.preset.ts
const preset = {
  theme: {
    extend: {
      colors: {
        bg:       'var(--bg)',
        surface:  'var(--surface)',
        'surface-2': 'var(--surface-2)',
        ink:      'var(--ink)',
        body:     'var(--body)',
        muted:    'var(--muted)',
        line:     'var(--line)',
        'line-2': 'var(--line-2)',
        accent:   'var(--accent)',
        'accent-2': 'var(--accent-2)',
        'accent-soft': 'var(--accent-soft)',
        good:     'var(--good)',
        'good-soft': 'var(--good-soft)',
        warn:     'var(--warn)',
        'warn-soft': 'var(--warn-soft)',
        crit:     'var(--crit)',
        'crit-soft': 'var(--crit-soft)',
        danger:   'var(--danger)',
        'danger-hover': 'var(--danger-hover)',
      },
      fontFamily: {
        sans: ['IBM Plex Sans', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['IBM Plex Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: {
        card: '10px',
        pill: '999px',
        control: '6px',
      },
      boxShadow: {
        card: 'var(--shadow)',
      },
    },
  },
};
```

---

## 7. Accessibility Requirements

### 7.1 WCAG 2.1 AA

- All text meets 4.5:1 contrast ratio (normal text) and 3:1 (large text).
- Focus visible: 2px accent ring with 2px offset on all interactive elements.
- Keyboard navigable: tab order follows visual order.
- Screen reader: `aria-label` on icon buttons, `role` on custom widgets.

### 7.2 Color-Blind Safety

- Risk conveyed as: color + label text + symbol.
- Never use red/green alone as the sole differentiator.
- Map markers have shape difference (circle for critical, diamond for warning, square for info) in addition to color.
- Edge stripes on alert cards provide grayscale-differentiable signal.

### 7.3 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 7.4 Screen Reader Announcements

- Alert toasts: `aria-live="polite"` for non-critical, `aria-live="assertive"` for critical.
- Loading states: `aria-busy="true"` on the container.
- Modal open: focus trapped inside modal, `Escape` closes.
- Map/graph actions: `aria-label` with human-readable description.

---

## 8. Code Block Styling

Code panels have a dark background in **both** themes (matching the repo/code aesthetic):

```css
.panel {
  background: var(--code-bg);
  border: 1px solid var(--line-2);
  border-radius: 10px;
  overflow: hidden;
}
.panel pre {
  color: var(--code-ink);
  font-family: var(--font-mono);
  font-size: 12.5px;
  line-height: 1.62;
}
```

Syntax highlighting tokens (for code panels):
- Keywords: `--code-kw` (#7e9bff light / #7493f7 dark)
- Strings: `--code-str` (#ffd28a light / #f4c173 dark)
- Functions: `--code-fn` (#5ee0c0 light / #4cd8b4 dark)
- Comments: `--code-mut` (#6f84ad light / #5c6f96 dark)

---

## 9. Responsive Breakpoints

| Breakpoint | Width | Behavior |
|-----------|-------|----------|
| Mobile | < 640px | Field Dashboard primary target. Single column. |
| Tablet | 640–1024px | Two-column grid for cards. |
| Desktop | 1024–1440px | Full layout. Command/Admin primary target. |
| Wide | > 1440px | Max-width container centered. |

**Command Center:** desktop-first, but must not break below 1024px (inspector laptops).
**Field Dashboard:** mobile-first, must be excellent below 640px.
**Admin Panel:** desktop-first, must not break below 1100px.

---

## 10. Print Styles

For report printing (Admin Panel audit logs, FIR drafts):
```css
@media print {
  #topbar, nav, .sidebar, .toast-container { display: none; }
  body { background: white; color: black; }
  .panel { background: white; border: 1px solid #ccc; }
}
```

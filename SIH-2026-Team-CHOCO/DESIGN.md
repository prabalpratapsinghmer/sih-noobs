# Design System: Linear × SpaceX Aerospace Telemetry

## 1. Visual Theme & Atmosphere

A **high-contrast cyber-defense telemetry interface** — where Linear's dark-mode precision meets SpaceX mission-control density. The atmosphere is clinical, authoritative, and razor-sharp: deep charcoal surfaces (#0D0D0E / #131314) with crisp Zinc-800 borders, a singular amber-copper accent (#D4A843) for active telemetry, and IBM Plex Sans/Mono providing technical gravitas. Every pixel communicates status, latency, and health — no decoration, only signal.

**Density:** Cockpit Dense (9/10) — information-rich panels, monospace data grids, zero waste.
**Variance:** Predictable Symmetric (2/10) — strict grid, aligned baselines, deterministic rhythm.
**Motion:** Static Restrained (1/10) — instant state transitions, no decorative animation. Only hardware-accelerated opacity/transform for focus rings and loading shimmers.

---

## 2. Color Palette & Roles

| Token | Hex | Role |
|-------|-----|------|
| **Void** | `#0D0D0E` | Primary canvas — deepest surface, near-black but never pure `#000000` |
| **Void-Elevated** | `#131314` | Card/panel background — one step up from canvas |
| **Void-Hover** | `#1A1A1B` | Interactive surface hover state |
| **Border-Subtle** | `#2A2A2C` | Primary structural borders (1px) — Zinc-800 equivalent |
| **Border-Accent** | `#3A3A3C` | Focus rings, active element borders |
| **Text-Primary** | `#F4F4F5` | Primary text — Zinc-50, high contrast on Void |
| **Text-Secondary** | `#A1A1AA` | Metadata, labels, timestamps — Zinc-400 |
| **Text-Muted** | `#71717A` | Disabled, placeholder, helper text — Zinc-500 |
| **Telemetry-Amber** | `#D4A843` | **SINGLE ACCENT** — active telemetry, live indicators, primary CTAs, focus rings (saturation ~65%, warm copper-amber) |
| **Telemetry-Amber-Dim** | `#B8923A` | Pressed/active state for accent elements |
| **Telemetry-Green** | `#10B981` | Nominal/healthy status — Emerald-500 (strictly for status, never UI chrome) |
| **Telemetry-Red** | `#EF4444` | Critical/warning status — Red-500 (strictly for status) |
| **Telemetry-Blue** | `#3B82F6` | Info/connection status — Blue-500 (strictly for status) |

**Constraints:**
- Maximum **one UI accent** (Telemetry-Amber). Status colors are semantic, not decorative.
- No purple, no neon, no gradients on text or buttons.
- No pure black (`#000000`) — use Void `#0D0D0E`.
- No glassmorphism, no blur, no transparency stacking. Flat, opaque surfaces only.

---

## 3. Typography Rules

### Font Stacks
- **Display / Headings / Body:** `IBM Plex Sans`, system-ui, -apple-system, sans-serif
- **Mono / Telemetry / Financial / ATM / Data Grids:** `IBM Plex Mono`, ui-monospace, SFMono-Regular, monospace

### Hierarchy (clamp-based fluid scaling)

| Token | Size (Desktop) | Size (Mobile) | Weight | Line Height | Letter Spacing | Use |
|-------|----------------|---------------|--------|-------------|----------------|-----|
| `display-xl` | `clamp(2.5rem, 4vw, 3.5rem)` | 40–56px | 600 | 1.05 | -0.02em | Page title, hero metric |
| `display-lg` | `clamp(1.75rem, 3vw, 2.25rem)` | 28–36px | 600 | 1.1 | -0.015em | Section header, panel title |
| `display-md` | `clamp(1.25rem, 2vw, 1.5rem)` | 20–24px | 500 | 1.2 | -0.01em | Card title, widget header |
| `heading-sm` | `1rem` | 16px | 500 | 1.3 | 0 | Sub-section label |
| `body-lg` | `1.125rem` | 18px | 400 | 1.6 | 0 | Lead paragraph, description |
| `body-md` | `1rem` | 16px | 400 | 1.6 | 0 | Default body text |
| `body-sm` | `0.875rem` | 14px | 400 | 1.5 | 0 | Metadata, helper text |
| `mono-xl` | `clamp(1.5rem, 2.5vw, 2rem)` | 24–32px | 500 | 1.1 | 0 | Hero telemetry value |
| `mono-lg` | `1.25rem` | 20px | 500 | 1.2 | 0 | Panel metric, large KPI |
| `mono-md` | `1rem` | 16px | 400 | 1.4 | 0 | Inline data, table cells |
| `mono-sm` | `0.875rem` | 14px | 400 | 1.4 | 0 | Timestamp, micro-label |
| `mono-xs` | `0.75rem` | 12px | 400 | 1.3 | 0.02em | Fine print, badge text |

**Principles:**
- **All numbers, currency, timestamps, IDs, coordinates, latency values → `IBM Plex Mono`**. No exceptions.
- Headings use weight for hierarchy, not massive size jumps. Track-tight on display.
- Body text max-width: `65ch` (enforced via container).
- **Banned:** Inter, generic system fonts for headings, pure black text, serif fonts anywhere.

---

## 4. Component Stylings

### Buttons
| Variant | Background | Text | Border | Radius | Padding | States |
|---------|------------|------|--------|--------|---------|--------|
| **Primary** | `Telemetry-Amber` | `Void` | None | `6px` | `12px 24px` | Hover: `Telemetry-Amber-Dim`, Active: `translateY(1px)`, Focus: `0 0 0 2px Telemetry-Amber` |
| **Secondary** | `Transparent` | `Text-Primary` | `1px Border-Subtle` | `6px` | `12px 24px` | Hover: `Void-Hover`, Focus: `0 0 0 2px Telemetry-Amber` |
| **Ghost** | `Transparent` | `Text-Secondary` | None | `6px` | `8px 16px` | Hover: `Void-Hover`, Text: `Text-Primary` |
| **Destructive** | `Transparent` | `Telemetry-Red` | `1px Telemetry-Red` | `6px` | `12px 24px` | Hover: `rgba(239,68,68,0.1)` |

- **No outer glows, no box-shadows on buttons.** Tactile `translateY(1px)` on active only.
- **Font:** `IBM Plex Sans` at `body-sm` / 600 weight.

### Cards / Panels
- **Background:** `Void-Elevated` (`#131314`)
- **Border:** `1px solid Border-Subtle` (`#2A2A2C`)
- **Radius:** `8px` (consistent, no `full`/`pill` except badges)
- **Padding:** `24px` (desktop) / `16px` (mobile)
- **No shadows.** Elevation communicated via border + background step only.
- **High-density override:** Replace card with `border-t Border-Subtle` divider + `py-4` spacing.

### Inputs / Form Fields
- **Background:** `Void` (`#0D0D0E`)
- **Border:** `1px solid Border-Subtle` (default) → `1px solid Border-Accent` (hover) → `1px solid Telemetry-Amber` (focus)
- **Text:** `Text-Primary` (`IBM Plex Sans`)
- **Placeholder:** `Text-Muted`
- **Label:** Above input, `body-sm` / `Text-Secondary` / `mb-2`
- **Error:** `Telemetry-Red` text below, `border-Telemetry-Red`
- **Radius:** `6px`
- **Padding:** `10px 14px`
- **Min-height:** `44px` (touch target)

### Data Tables / Telemetry Grids
- **Font:** `IBM Plex Mono` exclusively
- **Header:** `Void-Hover` background, `Text-Secondary`, `mono-sm`, uppercase, `tracking-wider`
- **Row:** `Void-Elevated` background, `border-b Border-Subtle`
- **Row Hover:** `Void-Hover`
- **Cell Padding:** `12px 16px`
- **Monospace alignment:** `tabular-nums` on all numeric columns

### Badges / Status Indicators
- **Radius:** `4px` (small, not pill)
- **Padding:** `2px 8px`
- **Font:** `mono-xs` / 500 weight
- **Nominal:** `bg-emerald-500/10 text-emerald-400 border-emerald-500/20`
- **Warning:** `bg-amber-500/10 text-amber-400 border-amber-500/20`
- **Critical:** `bg-red-500/10 text-red-400 border-red-500/20`
- **Live/Pulse:** `Telemetry-Amber` background, `Void` text, subtle `animate-pulse` (opacity only, 2s ease-in-out infinite)

### Loading States
- **Skeleton:** `Void-Hover` background, `animate-pulse` (opacity 0.4 → 1, 1.5s ease-in-out)
- **Exact dimensions** matching content — no generic spinners.
- **Shimmer:** Subtle `linear-gradient(90deg, Void-Hover 25%, Border-Subtle 50%, Void-Hover 75%)` moving at `2s linear infinite` — hardware accelerated.

### Empty States
- Composed illustration (SVG) + `display-md` headline + `body-sm` description + single Primary CTA.
- Centered, `py-16 px-8`, no "no data" plain text.

---

## 5. Layout Principles

### Grid System
- **12-column CSS Grid** with `gap: 24px` (desktop) / `16px` (tablet) / `12px` (mobile)
- **Max-width container:** `1400px` centered (`mx-auto px-6 md:px-12`)
- **Section vertical rhythm:** `clamp(4rem, 8vw, 6rem)` between major sections

### Spacing Scale (4px base)
| Token | Value | Use |
|-------|-------|-----|
| `space-1` | `4px` | Micro gap, icon-text |
| `space-2` | `8px` | Tight related elements |
| `space-3` | `12px` | Form field gap |
| `space-4` | `16px` | Card internal padding (mobile) |
| `space-6` | `24px` | Card internal padding (desktop), grid gap |
| `space-8` | `32px` | Section internal padding |
| `space-12` | `48px` | Major section separation |
| `space-16` | `64px` | Hero/landing vertical rhythm |

### Responsive Breakpoints
| Name | Width | Behavior |
|------|-------|----------|
| **Mobile** | `< 640px` | Single column, full-width cards, stacked nav |
| **Tablet** | `640–1023px` | 2-col grid, collapsible sidebar |
| **Desktop** | `1024–1439px` | 3-4 col grid, persistent sidebar |
| **Wide** | `≥ 1440px` | Full 12-col, max-width container active |

### Collapsing Rules
- **Mobile-first:** All multi-column → single column at `< 640px`. No exceptions.
- **No horizontal overflow** on mobile — critical failure if present.
- **Typography scales via `clamp()`** — no discrete breakpoint jumps for text.
- **Touch targets ≥ 44×44px** on all interactive elements.

---

## 6. Motion & Interaction

### Spring Physics (if any motion exists)
- **Stiffness:** `100` | **Damping:** `20` — weighty, precise, no bounce
- **Duration:** `150–200ms` for state transitions
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` (Material "standard")

### Permitted Animations (Only These)
| Trigger | Animation | Properties |
|---------|-----------|------------|
| Focus ring | Fade-in | `opacity` + `box-shadow` (150ms) |
| Live badge | Pulse | `opacity` (0.4 → 1, 2s ease-in-out infinite) |
| Skeleton loader | Shimmer | `background-position` (transform, 2s linear infinite) |
| Row hover | Background lift | `background-color` (100ms) |
| Modal/drawer | Slide + fade | `transform: translateX/Y` + `opacity` (200ms) |

### Banned
- No `animate-bounce`, `animate-spin`, `animate-ping` on UI chrome.
- No transitions on `width`, `height`, `top`, `left`, `margin`, `padding`.
- No keyframe animations on layout properties.
- No perpetual motion on static content.

---

## 7. Anti-Patterns (Explicitly Banned)

### Visual
- ❌ **Pure black** (`#000000`) — use `Void #0D0D0E`
- ❌ **Purple/neon gradients** — no `from-purple-500 to-pink-500`, no `bg-gradient-to-r` on text/buttons
- ❌ **Glassmorphism/blur** — no `backdrop-blur`, no `bg-opacity-<50>` layering
- ❌ **Outer glow shadows** — no `drop-shadow`, no `box-shadow: 0 0 20px accent`
- ❌ **Oversaturated accents** — accent saturation < 70%
- ❌ **Inter font** — use `IBM Plex Sans`
- ❌ **Generic serif fonts** (Times, Georgia, Garamond) — banned entirely
- ❌ **3-column equal card grids** — use asymmetric, zig-zag, or horizontal scroll
- ❌ **Centered hero sections** — left-aligned or split-screen only
- ❌ **Rounded-full/pill buttons** — `6px` radius only (badges: `4px`)

### Content
- ❌ **Emojis anywhere** — use inline SVG icons (20×20, `currentColor`)
- ❌ **AI copy clichés:** "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize", "Empower"
- ❌ **Fake precision:** `99.99%`, `50%`, `10x` — use real telemetry: `99.97%`, `47.3%`, `8.2x`
- ❌ **Generic names:** "John Doe", "Acme Corp", "Nexus", "Dashboard", "Platform"
- ❌ **Filler UI text:** "Scroll to explore", "Swipe down", bouncing chevrons, scroll arrows
- ❌ **Broken image links** — use `picsum.photos` or generated SVG placeholders

### Technical
- ❌ **Flexbox percentage math** (`calc(33.333% - 16px)`) — use CSS Grid
- ❌ **`h-screen` for full height** — use `min-h-[100dvh]`
- ❌ **Custom mouse cursors** — system cursors only
- ❌ **Overlapping elements** — every element owns its spatial zone

---

## 8. Implementation Tokens (Tailwind v4 / CSS Variables)

```css
@theme {
  /* Colors */
  --color-void: #0D0D0E;
  --color-void-elevated: #131314;
  --color-void-hover: #1A1A1B;
  --color-border-subtle: #2A2A2C;
  --color-border-accent: #3A3A3C;
  --color-text-primary: #F4F4F5;
  --color-text-secondary: #A1A1AA;
  --color-text-muted: #71717A;
  --color-telemetry-amber: #D4A843;
  --color-telemetry-amber-dim: #B8923A;
  --color-telemetry-green: #10B981;
  --color-telemetry-red: #EF4444;
  --color-telemetry-blue: #3B82F6;

  /* Fonts */
  --font-sans: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, monospace;

  /* Radius */
  --radius-card: 8px;
  --radius-input: 6px;
  --radius-btn: 6px;
  --radius-badge: 4px;

  /* Shadows (none for elevation, only focus) */
  --shadow-focus: 0 0 0 2px var(--color-telemetry-amber);
}

/* Base */
* { box-sizing: border-box; }
html { font-family: var(--font-sans); color: var(--color-text-primary); background: var(--color-void); }
body { line-height: 1.6; -webkit-font-smoothing: antialiased; }

/* Mono utility */
.font-mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }
.tabular-nums { font-variant-numeric: tabular-nums; }

/* Focus visible */
*:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
  border-color: var(--color-telemetry-amber);
}

/* Selection */
::selection { background: var(--color-telemetry-amber); color: var(--color-void); }
```

---

## 9. Google Fonts Loading (Next.js / Vite)

### Next.js (`app/layout.tsx`)
```tsx
import { IBM_Plex_Sans, IBM_Plex_Mono } from 'next/font/google';

const ibmPlexSans = IBM_Plex_Sans({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  weight: ['400', '500', '600', '700'],
});

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
  weight: ['400', '500', '600'],
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" class={`${ibmPlexSans.variable} ${ibmPlexMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

### Vite / React (`index.css`)
```css
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
  --font-sans: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, monospace;
}
```

---

## 10. Agent Prompt Implementation

> **For any AI agent generating screens in this system:**
>
> 1. **Canvas is always `Void #0D0D0E`** — never lighter, never pure black.
> 2. **One accent only: `Telemetry-Amber #D4A843`** — primary buttons, focus rings, live indicators.
> 3. **All data/numbers → `IBM Plex Mono` with `tabular-nums`.** No exceptions.
> 4. **Borders are `1px solid #2A2A2C`** — crisp, no blur, no glow.
> 5. **No gradients, no glass, no neon, no purple.** Flat, high-contrast, opaque.
> 6. **Layout = CSS Grid, 12-col, 24px gap, 1400px max-width.**
> 7. **Motion = 150ms opacity/transform only.** No layout animation.
> 8. **Status colors are semantic only** (Green/Red/Blue) — never used for UI chrome.
> 9. **Copy is technical, precise, real.** No marketing fluff. "Latency: 12ms" not "Blazing fast".
> 10. **If it doesn't communicate state/health/action — delete it.**

---

## 11. Quick Reference: Do / Don't

| Do | Don't |
|----|-------|
| `bg-void text-text-primary border-border-subtle` | `bg-black text-white border-gray-700` |
| `font-mono tabular-nums` on all metrics | `font-sans` on numbers/currency |
| Single `Telemetry-Amber` CTA per view | Multiple colored CTAs |
| `min-h-[100dvh]` for full-height sections | `h-screen` |
| CSS Grid + `gap` | Flexbox `calc()` hacks |
| Real telemetry values: `47.3%` `12ms` `99.97%` | Fake round numbers: `50%` `10ms` `99.99%` |
| Technical copy: "Packet loss: 0.02%" | Marketing copy: "Seamless connectivity" |
| `animate-pulse` on skeleton loaders only | Spinners on buttons/containers |
| SVG icons (20×20, currentColor) | Emojis / icon fonts |

---

*This DESIGN.md is the single source of truth for all UI generation. Any screen, component, or flow produced for this project must pass the anti-pattern checklist above.*
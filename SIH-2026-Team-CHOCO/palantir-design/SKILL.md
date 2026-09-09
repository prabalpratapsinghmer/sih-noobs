---
name: palantir-design
description: Design system skill for palantir. Activate when building UI components, pages, or any visual elements. Provides exact color tokens, typography scale, spacing grid, component patterns, and craft rules. Read references/DESIGN.md before writing any CSS or JSX. Includes ultra-mode visual journey: read references/ANIMATIONS.md, references/LAYOUT.md, references/COMPONENTS.md, and references/INTERACTIONS.md for full motion and layout details.
---

# palantir Design System

You are building UI for **palantir**. Dark-themed, neutral palette, sans-serif typography (Alliance No\.2), compact density on a 4px grid.

## Visual Reference

**IMPORTANT**: Study ALL screenshots below before writing any UI. Match colors, typography, spacing, layout, and motion exactly as shown.

### Homepage

![palantir Homepage](screenshots/homepage.png)

### Scroll Journey (Cinematic Visual States)

> These screenshots capture the website at different scroll depths. The design changes dramatically as you scroll — each frame shows a different cinematic state. Replicate these exact visual transitions.

#### 0% — Hero / Above the fold

![Scroll 0%](screens/scroll/scroll-000.png)

#### 17% — Mid-page at 17% scroll

![Scroll 17%](screens/scroll/scroll-017.png)

#### 33% — Mid-page at 33% scroll

![Scroll 33%](screens/scroll/scroll-033.png)

#### 50% — Mid-page at 50% scroll

![Scroll 50%](screens/scroll/scroll-050.png)

#### 67% — Mid-page at 67% scroll

![Scroll 67%](screens/scroll/scroll-067.png)

#### 83% — Mid-page at 83% scroll

![Scroll 83%](screens/scroll/scroll-083.png)

#### 100% — Footer / End of page

![Scroll 100%](screens/scroll/scroll-100.png)

### Video Backgrounds (First Frames)

![Video 1 (background)](screens/scroll/video-1-frame.png)

> Read `references/DESIGN.md` for full token details. Read `references/ANIMATIONS.md` for motion specs. Read `references/LAYOUT.md` for layout structure. Read `references/COMPONENTS.md` for component patterns.

## Ultra Reference Files

This package includes extended documentation. **Read these files before implementing:**

| File | Contents |
|------|----------|
| `references/DESIGN.md` | Full design system tokens, colors, typography, spacing |
| `references/VISUAL_GUIDE.md` | **START HERE** — Master visual guide with all screenshots embedded |
| `references/ANIMATIONS.md` | CSS keyframes, scroll triggers, motion library stack, video specs |
| `references/LAYOUT.md` | Flex/grid containers, page structure, spacing relationships |
| `references/COMPONENTS.md` | DOM component patterns, HTML structure, class fingerprints |
| `references/INTERACTIONS.md` | Hover/focus states with before/after style diffs |
| `screens/scroll/` | 7 scroll journey screenshots showing cinematic states |

### Animation Stack Detected

- **Web Animations API (38 active)** — animation

## Design Philosophy

- **Layered depth** — use shadow tokens to create a sense of physical layering. Each elevation level has a specific shadow.
- **Gradient accents** — gradients are used thoughtfully for emphasis, not decoration.
- **Type pairing** — Alliance No\.2 for body/UI text, Alliance No\.1 for headings/display. Never introduce a third typeface.
- **compact density** — 4px base grid. Every dimension is a multiple of 4.
- **neutral palette** — the color temperature runs neutral, matching the sans-serif typography.
- **Restrained accent** — `#2b5945` is the only pop of color. Used exclusively for CTAs, links, focus rings, and active states.
- **Subtle motion** — transitions smooth state changes. Keep durations under 300ms, use ease-out curves.

## Color System

### Core Palette

| Role | Token | Hex | Use |
|------|-------|-----|-----|
| Background | `--background` | `#1e2124` | Page/app background |
| Surface | `--surface` | `#000000` | Cards, panels, modals |
| Text Primary | `--text-primary` | `#ffffff` | Headings, body text |
| Text Muted | `--text-muted` | `#9b9b9b` | Captions, placeholders |
| Accent | `--accent` | `#2b5945` | CTAs, links, focus rings |
| Border | `--border` | `#636363` | Dividers, card borders |

### Status Colors

| Status | Hex | Use |
|--------|-----|-----|
| Danger | `#994500` | Errors, destructive actions |

### Extended Palette

- `#881280`
- `#0000ee`
- **accent05-opaque-color:** `#f4f7f6` — Light surface or highlight color
- `#aaaaaa`
- **text-color-medium:** `#b9b9b9`
- **text-color-light:** `#767676`
- `#565656`
- `#1a1aa6`

### CSS Variable Tokens

```css
--border-color: currentColor;
--input-border-color: var(--text-color-medium);
--accent-color: #2b5945;
--accent10-color: rgba(43,89,69,.1);
--accent05-color: rgba(43,89,69,.05);
--accent05-opaque-color: #f4f7f6;
--border-color: currentColor;
--input-border-color: var(--text-color-medium);
--accent-color: #2b5945;
--accent10-color: rgba(43,89,69,.1);
--accent05-color: rgba(43,89,69,.05);
--accent05-opaque-color: #f4f7f6;
--accent-color: #8c7847;
--accent10-color: rgba(140,120,71,.1);
--accent05-color: rgba(140,120,71,.05);
--accent05-opaque-color: #f9f8f6;
--border-color: currentColor;
--input-border-color: var(--text-color-medium);
--accent-color: #2b5945;
--accent10-color: rgba(43,89,69,.1);
```

## Typography

### Font Stack

- **Alliance No\.2** — Heading 1, Heading 2, Heading 3
- **Alliance No\.1** — Body, Caption

### Font Sources

```css
@font-face {
  font-family: "Alliance No\.1";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo1-Regular.woff2") format("woff2");
  font-weight: 400;
}
@font-face {
  font-family: "Alliance No\.1";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo1-Bold.woff2") format("woff2");
  font-weight: 700;
}
@font-face {
  font-family: "Alliance No\.2";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo2-Regular.woff2") format("woff2");
  font-weight: 400;
}
@font-face {
  font-family: "Alliance No\.2";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo2-Bold.woff2") format("woff2");
  font-weight: 700;
}
```

### Type Scale

| Role | Family | Size | Weight |
|------|--------|------|--------|
| Heading 1 | Alliance No\.2 | 18px | 700 |
| Heading 2 | Alliance No\.2 | 16px | 700 |
| Heading 3 | Alliance No\.2 | 13px | 700 |
| Body | Alliance No\.1 | .7777777778rem | 400 |
| Caption | Alliance No\.1 | 12px | 400 |

### Typography Rules

- Body/UI: **Alliance No\.2**, Headings: **Alliance No\.1** — these are the only display fonts
- Max 3-4 font sizes per screen
- Headings: weight 600-700, body: weight 400
- Use color and opacity for text hierarchy, not additional font sizes
- Line height: 1.5 for body, 1.2 for headings

## Spacing & Layout

### Base Grid: 4px

Every dimension (margin, padding, gap, width, height) must be a multiple of **4px**.

### Spacing Scale

`2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24` px

### Spacing as Meaning

| Spacing | Use |
|---------|-----|
| 4-8px | Tight: related items (icon + label, avatar + name) |
| 12-16px | Medium: between groups within a section |
| 24-32px | Wide: between distinct sections |
| 48px+ | Vast: major page section breaks |

### Border Radius

Scale: `.1111111111rem, 2px, 4px, 6px, 10px, 17px, 20px, 48px, 50px, 60px`
Default: `17px`

### Container

Max-width: `80rem`, centered with auto margins.

### Breakpoints

| Name | Value |
|------|-------|
| sm | 35em |
| md | 47.4375em |
| md | 47.5em |
| lg | 60em |
| 2xl | 90em |

Mobile-first: design for small screens, layer on responsive overrides.

## Component Patterns

### Card

```css
.card {
  background: #000000;
  border: 1px solid #636363;
  border-radius: 17px;
  padding: 16px;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 10px 0px;
}
```

```html
<div class="card">
  <h3>Card Title</h3>
  <p>Card content goes here.</p>
</div>
```

### Button

```css
/* Primary */
.btn-primary {
  background: #2b5945;
  color: #ffffff;
  border-radius: 17px;
  padding: 8px 16px;
  font-weight: 500;
  transition: opacity 150ms ease;
}
.btn-primary:hover { opacity: 0.9; }

/* Ghost */
.btn-ghost {
  background: transparent;
  border: 1px solid #636363;
  color: #ffffff;
  border-radius: 17px;
  padding: 8px 16px;
}
```

```html
<button class="btn-primary">Get Started</button>
<button class="btn-ghost">Learn More</button>
```

### Input

```css
.input {
  background: #1e2124;
  border: 1px solid #636363;
  border-radius: 17px;
  padding: 8px 12px;
  color: #ffffff;
  font-size: 14px;
}
.input:focus { border-color: #2b5945; outline: none; }
```

```html
<input class="input" type="text" placeholder="Search..." />
```

### Badge / Chip

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  background: #000000;
  color: #9b9b9b;
}
```

```html
<span class="badge">New</span>
<span class="badge">Beta</span>
```

### Modal / Dialog

```css
.modal-backdrop { background: rgba(0, 0, 0, 0.6); }
.modal {
  background: #000000;
  border: 1px solid #636363;
  border-radius: 60px;
  padding: 24px;
  max-width: 480px;
  width: 90vw;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 2px 10px 0px;
}
```

```html
<div class="modal-backdrop">
  <div class="modal">
    <h2>Dialog Title</h2>
    <p>Dialog content.</p>
    <button class="btn-primary">Confirm</button>
    <button class="btn-ghost">Cancel</button>
  </div>
</div>
```

### Table

```css
.table { width: 100%; border-collapse: collapse; }
.table th {
  text-align: left;
  padding: 8px 12px;
  font-weight: 500;
  font-size: 12px;
  color: #9b9b9b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #636363;
}
.table td {
  padding: 12px;
  border-bottom: 1px solid #636363;
}
```

```html
<table class="table">
  <thead><tr><th>Name</th><th>Status</th><th>Date</th></tr></thead>
  <tbody>
    <tr><td>Item One</td><td>Active</td><td>Jan 1</td></tr>
    <tr><td>Item Two</td><td>Pending</td><td>Jan 2</td></tr>
  </tbody>
</table>
```

### Navigation

```css
.nav {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid #636363;
}
.nav-link {
  color: #9b9b9b;
  padding: 8px 12px;
  border-radius: 17px;
  transition: color 150ms;
}
.nav-link:hover { color: #ffffff; }
.nav-link.active { color: #2b5945; }
```

```html
<nav class="nav">
  <a href="/" class="nav-link active">Home</a>
  <a href="/about" class="nav-link">About</a>
  <a href="/pricing" class="nav-link">Pricing</a>
  <button class="btn-primary" style="margin-left: auto">Get Started</button>
</nav>
```

## Animation & Motion

This project uses **subtle motion**. Transitions smooth state changes without calling attention.

### Motion Tokens

- **Duration scale:** `0ms`, `0s`, `.01ms`, `.13s`, `.15s`, `.2s`, `.22s`, `.25s`, `.275s`, `.4s`, `50ms`, `75ms`, `80ms`, `100ms`, `120ms`, `125ms`, `130ms`, `150ms`, `160ms`, `175ms`, `200ms`, `220ms`, `240ms`, `250ms`, `275ms`, `350ms`
- **Easing functions:** `ease-in-out`, `linear`, `ease`, `cubic-bezier(.645,.045,.355,1)`, `cubic-bezier(.165,.84,.44,1)`, `cubic-bezier(.895,.03,.685,.22)`, `cubic-bezier(.55,.055,.675,.19)`, `cubic-bezier(.33333,.66667,.66667,1)`, `cubic-bezier(.215,.61,.355,1)`, `cubic-bezier(.33333,0,.66667,.33333)`, `cubic-bezier(.68,-.55,.265,1.55)`, `ease-in`, `cubic-bezier(.6,.04,.98,.335)`, `ease-out`, `cubic-bezier(.075,.82,.165,1)`, `cubic-bezier(.19,1,.22,1)`
- **Animated properties:** `color`

### Motion Guidelines

- **Duration:** Use values from the duration scale above. Short (0ms) for micro-interactions, long (350ms) for page transitions
- **Easing:** Use `ease-in-out` as the default easing curve
- **Direction:** Elements enter from bottom/right, exit to top/left
- **Reduced motion:** Always respect `prefers-reduced-motion` — disable animations when set

## Depth & Elevation

### Shadow Tokens

- Floating (dropdowns, popovers): `rgba(0, 0, 0, 0.1) 0px 2px 10px 0px`

### Z-Index Scale

`1, 2, 500, 590, 900, 915, 925, 950`

Use these exact values — never invent z-index values.

## Anti-Patterns (Never Do)

- **No blur effects** — no backdrop-blur, no filter: blur()
- **No zebra striping** — tables and lists use borders for separation
- **No invented colors** — every hex value must come from the palette above
- **No arbitrary spacing** — every dimension is a multiple of 4px
- **No extra fonts** — only Alliance No\.2 and Alliance No\.1 are allowed
- **No arbitrary border-radius** — use the scale: .1111111111rem, 2px, 4px, 6px, 10px, 17px, 20px, 48px, 50px, 60px
- **No opacity for disabled states** — use muted colors instead
- **No pill shapes** — this design doesn't use rounded-full / 9999px radius

## Workflow

1. **Read** `references/DESIGN.md` before writing any UI code
2. **Pick colors** from the Color System section — never invent new ones
3. **Set typography** — Alliance No\.2, Alliance No\.1 only, using the type scale
4. **Build layout** on the 4px grid — check every margin, padding, gap
5. **Match components** to patterns above before creating new ones
6. **Apply elevation** — use shadow tokens
7. **Validate** — every value traces back to a design token. No magic numbers.

## Brand Spec

- **Favicon:** `/favicon.ico`
- **Site URL:** `https://www.palantir.com/`
- **Brand color:** `#2b5945`
- **Brand typeface:** Alliance No\.2

## Quick Reference

```
Background:     #1e2124
Surface:        #000000
Text:           #ffffff / #9b9b9b
Accent:         #2b5945
Border:         #636363
Font:           Alliance No\.2
Spacing:        4px grid
Radius:         17px
Components:     0 detected
```

## When to Trigger

Activate this skill when:
- Creating new components, pages, or visual elements for palantir
- Writing CSS, Tailwind classes, styled-components, or inline styles
- Building page layouts, templates, or responsive designs
- Reviewing UI code for design consistency
- The user mentions "palantir" design, style, UI, or theme
- Generating mockups, wireframes, or visual prototypes

---

# Full Reference Files

> Every output file is embedded below. Claude has full design system context from /skills alone.

## Design System Tokens (DESIGN.md)

# palantir DESIGN.md

> Auto-generated design system — reverse-engineered via static analysis by skillui.
> Frameworks: None detected
> Colors: 20 · Fonts: 2 · Components: 0
> Icon library: not detected · State: not detected
> Primary theme: dark · Dark mode toggle: no · Motion: subtle

## Visual Reference

**Match this design exactly** — study colors, fonts, spacing, and component shapes before writing any UI code.

![palantir Homepage](../screenshots/homepage.png)

---

## 1. Visual Theme & Atmosphere

This is a **dark-themed** interface with a neutral tone. Depth is expressed through layered shadows and subtle surface color variation. Typography pairs **Alliance No\.1** for display/headings with **Alliance No\.2** for body text, creating clear visual hierarchy through type contrast. Spacing follows a **4px base grid** (compact density), with scale: 2, 4, 6, 8, 10, 12, 14, 16px. The accent color **#2b5945** anchors interactive elements (buttons, links, focus rings). Motion is subtle — smooth transitions (150-300ms) ease state changes without drawing attention.

---

## 2. Color Palette & Roles

| Token | Hex | Role | Use |
|---|---|---|---|
| text-color | `#1e2124` | background | Page background, darkest surface |
| surface | `#000000` | surface | Card and panel backgrounds |
| body-color | `#ffffff` | text-primary | Headings and body text |
| text-color-light | `#9b9b9b` | text-muted | Captions, placeholders, secondary info |
| text-color-medium | `#636363` | border | Dividers, card borders, outlines |
| accent-color | `#2b5945` | accent | CTAs, links, focus rings, active states |
| accent-color | `#4e8af7` | accent | CTAs, links, focus rings, active states |
| error-color | `#ff4136` | accent | CTAs, links, focus rings, active states |
| accent-color | `#8c7847` | accent | CTAs, links, focus rings, active states |
| danger | `#994500` | danger | Error states, destructive actions |
| info | `#0000ee` | info | Informational highlights |
| unknown | `#881280` | unknown | Palette color |
| accent05-opaque-color | `#f4f7f6` | unknown | Palette color |
| unknown | `#aaaaaa` | unknown | Palette color |
| text-color-medium | `#b9b9b9` | unknown | Palette color |
| text-color-light | `#767676` | unknown | Palette color |
| unknown | `#565656` | unknown | Palette color |
| unknown | `#1a1aa6` | unknown | Palette color |
| body-color-medium | `#2f3234` | unknown | Palette color |
| body-color-light | `#494a4b` | unknown | Palette color |

### CSS Variable Tokens

```css
--border-color: currentColor;
--input-border-color: var(--text-color-medium);
--accent-color: #2b5945;
--accent10-color: rgba(43,89,69,.1);
--accent05-color: rgba(43,89,69,.05);
--accent05-opaque-color: #f4f7f6;
--border-color: currentColor;
--input-border-color: var(--text-color-medium);
--accent-color: #2b5945;
--accent10-color: rgba(43,89,69,.1);
--accent05-color: rgba(43,89,69,.05);
--accent05-opaque-color: #f4f7f6;
--accent-color: #8c7847;
--accent10-color: rgba(140,120,71,.1);
--accent05-color: rgba(140,120,71,.05);
--accent05-opaque-color: #f9f8f6;
--border-color: currentColor;
--input-border-color: var(--text-color-medium);
--accent-color: #2b5945;
--accent10-color: rgba(43,89,69,.1);
```


---

## 3. Typography Rules

**Font Stack:**
- **Alliance No\.2** — Heading 1, Heading 2, Heading 3
- **Alliance No\.1** — Body, Caption

**Font Sources:**

```css
@font-face {
  font-family: "Alliance No\.1";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo1-Regular.woff2") format("woff2");
  font-weight: 400;
}
@font-face {
  font-family: "Alliance No\.1";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo1-Bold.woff2") format("woff2");
  font-weight: 700;
}
@font-face {
  font-family: "Alliance No\.2";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo2-Regular.woff2") format("woff2");
  font-weight: 400;
}
@font-face {
  font-family: "Alliance No\.2";
  src: url("https://www.palantir.com/fonts/Alliance/AllianceNo2-Bold.woff2") format("woff2");
  font-weight: 700;
}
```

| Role | Font | Size | Weight |
|---|---|---|---|
| Heading 1 | Alliance No\.2 | 18px | 700 |
| Heading 2 | Alliance No\.2 | 16px | 700 |
| Heading 3 | Alliance No\.2 | 13px | 700 |
| Body | Alliance No\.1 | .7777777778rem | 400 |
| Caption | Alliance No\.1 | 12px | 400 |

**Typographic Rules:**
- Limit to 2 font families max per screen
- Use **Alliance No\.2** for body/UI text, **Alliance No\.1** for display/headings
- Maintain consistent hierarchy: no more than 3-4 font sizes per screen
- Headings use bold (600-700), body uses regular (400)
- Line height: 1.5 for body text, 1.2 for headings
- Use color and opacity for secondary hierarchy, not additional font sizes


---

## 4. Component Stylings

No components detected. Scan `src/components/` or `components/` to populate this section.

---

## 5. Layout Principles

- **Base spacing unit:** 4px
- **Spacing scale:** 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24
- **Border radius:** .1111111111rem, 2px, 4px, 6px, 10px, 17px, 20px, 48px, 50px, 60px
- **Max content width:** 80rem

**Spacing as Meaning:**
| Spacing | Use |
|---|---|
| 4-8px | Tight: related items within a group |
| 12-16px | Medium: between groups |
| 24-32px | Wide: between sections |
| 48px+ | Vast: major section breaks |


---

## 6. Depth & Elevation

### Floating — dropdowns, popovers, modals

- `rgba(0, 0, 0, 0.1) 0px 2px 10px 0px`

### Z-Index Scale

`1, 2, 500, 590, 900, 915, 925, 950`



---

## 7. Animation & Motion

This project uses **subtle motion**. Transitions smooth state changes without demanding attention.

### Motion Guidelines

- Duration: 150-300ms for micro-interactions, 300-500ms for page transitions
- Easing: `ease-out` for enters, `ease-in` for exits
- Always respect `prefers-reduced-motion`


---

## 8. Do's and Don'ts

### Do's

- Use `#2b5945` for interactive elements (buttons, links, focus rings)
- Use `#1e2124` as the primary page background
- Pair **Alliance No\.2** (body) with **Alliance No\.1** (display) — these are the only allowed fonts
- Follow the **4px** spacing grid for all margins, padding, and gaps
- Use the defined shadow tokens for elevation — see Section 6
- Use border-radius from the scale: .1111111111rem, 2px, 4px, 6px, 10px

### Don'ts

- Don't introduce colors outside this palette — extend the design tokens first
- Don't introduce additional font families beyond Alliance No\.2 and Alliance No\.1
- Don't use arbitrary spacing values — stick to multiples of 4px
- Don't create custom box-shadow values outside the system tokens
- Don't use arbitrary border-radius values — pick from the defined scale
- Don't use backdrop-blur or blur effects

### Anti-Patterns (detected from codebase)

- No blur or backdrop-blur effects
- No zebra striping on tables/lists


---

## 9. Responsive Behavior

| Name | Value | Source |
|---|---|---|
| sm | 35em | css |
| md | 47.4375em | css |
| md | 47.5em | css |
| lg | 60em | css |
| 2xl | 90em | css |

**Approach:** Use `@media (min-width: ...)` queries matching the breakpoints above.


---

## 10. Agent Prompt Guide

Use these as starting points when building new UI:

### Build a Card

```
Background: #000000
Border: 1px solid #636363
Radius: 17px
Padding: 16px
Font: Alliance No\.2
Use shadow tokens from Section 6.
```

### Build a Button

```
Primary: bg #2b5945, text white
Ghost: bg transparent, border #636363
Padding: 8px 16px
Radius: 17px
Hover: opacity 0.9 or lighter shade
Focus: ring with #2b5945
```

### Build a Page Layout

```
Background: #1e2124
Max-width: 80rem, centered
Grid: 4px base
Responsive: mobile-first, breakpoints from Section 9
```

### Build a Stats Card

```
Surface: #000000
Label: #9b9b9b (muted, 12px, uppercase)
Value: #ffffff (primary, 24-32px, bold)
Status: use success/warning/danger from Section 2
```

### Build a Form

```
Input bg: #1e2124
Input border: 1px solid #636363
Focus: border-color #2b5945
Label: #9b9b9b 12px
Spacing: 16px between fields
Radius: 17px
```

### General Component

```
1. Read DESIGN.md Sections 2-6 for tokens
2. Colors: only from palette
3. Font: Alliance No\.2, type scale from Section 3
4. Spacing: 4px grid
5. Components: match patterns from Section 4
6. Elevation: shadow tokens
```

## Visual Guide — Screenshots (VISUAL_GUIDE.md)

# palantir — Visual Guide

> Master visual reference. Study every screenshot carefully before implementing any UI.
> Match colors, layout, typography, spacing, and motion states exactly.

**Motion Stack:** **Web Animations API (38 active)**

## Scroll Journey

The page has cinematic scroll animations. Each screenshot below shows the exact visual state at that scroll depth.
**Replicate these transitions precisely** — the design changes dramatically as you scroll.

### Hero — Above the fold

*Scroll position: 0px of 6654px total*

![Hero — Above the fold](../screens/scroll/scroll-000.png)

### 17% scroll depth

*Scroll position: 978px of 6654px total*

![17% scroll depth](../screens/scroll/scroll-017.png)

### 33% scroll depth

*Scroll position: 1899px of 6654px total*

![33% scroll depth](../screens/scroll/scroll-033.png)

### 50% scroll depth

*Scroll position: 2848px of 6654px total*

![50% scroll depth](../screens/scroll/scroll-050.png)

### 67% scroll depth

*Scroll position: 3854px of 6654px total*

![67% scroll depth](../screens/scroll/scroll-067.png)

### 83% scroll depth

*Scroll position: 4776px of 6654px total*

![83% scroll depth](../screens/scroll/scroll-083.png)

### Footer — End of page

*Scroll position: 5699px of 6654px total*

![Footer — End of page](../screens/scroll/scroll-100.png)

## Video Backgrounds

These videos play as background elements. Use first-frame as poster image while video loads.

### Video 1 (background)

*Source: `/assets/xrfr7uokpv1b/n6ice73sfdWoNOQiDq6NA/d60f7448d43d38400eec368c062c0348/PAL_...`*

![Video 1 first frame](../screens/scroll/video-1-frame.png)

## Full Page Screenshots

### Home | Palantir

*URL: `https://www.palantir.com/`*

![Home | Palantir](../screens/pages/home.png)

### Palantir Sovereign AI

*URL: `https://www.palantir.com/protect-your-sovereignty/`*

![Palantir Sovereign AI](../screens/pages/protect-your-sovereignty.png)

### Palantir Artificial Intelligence Platform

*URL: `https://www.palantir.com/platforms/aip/`*

![Palantir Artificial Intelligence Platform](../screens/pages/platforms-aip.png)

### Palantir Foundry

*URL: `https://www.palantir.com/platforms/foundry/`*

![Palantir Foundry](../screens/pages/platforms-foundry.png)

### Gotham | Palantir

*URL: `https://www.palantir.com/platforms/gotham/`*

![Gotham | Palantir](../screens/pages/platforms-gotham.png)

## Section Screenshots

Clipped sections showing individual components in context.

### Section 1 — `header`

*1440×1000px*

![Section 1](../screens/sections/home-section-1.png)

### Section 3 — `[class*="hero"]`

*1440×900px*

![Section 3](../screens/sections/home-section-3.png)

### Section 5 — `header`

*1440×1041px*

![Section 5](../screens/sections/protect-your-sovereignty-section-5.png)

### Section 7 — `[class*="hero"]`

*1380×321px*

![Section 7](../screens/sections/protect-your-sovereignty-section-7.png)

### Section 7 — `header`

*1440×900px*

![Section 7](../screens/sections/platforms-aip-section-7.png)

### Section 9 — `[class*="hero"]`

*1360×205px*

![Section 9](../screens/sections/platforms-aip-section-9.png)

### Section 1 — `section`

*1440×791px*

![Section 1](../screens/sections/platforms-foundry-section-1.png)

### Section 9 — `header`

*1440×900px*

![Section 9](../screens/sections/platforms-gotham-section-9.png)

## Animations & Motion (ANIMATIONS.md)

# Animation Reference

> Cinematic motion design extracted from live DOM. Follow these specs exactly to recreate the experience.

## Motion Technology Stack

| Library | Type | Notes |
|---------|------|-------|
| **Web Animations API (38 active)** | animation |  |

## Scroll Journey

The page is **6,654px** tall. Each frame below shows what the user sees at that scroll depth.

> **Use these screenshots to understand WHAT animates, WHEN it animates, and HOW it moves.**

### 0% — Top / Hero
Scroll position: 0px

![Scroll 0%](../screens/scroll/scroll-000.png)

### 17% — Opening Section
Scroll position: 978px

![Scroll 17%](../screens/scroll/scroll-017.png)

### 33% — First Feature Section
Scroll position: 1,899px

![Scroll 33%](../screens/scroll/scroll-033.png)

### 50% — Mid-Page
Scroll position: 2,848px

![Scroll 50%](../screens/scroll/scroll-050.png)

### 67% — Lower Content
Scroll position: 3,854px

![Scroll 67%](../screens/scroll/scroll-067.png)

### 83% — Near Footer
Scroll position: 4,776px

![Scroll 83%](../screens/scroll/scroll-083.png)

### 100% — Bottom / Footer
Scroll position: 5,699px

![Scroll 100%](../screens/scroll/scroll-100.png)

## Video Elements

| # | Role | Autoplay | Loop | Muted | Size | First Frame |
|---|------|----------|------|-------|------|-------------|
| 1 | background | ✓ | ✓ | ✓ | 1440×900 | [view](../screens/scroll/video-1-frame.png) |
| 2 | content | ✓ | ✓ | ✓ | — | — |
| 3 | content | ✓ | ✓ | ✓ | — | — |
| 4 | content | ✓ | ✓ | ✓ | — | — |
| 5 | content | ✓ | ✓ | ✓ | — | — |
| 6 | content | ✓ | ✓ | ✓ | — | — |

**Video 1 first frame:**

![Video 1 Frame](../screens/scroll/video-1-frame.png)

- **Source:** `/assets/xrfr7uokpv1b/n6ice73sfdWoNOQiDq6NA/d60f7448d43d38400eec368c062c0348/PAL_HERO_REEL_v1.9.mp4`
- **Poster:** `https://www.palantir.com/assets/xrfr7uokpv1b/XmNgFr3RG44TRnXn3NjQK/64e27271f756a727824b8de7c692eef0/PAL_HERO_REEL_Static`
- **Source:** `https://www.palantir.com/assets/xrfr7uokpv1b/1ZAGlJWcYtVmMckdqFKUNW/7ff05eda0bd3471eba68c522caa32872/homepage_-_AIP.mov?`
- **Source:** `https://www.palantir.com/assets/xrfr7uokpv1b/6pvakzOU4AhfZjrgbrRXr9/ed5bb90509c20aa199058c74b3d7efd0/homepage_-_Gotham.m`
- **Source:** `https://www.palantir.com/assets/xrfr7uokpv1b/2yuGstJPCnqZBe7DOcOVNx/85275c8cb70fef128d8eda7af4900690/homepage_-_Foundry.`
- **Source:** `https://www.palantir.com/assets/xrfr7uokpv1b/727o8CbUwqHs2hTt02hIiO/cf08155d0843b07849af7d85c8e1aac0/Ontology.mov`
- **Source:** `https://www.palantir.com/assets/xrfr7uokpv1b/4hKQ7uw6vsjxrlntoFav6k/d9ea76812927c7b04539acc5463d3300/homepage_-_Apollo.m`

## Scroll Animation Patterns

| Pattern | Library | Element Count | Duration | Delay | Easing |
|---------|---------|---------------|----------|-------|--------|
| scroll-trigger | GSAP | 95 | — | — | — |

### GSAP Implementation

```javascript
// GSAP ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

gsap.from('.element', {
  opacity: 0,
  y: 60,
  duration: 0.8,
  ease: 'power2.out',
  scrollTrigger: {
    trigger: '.element',
    start: 'top 80%',
    end: 'bottom 20%',
  }
});
```

## CSS Keyframes (50 extracted)

### `@keyframes ptcom-design__flicker-temp__yu6kq9`

Duration: `2s` · Easing: `ease` · Delay: `1s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroContent__yu6kq9 > p`, `.ptcom-design__arrow__yu6kq9`

```css
@keyframes ptcom-design__flicker-temp__yu6kq9 {
  0% {
    opacity: 1;
  }
  2% {
    opacity: 1;
  }
  3% {
    opacity: 0.1;
  }
  5% {
    opacity: 0.1;
  }
  6% {
    opacity: 1;
  }
  8% {
    opacity: 1;
  }
  9% {
    opacity: 0.1;
  }
  11% {
    opacity: 0.1;
  }
  12% {
    opacity: 1;
  }
  16% {
    opacity: 1;
  }
  15% {
    opacity: 0.1;
  }
  17% {
    opacity: 0.1;
  }
  18% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__flicker-temp__16vqtz9`

Duration: `2s` · Easing: `ease` · Delay: `1s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroContent__16vqtz9 > p`, `.ptcom-design__arrow__16vqtz9`

```css
@keyframes ptcom-design__flicker-temp__16vqtz9 {
  0% {
    opacity: 1;
  }
  2% {
    opacity: 1;
  }
  3% {
    opacity: 0.1;
  }
  5% {
    opacity: 0.1;
  }
  6% {
    opacity: 1;
  }
  8% {
    opacity: 1;
  }
  9% {
    opacity: 0.1;
  }
  11% {
    opacity: 0.1;
  }
  12% {
    opacity: 1;
  }
  16% {
    opacity: 1;
  }
  15% {
    opacity: 0.1;
  }
  17% {
    opacity: 0.1;
  }
  18% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__flicker-temp__16vqtz9`

Duration: `2s` · Easing: `ease` · Delay: `1s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroContent__16vqtz9 > p`, `.ptcom-design__arrow__16vqtz9`

```css
@keyframes ptcom-design__flicker-temp__16vqtz9 {
  0% {
    opacity: 1;
  }
  2% {
    opacity: 1;
  }
  3% {
    opacity: 0.1;
  }
  5% {
    opacity: 0.1;
  }
  6% {
    opacity: 1;
  }
  8% {
    opacity: 1;
  }
  9% {
    opacity: 0.1;
  }
  11% {
    opacity: 0.1;
  }
  12% {
    opacity: 1;
  }
  16% {
    opacity: 1;
  }
  15% {
    opacity: 0.1;
  }
  17% {
    opacity: 0.1;
  }
  18% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__fadeOutDown__1r4l8zu`

Duration: `0.5s` · Easing: `ease` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__feature__1r4l8zu:not(:hover, :focus-within) .ptcom-design__contro`

```css
@keyframes ptcom-design__fadeOutDown__1r4l8zu {
  0% {
    opacity: 1;
    transform: translateY(0px);
  }
  100% {
    opacity: 0;
    transform: translateY(20px);
  }
}
```

> Fade + motion enter animation

### `@keyframes ptcom-design__shimmer__11r2569`

Duration: `4s` · Easing: `linear` · Delay: `0s` · Iteration: `infinite` · Fill: `none`

Used by: `.ptcom-design__filterButtonSkeleton__11r2569, .ptcom-design__filterTitleSkeleton`

```css
@keyframes ptcom-design__shimmer__11r2569 {
  0% {
    background-position-x: -200px;
    background-position-y: 0px;
  }
  100% {
    background-position-x: calc(100% + 200px);
    background-position-y: 0px;
  }
}
```

> Background color/gradient shift · Background position (shimmer/scroll)

### `@keyframes ptcom-design__cover-reveal__ryusq1`

Duration: `0.3s` · Easing: `ease-out` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__splash__ryusq1:has(.ptcom-design__hoverContainer__ryusq1 .ptcom-d`

```css
@keyframes ptcom-design__cover-reveal__ryusq1 {
  0% {
    height: 100%;
  }
  100% {
    height: 0px;
  }
}
```

> Dimension expand/collapse

### `@keyframes ptcom-design__side-cover-reveal__ryusq1`

Duration: `0.3s` · Easing: `ease-out` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__splash__ryusq1:has(.ptcom-design__hoverContainer__ryusq1 .ptcom-d`

```css
@keyframes ptcom-design__side-cover-reveal__ryusq1 {
  0% {
    clip-path: polygon(35% 0px, 35% 100%, calc(35% + 1px) 100%, 35% 1px);
  }
  100% {
    clip-path: polygon(0px 0px, 0px 100%, 35% 100%, 35% 0px);
  }
}
```

> Clip-path reveal

### `@keyframes ptcom-design__right-side-cover-reveal__ryusq1`

Duration: `0.3s` · Easing: `ease-out` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__splash__ryusq1:has(.ptcom-design__hoverContainer__ryusq1 .ptcom-d`

```css
@keyframes ptcom-design__right-side-cover-reveal__ryusq1 {
  0% {
    clip-path: polygon(0px 0px, 35% 0px, 35% 1px, 0px 1px);
  }
  100% {
    clip-path: polygon(0px 0px, 35% 0px, 35% 100%, 0px 100%);
  }
}
```

> Clip-path reveal

### `@keyframes ptcom-design__far-right-side-cover-reveal__ryusq1`

Duration: `0.3s` · Easing: `ease-out` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__splash__ryusq1:has(.ptcom-design__hoverContainer__ryusq1 .ptcom-d`

```css
@keyframes ptcom-design__far-right-side-cover-reveal__ryusq1 {
  0% {
    clip-path: polygon(0px 0px, 1px 0px, 1px 100%, 0px 100%);
  }
  100% {
    clip-path: polygon(0px 0px, 35% 0px, 35% 100%, 0px 100%);
  }
}
```

> Clip-path reveal

### `@keyframes gothamFlicker`

Used by: `.letter-link.is-active, .letter-link.is-active::after, .letter-link.is-active::b`

```css
@keyframes gothamFlicker {
  0% {
    opacity: 1;
  }
  14% {
    opacity: 1;
  }
  15% {
    opacity: 0;
  }
  29% {
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  44% {
    opacity: 1;
  }
  45% {
    opacity: 0;
  }
  59% {
    opacity: 0;
  }
  60% {
    opacity: 1;
  }
  74% {
    opacity: 1;
  }
  75% {
    opacity: 0;
  }
  89% {
    opacity: 0;
  }
  90% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__glitch__1qhgft3`

Duration: `var(--duration-glitch)` · Easing: `steps(11)` · Delay: `var(--delay-glitch)`

Used by: `.ptcom-design__wordDupe__1qhgft3.ptcom-design__bottom__1qhgft3`

```css
@keyframes ptcom-design__glitch__1qhgft3 {
  0% {
    transform: translateZ(0px);
  }
  10% {
    transform: translateZ(0px);
  }
  20% {
    transform: translateZ(0px);
  }
  30% {
    transform: translate3d(-50px, 0px, 0px);
  }
  40% {
    transform: translateZ(0px);
  }
  50% {
    transform: translateZ(0px);
  }
  60% {
    transform: translateZ(0px);
  }
  70% {
    transform: translate3d(100px, 0px, 0px);
  }
  80% {
    transform: translateZ(0px);
  }
  90% {
    transform: translateZ(0px);
  }
  100% {
    transform: translateZ(0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__bounce__1qhgft3`

Duration: `1s` · Easing: `linear` · Delay: `0s` · Iteration: `infinite` · Fill: `none`

Used by: `.ptcom-design__arrowIcon__1qhgft3`

```css
@keyframes ptcom-design__bounce__1qhgft3 {
  0%, 50%, 100% {
    transform: translateZ(0px);
  }
  25% {
    transform: translate3d(0px, 3px, 0px);
  }
  75% {
    transform: translate3d(0px, -3px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__fadeIn__160n6a6`

Duration: `0.3s` · Easing: `ease-in-out` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__fadeIn__160n6a6`

```css
@keyframes ptcom-design__fadeIn__160n6a6 {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__fadeOut__160n6a6`

Duration: `0.3s` · Easing: `ease-in-out` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__fadeOut__160n6a6`

```css
@keyframes ptcom-design__fadeOut__160n6a6 {
  0% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__bounce__yu6kq9`

Duration: `2s, 1s` · Easing: `ease, linear` · Delay: `1s` · Iteration: `1, infinite` · Fill: `forwards, none`

Used by: `.ptcom-design__arrow__yu6kq9`

```css
@keyframes ptcom-design__bounce__yu6kq9 {
  0%, 50%, 100% {
    transform: translateZ(0px);
  }
  25% {
    transform: translate3d(0px, 2px, 0px);
  }
  75% {
    transform: translate3d(0px, -2px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__popUp__yu6kq9`

Duration: `0.5s` · Easing: `ease` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroContent__yu6kq9 > h1 .ptcom-design__word__yu6kq9`

```css
@keyframes ptcom-design__popUp__yu6kq9 {
  100% {
    clip-path: inset(0px);
    transform: translateY(0px);
  }
}
```

> Transform/motion animation · Clip-path reveal

### `@keyframes ptcom-design__moveGrayBackground__p8p865`

Duration: `8s` · Easing: `linear` · Delay: `0s` · Iteration: `1` · Fill: `none`

Used by: `.ptcom-design__cardSelectorSelected__p8p865::after`

```css
@keyframes ptcom-design__moveGrayBackground__p8p865 {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__fade__1iydl1d`

Duration: `10s` · Easing: `ease` · Delay: `0s` · Iteration: `infinite` · Fill: `none`

Used by: `.ptcom-design__duplexLeft__1iydl1d img:nth-child(2)`

```css
@keyframes ptcom-design__fade__1iydl1d {
  0%, 20% {
    opacity: 0;
  }
  30%, 70% {
    opacity: 1;
  }
  80%, 100% {
    opacity: 0;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__heroReveal__1li4q5w`

Duration: `0.7s` · Easing: `cubic-bezier(0.65, 0, 0.35, 1)` · Delay: `0.1s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroTitleLine__1li4q5w:first-child`

```css
@keyframes ptcom-design__heroReveal__1li4q5w {
  0% {
    clip-path: inset(0px 0px 100%);
  }
  100% {
    clip-path: inset(0px);
  }
}
```

> Clip-path reveal

### `@keyframes ptcom-design__heroFadeIn__1li4q5w`

Duration: `0.7s` · Easing: `cubic-bezier(0.65, 0, 0.35, 1)` · Delay: `0.25s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroTitleLine__1li4q5w:nth-child(2)`

```css
@keyframes ptcom-design__heroFadeIn__1li4q5w {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__heroIconReveal__1li4q5w`

Duration: `0.5s` · Easing: `cubic-bezier(0.65, 0, 0.35, 1)` · Delay: `0.5s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroIconInline__1li4q5w`

```css
@keyframes ptcom-design__heroIconReveal__1li4q5w {
  0% {
    opacity: 0;
    transform: translateY(-0.5em) scale(0.8);
  }
  100% {
    opacity: 1;
    transform: translateY(-0.5em) scale(1);
  }
}
```

> Fade + motion enter animation

### `@keyframes ptcom-design__expandSlideIn__zmxckp`

Duration: `0.5s` · Easing: `cubic-bezier(0.16, 1, 0.3, 1)` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__expandedContent__zmxckp`

```css
@keyframes ptcom-design__expandSlideIn__zmxckp {
  0% {
    max-height: 0px;
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    max-height: 500px;
    opacity: 1;
    transform: translateY(0px);
  }
}
```

> Fade + motion enter animation · Dimension expand/collapse

### `@keyframes ptcom-design__fadeInUp__zmxckp`

Duration: `0.5s` · Easing: `cubic-bezier(0.4, 0, 0.2, 1)` · Delay: `0.1s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__coverContainer__zmxckp`

```css
@keyframes ptcom-design__fadeInUp__zmxckp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0px);
  }
}
```

> Fade + motion enter animation

### `@keyframes ptcom-design__heroLayerIn__1el9558`

Duration: `0.6s` · Easing: `ease` · Delay: `var(--layer-delay,0s)` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroLayer__1el9558`

```css
@keyframes ptcom-design__heroLayerIn__1el9558 {
  0% {
    opacity: 0;
    transform: translateY(1rem);
  }
  100% {
    opacity: 1;
    transform: translateY(0px);
  }
}
```

> Fade + motion enter animation

### `@keyframes ptcom-design__arrowBounce__1el9558`

Duration: `1.4s` · Easing: `cubic-bezier(0.4, 0, 0.2, 1)` · Delay: `0s` · Iteration: `infinite` · Fill: `none`

Used by: `.ptcom-design__arrowIcon__1el9558`

```css
@keyframes ptcom-design__arrowBounce__1el9558 {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(16px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__enter__ez0mgp`

Duration: `var(--duration)` · Easing: `var(--ease-out-quint)` · Delay: `calc(var(--base-delay) + var(--line-delay))` · Fill: `forwards`

Used by: `.ptcom-design__play__ez0mgp .ptcom-design__line__ez0mgp`

```css
@keyframes ptcom-design__enter__ez0mgp {
  100% {
    opacity: 1;
    transform: translateZ(0px);
  }
}
```

> Fade + motion enter animation

### `@keyframes ptcom-design__glow__ascdjs`

Duration: `4s` · Easing: `ease-in-out` · Delay: `calc(5 * var(--step))` · Iteration: `infinite` · Fill: `both`

Used by: `.ptcom-design__inView__ascdjs .ptcom-design__glow__ascdjs`

```css
@keyframes ptcom-design__glow__ascdjs {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__dash__1ns762s`

Duration: `30s` · Easing: `linear` · Delay: `0s` · Iteration: `infinite` · Fill: `none`

Used by: `.ptcom-design__dash__1ns762s`

```css
@keyframes ptcom-design__dash__1ns762s {
  0% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: 860;
  }
}
```

> SVG stroke animation

### `@keyframes ptcom-design__glow__edgwaz`

Duration: `4s` · Easing: `ease-in-out` · Delay: `0.5s` · Iteration: `infinite` · Fill: `both`

Used by: `.ptcom-design__inView__edgwaz .ptcom-design__glow__edgwaz`

```css
@keyframes ptcom-design__glow__edgwaz {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__bg__c4npw7`

Duration: `2s` · Easing: `ease-in` · Delay: `0s` · Iteration: `1` · Fill: `none`

Used by: `.ptcom-design__highlight-hash__c4npw7`

```css
@keyframes ptcom-design__bg__c4npw7 {
  0% {
    background-color: rgb(255, 244, 159);
  }
  20% {
    background-color: rgba(255, 244, 159, 0.8);
  }
  50% {
    background-color: rgba(255, 244, 159, 0.4);
  }
  100% {
    background-color: rgba(255, 244, 159, 0);
  }
}
```

> Background color/gradient shift · Background position (shimmer/scroll)

### `@keyframes ptcom-design__fadeIn__nmg7h`

Duration: `0.2s` · Easing: `ease` · Delay: `0s` · Iteration: `1` · Fill: `none`

Used by: `.ptcom-design__drawerOverlay__nmg7h`

```css
@keyframes ptcom-design__fadeIn__nmg7h {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__slideUp__nmg7h`

Duration: `0.3s` · Easing: `ease` · Delay: `0s` · Iteration: `1` · Fill: `none`

Used by: `.ptcom-design__drawerContainer__nmg7h`

```css
@keyframes ptcom-design__slideUp__nmg7h {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__bounce__16vqtz9`

Duration: `2s, 1s` · Easing: `ease, linear` · Delay: `1s` · Iteration: `1, infinite` · Fill: `forwards, none`

Used by: `.ptcom-design__arrow__16vqtz9`

```css
@keyframes ptcom-design__bounce__16vqtz9 {
  0%, 50%, 100% {
    transform: translateZ(0px);
  }
  25% {
    transform: translate3d(0px, 2px, 0px);
  }
  75% {
    transform: translate3d(0px, -2px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__popUp__16vqtz9`

Duration: `0.5s` · Easing: `ease` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroContent__16vqtz9 > h1 .ptcom-design__word__16vqtz9`

```css
@keyframes ptcom-design__popUp__16vqtz9 {
  100% {
    clip-path: inset(0px);
    transform: translateY(0px);
  }
}
```

> Transform/motion animation · Clip-path reveal

### `@keyframes ptcom-design__flicker-temp__10yze31`

Duration: `2s`

Used by: `.ptcom-design__inPageNavList__10yze31:hover .ptcom-design__inPageNavItemSelected`

```css
@keyframes ptcom-design__flicker-temp__10yze31 {
  0% {
    opacity: 1;
  }
  2% {
    opacity: 1;
  }
  3% {
    opacity: 0;
  }
  5% {
    opacity: 0;
  }
  6% {
    opacity: 1;
  }
  8% {
    opacity: 1;
  }
  9% {
    opacity: 0;
  }
  11% {
    opacity: 0;
  }
  12% {
    opacity: 1;
  }
  16% {
    opacity: 1;
  }
  15% {
    opacity: 0;
  }
  17% {
    opacity: 0;
  }
  18% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__flicker-stay-on__10yze31`

Duration: `0.3s`

Used by: `.ptcom-design__inPageNavLink__10yze31:hover .ptcom-design__inPageNavItemTitle__1`

```css
@keyframes ptcom-design__flicker-stay-on__10yze31 {
  0% {
    opacity: 1;
  }
  14% {
    opacity: 1;
  }
  15% {
    opacity: 0;
  }
  29% {
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  44% {
    opacity: 1;
  }
  45% {
    opacity: 0;
  }
  59% {
    opacity: 0;
  }
  60% {
    opacity: 1;
  }
  74% {
    opacity: 1;
  }
  75% {
    opacity: 0;
  }
  89% {
    opacity: 0;
  }
  90% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__bounce__16vqtz9`

Duration: `2s, 1s` · Easing: `ease, linear` · Delay: `1s` · Iteration: `1, infinite` · Fill: `forwards, none`

Used by: `.ptcom-design__arrow__16vqtz9`

```css
@keyframes ptcom-design__bounce__16vqtz9 {
  0%, 50%, 100% {
    transform: translateZ(0px);
  }
  25% {
    transform: translate3d(0px, 2px, 0px);
  }
  75% {
    transform: translate3d(0px, -2px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__popUp__16vqtz9`

Duration: `0.5s` · Easing: `ease` · Delay: `0s` · Iteration: `1` · Fill: `forwards`

Used by: `.ptcom-design__heroContent__16vqtz9 > h1 .ptcom-design__word__16vqtz9`

```css
@keyframes ptcom-design__popUp__16vqtz9 {
  100% {
    clip-path: inset(0px);
    transform: translateY(0px);
  }
}
```

> Transform/motion animation · Clip-path reveal

### `@keyframes ptcom-design__flicker-temp__10yze31`

Duration: `2s`

Used by: `.ptcom-design__inPageNavList__10yze31:hover .ptcom-design__inPageNavItemSelected`

```css
@keyframes ptcom-design__flicker-temp__10yze31 {
  0% {
    opacity: 1;
  }
  2% {
    opacity: 1;
  }
  3% {
    opacity: 0;
  }
  5% {
    opacity: 0;
  }
  6% {
    opacity: 1;
  }
  8% {
    opacity: 1;
  }
  9% {
    opacity: 0;
  }
  11% {
    opacity: 0;
  }
  12% {
    opacity: 1;
  }
  16% {
    opacity: 1;
  }
  15% {
    opacity: 0;
  }
  17% {
    opacity: 0;
  }
  18% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__flicker-stay-on__10yze31`

Duration: `0.3s`

Used by: `.ptcom-design__inPageNavLink__10yze31:hover .ptcom-design__inPageNavItemTitle__1`

```css
@keyframes ptcom-design__flicker-stay-on__10yze31 {
  0% {
    opacity: 1;
  }
  14% {
    opacity: 1;
  }
  15% {
    opacity: 0;
  }
  29% {
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  44% {
    opacity: 1;
  }
  45% {
    opacity: 0;
  }
  59% {
    opacity: 0;
  }
  60% {
    opacity: 1;
  }
  74% {
    opacity: 1;
  }
  75% {
    opacity: 0;
  }
  89% {
    opacity: 0;
  }
  90% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes onetrust-fade-in`

Duration: `400ms` · Easing: `ease-in-out`

Used by: `#onetrust-pc-sdk.ot-fade-in, .onetrust-pc-dark-filter.ot-fade-in, #onetrust-bann`

```css
@keyframes onetrust-fade-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
```

> Opacity fade

### `@keyframes ptcom-design__progress__1s5jo4t`

```css
@keyframes ptcom-design__progress__1s5jo4t {
  0% {
    background-color: rgb(30, 33, 36);
    left: -130%;
  }
  50% {
    background-color: rgb(30, 33, 36);
    left: 130%;
  }
  51% {
    background-color: rgb(255, 255, 255);
  }
  100% {
    background-color: rgb(255, 255, 255);
  }
}
```

> Background color/gradient shift · Background position (shimmer/scroll)

### `@keyframes ptcom-design__fadeInUp__1r4l8zu`

```css
@keyframes ptcom-design__fadeInUp__1r4l8zu {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0px);
  }
}
```

> Fade + motion enter animation

### `@keyframes ptcom-design__horizontalScrollingCardsTrack__1pqcjb7`

```css
@keyframes ptcom-design__horizontalScrollingCardsTrack__1pqcjb7 {
  0% {
    transform: translateZ(0px);
  }
  100% {
    transform: translate3d(-100%, 0px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__horizontalScrollingCardsTrack__1xz2rij`

```css
@keyframes ptcom-design__horizontalScrollingCardsTrack__1xz2rij {
  0% {
    transform: translateZ(0px);
  }
  100% {
    transform: translate3d(-100%, 0px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__trackScroll__1uylacw`

```css
@keyframes ptcom-design__trackScroll__1uylacw {
  0% {
    transform: translateZ(0px);
  }
  100% {
    transform: translate3d(-100%, 0px, 0px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__turnBlack__1wh9urk`

```css
@keyframes ptcom-design__turnBlack__1wh9urk {
  0% {
    color: var(--text-color-light);
  }
  100% {
    color: var(--text-color);
  }
}
```

> Text color shift

### `@keyframes ptcom-design__turnOriginal__1wh9urk`

```css
@keyframes ptcom-design__turnOriginal__1wh9urk {
  0% {
    color: var(--text-color);
  }
  100% {
    color: var(--text-color-light);
  }
}
```

> Text color shift

### `@keyframes ptcom-design__slide-right__1wh9urk`

```css
@keyframes ptcom-design__slide-right__1wh9urk {
  0% {
    transform: translateX(0px);
  }
  100% {
    transform: translateX(16px);
  }
}
```

> Transform/motion animation

### `@keyframes ptcom-design__slide-left__1wh9urk`

```css
@keyframes ptcom-design__slide-left__1wh9urk {
  0% {
    transform: translateX(16px);
  }
  100% {
    transform: translateX(0px);
  }
}
```

> Transform/motion animation

## Global Transition Declarations

These `transition` values were extracted from CSS rules across the site:

```css
transition: color 0.25s ease-in-out;
transition: transform 0.15s cubic-bezier(0.645, 0.045, 0.355, 1), background-color cubic-bezier(0.645, 0.045, 0.355, 1) 0.1s;
transition: transform cubic-bezier(0.645, 0.045, 0.355, 1) 0.1s;
transition: top 0.1s 0.1s, transform 0.1s cubic-bezier(0.165, 0.84, 0.44, 1);
transition: bottom 0.1s 0.1s, transform 0.1s cubic-bezier(0.165, 0.84, 0.44, 1);
transition: top 0.1s, transform 0.1s cubic-bezier(0.895, 0.03, 0.685, 0.22) 0.1s;
transition: bottom 0.1s, transform 0.1s cubic-bezier(0.895, 0.03, 0.685, 0.22) 0.1s;
transition: top 0.2s cubic-bezier(0.33333, 0.66667, 0.66667, 1) 0.2s, opacity 0.1s linear;
transition: top 0.12s cubic-bezier(0.33333, 0.66667, 0.66667, 1) 0.2s, transform 0.13s cubic-bezier(0.55, 0.055, 0.675, 0.19);
transition: top 0.2s cubic-bezier(0.33333, 0, 0.66667, 0.33333), opacity 0.1s linear 0.22s;
transition: top 0.1s cubic-bezier(0.33333, 0, 0.66667, 0.33333) 0.16s, transform 0.13s cubic-bezier(0.215, 0.61, 0.355, 1) 0.25s;
transition: opacity 0.125s 0.275s;
```

## How to Recreate This Motion Design

### Step 1 — Install Dependencies

```bash
```

### Step 2 — Scroll-Reveal Pattern

Elements that animate into view follow this pattern:

```css
/* Initial hidden state */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Step 3 — Key Motion Principles

- **Video backgrounds** — use `<video autoplay loop muted playsinline>` for background videos. Always include a poster image fallback
- **Duration scale:** `0.25s` · `0.15s` · `0.1s` — use these values, never invent new durations
- **Always add** `@media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }`

### Step 4 — Scroll Journey Reference

Match what happens at each scroll position:

- **0%** (`0px`) → `screens/scroll/scroll-000.png`
- **17%** (`978px`) → `screens/scroll/scroll-017.png`
- **33%** (`1899px`) → `screens/scroll/scroll-033.png`
- **50%** (`2848px`) → `screens/scroll/scroll-050.png`
- **67%** (`3854px`) → `screens/scroll/scroll-067.png`
- **83%** (`4776px`) → `screens/scroll/scroll-083.png`
- **100%** (`5699px`) → `screens/scroll/scroll-100.png`

## Layout & Grid (LAYOUT.md)

# Layout Reference

> Auto-extracted from live DOM. Use this to understand how the site is structured spatially.

## Spacing System

**Base grid:** 4px

**Scale:** `2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 30, 32` px

| Spacing | Semantic Use |
|---------|-------------|
| 4px | Tight — within a component |
| 8px | Medium — between sibling items |
| 16px | Wide — between sections |
| 32px | Vast — major section breaks |

## Flex Layouts

| Element | Direction | Justify | Align | Gap | Children |
|---------|-----------|---------|-------|-----|----------|
| `div.ptcom-design__cards__1xz2rij` | row | — | — | — | 2 |
| `article.ptcom-design__launchpadItem__4os7w7.ptcom-design__qu` | row | space-between | — | 30px | 2 |
| `div.ptcom-design__container__p8p865` | row | — | — | 30px | 27 |
| `div.ptcom-design__track__1xz2rij.ptcom-design__narrowCardTra` | row | space-between | — | — | 27 |
| `div.ptcom-design__track__1xz2rij.ptcom-design__narrowCardTra` | row | space-between | — | — | 27 |
| `div.ptcom-design__cardSelectorContainer__p8p865` | row | — | — | 12px | 9 |
| `button.ptcom-design__cardSelector__p8p865` | row | center | center | 20px | 1 |
| `button.ptcom-design__cardSelector__p8p865` | row | center | center | 20px | 1 |
| `button.ptcom-design__cardSelector__p8p865` | row | center | center | 20px | 1 |
| `button.ptcom-design__cardSelector__p8p865` | row | center | center | 20px | 1 |
| `button.ptcom-design__cardSelector__p8p865` | row | center | center | 20px | 1 |
| `button.ptcom-design__cardSelector__p8p865` | row | center | center | 20px | 1 |
| `div.ptcom-design__card__c3vru4` | column | space-between | — | — | 1 |
| `div.ptcom-design__card__c3vru4` | column | space-between | — | — | 1 |
| `div.ptcom-design__card__c3vru4` | column | space-between | — | — | 1 |

## Grid Layouts

| Element | Template Columns | Gap | Children |
|---------|-----------------|-----|----------|
| `header.ptcom-design__hero__yu6kq9` | `1360px` | — | 1 |
| `div.ptcom-design__wrapper__4os7w7` | `92.5px 92.5px 92.5px 92.5px 92.5px 92.5px 92.5px 9` | 0px 30px | 2 |
| `div.ptcom-design__wrapper__1xz2rij` | `87.5px 87.5px 87.5px 87.5px 87.5px 87.5px 87.5px 8` | 30px | 2 |
| `div.ptcom-design__gridItemRight__4os7w7` | `950px` | normal 30px | 1 |
| `div.ptcom-design__gridRow__4os7w7` | `460px 460px` | 0px 30px | 4 |

## Structural Containers

### `<header>` (`header.ptcom-design__hero__yu6kq9`)

```
display:          grid
grid-template-columns: 1360px
padding:          40px
children:         1
```

### `<footer>` (`footer.ptcom-design__footer__1v32dv`)

```
display:          block
padding:          90px 0px 100px
children:         1
```

### `<article>` (`article.ptcom-design__launchpadItem__4os7w7.ptcom-design__gr`)

```
display:          block
padding:          20px 0px
children:         2
```

### `<article>` (`article.ptcom-design__launchpadItem__4os7w7`)

```
display:          block
padding:          20px 0px
children:         2
```

### `<article>` (`article.ptcom-design__launchpadItem__4os7w7`)

```
display:          block
padding:          20px 0px
children:         2
```

### `<article>` (`article.ptcom-design__launchpadItem__4os7w7`)

```
display:          block
padding:          20px 0px
children:         2
```

### `<article>` (`article.ptcom-design__launchpadItem__4os7w7.ptcom-design__qu`)

```
display:          flex
flex-direction:   row
justify-content:  space-between
align-items:      —
gap:              30px
padding:          20px 0px
children:         2
```

### `<nav>` (`nav.ptcom-design__quickLinksList__4os7w7`)

```
display:          block
children:         1
```

## Layout Rules

- **Container max-width:** `1440px` — always center with `margin: auto`
- Primary layout system: **Flexbox**
- Secondary layout system: **CSS Grid** (used for card grids and multi-column layouts)
- Every spacing value must be a multiple of **4px**
- Never use arbitrary margin/padding values outside the spacing scale

## Component Patterns (COMPONENTS.md)

# Component Reference

> Repeated DOM patterns detected by structural analysis. Each component appeared 3+ times.

## Detected Components

| Component | Category | Instances | Key Classes |
|-----------|----------|-----------|-------------|
| **Ptcom Design  ListItem  1h0l6bb** | card | 82× | `.ptcom-design__listItem__1h0l6bb` |
| **Ptcom Design  Item  P8p865** | card | 27× | `.ptcom-design__item__p8p865` |
| **Ptcom Design  Feature  1r4l8zu** | unknown | 27× | `.ptcom-design__feature__1r4l8zu` |
| **Ptcom Design  FeatureLink  1r4l8zu** | unknown | 27× | `.ptcom-design__featureLink__1r4l8zu` |
| **Ptcom Design  Image  1r4l8zu** | unknown | 27× | `.ptcom-design__image__1r4l8zu` |
| **Ptcom Design  TextContainerSingle  1r4l8zu** | unknown | 27× | `.ptcom-design__textContainerSingle__1r4l8zu`, `.ptcom-design__textContainer__1r4l8zu` |
| **Ptcom Design  Earmark  1r4l8zu** | unknown | 27× | `.ptcom-design__earmark__1r4l8zu` |
| **Ptcom Design  LaunchpadLink  4os7w7** | unknown | 12× | `.ptcom-design__launchpadLink__4os7w7` |
| **Ptcom Design  CardSelectorSelected  P8p865** | card | 9× | `.ptcom-design__cardSelectorSelected__p8p865`, `.ptcom-design__cardSelector__p8p865` |
| **Ptcom Design  TextContent  P8p865** | unknown | 9× | `.ptcom-design__textContent__p8p865` |
| **Ptcom Design  Word  Yu6kq9** | unknown | 6× | `.ptcom-design__word__yu6kq9` |
| **Ptcom Design  ListPlain  1h0l6bb** | unknown | 5× | `.ptcom-design__listPlain__1h0l6bb`, `.ptcom-design__list__1h0l6bb` |
| **Ptcom Design  Title  Uynxlv** | unknown | 4× | `.ptcom-design__title__uynxlv` |
| **Ptcom Design  Text  1nkr7ha** | unknown | 4× | `.ptcom-design__text__1nkr7ha` |
| **Ptcom Design  AnnouncementBarTextCell  1ulabpz** | unknown | 4× | `.ptcom-design__announcementBarTextCell__1ulabpz` |
| **Ptcom Design  LaunchpadItem  4os7w7** | card | 3× | `.ptcom-design__launchpadItem__4os7w7` |
| **Ptcom Design  LaunchpadHeader  4os7w7** | unknown | 3× | `.ptcom-design__launchpadHeader__4os7w7` |
| **Ptcom Design  ContainerImage  Uynxlv** | unknown | 3× | `.ptcom-design__containerImage__uynxlv`, `.ptcom-design__container__uynxlv` |
| **Ptcom Design  Image  1bamxf7** | unknown | 3× | `.ptcom-design__image__1bamxf7` |
| **Ptcom Design  Link  Uynxlv** | unknown | 3× | `.ptcom-design__link__uynxlv` |

## Cards

### Ptcom Design  ListItem  1h0l6bb

**Instances found:** 82

**CSS classes:** `.ptcom-design__listItem__1h0l6bb`

**HTML structure:**

```html
<li data-animation="list" class="ptcom-design__listItem__1h0l6bb"><a href="/about/">About Palantir</a></li>
```

**Base styles (from design tokens):**

```css
.ptcom-design__listItem__1h0l6bb {
  background: #000000;
  border: 1px solid #636363;
  border-radius: 17px;
  padding: 8px;
}```

### Ptcom Design  Item  P8p865

**Instances found:** 27

**CSS classes:** `.ptcom-design__item__p8p865`

**HTML structure:**

```html
<div class="ptcom-design__item__p8p865"><p class="ptcom-design__mobileReferenceText__p8p865">ShipOS</p><div class="ptcom-design__feature__1r4l8zu"><a class="ptcom-design__featureLink__1r4l8zu" href="https://www.palantir.com/shipos" id="card-0"><img class="ptcom-design__image__1r4l8zu" src="/assets/xrfr7uokpv1b/7M8IyM7xipV1h9mdqIUZpB/5f53ac4d162dbe9c9153b546ae92cee4/shutterstock_690389866.jpg" alt="Rebuilding American Sea Power"><div class="ptcom-design__textContainer__1r4l8zu ptcom-design__textContainerSingle__1r4l8zu"><p class="ptcom-design__earmark__1r4l8zu">ShipOS</p><h3 class="ptcom-design
```

**Base styles (from design tokens):**

```css
.ptcom-design__item__p8p865 {
  background: #000000;
  border: 1px solid #636363;
  border-radius: 17px;
  padding: 8px;
}```

### Ptcom Design  CardSelectorSelected  P8p865

**Instances found:** 9

**CSS classes:** `.ptcom-design__cardSelectorSelected__p8p865` `.ptcom-design__cardSelector__p8p865`

**HTML structure:**

```html
<button class="ptcom-design__cardSelector__p8p865 ptcom-design__cardSelectorSelected__p8p865"><div class="ptcom-design__textContent__p8p865">ShipOS</div></button>
```

**Base styles (from design tokens):**

```css
.ptcom-design__cardSelectorSelected__p8p865 {
  background: #000000;
  border: 1px solid #636363;
  border-radius: 17px;
  padding: 8px;
}```

### Ptcom Design  LaunchpadItem  4os7w7

**Instances found:** 3

**CSS classes:** `.ptcom-design__launchpadItem__4os7w7`

**HTML structure:**

```html
<article data-animation="navBlock" class="ptcom-design__launchpadItem__4os7w7"><div class="ptcom-design__launchpadHeader__4os7w7"><h2 data-animation="heading" class="ptcom-design__launchpadEarmark__4os7w7">Latest News</h2><a class="ptcom-design__launchpadEarmark__4os7w7 ptcom-design__launchpadLink__4os7w7" href="/newsroom/">Newsroom <span aria-hidden="true">↗</span></a></div><ul class="ptcom-design__launchpadBlock__4os7w7"><li><a class="ptcom-design__card__gb1gxh ptcom-design__card__uynxlv" href="https://www.thetimes.com/uk/healthcare/article/palantir-software-halves-sepsis-deaths-hospital-tam
```

**Base styles (from design tokens):**

```css
.ptcom-design__launchpadItem__4os7w7 {
  background: #000000;
  border: 1px solid #636363;
  border-radius: 17px;
  padding: 8px;
}```

## Other Components

### Ptcom Design  Feature  1r4l8zu

**Instances found:** 27

**CSS classes:** `.ptcom-design__feature__1r4l8zu`

**HTML structure:**

```html
<div class="ptcom-design__feature__1r4l8zu"><a class="ptcom-design__featureLink__1r4l8zu" href="https://www.palantir.com/shipos" id="card-0"><img class="ptcom-design__image__1r4l8zu" src="/assets/xrfr7uokpv1b/7M8IyM7xipV1h9mdqIUZpB/5f53ac4d162dbe9c9153b546ae92cee4/shutterstock_690389866.jpg" alt="Rebuilding American Sea Power"><div class="ptcom-design__textContainer__1r4l8zu ptcom-design__textContainerSingle__1r4l8zu"><p class="ptcom-design__earmark__1r4l8zu">ShipOS</p><h3 class="ptcom-design__title__1r4l8zu">Rebuilding American Sea Power</h3></div></a><div class="ptcom-design__controls__1r4l8
```

**Base styles (from design tokens):**

```css
.ptcom-design__feature__1r4l8zu {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  FeatureLink  1r4l8zu

**Instances found:** 27

**CSS classes:** `.ptcom-design__featureLink__1r4l8zu`

**HTML structure:**

```html
<a class="ptcom-design__featureLink__1r4l8zu" href="https://www.palantir.com/shipos" id="card-0"><img class="ptcom-design__image__1r4l8zu" src="/assets/xrfr7uokpv1b/7M8IyM7xipV1h9mdqIUZpB/5f53ac4d162dbe9c9153b546ae92cee4/shutterstock_690389866.jpg" alt="Rebuilding American Sea Power"><div class="ptcom-design__textContainer__1r4l8zu ptcom-design__textContainerSingle__1r4l8zu"><p class="ptcom-design__earmark__1r4l8zu">ShipOS</p><h3 class="ptcom-design__title__1r4l8zu">Rebuilding American Sea Power</h3></div></a>
```

**Base styles (from design tokens):**

```css
.ptcom-design__featureLink__1r4l8zu {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Image  1r4l8zu

**Instances found:** 27

**CSS classes:** `.ptcom-design__image__1r4l8zu`

**HTML structure:**

```html
<img class="ptcom-design__image__1r4l8zu" src="/assets/xrfr7uokpv1b/7M8IyM7xipV1h9mdqIUZpB/5f53ac4d162dbe9c9153b546ae92cee4/shutterstock_690389866.jpg" alt="Rebuilding American Sea Power">
```

**Base styles (from design tokens):**

```css
.ptcom-design__image__1r4l8zu {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  TextContainerSingle  1r4l8zu

**Instances found:** 27

**CSS classes:** `.ptcom-design__textContainerSingle__1r4l8zu` `.ptcom-design__textContainer__1r4l8zu`

**HTML structure:**

```html
<div class="ptcom-design__textContainer__1r4l8zu ptcom-design__textContainerSingle__1r4l8zu"><p class="ptcom-design__earmark__1r4l8zu">ShipOS</p><h3 class="ptcom-design__title__1r4l8zu">Rebuilding American Sea Power</h3></div>
```

**Base styles (from design tokens):**

```css
.ptcom-design__textContainerSingle__1r4l8zu {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Earmark  1r4l8zu

**Instances found:** 27

**CSS classes:** `.ptcom-design__earmark__1r4l8zu`

**HTML structure:**

```html
<p class="ptcom-design__earmark__1r4l8zu">ShipOS</p>
```

**Base styles (from design tokens):**

```css
.ptcom-design__earmark__1r4l8zu {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  LaunchpadLink  4os7w7

**Instances found:** 12

**CSS classes:** `.ptcom-design__launchpadLink__4os7w7`

**HTML structure:**

```html
<a class="ptcom-design__launchpadLink__4os7w7" href="/protect-your-sovereignty/">Sovereign AI</a>
```

**Base styles (from design tokens):**

```css
.ptcom-design__launchpadLink__4os7w7 {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  TextContent  P8p865

**Instances found:** 9

**CSS classes:** `.ptcom-design__textContent__p8p865`

**HTML structure:**

```html
<div class="ptcom-design__textContent__p8p865">ShipOS</div>
```

**Base styles (from design tokens):**

```css
.ptcom-design__textContent__p8p865 {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Word  Yu6kq9

**Instances found:** 6

**CSS classes:** `.ptcom-design__word__yu6kq9`

**HTML structure:**

```html
<span class="ptcom-design__word__yu6kq9">Sovereign </span>
```

**Base styles (from design tokens):**

```css
.ptcom-design__word__yu6kq9 {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  ListPlain  1h0l6bb

**Instances found:** 5

**CSS classes:** `.ptcom-design__listPlain__1h0l6bb` `.ptcom-design__list__1h0l6bb`

**HTML structure:**

```html
<ul class="ptcom-design__list__1h0l6bb ptcom-design__listPlain__1h0l6bb"><li data-animation="list" class="ptcom-design__listItem__1h0l6bb"><a href="/about/">About Palantir</a></li><li data-animation="list" class="ptcom-design__listItem__1h0l6bb"><a href="/blog/">Blog</a></li><li data-animation="list" class="ptcom-design__listItem__1h0l6bb"><a href="https://investors.palantir.com/">Investor Relations</a></li><li data-animation="list" class="ptcom-design__listItem__1h0l6bb"><a href="/newsroom/letters/">Letters from the CEO</a></li><li data-animation="list" class="ptcom-design__listItem__1h0l6bb"
```

**Base styles (from design tokens):**

```css
.ptcom-design__listPlain__1h0l6bb {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Title  Uynxlv

**Instances found:** 4

**CSS classes:** `.ptcom-design__title__uynxlv`

**HTML structure:**

```html
<div class="ptcom-design__title__uynxlv"><div class="ptcom-design__text__1nkr7ha"><div><p>Palantir software halves sepsis deaths a…</p><p>The Sepsis Hub, developed with Tampa Gen…</p></div></div></div>
```

**Base styles (from design tokens):**

```css
.ptcom-design__title__uynxlv {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Text  1nkr7ha

**Instances found:** 4

**CSS classes:** `.ptcom-design__text__1nkr7ha`

**HTML structure:**

```html
<div class="ptcom-design__text__1nkr7ha"><div><p>Palantir software halves sepsis deaths a…</p><p>The Sepsis Hub, developed with Tampa Gen…</p></div></div>
```

**Base styles (from design tokens):**

```css
.ptcom-design__text__1nkr7ha {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  AnnouncementBarTextCell  1ulabpz

**Instances found:** 4

**CSS classes:** `.ptcom-design__announcementBarTextCell__1ulabpz`

**HTML structure:**

```html
<div class="ptcom-design__announcementBarTextCell__1ulabpz"><div><p>Read CEO Alex Karp’s <a href="/q2-2026-letter">Letter to Shareholders</a> </p></div></div>
```

**Base styles (from design tokens):**

```css
.ptcom-design__announcementBarTextCell__1ulabpz {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  LaunchpadHeader  4os7w7

**Instances found:** 3

**CSS classes:** `.ptcom-design__launchpadHeader__4os7w7`

**HTML structure:**

```html
<div class="ptcom-design__launchpadHeader__4os7w7"><h2 data-animation="heading" class="ptcom-design__launchpadEarmark__4os7w7">Latest News</h2><a class="ptcom-design__launchpadEarmark__4os7w7 ptcom-design__launchpadLink__4os7w7" href="/newsroom/">Newsroom <span aria-hidden="true">↗</span></a></div>
```

**Base styles (from design tokens):**

```css
.ptcom-design__launchpadHeader__4os7w7 {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  ContainerImage  Uynxlv

**Instances found:** 3

**CSS classes:** `.ptcom-design__containerImage__uynxlv` `.ptcom-design__container__uynxlv`

**HTML structure:**

```html
<div class="ptcom-design__container__uynxlv ptcom-design__containerImage__uynxlv"><header class="ptcom-design__earmark__uynxlv">The Times, June 9, 2026</header><div class="ptcom-design__image__1bamxf7"><div><img src="/assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46e4f80ced02af83302/Screenshot_2023-06-20_at_4.45.51_PM.png?quality=70&amp;width=700&amp;height=467&amp;fit=crop" srcset="/assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46e4f80ced02af83302/Screenshot_2023-06-20_at_4.45.51_PM.png?quality=70&amp;width=300 300w, /assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46
```

**Base styles (from design tokens):**

```css
.ptcom-design__containerImage__uynxlv {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Image  1bamxf7

**Instances found:** 3

**CSS classes:** `.ptcom-design__image__1bamxf7`

**HTML structure:**

```html
<div class="ptcom-design__image__1bamxf7"><div><img src="/assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46e4f80ced02af83302/Screenshot_2023-06-20_at_4.45.51_PM.png?quality=70&amp;width=700&amp;height=467&amp;fit=crop" srcset="/assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46e4f80ced02af83302/Screenshot_2023-06-20_at_4.45.51_PM.png?quality=70&amp;width=300 300w, /assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46e4f80ced02af83302/Screenshot_2023-06-20_at_4.45.51_PM.png?quality=70&amp;width=500 500w, /assets/xrfr7uokpv1b/p0SnKDNyQWsOTZcggrW99/3d36d692f36dd46e4f80ced02af8
```

**Base styles (from design tokens):**

```css
.ptcom-design__image__1bamxf7 {
  background: #000000;
  padding: 4px;
}```

### Ptcom Design  Link  Uynxlv

**Instances found:** 3

**CSS classes:** `.ptcom-design__link__uynxlv`

**HTML structure:**

```html
<span class="ptcom-design__link__uynxlv"><span aria-hidden="true">↳</span> <span>Read Here</span></span>
```

**Base styles (from design tokens):**

```css
.ptcom-design__link__uynxlv {
  background: #000000;
  padding: 4px;
}```

## Component Rules

- Match class names exactly from the patterns above
- Each component instance must be visually identical to others of its type
- Do not add extra wrappers or change the DOM structure
- Use `#636363` for all dividers within components
- Use `#2b5945` for all interactive/active states

## Interactions & States (INTERACTIONS.md)

# Interaction Reference

> Micro-interactions extracted from live DOM. Recreate these exactly for authentic feel.

## Coverage

| Component Type | Count | States Captured |
|----------------|-------|----------------|
| Button | 3 | default, hover, focus |
| Role Button | 1 | default, focus |
| Link | 3 | default, hover, focus |

## Transition System

These transition declarations were extracted from interactive elements:

```css
transition: background-color 0.25s ease-in-out, color 0.25s ease-in-out;
transition: 0.25s ease-in-out;
transition: transform 0.25s ease-in-out, opacity 0s linear 0.25s;
transition: color 0.25s ease-in-out;
```

Apply these to all interactive elements. Never invent new durations or easings.

## Button Interactions

### Button 1 — `button`

**States:**

- Default: `../screens/states/button-1-default.png`
- Hover: `../screens/states/button-1-hover.png`
- Focus: `../screens/states/button-1-focus.png`

**On hover:**

```css
/* background-color: rgb(30, 31, 43) → */ background-color: rgb(255, 255, 255);
/* color: rgb(255, 255, 255) → */ color: rgb(30, 31, 43);
/* outline: rgb(255, 255, 255) none 3px → */ outline: rgb(30, 31, 43) none 3px;
/* outline-color: rgb(255, 255, 255) → */ outline-color: rgb(30, 31, 43);
```

**On focus:**

```css
/* outline: rgb(255, 255, 255) none 3px → */ outline: rgb(16, 16, 16) auto 1px;
/* outline-color: rgb(255, 255, 255) → */ outline-color: rgb(16, 16, 16);
```

**Transition:** `background-color 0.25s ease-in-out, color 0.25s ease-in-out`

### Button 2 — `button`

**States:**

- Default: `../screens/states/button-2-default.png`
- Hover: `../screens/states/button-2-hover.png`
- Focus: `../screens/states/button-2-focus.png`

**On hover:**

```css
/* background-color: rgb(255, 255, 255) → */ background-color: rgb(30, 33, 36);
/* color: rgb(30, 33, 36) → */ color: rgb(255, 255, 255);
/* outline: rgb(30, 33, 36) none 3px → */ outline: rgb(255, 255, 255) none 3px;
/* outline-color: rgb(30, 33, 36) → */ outline-color: rgb(255, 255, 255);
```

**On focus:**

```css
/* background-color: rgb(255, 255, 255) → */ background-color: rgb(30, 33, 36);
/* color: rgb(30, 33, 36) → */ color: rgb(255, 255, 255);
/* border-color: rgb(30, 33, 36) → */ border-color: rgb(255, 255, 255);
/* outline: rgb(30, 33, 36) none 3px → */ outline: rgb(16, 16, 16) auto 1px;
/* outline-color: rgb(30, 33, 36) → */ outline-color: rgb(16, 16, 16);
```

**Transition:** `0.25s ease-in-out`

### Button 3 — `button`

**States:**

- Default: `../screens/states/button-3-default.png`
- Hover: `../screens/states/button-3-hover.png`
- Focus: `../screens/states/button-3-focus.png`

**On hover:**

```css
/* background-color: rgb(255, 255, 255) → */ background-color: rgb(30, 33, 36);
/* color: rgb(30, 33, 36) → */ color: rgb(255, 255, 255);
/* outline: rgb(30, 33, 36) none 3px → */ outline: rgb(255, 255, 255) none 3px;
/* outline-color: rgb(30, 33, 36) → */ outline-color: rgb(255, 255, 255);
```

**On focus:**

```css
/* background-color: rgb(255, 255, 255) → */ background-color: rgb(30, 33, 36);
/* color: rgb(30, 33, 36) → */ color: rgb(255, 255, 255);
/* border-color: rgb(30, 33, 36) → */ border-color: rgb(255, 255, 255);
/* outline: rgb(30, 33, 36) none 3px → */ outline: rgb(16, 16, 16) auto 1px;
/* outline-color: rgb(30, 33, 36) → */ outline-color: rgb(16, 16, 16);
```

**Transition:** `0.25s ease-in-out`

## Role Button Interactions

### Role Button 1 — `Skip to Content`

**States:**

- Default: `../screens/states/role-button-1-default.png`
- Focus: `../screens/states/role-button-1-focus.png`

**On focus:**

```css
/* opacity: 0 → */ opacity: 1;
/* transform: matrix(1, 0, 0, 1, 0, -23.8438) → */ transform: matrix(1, 0, 0, 1, 0, 0);
/* transition: transform 0.25s ease-in-out, opacity 0s linear 0.25s → */ transition: transform 0.25s ease-in-out;
```

**Transition:** `transform 0.25s ease-in-out, opacity 0s linear 0.25s`

## Link Interactions

### Link 1 — `Sovereign AI`

**States:**

- Default: `../screens/states/link-1-default.png`
- Hover: `../screens/states/link-1-hover.png`
- Focus: `../screens/states/link-1-focus.png`

**On focus:**

```css
/* color: rgb(255, 255, 255) → */ color: rgb(138, 138, 138);
/* border-color: rgb(255, 255, 255) → */ border-color: rgb(138, 138, 138);
/* outline: rgb(255, 255, 255) none 3px → */ outline: rgb(16, 16, 16) auto 1px;
/* outline-color: rgb(255, 255, 255) → */ outline-color: rgb(16, 16, 16);
```

**Transition:** `color 0.25s ease-in-out`

### Link 2 — `↳ AIP`

**States:**

- Default: `../screens/states/link-2-default.png`
- Hover: `../screens/states/link-2-hover.png`
- Focus: `../screens/states/link-2-focus.png`

**On focus:**

```css
/* color: rgb(255, 255, 255) → */ color: rgb(138, 138, 138);
/* border-color: rgb(255, 255, 255) → */ border-color: rgb(138, 138, 138);
/* outline: rgb(255, 255, 255) none 3px → */ outline: rgb(16, 16, 16) auto 1px;
/* outline-color: rgb(255, 255, 255) → */ outline-color: rgb(16, 16, 16);
```

**Transition:** `color 0.25s ease-in-out`

### Link 3 — `↳ Foundry`

**States:**

- Default: `../screens/states/link-3-default.png`
- Hover: `../screens/states/link-3-hover.png`
- Focus: `../screens/states/link-3-focus.png`

**On focus:**

```css
/* color: rgb(255, 255, 255) → */ color: rgb(138, 138, 138);
/* border-color: rgb(255, 255, 255) → */ border-color: rgb(138, 138, 138);
/* outline: rgb(255, 255, 255) none 3px → */ outline: rgb(16, 16, 16) auto 1px;
/* outline-color: rgb(255, 255, 255) → */ outline-color: rgb(16, 16, 16);
```

**Transition:** `color 0.25s ease-in-out`

## Interaction Rules

- Accent color `#2b5945` is used for focus rings, active states, and hover highlights
- Hover effects include **color transitions** — use the extracted values, not approximations
- Focus states use **outline** (not box-shadow) — always match the extracted focus ring
- Transition durations in use: `0.25s`, `0s`
- Always respect `prefers-reduced-motion` — set all transitions to `0s` when enabled

## Design Tokens — JSON Files

### tokens/colors.json
```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "core": {
    "text-primary": {
      "value": "#ffffff",
      "role": "text-primary",
      "name": "body-color"
    },
    "background": {
      "value": "#1e2124",
      "role": "background",
      "name": "text-color"
    },
    "surface": {
      "value": "#000000",
      "role": "surface"
    },
    "text-muted": {
      "value": "#9b9b9b",
      "role": "text-muted",
      "name": "text-color-light"
    },
    "accent": {
      "value": "#8c7847",
      "role": "accent",
      "name": "accent-color"
    },
    "border": {
      "value": "#636363",
      "role": "border",
      "name": "text-color-medium"
    }
  },
  "status": {
    "danger": {
      "value": "#994500",
      "role": "danger"
    }
  },
  "extended": {
    "color-881280": {
      "value": "#881280",
      "role": "unknown"
    },
    "color-0000ee": {
      "value": "#0000ee",
      "role": "info"
    },
    "accent05-opaque-color": {
      "value": "#f4f7f6",
      "role": "unknown",
      "name": "accent05-opaque-color"
    },
    "color-aaaaaa": {
      "value": "#aaaaaa",
      "role": "unknown"
    },
    "text-color-medium": {
      "value": "#b9b9b9",
      "role": "unknown",
      "name": "text-color-medium"
    },
    "text-color-light": {
      "value": "#767676",
      "role": "unknown",
      "name": "text-color-light"
    },
    "color-565656": {
      "value": "#565656",
      "role": "unknown"
    },
    "color-1a1aa6": {
      "value": "#1a1aa6",
      "role": "unknown"
    },
    "body-color-medium": {
      "value": "#2f3234",
      "role": "unknown",
      "name": "body-color-medium"
    },
    "body-color-light": {
      "value": "#494a4b",
      "role": "unknown",
      "name": "body-color-light"
    }
  },
  "meta": {
    "theme": "dark",
    "extracted": "2026-09-06"
  }
}
```

### tokens/spacing.json
```json
{
  "base": {
    "value": "4px",
    "description": "Grid unit — all spacing must be multiples of this"
  },
  "unit": "px",
  "scale": {
    "xs": {
      "value": "2px",
      "px": 2
    },
    "sm": {
      "value": "4px",
      "px": 4
    },
    "md": {
      "value": "6px",
      "px": 6
    },
    "lg": {
      "value": "8px",
      "px": 8
    },
    "xl": {
      "value": "10px",
      "px": 10
    },
    "2xl": {
      "value": "12px",
      "px": 12
    },
    "3xl": {
      "value": "14px",
      "px": 14
    },
    "4xl": {
      "value": "16px",
      "px": 16
    },
    "5xl": {
      "value": "18px",
      "px": 18
    },
    "6xl": {
      "value": "20px",
      "px": 20
    }
  },
  "multipliers": {
    "1x": {
      "value": "4px",
      "raw": 4
    },
    "2x": {
      "value": "8px",
      "raw": 8
    },
    "3x": {
      "value": "12px",
      "raw": 12
    },
    "4x": {
      "value": "16px",
      "raw": 16
    },
    "5x": {
      "value": "20px",
      "raw": 20
    },
    "6x": {
      "value": "24px",
      "raw": 24
    },
    "7x": {
      "value": "28px",
      "raw": 28
    },
    "8x": {
      "value": "32px",
      "raw": 32
    },
    "9x": {
      "value": "36px",
      "raw": 36
    },
    "10x": {
      "value": "40px",
      "raw": 40
    },
    "11x": {
      "value": "44px",
      "raw": 44
    },
    "12x": {
      "value": "48px",
      "raw": 48
    },
    "13x": {
      "value": "52px",
      "raw": 52
    },
    "14x": {
      "value": "56px",
      "raw": 56
    },
    "15x": {
      "value": "60px",
      "raw": 60
    },
    "16x": {
      "value": "64px",
      "raw": 64
    }
  },
  "meta": {
    "totalValues": 15,
    "min": 2,
    "max": 32
  }
}
```

### tokens/typography.json
```json
{
  "families": [
    "Alliance No\\.2",
    "Alliance No\\.1"
  ],
  "scale": {
    "heading-1": {
      "fontFamily": "Alliance No\\.2",
      "fontSize": "18px",
      "fontWeight": "700",
      "lineHeight": null,
      "source": "css"
    },
    "heading-2": {
      "fontFamily": "Alliance No\\.2",
      "fontSize": "16px",
      "fontWeight": "700",
      "lineHeight": null,
      "source": "css"
    },
    "heading-3": {
      "fontFamily": "Alliance No\\.2",
      "fontSize": "13px",
      "fontWeight": "700",
      "lineHeight": null,
      "source": "css"
    },
    "body": {
      "fontFamily": "Alliance No\\.1",
      "fontSize": ".7777777778rem",
      "fontWeight": "400",
      "lineHeight": null,
      "source": "css"
    },
    "caption": {
      "fontFamily": "Alliance No\\.1",
      "fontSize": "12px",
      "fontWeight": "400",
      "lineHeight": null,
      "source": "css"
    }
  },
  "fontFaces": [
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-Regular.woff2",
      "format": "woff2",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-Regular.woff",
      "format": "woff",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-RegularItalic.woff2",
      "format": "woff2",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-RegularItalic.woff",
      "format": "woff",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-Bold.woff2",
      "format": "woff2",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-Bold.woff",
      "format": "woff",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-BoldItalic.woff2",
      "format": "woff2",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.1",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo1-BoldItalic.woff",
      "format": "woff",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-Regular.woff2",
      "format": "woff2",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-Regular.woff",
      "format": "woff",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-RegularItalic.woff2",
      "format": "woff2",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-RegularItalic.woff",
      "format": "woff",
      "weight": "400"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-Bold.woff2",
      "format": "woff2",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-Bold.woff",
      "format": "woff",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-BoldItalic.woff2",
      "format": "woff2",
      "weight": "700"
    },
    {
      "family": "Alliance No\\.2",
      "src": "https://www.palantir.com/fonts/Alliance/AllianceNo2-BoldItalic.woff",
      "format": "woff",
      "weight": "700"
    }
  ],
  "rules": {
    "maxSizesPerScreen": 4,
    "headingWeightRange": "600-700",
    "bodyWeight": 400,
    "lineHeightBody": 1.5,
    "lineHeightHeading": 1.2
  }
}
```

## Screenshots Inventory (screens/)

> Study all screenshots carefully before implementing any UI. Match every visual detail exactly.

### Scroll Journey (screens/scroll/)

*Cinematic scroll states — page visual at each scroll depth*

![scroll-000.png](screens/scroll/scroll-000.png)

![scroll-017.png](screens/scroll/scroll-017.png)

![scroll-033.png](screens/scroll/scroll-033.png)

![scroll-050.png](screens/scroll/scroll-050.png)

![scroll-067.png](screens/scroll/scroll-067.png)

![scroll-083.png](screens/scroll/scroll-083.png)

![scroll-100.png](screens/scroll/scroll-100.png)

![video-1-frame.png](screens/scroll/video-1-frame.png)

### Full Page Screenshots (screens/pages/)

*Full-page screenshots of each crawled URL*

![home.png](screens/pages/home.png)

![platforms-aip.png](screens/pages/platforms-aip.png)

![platforms-foundry.png](screens/pages/platforms-foundry.png)

![platforms-gotham.png](screens/pages/platforms-gotham.png)

![protect-your-sovereignty.png](screens/pages/protect-your-sovereignty.png)

### Section Clips (screens/sections/)

*Clipped individual sections and components*

![home-section-1.png](screens/sections/home-section-1.png)

![home-section-3.png](screens/sections/home-section-3.png)

![platforms-aip-section-7.png](screens/sections/platforms-aip-section-7.png)

![platforms-aip-section-9.png](screens/sections/platforms-aip-section-9.png)

![platforms-foundry-section-1.png](screens/sections/platforms-foundry-section-1.png)

![platforms-gotham-section-9.png](screens/sections/platforms-gotham-section-9.png)

![protect-your-sovereignty-section-5.png](screens/sections/protect-your-sovereignty-section-5.png)

![protect-your-sovereignty-section-7.png](screens/sections/protect-your-sovereignty-section-7.png)

### Interaction States (screens/states/)

*Hover, focus, and active state captures*

![button-1-default.png](screens/states/button-1-default.png)

![button-1-focus.png](screens/states/button-1-focus.png)

![button-1-hover.png](screens/states/button-1-hover.png)

![button-2-default.png](screens/states/button-2-default.png)

![button-2-focus.png](screens/states/button-2-focus.png)

![button-2-hover.png](screens/states/button-2-hover.png)

![button-3-default.png](screens/states/button-3-default.png)

![button-3-focus.png](screens/states/button-3-focus.png)

![button-3-hover.png](screens/states/button-3-hover.png)

![link-1-default.png](screens/states/link-1-default.png)

![link-1-focus.png](screens/states/link-1-focus.png)

![link-1-hover.png](screens/states/link-1-hover.png)

![link-2-default.png](screens/states/link-2-default.png)

![link-2-focus.png](screens/states/link-2-focus.png)

![link-2-hover.png](screens/states/link-2-hover.png)

![link-3-default.png](screens/states/link-3-default.png)

![link-3-focus.png](screens/states/link-3-focus.png)

![link-3-hover.png](screens/states/link-3-hover.png)

![role-button-1-default.png](screens/states/role-button-1-default.png)

![role-button-1-focus.png](screens/states/role-button-1-focus.png)

### Screenshot Index (screens/INDEX.md)

# Screenshot Index

## Scroll Journey

> Shows the cinematic state at each point of the page

| Scroll | Y Position | File |
|--------|-----------|------|
| 0% | 0px | `screens/scroll/scroll-000.png` |
| 17% | 978px | `screens/scroll/scroll-017.png` |
| 33% | 1899px | `screens/scroll/scroll-033.png` |
| 50% | 2848px | `screens/scroll/scroll-050.png` |
| 67% | 3854px | `screens/scroll/scroll-067.png` |
| 83% | 4776px | `screens/scroll/scroll-083.png` |
| 100% | 5699px | `screens/scroll/scroll-100.png` |

## Video First Frames

- Video 1 (background): `screens/scroll/video-1-frame.png`

## Pages

| Page | URL | File |
|------|-----|------|
| Home | Palantir | `https://www.palantir.com/` | `screens/pages/home.png` |
| Palantir Sovereign AI | `https://www.palantir.com/protect-your-sovereignty/` | `screens/pages/protect-your-sovereignty.png` |
| Palantir Artificial Intelligence Platform | `https://www.palantir.com/platforms/aip/` | `screens/pages/platforms-aip.png` |
| Palantir Foundry | `https://www.palantir.com/platforms/foundry/` | `screens/pages/platforms-foundry.png` |
| Gotham | Palantir | `https://www.palantir.com/platforms/gotham/` | `screens/pages/platforms-gotham.png` |

## Sections

| Page | Section | File |
|------|---------|------|
| home | #1 (header) | `screens/sections/home-section-1.png` |
| home | #3 ([class*="hero"]) | `screens/sections/home-section-3.png` |
| protect-your-sovereignty | #5 (header) | `screens/sections/protect-your-sovereignty-section-5.png` |
| protect-your-sovereignty | #7 ([class*="hero"]) | `screens/sections/protect-your-sovereignty-section-7.png` |
| platforms-aip | #7 (header) | `screens/sections/platforms-aip-section-7.png` |
| platforms-aip | #9 ([class*="hero"]) | `screens/sections/platforms-aip-section-9.png` |
| platforms-foundry | #1 (section) | `screens/sections/platforms-foundry-section-1.png` |
| platforms-gotham | #9 (header) | `screens/sections/platforms-gotham-section-9.png` |

## Homepage Screenshots (screenshots/)

![homepage.png](screenshots/homepage.png)


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

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


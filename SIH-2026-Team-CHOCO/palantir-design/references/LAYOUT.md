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


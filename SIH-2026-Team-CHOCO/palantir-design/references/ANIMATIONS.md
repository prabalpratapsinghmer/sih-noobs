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


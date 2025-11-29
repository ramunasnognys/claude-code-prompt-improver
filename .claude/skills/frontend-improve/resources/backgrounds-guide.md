# Backgrounds Guide

Comprehensive background design guidance for distinctive frontend design.

## Table of Contents
- [Core Principles](#core-principles)
- [Gradient Techniques](#gradient-techniques)
- [Geometric Patterns](#geometric-patterns)
- [Noise and Grain](#noise-and-grain)
- [Layered Backgrounds](#layered-backgrounds)
- [Parallax Effects](#parallax-effects)
- [Complete Background Examples](#complete-background-examples)

---

## Core Principles

### Never Default to Solid Colors

Solid white or gray backgrounds are the hallmark of generic design. Always add depth:

```css
/* DON'T */
background-color: #ffffff;
background-color: #f5f5f5;

/* DO - Add subtle depth */
background: linear-gradient(180deg, #fafafa 0%, #f0f0f0 100%);
```

### Match Background to Aesthetic

The background should reinforce your design direction:
- **Dark tech** → Deep gradients with color accents
- **Editorial** → Warm paper textures
- **Brutalist** → Flat with stark contrast
- **Luxury** → Subtle gradients, dark surfaces

---

## Gradient Techniques

### Radial Gradient Glow
```css
/* Soft glow from center */
.hero {
  background: radial-gradient(
    ellipse at 50% 50%,
    rgba(0, 255, 136, 0.15) 0%,
    transparent 50%
  ),
  var(--color-bg);
}

/* Glow from corner */
.section {
  background: radial-gradient(
    ellipse at 0% 0%,
    rgba(136, 0, 255, 0.1) 0%,
    transparent 40%
  ),
  var(--color-bg);
}
```

### Multi-Stop Linear Gradients
```css
/* Smooth multi-color gradient */
.gradient-bg {
  background: linear-gradient(
    135deg,
    #0a0a0f 0%,
    #12121a 25%,
    #1a1a24 50%,
    #12121a 75%,
    #0a0a0f 100%
  );
}

/* Sharp color bands */
.sharp-gradient {
  background: linear-gradient(
    180deg,
    var(--color-primary) 0%,
    var(--color-primary) 50%,
    var(--color-bg) 50%
  );
}
```

### Conic Gradients
```css
/* Spotlight effect */
.spotlight {
  background: conic-gradient(
    from 180deg at 50% 50%,
    var(--color-bg) 0deg,
    rgba(255, 255, 255, 0.05) 180deg,
    var(--color-bg) 360deg
  );
}

/* Color wheel */
.color-wheel {
  background: conic-gradient(
    from 0deg,
    #ff0000,
    #ffff00,
    #00ff00,
    #00ffff,
    #0000ff,
    #ff00ff,
    #ff0000
  );
}
```

### Gradient Mesh Effect
```css
/* Multiple radial gradients for mesh look */
.gradient-mesh {
  background:
    radial-gradient(at 40% 20%, rgba(0, 255, 136, 0.2) 0%, transparent 50%),
    radial-gradient(at 80% 0%, rgba(255, 51, 102, 0.15) 0%, transparent 50%),
    radial-gradient(at 0% 50%, rgba(106, 90, 205, 0.1) 0%, transparent 50%),
    radial-gradient(at 80% 50%, rgba(0, 212, 255, 0.1) 0%, transparent 50%),
    radial-gradient(at 0% 100%, rgba(255, 165, 0, 0.15) 0%, transparent 50%),
    var(--color-bg);
}
```

---

## Geometric Patterns

### CSS Grid Pattern
```css
.grid-pattern {
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
}

/* With accent color */
.grid-pattern-accent {
  background-image:
    linear-gradient(var(--color-primary) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-primary) 1px, transparent 1px);
  background-size: 60px 60px;
  opacity: 0.1;
}
```

### Dot Pattern
```css
.dot-pattern {
  background-image: radial-gradient(
    rgba(255, 255, 255, 0.1) 1px,
    transparent 1px
  );
  background-size: 20px 20px;
}

/* Larger dots */
.dot-pattern-large {
  background-image: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.08) 2px,
    transparent 2px
  );
  background-size: 32px 32px;
}
```

### Diagonal Lines
```css
.diagonal-lines {
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    rgba(255, 255, 255, 0.03) 10px,
    rgba(255, 255, 255, 0.03) 20px
  );
}
```

### Chevron Pattern
```css
.chevron-pattern {
  background:
    linear-gradient(135deg, var(--color-surface) 25%, transparent 25%) -50px 0,
    linear-gradient(225deg, var(--color-surface) 25%, transparent 25%) -50px 0,
    linear-gradient(315deg, var(--color-surface) 25%, transparent 25%),
    linear-gradient(45deg, var(--color-surface) 25%, transparent 25%);
  background-size: 100px 50px;
  background-color: var(--color-bg);
}
```

### SVG Pattern Background
```css
.svg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}
```

---

## Noise and Grain

### CSS Noise Filter
```css
.noise-overlay {
  position: relative;
}

.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
}
```

### Animated Grain (Subtle)
```css
@keyframes grain {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-1%, -1%); }
  20% { transform: translate(1%, 1%); }
  30% { transform: translate(-1%, 1%); }
  40% { transform: translate(1%, -1%); }
  50% { transform: translate(-1%, 0); }
  60% { transform: translate(1%, 0); }
  70% { transform: translate(0, 1%); }
  80% { transform: translate(0, -1%); }
  90% { transform: translate(1%, 1%); }
}

.animated-grain::before {
  content: '';
  position: fixed;
  inset: -50%;
  background-image: url("data:image/svg+xml,...");
  opacity: 0.02;
  animation: grain 0.5s steps(10) infinite;
  pointer-events: none;
}
```

### Film Grain with Blend Mode
```css
.film-grain {
  position: relative;
  isolation: isolate;
}

.film-grain::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/noise.png');
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

---

## Layered Backgrounds

### Multiple Background Layers
```css
.hero {
  background:
    /* Top layer: Radial glow */
    radial-gradient(
      ellipse at 20% 50%,
      rgba(0, 255, 136, 0.15) 0%,
      transparent 50%
    ),
    /* Second layer: Another glow */
    radial-gradient(
      ellipse at 80% 50%,
      rgba(255, 51, 102, 0.1) 0%,
      transparent 50%
    ),
    /* Third layer: Vertical gradient */
    linear-gradient(
      180deg,
      var(--color-bg) 0%,
      var(--color-surface) 100%
    ),
    /* Base layer: Solid color */
    var(--color-bg);
}
```

### Background with Pattern Overlay
```css
.textured-hero {
  position: relative;
  background: linear-gradient(180deg, #0a0a0f 0%, #1a1a24 100%);
}

.textured-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
}

.textured-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at 50% 0%,
    rgba(0, 255, 136, 0.1) 0%,
    transparent 60%
  );
  pointer-events: none;
}
```

---

## Parallax Effects

### CSS-Only Parallax
```css
.parallax-container {
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  perspective: 1px;
}

.parallax-bg {
  position: absolute;
  inset: 0;
  transform: translateZ(-1px) scale(2);
  background: url('/bg-image.jpg') center/cover;
  z-index: -1;
}

.parallax-content {
  position: relative;
  z-index: 1;
  background: var(--color-bg);
}
```

### Scroll-Based Parallax (JS)
```javascript
// Vanilla JS parallax
const parallaxElements = document.querySelectorAll('.parallax');

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;

  parallaxElements.forEach(el => {
    const speed = el.dataset.speed || 0.5;
    el.style.transform = `translateY(${scrollY * speed}px)`;
  });
});
```

```css
.parallax-layer {
  position: absolute;
  inset: 0;
  will-change: transform;
}

.parallax-layer.slow {
  --speed: 0.3;
}

.parallax-layer.medium {
  --speed: 0.5;
}

.parallax-layer.fast {
  --speed: 0.7;
}
```

---

## Complete Background Examples

### Example 1: Dark Tech Hero
```css
.dark-tech-hero {
  position: relative;
  background: #0a0a0f;
  overflow: hidden;
}

/* Grid pattern */
.dark-tech-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 255, 136, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 136, 0.05) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse at 50% 50%, black 30%, transparent 70%);
}

/* Glow effects */
.dark-tech-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 30% 20%, rgba(0, 255, 136, 0.15) 0%, transparent 40%),
    radial-gradient(ellipse at 70% 60%, rgba(255, 51, 102, 0.1) 0%, transparent 40%);
}
```

### Example 2: Editorial Paper Texture
```css
.editorial-bg {
  background:
    /* Subtle vignette */
    radial-gradient(
      ellipse at 50% 50%,
      transparent 50%,
      rgba(0, 0, 0, 0.05) 100%
    ),
    /* Paper texture gradient */
    linear-gradient(
      180deg,
      #faf7f2 0%,
      #f5f0e8 50%,
      #faf7f2 100%
    );
}

/* Paper grain */
.editorial-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,..."); /* noise */
  opacity: 0.02;
  pointer-events: none;
}
```

### Example 3: Gradient Mesh Background
```css
.mesh-bg {
  background:
    radial-gradient(at 0% 0%, rgba(0, 255, 136, 0.2) 0%, transparent 50%),
    radial-gradient(at 100% 0%, rgba(255, 51, 102, 0.15) 0%, transparent 50%),
    radial-gradient(at 100% 100%, rgba(106, 90, 205, 0.2) 0%, transparent 50%),
    radial-gradient(at 0% 100%, rgba(0, 212, 255, 0.15) 0%, transparent 50%),
    radial-gradient(at 50% 50%, rgba(255, 165, 0, 0.1) 0%, transparent 50%),
    linear-gradient(180deg, #0a0a0f 0%, #12121a 100%);
  background-attachment: fixed;
}
```

### Example 4: Brutalist Flat with Accent
```css
.brutalist-bg {
  background: #000000;
  position: relative;
}

/* Sharp accent bar */
.brutalist-bg::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 8px;
  background: #ff0000;
}
```

### Example 5: Animated Gradient
```css
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.animated-gradient {
  background: linear-gradient(
    -45deg,
    #0a0a0f,
    #1a1a24,
    #0f1a2a,
    #1a0f2a
  );
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}
```

---

## Quick Reference

### Background Layer Order
```
1. Radial glows (top)
2. Patterns/textures
3. Linear gradients
4. Solid color (bottom)
```

### Common Pattern Sizes
| Pattern | Size |
|---------|------|
| Dot grid | 20-32px |
| Line grid | 40-60px |
| Large pattern | 80-120px |

### Opacity Guidelines
| Effect | Opacity |
|--------|---------|
| Subtle pattern | 0.02-0.05 |
| Visible pattern | 0.05-0.1 |
| Accent glow | 0.1-0.2 |
| Strong glow | 0.2-0.3 |

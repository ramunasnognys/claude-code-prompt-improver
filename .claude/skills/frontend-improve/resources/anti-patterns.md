# Anti-Patterns Guide

What to avoid when creating distinctive frontend designs.

## Table of Contents
- [The "AI Slop" Aesthetic](#the-ai-slop-aesthetic)
- [Typography Anti-Patterns](#typography-anti-patterns)
- [Color Anti-Patterns](#color-anti-patterns)
- [Layout Anti-Patterns](#layout-anti-patterns)
- [Animation Anti-Patterns](#animation-anti-patterns)
- [Self-Check Questions](#self-check-questions)
- [Before/After Examples](#beforeafter-examples)

---

## The "AI Slop" Aesthetic

### What It Is

"AI slop" refers to the generic, immediately recognizable output that AI systems produce due to distributional convergence - sampling from the statistical center of training data.

### Key Tells

1. **Inter font** - Most common default across AI tools
2. **Purple → white gradient** - Statistical mode of web training data
3. **Perfectly even spacing** - No visual hierarchy
4. **Generic rounded corners** - 8px radius on everything
5. **Blue CTA buttons** - Bootstrap #007bff
6. **Hero with gradient + abstract shape** - Every AI landing page
7. **Card-based layout** - Safe, boring, expected

### Why It Happens

AI models learn to output "safe" choices that:
- Work universally
- Offend no one
- Appear in training data frequently

This creates a local maximum where outputs cluster around statistically common patterns.

---

## Typography Anti-Patterns

### Banned Fonts

```css
/* NEVER USE THESE */

/* System/Default */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui;

/* Overused Sans-Serif */
font-family: 'Inter', sans-serif;
font-family: 'Roboto', sans-serif;
font-family: 'Open Sans', sans-serif;
font-family: 'Lato', sans-serif;
font-family: 'Arial', sans-serif;
font-family: 'Helvetica Neue', sans-serif;

/* New AI Favorites (becoming overused) */
font-family: 'Space Grotesk', sans-serif;
font-family: 'Poppins', sans-serif;
font-family: 'Nunito', sans-serif;
```

### Weak Weight Contrast

```css
/* BAD - Too subtle */
h1 { font-weight: 600; }
p { font-weight: 400; }

/* GOOD - Dramatic contrast */
h1 { font-weight: 900; }
p { font-weight: 200; }
```

### Timid Size Scale

```css
/* BAD - Safe, boring scale */
--text-base: 16px;
--text-lg: 18px;   /* Only 1.125x */
--text-xl: 20px;   /* Only 1.25x */
--text-2xl: 24px;  /* Only 1.5x */

/* GOOD - Dramatic jumps */
--text-base: 16px;
--text-lg: 24px;   /* 1.5x */
--text-xl: 40px;   /* 2.5x */
--text-2xl: 64px;  /* 4x */
```

---

## Color Anti-Patterns

### The Purple Gradient

```css
/* THE MOST COMMON AI DEFAULT - AVOID */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
background: linear-gradient(to right, #6366f1, #8b5cf6);
background: linear-gradient(135deg, #7c3aed, #ec4899);

/* Also avoid these purple variations */
--color-primary: #8b5cf6;
--color-primary: #7c3aed;
--color-primary: #6366f1;
```

### Generic Blues

```css
/* AVOID - Bootstrap/generic blue */
--color-primary: #007bff;
--color-primary: #0d6efd;
--color-primary: #3b82f6; /* Tailwind blue-500 */

/* AVOID - Corporate blue */
--color-primary: #2563eb;
--color-primary: #1e40af;
```

### Boring Gray Backgrounds

```css
/* AVOID - Expected, flat */
background-color: #ffffff;
background-color: #f5f5f5;
background-color: #fafafa;
background-color: #f8f9fa;

/* BETTER - Add depth */
background: linear-gradient(180deg, #fafafa 0%, #f0f0f0 100%);
```

### Evenly Distributed Palettes

```css
/* BAD - No hierarchy */
.header { background: var(--color-1); }  /* 25% */
.sidebar { background: var(--color-2); } /* 25% */
.content { background: var(--color-3); } /* 25% */
.footer { background: var(--color-4); }  /* 25% */

/* GOOD - Dominant + accent */
.main { background: var(--color-bg); }      /* 70% */
.accent-elements { color: var(--primary); } /* 20% */
.highlights { color: var(--accent); }       /* 10% */
```

---

## Layout Anti-Patterns

### Card Everywhere Layout

```html
<!-- BAD - Generic card grid -->
<div class="grid grid-cols-3 gap-4">
  <div class="card">...</div>
  <div class="card">...</div>
  <div class="card">...</div>
</div>

<!-- BETTER - Break the pattern -->
<div class="featured-large">...</div>
<div class="grid-asymmetric">...</div>
```

### Perfect Symmetry

```css
/* BAD - Everything centered, balanced */
.hero {
  text-align: center;
  padding: 80px;
}

/* BETTER - Intentional asymmetry */
.hero {
  text-align: left;
  padding: 120px 60px 80px 120px; /* Uneven */
}
```

### Safe Container Width

```css
/* BAD - Staying safe */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* BETTER - Full width sections, varied widths */
.section-full { max-width: none; }
.section-narrow { max-width: 720px; }
.section-wide { max-width: 1400px; }
```

### Generic Hero Pattern

```
┌─────────────────────────────────────┐
│                                     │
│          [Badge/Label]              │
│                                     │
│       Big Headline Text             │
│                                     │
│     Supporting description          │
│                                     │
│    [Primary CTA]  [Secondary]       │
│                                     │
│          [Abstract Shape]           │
│                                     │
└─────────────────────────────────────┘

This layout appears on every AI-generated landing page.
```

---

## Animation Anti-Patterns

### Subtle Fade-in Only

```css
/* BAD - Too subtle, forgettable */
.element {
  animation: fadeIn 0.3s ease;
}

/* BETTER - Movement + fade */
.element {
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Everything Animates

```css
/* BAD - No focus, visual noise */
.every-element {
  animation: something 0.3s ease;
}

/* BETTER - Strategic animation on key moments */
.hero-content { animation: heroReveal 0.8s ease; }
/* Other elements: no animation */
```

### Generic Hover States

```css
/* BAD - Expected, boring */
.button:hover {
  background: var(--color-primary-dark);
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* BETTER - Unexpected, delightful */
.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px var(--glow-primary);
}

.card:hover {
  transform: translateY(-8px) scale(1.02);
}
```

---

## Self-Check Questions

Ask these before shipping any frontend:

### Identity Questions
1. "Would a human designer make this exact choice?"
2. "Does this look like every other AI-generated site?"
3. "If I removed the logo, would anyone know what brand this is?"

### Distinctiveness Questions
1. "What makes this memorable?"
2. "What would someone remember about this design tomorrow?"
3. "Is there ONE bold choice that defines this?"

### Authenticity Questions
1. "Does this feel designed for THIS context?"
2. "Or does it feel like a template?"
3. "Does the aesthetic match the brand/product?"

### Technical Questions
1. "Am I using Inter, Roboto, or system fonts?"
2. "Is there a purple gradient anywhere?"
3. "Is everything perfectly centered and symmetrical?"
4. "Are all my colors evenly distributed?"

---

## Before/After Examples

### Example 1: Hero Section

**Before (AI Slop)**
```css
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  text-align: center;
  padding: 80px 20px;
  font-family: 'Inter', sans-serif;
}

.hero h1 {
  font-size: 48px;
  font-weight: 600;
  color: white;
}

.hero-cta {
  background: white;
  color: #667eea;
  padding: 12px 24px;
  border-radius: 8px;
}
```

**After (Distinctive)**
```css
.hero {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 255, 136, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(255, 51, 102, 0.1) 0%, transparent 50%),
    linear-gradient(180deg, #0a0a0f 0%, #12121a 100%);
  text-align: left;
  padding: 160px 80px 120px;
  font-family: 'Bricolage Grotesque', sans-serif;
}

.hero h1 {
  font-size: 7rem;
  font-weight: 800;
  color: #e8e8ed;
  line-height: 0.95;
  letter-spacing: -0.03em;
}

.hero-cta {
  background: transparent;
  color: #00ff88;
  padding: 16px 32px;
  border: 1px solid #00ff88;
  box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
}
```

### Example 2: Card Component

**Before (AI Slop)**
```css
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 24px;
  font-family: 'Inter', sans-serif;
}

.card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
```

**After (Distinctive)**
```css
.card {
  background: #12121a;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  padding: 32px;
  font-family: 'JetBrains Mono', monospace;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #00ff88, #00d4ff);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.card:hover {
  transform: translateY(-4px);
  border-color: rgba(0, 255, 136, 0.3);
}

.card:hover::before {
  transform: scaleX(1);
}
```

---

## Quick Checklist

Before submitting frontend code, verify:

- [ ] NOT using Inter, Roboto, or system fonts
- [ ] NOT using purple gradients
- [ ] NOT using Bootstrap blue (#007bff)
- [ ] Background is NOT solid white/gray
- [ ] Font weights are extreme (not 400 vs 600)
- [ ] Size scale has dramatic jumps
- [ ] Layout breaks symmetry somewhere
- [ ] At least ONE bold aesthetic choice
- [ ] Hover states are meaningful
- [ ] Would pass the "remember tomorrow" test

---

## The Golden Rule

**Every AI makes the same safe choices. Your job is to make the bold one.**

When in doubt:
- Darker background
- Bolder typography
- Sharper color contrast
- One dramatic element
- Less perfect symmetry

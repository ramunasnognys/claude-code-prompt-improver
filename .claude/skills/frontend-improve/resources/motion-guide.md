# Motion Guide

Comprehensive animation and motion guidance for distinctive frontend design.

## Table of Contents
- [Core Principles](#core-principles)
- [CSS-Only Animations](#css-only-animations)
- [Staggered Reveals](#staggered-reveals)
- [Hover and Interaction States](#hover-and-interaction-states)
- [Scroll-Based Animations](#scroll-based-animations)
- [Framer Motion (React)](#framer-motion-react)
- [Performance Optimization](#performance-optimization)
- [Accessibility](#accessibility)
- [Complete Animation Examples](#complete-animation-examples)

---

## Core Principles

### High-Impact Moments

Focus animation budget on moments that matter:

1. **Page Load** - First impression, staggered reveals
2. **Scroll Reveals** - Content appearing as user scrolls
3. **Hover States** - Interactive feedback
4. **State Changes** - Loading → loaded, open → closed

### Quality Over Quantity

One well-orchestrated page load animation creates more delight than scattered micro-interactions everywhere.

```
Good:  [████░░░░░░] - Focused, impactful
Bad:   [░░░░░░░░░░] - Everything animates = nothing stands out
```

### Animation Properties Hierarchy

Only animate these properties for 60fps:
1. `transform` (translate, scale, rotate)
2. `opacity`

Avoid animating:
- `width`, `height` (causes layout)
- `top`, `left`, `right`, `bottom` (causes layout)
- `margin`, `padding` (causes layout)
- `border-radius` (causes paint)
- `box-shadow` (causes paint)

---

## CSS-Only Animations

### Base Easing Functions
```css
:root {
  /* Standard easings */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);      /* Expo out - snappy */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);  /* Smooth */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* Bouncy */

  /* Durations */
  --duration-instant: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  --duration-slower: 800ms;
}
```

### Fade In Up (Most Common)
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s var(--ease-out) forwards;
}
```

### Fade In Scale
```css
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fade-in-scale {
  animation: fadeInScale 0.4s var(--ease-out) forwards;
}
```

### Slide In From Side
```css
@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

---

## Staggered Reveals

### CSS Stagger Pattern
```css
.card-list .card {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s var(--ease-out) forwards;
}

/* Stagger delays */
.card-list .card:nth-child(1) { animation-delay: 0ms; }
.card-list .card:nth-child(2) { animation-delay: 100ms; }
.card-list .card:nth-child(3) { animation-delay: 200ms; }
.card-list .card:nth-child(4) { animation-delay: 300ms; }
.card-list .card:nth-child(5) { animation-delay: 400ms; }
.card-list .card:nth-child(6) { animation-delay: 500ms; }
```

### CSS Custom Properties for Dynamic Stagger
```css
.card-list .card {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s var(--ease-out) forwards;
  animation-delay: calc(var(--index, 0) * 100ms);
}
```

```html
<div class="card" style="--index: 0">Card 1</div>
<div class="card" style="--index: 1">Card 2</div>
<div class="card" style="--index: 2">Card 3</div>
```

### Hero Section Stagger
```css
.hero-content > * {
  opacity: 0;
  transform: translateY(30px);
  animation: fadeInUp 0.8s var(--ease-out) forwards;
}

.hero-content > *:nth-child(1) { animation-delay: 0ms; }      /* Badge */
.hero-content > *:nth-child(2) { animation-delay: 150ms; }   /* Headline */
.hero-content > *:nth-child(3) { animation-delay: 300ms; }   /* Subheadline */
.hero-content > *:nth-child(4) { animation-delay: 450ms; }   /* CTA buttons */
```

---

## Hover and Interaction States

### Button Hover
```css
.button {
  transform: translateY(0);
  transition: transform var(--duration-fast) var(--ease-out),
              box-shadow var(--duration-fast) var(--ease-out);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.button:active {
  transform: translateY(0);
  transition-duration: 50ms;
}
```

### Card Hover with Lift
```css
.card {
  transform: translateY(0);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform var(--duration-normal) var(--ease-out),
              box-shadow var(--duration-normal) var(--ease-out);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}
```

### Link Underline Animation
```css
.link {
  position: relative;
  text-decoration: none;
}

.link::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 100%;
  height: 2px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: right;
  transition: transform var(--duration-normal) var(--ease-out);
}

.link:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}
```

### Image Zoom on Hover
```css
.image-container {
  overflow: hidden;
  border-radius: 8px;
}

.image-container img {
  transition: transform var(--duration-slow) var(--ease-out);
}

.image-container:hover img {
  transform: scale(1.05);
}
```

---

## Scroll-Based Animations

### Intersection Observer Pattern
```javascript
// Vanilla JS
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s var(--ease-out),
              transform 0.6s var(--ease-out);
}

.animate-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

### React Hook for Scroll Animation
```tsx
import { useEffect, useRef, useState } from 'react';

function useInView(options = {}) {
  const ref = useRef<HTMLElement>(null);
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    if (!ref.current) return;

    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsInView(true);
        observer.disconnect();
      }
    }, { threshold: 0.1, ...options });

    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return { ref, isInView };
}

// Usage
function Card() {
  const { ref, isInView } = useInView();

  return (
    <div
      ref={ref}
      style={{
        opacity: isInView ? 1 : 0,
        transform: isInView ? 'translateY(0)' : 'translateY(30px)',
        transition: 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)'
      }}
    >
      Card content
    </div>
  );
}
```

---

## Framer Motion (React)

### Installation
```bash
npm install framer-motion
```

### Basic Fade In Up
```tsx
import { motion } from 'framer-motion';

function Card() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      Card content
    </motion.div>
  );
}
```

### Staggered Children
```tsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] }
  }
};

function CardList({ cards }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {cards.map((card, i) => (
        <motion.div key={i} variants={itemVariants}>
          {card.content}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### Scroll-Triggered Animation
```tsx
import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

function Section() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <motion.section
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
    >
      Section content
    </motion.section>
  );
}
```

### Hover Animations
```tsx
import { motion } from 'framer-motion';

function Button() {
  return (
    <motion.button
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.15 }}
    >
      Click me
    </motion.button>
  );
}
```

---

## Performance Optimization

### Use `will-change` Sparingly
```css
/* Only add when animation is about to start */
.card:hover {
  will-change: transform;
}

/* Remove after animation */
.card {
  will-change: auto;
}
```

### Composite Layer Promotion
```css
/* Force GPU acceleration when needed */
.heavy-animation {
  transform: translateZ(0);
  /* or */
  backface-visibility: hidden;
}
```

### Reduce Layout Thrashing
```javascript
// Bad - causes layout thrashing
elements.forEach(el => {
  el.style.width = el.offsetWidth + 10 + 'px';
});

// Good - batch reads and writes
const widths = elements.map(el => el.offsetWidth);
elements.forEach((el, i) => {
  el.style.width = widths[i] + 10 + 'px';
});
```

### RequestAnimationFrame
```javascript
// Smooth scroll position updates
function smoothScroll() {
  requestAnimationFrame(() => {
    // Animation logic here
    if (shouldContinue) smoothScroll();
  });
}
```

---

## Accessibility

### Respect Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Safe Alternative Animations
```css
.card {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

@media (prefers-reduced-motion: reduce) {
  .card {
    /* Still provide feedback, but simpler */
    transition: opacity 0.15s ease;
    transform: none !important;
  }
}
```

### Framer Motion Reduced Motion
```tsx
import { motion, useReducedMotion } from 'framer-motion';

function Card() {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      initial={prefersReducedMotion ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.6 }}
    >
      Content
    </motion.div>
  );
}
```

---

## Complete Animation Examples

### Example 1: Hero Section Entry
```css
.hero {
  overflow: hidden;
}

.hero-badge,
.hero-headline,
.hero-description,
.hero-cta {
  opacity: 0;
  transform: translateY(40px);
  animation: heroReveal 0.8s var(--ease-out) forwards;
}

.hero-badge { animation-delay: 0ms; }
.hero-headline { animation-delay: 200ms; }
.hero-description { animation-delay: 400ms; }
.hero-cta { animation-delay: 600ms; }

@keyframes heroReveal {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Background animation */
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center,
    rgba(0, 255, 136, 0.1) 0%,
    transparent 70%
  );
  opacity: 0;
  animation: bgFadeIn 1.5s ease forwards 0.3s;
}

@keyframes bgFadeIn {
  to { opacity: 1; }
}
```

### Example 2: Card Grid with Stagger
```tsx
import { motion } from 'framer-motion';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.3
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 30 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: [0.16, 1, 0.3, 1]
    }
  }
};

function CardGrid({ cards }) {
  return (
    <motion.div
      className="grid grid-cols-3 gap-6"
      variants={container}
      initial="hidden"
      animate="show"
    >
      {cards.map((card) => (
        <motion.div
          key={card.id}
          variants={item}
          whileHover={{ y: -8, transition: { duration: 0.2 } }}
          className="card"
        >
          {card.content}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### Example 3: Menu Toggle
```tsx
import { motion, AnimatePresence } from 'framer-motion';

function MobileMenu({ isOpen, onClose }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Menu */}
          <motion.nav
            className="mobile-menu"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          >
            {/* Menu items with stagger */}
            <motion.ul
              initial="hidden"
              animate="visible"
              variants={{
                visible: { transition: { staggerChildren: 0.1, delayChildren: 0.2 } }
              }}
            >
              {menuItems.map((item) => (
                <motion.li
                  key={item.id}
                  variants={{
                    hidden: { opacity: 0, x: 20 },
                    visible: { opacity: 1, x: 0 }
                  }}
                >
                  {item.label}
                </motion.li>
              ))}
            </motion.ul>
          </motion.nav>
        </>
      )}
    </AnimatePresence>
  );
}
```

---

## Quick Reference

### Timing Functions
| Name | Value | Use Case |
|------|-------|----------|
| Expo Out | `cubic-bezier(0.16, 1, 0.3, 1)` | Most animations |
| Spring | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Bouncy effects |
| Smooth | `cubic-bezier(0.65, 0, 0.35, 1)` | Subtle transitions |

### Duration Guide
| Duration | Use Case |
|----------|----------|
| 100-150ms | Hover states, micro-interactions |
| 200-300ms | UI transitions, toggles |
| 400-600ms | Page reveals, large movements |
| 800-1000ms | Hero animations, dramatic effects |

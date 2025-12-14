# Transitions & Animations Guide

## Table of Contents
- [Duration Scale](#duration-scale)
- [Easing Functions](#easing-functions)
- [Common Patterns](#common-patterns)
- [Tailwind Classes](#tailwind-classes)
- [Framer Motion Patterns](#framer-motion-patterns)

---

## Duration Scale

| Duration | Use Case | Tailwind Class |
|----------|----------|----------------|
| 75ms | Micro: toggle, checkbox | `duration-75` |
| 100ms | Quick: tooltip show | `duration-100` |
| 150ms | Fast: button hover, focus | `duration-150` |
| 200ms | Standard: most interactions | `duration-200` |
| 300ms | Moderate: modal, dropdown | `duration-300` |
| 500ms | Slow: page transitions | `duration-500` |

**Rule of thumb**: Faster for small UI, slower for large changes.

---

## Easing Functions

| Easing | Use Case | Tailwind Class |
|--------|----------|----------------|
| ease-out | Entering elements | `ease-out` |
| ease-in | Exiting elements | `ease-in` |
| ease-in-out | Position changes | `ease-in-out` |
| linear | Spinners, progress | `ease-linear` |

```css
/* Custom easings in tailwind.config */
extend: {
  transitionTimingFunction: {
    'bounce-in': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
  }
}
```

---

## Common Patterns

### Hover Effects
```typescript
// Subtle scale
className="transition-transform duration-150 hover:scale-105"

// Lift with shadow
className="transition-all duration-200 hover:-translate-y-1 hover:shadow-lg"

// Background change
className="transition-colors duration-150 hover:bg-accent"

// Combined
className="transition-all duration-200 hover:bg-accent hover:shadow-md"
```

### Focus States
```typescript
// Ring focus (recommended)
className="focus-visible:outline-none focus-visible:ring-2
           focus-visible:ring-ring focus-visible:ring-offset-2"

// Border focus
className="transition-colors duration-150
           focus:border-primary focus:ring-1 focus:ring-primary"
```

### Active/Press States
```typescript
// Scale down
className="active:scale-[0.98] transition-transform duration-75"

// Darken
className="active:bg-primary/90 transition-colors duration-75"
```

### Enter/Exit Animations
```typescript
// Fade in
className="animate-in fade-in duration-200"

// Fade out
className="animate-out fade-out duration-150"

// Slide in from bottom
className="animate-in slide-in-from-bottom-4 duration-300"

// Zoom in
className="animate-in zoom-in-95 duration-200"
```

### Modal/Dialog
```typescript
// Overlay
<div className="fixed inset-0 bg-black/50
                animate-in fade-in duration-200" />

// Content
<div className="animate-in fade-in zoom-in-95
                slide-in-from-bottom-4 duration-300" />
```

### Dropdown/Popover
```typescript
// Opening
className="animate-in fade-in-0 zoom-in-95 duration-200"

// Position specific
className="data-[side=bottom]:slide-in-from-top-2
           data-[side=top]:slide-in-from-bottom-2"
```

### List Items (Staggered)
```typescript
// With Framer Motion
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: index * 0.05 }}
>
  {item}
</motion.div>
```

### Accordion/Collapse
```typescript
// Using tailwind-animate or custom
<div
  className={cn(
    "grid transition-all duration-300",
    isOpen ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
  )}
>
  <div className="overflow-hidden">
    {content}
  </div>
</div>
```

---

## Tailwind Classes Quick Reference

### Transition Properties
```css
transition-none      /* No transition */
transition-all       /* All properties */
transition-colors    /* Color properties */
transition-opacity   /* Opacity only */
transition-shadow    /* Box shadow */
transition-transform /* Transform only */
```

### Duration
```css
duration-75   /* 75ms */
duration-100  /* 100ms */
duration-150  /* 150ms */
duration-200  /* 200ms */
duration-300  /* 300ms */
duration-500  /* 500ms */
duration-700  /* 700ms */
duration-1000 /* 1000ms */
```

### Easing
```css
ease-linear    /* linear */
ease-in        /* ease-in (accelerate) */
ease-out       /* ease-out (decelerate) */
ease-in-out    /* ease-in-out (both) */
```

### Built-in Animations
```css
animate-none        /* No animation */
animate-spin        /* Continuous spin */
animate-ping        /* Pulse out */
animate-pulse       /* Fade in/out */
animate-bounce      /* Bounce up/down */
```

---

## Framer Motion Patterns

### Basic Fade
```typescript
import { motion } from "framer-motion";

<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  exit={{ opacity: 0 }}
  transition={{ duration: 0.2 }}
>
  Content
</motion.div>
```

### Slide In
```typescript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3, ease: "easeOut" }}
>
  Content
</motion.div>
```

### Scale
```typescript
<motion.div
  initial={{ opacity: 0, scale: 0.95 }}
  animate={{ opacity: 1, scale: 1 }}
  exit={{ opacity: 0, scale: 0.95 }}
  transition={{ duration: 0.2 }}
>
  Content
</motion.div>
```

### AnimatePresence for Exit
```typescript
import { AnimatePresence, motion } from "framer-motion";

<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Content
    </motion.div>
  )}
</AnimatePresence>
```

---

## Anti-Patterns

```typescript
// ❌ Too slow for small UI
className="transition-colors duration-500"

// ❌ Too fast for large changes
className="transition-all duration-75"

// ❌ Wrong easing for entry
className="animate-in ease-in"  // Should be ease-out

// ❌ No transition on interactive elements
<button className="hover:bg-accent">Click</button>

// ✅ With transition
<button className="transition-colors hover:bg-accent">Click</button>
```

---

## Performance Tips

1. **Animate only transform and opacity** - Hardware accelerated
2. **Avoid animating layout properties** - width, height, margin, padding
3. **Use `will-change` sparingly** - Only for complex animations
4. **Prefer CSS over JS** - Better performance for simple transitions
5. **Reduce motion for accessibility** - Check `prefers-reduced-motion`

```typescript
// Respect reduced motion
className="motion-safe:transition-transform motion-safe:hover:scale-105"
```

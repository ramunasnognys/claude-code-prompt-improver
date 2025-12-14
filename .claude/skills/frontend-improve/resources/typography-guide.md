# Typography Guide

Comprehensive typography guidance for distinctive frontend design.

## Table of Contents
- [Banned Fonts](#banned-fonts)
- [Recommended Fonts by Aesthetic](#recommended-fonts-by-aesthetic)
- [Font Pairing Principles](#font-pairing-principles)
- [Weight and Scale](#weight-and-scale)
- [Google Fonts Integration](#google-fonts-integration)
- [Complete Pairing Examples](#complete-pairing-examples)
- [Variable Fonts](#variable-fonts)
- [Responsive Typography](#responsive-typography)

---

## Banned Fonts

Never use these fonts - they signal generic AI output:

### System/Default Fonts
- `-apple-system`
- `BlinkMacSystemFont`
- `Segoe UI`
- `system-ui`

### Overused Sans-Serif
- **Inter** - Most common AI default
- **Roboto** - Google's generic choice
- **Open Sans** - Ubiquitous and bland
- **Lato** - Overused in templates
- **Arial** - Windows default
- **Helvetica** - When used generically

### Recently Overused by AI
- **Space Grotesk** - Becoming new local maximum
- **Poppins** - Template favorite
- **Nunito** - Overly friendly

---

## Recommended Fonts by Aesthetic

### Code/Technical Aesthetic
```css
/* Monospace display fonts */
font-family: 'JetBrains Mono', monospace;
font-family: 'Fira Code', monospace;
font-family: 'Source Code Pro', monospace;
font-family: 'IBM Plex Mono', monospace;

/* Technical sans-serif */
font-family: 'Space Grotesk', sans-serif; /* Use sparingly */
font-family: 'IBM Plex Sans', sans-serif;
font-family: 'Source Sans 3', sans-serif;
```

### Editorial/Magazine Aesthetic
```css
/* Serif display fonts */
font-family: 'Playfair Display', serif;
font-family: 'Crimson Pro', serif;
font-family: 'Newsreader', serif;
font-family: 'Instrument Serif', serif;
font-family: 'Cormorant Garamond', serif;

/* Editorial sans pairing */
font-family: 'DM Sans', sans-serif;
font-family: 'Libre Franklin', sans-serif;
```

### Distinctive/Unique Aesthetic
```css
/* Characterful display fonts */
font-family: 'Bricolage Grotesque', sans-serif;
font-family: 'Syne', sans-serif;
font-family: 'Clash Display', sans-serif;
font-family: 'Cabinet Grotesk', sans-serif;
font-family: 'Satoshi', sans-serif;

/* Unusual choices */
font-family: 'Fraunces', serif;
font-family: 'Outfit', sans-serif;
font-family: 'Plus Jakarta Sans', sans-serif;
```

### Brutalist/Raw Aesthetic
```css
/* Blunt, honest fonts */
font-family: 'Archivo Black', sans-serif;
font-family: 'Anton', sans-serif;
font-family: 'Bebas Neue', sans-serif;
font-family: 'Oswald', sans-serif;

/* Monospace for body */
font-family: 'Space Mono', monospace;
font-family: 'Courier Prime', monospace;
```

### Luxury/Refined Aesthetic
```css
/* Elegant serif fonts */
font-family: 'Cormorant', serif;
font-family: 'EB Garamond', serif;
font-family: 'Libre Baskerville', serif;

/* Refined sans-serif */
font-family: 'Jost', sans-serif;
font-family: 'Urbanist', sans-serif;
```

---

## Font Pairing Principles

### High Contrast = Interesting

The best pairings create visual tension:

1. **Display + Monospace**
   - Headlines in expressive display font
   - Body/code in clean monospace
   - Maximum contrast between purposes

2. **Serif + Geometric Sans**
   - Serif for editorial authority
   - Geometric sans for modern clarity
   - Classic pairing, always works

3. **Variable Font Across Weights**
   - Single font family
   - Extreme weight variation (200 → 900)
   - Unity with dramatic contrast

### Bad Pairings (Avoid)
- Two similar sans-serif fonts
- Two serif fonts from same era
- Fonts that compete for attention
- More than 2 font families

---

## Weight and Scale

### Extreme Weight Contrast

**Good**: 200 weight vs 900 weight
```css
h1 { font-weight: 900; }
p { font-weight: 200; }
```

**Bad**: 400 weight vs 600 weight (too subtle)
```css
/* Don't do this */
h1 { font-weight: 600; }
p { font-weight: 400; }
```

### Dramatic Size Scale

**Good**: 3x+ jumps between levels
```css
:root {
  --text-xs: 0.75rem;   /* 12px */
  --text-sm: 0.875rem;  /* 14px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.5rem;    /* 24px - 1.5x jump */
  --text-xl: 2.5rem;    /* 40px - 1.67x jump */
  --text-2xl: 4rem;     /* 64px - 1.6x jump */
  --text-3xl: 7rem;     /* 112px - 1.75x jump */
}
```

**Bad**: Timid 1.25x scale
```css
/* Don't do this - too subtle */
--text-base: 1rem;
--text-lg: 1.25rem;
--text-xl: 1.5rem;
```

### Line Height Guidelines
```css
/* Headings - tight */
h1, h2, h3 { line-height: 1.1; }

/* Body - comfortable */
p, li { line-height: 1.6; }

/* Large display text - very tight */
.hero-text { line-height: 0.95; }
```

---

## Google Fonts Integration

### Preconnect Pattern (Recommended)
```html
<head>
  <!-- Preconnect for performance -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Font request - specific weights only -->
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@200;400;800&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
</head>
```

### CSS Import (Alternative)
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;900&family=Source+Sans+3:wght@300;400&display=swap');
```

### Font Loading Optimization
```css
/* Use font-display: swap for better UX */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
}

/* Fallback stack */
body {
  font-family: 'Bricolage Grotesque', 'Segoe UI', sans-serif;
}
```

---

## Complete Pairing Examples

### Example 1: Code/Tech Landing Page
```css
:root {
  --font-display: 'Bricolage Grotesque', sans-serif;
  --font-body: 'JetBrains Mono', monospace;
}

h1 {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 5rem;
  line-height: 0.95;
  letter-spacing: -0.02em;
}

p {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 1rem;
  line-height: 1.7;
}

code {
  font-family: var(--font-body);
  font-size: 0.875em;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.2em 0.4em;
  border-radius: 4px;
}
```

### Example 2: Editorial/Magazine
```css
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Source Sans 3', sans-serif;
}

h1 {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 4rem;
  font-style: italic;
  line-height: 1.1;
}

p {
  font-family: var(--font-body);
  font-weight: 300;
  font-size: 1.125rem;
  line-height: 1.8;
}

.byline {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

### Example 3: Brutalist/Raw
```css
:root {
  --font-display: 'Archivo Black', sans-serif;
  --font-body: 'Space Mono', monospace;
}

h1 {
  font-family: var(--font-display);
  font-size: 6rem;
  text-transform: uppercase;
  line-height: 0.9;
}

p {
  font-family: var(--font-body);
  font-size: 0.875rem;
  line-height: 1.6;
  text-transform: uppercase;
}
```

---

## Variable Fonts

### Benefits
- Single file, multiple weights
- Smooth weight transitions on hover
- Smaller total file size

### Using Variable Fonts
```css
/* Google Fonts variable axis */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

/* Animate weight on hover */
.card-title {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
  transition: font-weight 0.3s ease;
}

.card:hover .card-title {
  font-weight: 700;
}
```

### Popular Variable Fonts
- Inter (if you must - but avoid!)
- Roboto Flex
- Plus Jakarta Sans
- Outfit
- Work Sans
- Fraunces

---

## Responsive Typography

### Fluid Typography with clamp()
```css
h1 {
  /* Min 2.5rem, scales with viewport, max 6rem */
  font-size: clamp(2.5rem, 5vw + 1rem, 6rem);
}

p {
  /* Min 1rem, scales slightly, max 1.25rem */
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.25rem);
}
```

### Responsive Scale System
```css
:root {
  --scale-ratio: 1.25;
  --text-base: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
}

h6 { font-size: calc(var(--text-base) * var(--scale-ratio)); }
h5 { font-size: calc(var(--text-base) * var(--scale-ratio) * var(--scale-ratio)); }
h4 { font-size: calc(var(--text-base) * pow(var(--scale-ratio), 3)); }
/* ... and so on */
```

### Breakpoint Adjustments
```css
h1 {
  font-size: 3rem;
  line-height: 1.1;
}

@media (min-width: 768px) {
  h1 {
    font-size: 5rem;
    line-height: 0.95;
  }
}

@media (min-width: 1200px) {
  h1 {
    font-size: 7rem;
    letter-spacing: -0.03em;
  }
}
```

---

## Quick Reference

### Safe Distinctive Choices
| Use Case | Font | Weight |
|----------|------|--------|
| Tech headline | Bricolage Grotesque | 800 |
| Code body | JetBrains Mono | 400 |
| Editorial headline | Playfair Display | 900 |
| Editorial body | Source Sans 3 | 300 |
| Brutalist | Archivo Black | 400 |
| Luxury | Cormorant | 300-700 |

### Google Fonts URL Builder
```
https://fonts.googleapis.com/css2?
  family=FONT_NAME:wght@WEIGHTS
  &family=FONT_NAME_2:wght@WEIGHTS
  &display=swap
```

Example:
```
https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@200;800&family=JetBrains+Mono&display=swap
```

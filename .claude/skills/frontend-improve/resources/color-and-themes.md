# Color and Themes Guide

Comprehensive color theory and theming guidance for distinctive frontend design.

## Table of Contents
- [Core Principles](#core-principles)
- [Banned Color Patterns](#banned-color-patterns)
- [CSS Variables Setup](#css-variables-setup)
- [Color Palette Strategies](#color-palette-strategies)
- [Theme Inspiration Sources](#theme-inspiration-sources)
- [Dark Mode Implementation](#dark-mode-implementation)
- [Accessibility Considerations](#accessibility-considerations)
- [Complete Theme Examples](#complete-theme-examples)

---

## Core Principles

### Dominant + Accent Model

The most effective color schemes use:
- **One dominant color** (60-70% of palette usage)
- **One or two sharp accents** (20-30% usage)
- **Neutral base** (background, text)

```
Good:  [████████████] Dominant + [██] Accent
Bad:   [████] [████] [████] Evenly distributed
```

### Commit Fully to an Aesthetic

Half-measures create generic results. Choose a direction and push it:
- Dark mode? Make it truly dark (#0a0a0f, not #1a1a1a)
- Colorful? Use saturated, vibrant colors
- Minimal? Restrict to 2-3 colors maximum

---

## Banned Color Patterns

### The Purple Gradient Trap
```css
/* DON'T - Most common AI default */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* DON'T - Variations of the same */
background: linear-gradient(to right, #6366f1, #8b5cf6);
background: linear-gradient(135deg, #7c3aed, #ec4899);
```

### Generic Blues
```css
/* DON'T - Bootstrap/generic blue */
--color-primary: #007bff;
--color-primary: #3b82f6; /* Tailwind blue-500 */
--color-primary: #2563eb; /* Tailwind blue-600 */
```

### Safe Gray Backgrounds
```css
/* DON'T - Boring and expected */
background-color: #f5f5f5;
background-color: #fafafa;
background-color: #f8f9fa;
```

---

## CSS Variables Setup

### Semantic Naming Convention
```css
:root {
  /* Base colors - rarely used directly */
  --raw-black: #0a0a0f;
  --raw-white: #fafafa;

  /* Semantic colors - use these */
  --color-bg: var(--raw-black);
  --color-bg-elevated: #12121a;
  --color-bg-subtle: #1a1a24;

  --color-text: #e8e8ed;
  --color-text-muted: #888892;
  --color-text-subtle: #555560;

  --color-primary: #00ff88;
  --color-primary-muted: rgba(0, 255, 136, 0.2);

  --color-accent: #ff3366;
  --color-accent-muted: rgba(255, 51, 102, 0.2);

  --color-border: rgba(255, 255, 255, 0.1);
  --color-border-strong: rgba(255, 255, 255, 0.2);
}
```

### Component-Level Variables
```css
.card {
  --card-bg: var(--color-bg-elevated);
  --card-border: var(--color-border);
  --card-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);

  background: var(--card-bg);
  border: 1px solid var(--card-border);
  box-shadow: var(--card-shadow);
}
```

---

## Color Palette Strategies

### Strategy 1: Monochromatic + Accent
Single hue with one contrasting accent.

```css
:root {
  /* Monochromatic base - deep blue */
  --color-bg: #0a0e17;
  --color-surface: #111827;
  --color-surface-elevated: #1f2937;

  /* Single accent - electric cyan */
  --color-accent: #06b6d4;
  --color-accent-glow: rgba(6, 182, 212, 0.3);

  /* Text hierarchy */
  --color-text: #f3f4f6;
  --color-text-muted: #9ca3af;
}
```

### Strategy 2: Complementary Contrast
Two colors from opposite sides of the color wheel.

```css
:root {
  /* Deep violet base */
  --color-bg: #0f0a1a;
  --color-primary: #8b5cf6;

  /* Complementary yellow-gold accent */
  --color-accent: #f59e0b;

  /* Creates visual tension */
}
```

### Strategy 3: Analogous Harmony
Colors adjacent on the color wheel for cohesion.

```css
:root {
  /* Warm sunset palette */
  --color-bg: #1a0a0a;
  --color-primary: #f97316;   /* Orange */
  --color-secondary: #ef4444; /* Red */
  --color-accent: #eab308;    /* Yellow */
}
```

### Strategy 4: Split-Complementary
One dominant + two flanking accents.

```css
:root {
  /* Teal dominant */
  --color-primary: #14b8a6;

  /* Split-complement accents */
  --color-accent-warm: #f97316;
  --color-accent-cool: #ec4899;
}
```

---

## Theme Inspiration Sources

### IDE Themes

#### Dracula Theme
```css
:root {
  --color-bg: #282a36;
  --color-surface: #44475a;
  --color-text: #f8f8f2;
  --color-cyan: #8be9fd;
  --color-green: #50fa7b;
  --color-orange: #ffb86c;
  --color-pink: #ff79c6;
  --color-purple: #bd93f9;
  --color-red: #ff5555;
  --color-yellow: #f1fa8c;
}
```

#### Nord Theme
```css
:root {
  /* Polar Night */
  --color-bg: #2e3440;
  --color-surface: #3b4252;
  --color-surface-elevated: #434c5e;

  /* Snow Storm */
  --color-text: #eceff4;
  --color-text-muted: #d8dee9;

  /* Frost */
  --color-frost-1: #8fbcbb;
  --color-frost-2: #88c0d0;
  --color-frost-3: #81a1c1;
  --color-frost-4: #5e81ac;

  /* Aurora */
  --color-red: #bf616a;
  --color-orange: #d08770;
  --color-yellow: #ebcb8b;
  --color-green: #a3be8c;
  --color-purple: #b48ead;
}
```

#### Tokyo Night Theme
```css
:root {
  --color-bg: #1a1b26;
  --color-surface: #24283b;
  --color-text: #c0caf5;
  --color-blue: #7aa2f7;
  --color-cyan: #7dcfff;
  --color-magenta: #bb9af7;
  --color-green: #9ece6a;
  --color-orange: #ff9e64;
  --color-red: #f7768e;
}
```

### Cultural Aesthetics

#### Japanese Minimalism
```css
:root {
  --color-bg: #faf8f5;           /* Warm off-white */
  --color-text: #1a1a1a;
  --color-accent: #c41e3a;       /* Traditional red */
  --color-secondary: #264653;    /* Deep teal */
  --color-border: rgba(0,0,0,0.08);
}
```

#### Scandinavian
```css
:root {
  --color-bg: #f5f5f0;           /* Warm gray-white */
  --color-surface: #ffffff;
  --color-text: #2d3436;
  --color-accent: #0984e3;       /* Clear blue */
  --color-wood: #d4a373;         /* Natural wood tone */
}
```

---

## Dark Mode Implementation

### CSS Custom Properties Approach
```css
/* Light mode defaults */
:root {
  --color-bg: #ffffff;
  --color-surface: #f5f5f5;
  --color-text: #1a1a1a;
  --color-text-muted: #666666;
  --color-primary: #2563eb;
  --color-border: rgba(0, 0, 0, 0.1);
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0a0a0f;
    --color-surface: #12121a;
    --color-text: #e8e8ed;
    --color-text-muted: #888892;
    --color-primary: #60a5fa;
    --color-border: rgba(255, 255, 255, 0.1);
  }
}

/* Manual toggle support */
[data-theme="dark"] {
  --color-bg: #0a0a0f;
  /* ... dark values */
}
```

### Component Adaptation
```css
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);

  /* Shadows adapt to theme */
  box-shadow: 0 4px 12px var(--shadow-color, rgba(0, 0, 0, 0.1));
}

@media (prefers-color-scheme: dark) {
  .card {
    --shadow-color: rgba(0, 0, 0, 0.4);
  }
}
```

### React/Next.js Theme Toggle
```tsx
// ThemeProvider.tsx
import { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: (theme: Theme) => void;
}>({ theme: 'system', setTheme: () => {} });

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');

  useEffect(() => {
    const root = document.documentElement;

    if (theme === 'system') {
      const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      root.setAttribute('data-theme', systemDark ? 'dark' : 'light');
    } else {
      root.setAttribute('data-theme', theme);
    }
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

---

## Accessibility Considerations

### Contrast Ratios
```css
/* WCAG AA requires 4.5:1 for normal text, 3:1 for large text */

/* Good - high contrast */
--color-text: #e8e8ed;      /* on #0a0a0f = 15.3:1 */
--color-text-muted: #888892; /* on #0a0a0f = 5.9:1 */

/* Check interactive elements */
--color-link: #60a5fa;       /* on #0a0a0f = 8.1:1 */
```

### Focus States
```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (forced-colors: active) {
  .button {
    border: 2px solid currentColor;
  }
}
```

### Color Blindness Considerations
```css
/* Don't rely on color alone */
.status-success {
  color: var(--color-green);
  /* Also add icon or text indicator */
}

.status-success::before {
  content: "✓ ";
}
```

---

## Complete Theme Examples

### Example 1: Neon Cyberpunk
```css
:root {
  /* Deep dark base */
  --color-bg: #0a0a0f;
  --color-surface: #12121a;
  --color-surface-elevated: #1a1a24;

  /* Neon accents */
  --color-primary: #00ff88;
  --color-primary-glow: rgba(0, 255, 136, 0.4);
  --color-accent: #ff3366;
  --color-accent-glow: rgba(255, 51, 102, 0.4);
  --color-cyan: #00d4ff;

  /* Text */
  --color-text: #e8e8ed;
  --color-text-muted: #888892;

  /* Effects */
  --glow-primary: 0 0 20px var(--color-primary-glow);
  --glow-accent: 0 0 20px var(--color-accent-glow);
}

.neon-text {
  color: var(--color-primary);
  text-shadow: var(--glow-primary);
}

.neon-button {
  background: transparent;
  border: 1px solid var(--color-primary);
  box-shadow: var(--glow-primary), inset var(--glow-primary);
}
```

### Example 2: Warm Editorial
```css
:root {
  /* Cream/paper base */
  --color-bg: #faf7f2;
  --color-surface: #ffffff;
  --color-surface-muted: #f5f0e8;

  /* Editorial accents */
  --color-primary: #1a1a1a;
  --color-accent: #c41e3a;
  --color-gold: #b8860b;

  /* Text */
  --color-text: #1a1a1a;
  --color-text-muted: #666666;
  --color-text-subtle: #999999;

  /* Borders */
  --color-border: rgba(0, 0, 0, 0.08);
  --color-border-strong: rgba(0, 0, 0, 0.15);
}

.editorial-headline {
  color: var(--color-text);
  border-bottom: 3px solid var(--color-accent);
}

.editorial-byline {
  color: var(--color-text-muted);
  border-left: 2px solid var(--color-gold);
  padding-left: 1rem;
}
```

### Example 3: Minimal Monochrome
```css
:root {
  /* Pure black and white */
  --color-bg: #000000;
  --color-surface: #0a0a0a;
  --color-surface-elevated: #141414;

  /* Single accent */
  --color-accent: #ffffff;

  /* Grayscale text */
  --color-text: #ffffff;
  --color-text-muted: #808080;
  --color-text-subtle: #404040;

  /* Borders */
  --color-border: rgba(255, 255, 255, 0.1);
}

.mono-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}

.mono-card:hover {
  border-color: var(--color-accent);
}
```

---

## Quick Reference

### Color Contrast Checker
- WebAIM: https://webaim.org/resources/contrastchecker/
- Contrast Ratio: https://contrast-ratio.com/

### Palette Generators
- Coolors: https://coolors.co/
- Realtime Colors: https://realtimecolors.com/
- Huemint: https://huemint.com/

### IDE Theme References
- Dracula: https://draculatheme.com/
- Nord: https://nordtheme.com/
- Tokyo Night: https://github.com/enkia/tokyo-night-vscode-theme
- Catppuccin: https://catppuccin.com/

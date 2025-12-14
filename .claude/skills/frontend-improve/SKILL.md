---
name: frontend-improve
description: Improve frontend visual design quality. Avoid generic AI aesthetics (Inter fonts, purple gradients). Creates distinctive, creative UIs with thoughtful typography, color, motion, and backgrounds. Use when building landing pages, hero sections, or any UI requiring visual polish and design quality.
---

# Frontend Design Improvement

## Purpose

Break out of "distributional convergence" - the tendency to output generic "AI slop" aesthetics. This skill provides guidance to create distinctive, memorable frontends that surprise and delight.

## The Problem

Without guidance, Claude converges to statistically common patterns:
- Inter/Roboto fonts
- Purple gradients on white backgrounds
- Minimal or no animations
- Predictable, cookie-cutter layouts

These safe choices dominate web training data but undermine brand identity and make AI-generated interfaces immediately recognizable.

---

## Core Aesthetics Directive

<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- **Backgrounds**: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>

---

## Quick Checklist

Before submitting any frontend code, verify:

### Typography
- [ ] NOT using: Inter, Roboto, Open Sans, Lato, Arial, system fonts
- [ ] Font choice is distinctive and context-appropriate
- [ ] Weight contrast is extreme (100-200 vs 800-900)
- [ ] Size jumps are dramatic (3x+, not 1.5x)
- [ ] Font loaded from Google Fonts or self-hosted

### Color & Theme
- [ ] NOT using purple gradients on white
- [ ] Dominant color with sharp accents (not evenly distributed)
- [ ] CSS variables for all colors
- [ ] Cohesive aesthetic committed to fully
- [ ] Dark mode considered if appropriate

### Motion
- [ ] Page load has staggered reveals
- [ ] Hover states are meaningful
- [ ] Animations use CSS transforms (not position/size changes)
- [ ] `prefers-reduced-motion` respected

### Backgrounds
- [ ] NOT solid white/gray
- [ ] Depth created through gradients, patterns, or effects
- [ ] Background matches overall aesthetic

---

## Design Axes

### 1. Typography
See: [resources/typography-guide.md](resources/typography-guide.md)

Key principles:
- **Banned fonts**: Inter, Roboto, Open Sans, Lato, Arial, system defaults
- **High contrast pairings**: Display + monospace, serif + geometric sans
- **Extreme weights**: 100/200 vs 800/900, never 400 vs 600
- **Dramatic scale**: Size jumps of 3x+, not 1.5x

Quick font picks by aesthetic:
| Aesthetic | Font Options |
|-----------|--------------|
| Code/Tech | JetBrains Mono, Fira Code, Space Grotesk |
| Editorial | Playfair Display, Crimson Pro, Newsreader |
| Technical | IBM Plex, Source Sans 3 |
| Distinctive | Bricolage Grotesque, Instrument Serif |

### 2. Color & Theme
See: [resources/color-and-themes.md](resources/color-and-themes.md)

Key principles:
- **Dominant + accent**: One main color, sharp contrasting accents
- **CSS variables**: `--color-primary`, `--color-accent`, etc.
- **Theme sources**: IDE themes (Dracula, Nord, Tokyo Night), cultural aesthetics

Avoid:
- Purple/violet gradients on white (most common AI default)
- Evenly distributed palettes (no hierarchy)
- Generic blue (#007bff, Bootstrap blue)

### 3. Motion
See: [resources/motion-guide.md](resources/motion-guide.md)

Key principles:
- **High-impact moments**: Focus on page load, not scattered micro-interactions
- **Staggered reveals**: Use `animation-delay` for orchestrated entrances
- **CSS-first**: `@keyframes` and `transition` before JS libraries
- **React**: Use Framer Motion when available

Performance:
- Use `transform` and `opacity` only (GPU-accelerated)
- Add `will-change` sparingly
- Respect `prefers-reduced-motion`

### 4. Backgrounds
See: [resources/backgrounds-guide.md](resources/backgrounds-guide.md)

Key principles:
- **Never solid colors**: Always add depth
- **Layered gradients**: Multiple gradient layers
- **Patterns**: Geometric SVG, noise textures, grain overlays
- **Contextual**: Match the overall aesthetic

Techniques:
- Gradient meshes
- Noise/grain overlays (SVG filter or CSS)
- Geometric patterns (CSS or SVG)
- Parallax depth layers

---

## Anti-Patterns to Avoid

See: [resources/anti-patterns.md](resources/anti-patterns.md)

### The "AI Slop" Tells
1. **Inter font** - Most common default
2. **Purple → white gradient** - Statistical mode of training data
3. **Perfectly even spacing** - No visual hierarchy
4. **Generic rounded corners** - 8px everywhere
5. **Blue call-to-action** - Bootstrap #007bff
6. **Space Grotesk** - Even this becomes a local maximum when avoiding Inter

### Self-Check Questions
- "Would a human designer make this exact choice?"
- "Does this look like every other AI-generated site?"
- "What makes this memorable?"
- "Could I remove the content and still know what brand this is?"

---

## Theme Inspiration Sources

### IDE Themes
- **Dracula** - Purple/pink accents on dark
- **Nord** - Arctic blue-gray palette
- **Tokyo Night** - Vibrant purples and blues on dark
- **One Dark** - Warm accent colors
- **Catppuccin** - Pastel color schemes

### Cultural Aesthetics
- **Japanese minimalism** - Generous whitespace, subtle colors
- **Bauhaus** - Primary colors, geometric shapes
- **Art Deco** - Gold accents, geometric patterns
- **Brutalist** - Raw, honest, no decoration
- **Y2K** - Chrome, gradients, futuristic optimism

### Design Movements
- **Swiss Design** - Grid-based, clean typography
- **Memphis** - Bold patterns, unexpected colors
- **Vaporwave** - Retro-futuristic, pastels + neon

---

## Implementation Tips

### Font Loading (Google Fonts)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@200;800&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

### CSS Variables Setup
```css
:root {
  /* Colors - Dominant + Accent */
  --color-bg: #0a0a0f;
  --color-surface: #12121a;
  --color-text: #e8e8ed;
  --color-primary: #00ff88;
  --color-accent: #ff3366;

  /* Typography */
  --font-display: 'Bricolage Grotesque', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Motion */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 150ms;
  --duration-normal: 300ms;
}
```

### Staggered Animation Pattern
```css
.card {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s var(--ease-out-expo) forwards;
}

.card:nth-child(1) { animation-delay: 0ms; }
.card:nth-child(2) { animation-delay: 100ms; }
.card:nth-child(3) { animation-delay: 200ms; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Background with Depth
```css
.hero {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0, 255, 136, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(255, 51, 102, 0.1) 0%, transparent 50%),
    linear-gradient(180deg, var(--color-bg) 0%, var(--color-surface) 100%);
}
```

---

## Related Skills

- **frontend-dev-guidelines** - React/TypeScript code patterns (complements this skill)
- **ui-ux-refinement** - User experience polish and interaction patterns

---

## Resource Files

| Topic | File | Content |
|-------|------|---------|
| Typography | [typography-guide.md](resources/typography-guide.md) | Fonts, pairings, weights, responsive |
| Color | [color-and-themes.md](resources/color-and-themes.md) | Palettes, CSS variables, dark mode |
| Motion | [motion-guide.md](resources/motion-guide.md) | Animations, Framer Motion, performance |
| Backgrounds | [backgrounds-guide.md](resources/backgrounds-guide.md) | Gradients, patterns, textures |
| Anti-patterns | [anti-patterns.md](resources/anti-patterns.md) | What to avoid, self-checks |

---

**Skill Status**: Active guardrail for frontend design quality
**Line Count**: < 500 (following 500-line rule)
**Progressive Disclosure**: Detailed guidance in resource files

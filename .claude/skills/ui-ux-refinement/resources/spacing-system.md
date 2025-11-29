# Spacing System Guide

## Table of Contents
- [Base Unit](#base-unit)
- [Spacing Scale](#spacing-scale)
- [Component Spacing](#component-spacing)
- [Layout Patterns](#layout-patterns)
- [Common Mistakes](#common-mistakes)

---

## Base Unit

Tailwind uses **4px** as base unit. All spacing should be multiples of 4.

| Tailwind | Pixels | rem |
|----------|--------|-----|
| 0 | 0px | 0 |
| 0.5 | 2px | 0.125rem |
| 1 | 4px | 0.25rem |
| 2 | 8px | 0.5rem |
| 3 | 12px | 0.75rem |
| 4 | 16px | 1rem |
| 5 | 20px | 1.25rem |
| 6 | 24px | 1.5rem |
| 8 | 32px | 2rem |
| 10 | 40px | 2.5rem |
| 12 | 48px | 3rem |
| 16 | 64px | 4rem |

---

## Spacing Scale

### Micro (0-8px)
For tight relationships
- Icon + label: `gap-1` (4px)
- Badge padding: `px-2` (8px)
- Input icon spacing: `gap-2` (8px)

### Small (8-16px)
For related items
- Form field groups: `space-y-2` (8px)
- Button group gaps: `gap-2` (8px)
- List item padding: `p-3` (12px)

### Medium (16-24px)
For sections within components
- Card padding: `p-4` (16px)
- Section spacing: `space-y-4` (16px)
- Modal padding: `p-6` (24px)

### Large (24-48px)
For major sections
- Page section gaps: `space-y-6` (24px)
- Between cards: `gap-4` to `gap-6`
- Page margins: `p-6` to `p-8`

### XL (48px+)
For page-level separation
- Hero sections: `py-12` to `py-24`
- Footer spacing: `mt-12`

---

## Component Spacing

### Buttons
```typescript
// Small
className="px-2 py-1 text-sm"

// Default
className="px-4 py-2"

// Large
className="px-6 py-3 text-lg"

// Icon only
className="p-2"  // Square
```

### Cards
```typescript
// Compact
<Card className="p-3">

// Default
<Card className="p-4">

// Spacious
<Card className="p-6">

// Header/Content separation
<CardHeader className="pb-2">
<CardContent className="pt-0">
```

### Forms
```typescript
// Label + input
<div className="space-y-2">
  <Label>Email</Label>
  <Input />
</div>

// Between form fields
<div className="space-y-4">
  <Field />
  <Field />
</div>

// Form sections
<div className="space-y-6">
  <Section />
  <Section />
</div>
```

### Lists
```typescript
// Tight list
<ul className="space-y-1">

// Standard list
<ul className="space-y-2">

// Card list
<div className="space-y-4">
```

### Modals/Dialogs
```typescript
<DialogContent className="p-6">
  <DialogHeader className="pb-4">
    <DialogTitle>Title</DialogTitle>
    <DialogDescription>Description</DialogDescription>
  </DialogHeader>

  <div className="space-y-4">
    {/* Content */}
  </div>

  <DialogFooter className="pt-4">
    <Button>Action</Button>
  </DialogFooter>
</DialogContent>
```

---

## Layout Patterns

### Page Layout
```typescript
// Standard page
<div className="container mx-auto px-4 py-6">
  <header className="mb-6">
    <h1>Page Title</h1>
  </header>

  <main className="space-y-6">
    <Section />
    <Section />
  </main>
</div>
```

### Grid Layouts
```typescript
// Card grid
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
  <Card />
  <Card />
  <Card />
</div>

// Dashboard grid
<div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
  <StatCard />
  <StatCard />
  <StatCard />
  <StatCard />
</div>
```

### Sidebar Layout
```typescript
<div className="flex gap-6">
  <aside className="w-64 space-y-4">
    <Nav />
  </aside>
  <main className="flex-1 space-y-6">
    <Content />
  </main>
</div>
```

### Stack with Dividers
```typescript
<div className="divide-y">
  <div className="py-4">Item 1</div>
  <div className="py-4">Item 2</div>
  <div className="py-4">Item 3</div>
</div>
```

---

## Responsive Spacing

```typescript
// Increase spacing on larger screens
className="p-4 md:p-6 lg:p-8"

// Gap adjustments
className="gap-4 md:gap-6"

// Margin adjustments
className="mt-6 md:mt-8 lg:mt-12"
```

---

## Common Mistakes

### Inconsistent Padding
```typescript
// ❌ Different padding in similar cards
<Card className="p-4">
<Card className="p-6">  // Why different?

// ✅ Consistent
<Card className="p-4">
<Card className="p-4">
```

### Breaking the Scale
```typescript
// ❌ Arbitrary values
className="p-[17px] gap-[11px]"

// ✅ Use scale values
className="p-4 gap-3"
```

### Tight Related, Loose Unrelated
```typescript
// ❌ Same spacing everywhere
<div className="space-y-4">
  <Label>Email</Label>      {/* Too far from input */}
  <Input />
  <Label>Password</Label>   {/* Too far from input */}
  <Input />
</div>

// ✅ Tight for related, loose for groups
<div className="space-y-4">        {/* Between groups */}
  <div className="space-y-2">      {/* Within group */}
    <Label>Email</Label>
    <Input />
  </div>
  <div className="space-y-2">
    <Label>Password</Label>
    <Input />
  </div>
</div>
```

### Missing Horizontal Consistency
```typescript
// ❌ Horizontal padding mismatch
<Card>
  <CardHeader className="px-4">
  <CardContent className="px-6">  // Misaligned!
</Card>

// ✅ Consistent horizontal padding
<Card>
  <CardHeader className="px-4">
  <CardContent className="px-4">
</Card>
```

---

## Quick Reference

| Element | Spacing | Class |
|---------|---------|-------|
| Icon + text | 4px | `gap-1` |
| Label + input | 8px | `space-y-2` |
| Form fields | 16px | `space-y-4` |
| Card padding | 16px | `p-4` |
| Section gap | 24px | `space-y-6` |
| Page padding | 16-24px | `p-4` / `p-6` |
| Page sections | 24-32px | `space-y-6` / `space-y-8` |

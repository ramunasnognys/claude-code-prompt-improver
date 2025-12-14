# Interactive States Guide

## Table of Contents
- [Required States](#required-states)
- [Button States](#button-states)
- [Input States](#input-states)
- [Link States](#link-states)
- [Touch Targets](#touch-targets)
- [Keyboard Navigation](#keyboard-navigation)

---

## Required States

Every interactive element needs:

| State | Trigger | Purpose |
|-------|---------|---------|
| Default | None | Base appearance |
| Hover | Mouse over | Indicates clickable |
| Focus | Tab/click | Keyboard accessibility |
| Active | Click/tap | Feedback on press |
| Disabled | prop | Shows unavailable |
| Loading | prop | Shows in-progress |

---

## Button States

### Complete Button Pattern
```typescript
<Button
  disabled={isDisabled || isPending}
  className={cn(
    // Base
    "relative inline-flex items-center justify-center",
    "px-4 py-2 rounded-md font-medium text-sm",
    "transition-all duration-200",

    // Hover
    "hover:bg-primary/90 hover:shadow-md",

    // Focus
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring focus-visible:ring-offset-2",

    // Active
    "active:scale-[0.98]",

    // Disabled
    "disabled:opacity-50 disabled:cursor-not-allowed",
    "disabled:hover:bg-primary disabled:hover:shadow-none",
  )}
>
  {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  {children}
</Button>
```

### Button Variants
```typescript
// Primary (filled)
"bg-primary text-primary-foreground hover:bg-primary/90"

// Secondary (muted)
"bg-secondary text-secondary-foreground hover:bg-secondary/80"

// Outline
"border border-input bg-background hover:bg-accent hover:text-accent-foreground"

// Ghost
"hover:bg-accent hover:text-accent-foreground"

// Destructive
"bg-destructive text-destructive-foreground hover:bg-destructive/90"

// Link
"text-primary underline-offset-4 hover:underline"
```

### Icon Button
```typescript
<button
  className={cn(
    "p-2 rounded-md",
    "transition-colors duration-150",
    "hover:bg-accent",
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring",
    "disabled:opacity-50 disabled:cursor-not-allowed"
  )}
  aria-label="Close"
>
  <X className="h-4 w-4" />
</button>
```

---

## Input States

### Text Input
```typescript
<Input
  className={cn(
    // Base
    "flex h-10 w-full rounded-md border border-input",
    "bg-background px-3 py-2 text-sm",
    "transition-colors duration-150",

    // Placeholder
    "placeholder:text-muted-foreground",

    // Focus
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring",

    // Disabled
    "disabled:cursor-not-allowed disabled:opacity-50",

    // Error (conditional)
    hasError && "border-destructive focus-visible:ring-destructive"
  )}
/>
```

### Checkbox
```typescript
<Checkbox
  className={cn(
    "h-4 w-4 rounded border border-primary",
    "transition-colors duration-150",

    // Checked
    "data-[state=checked]:bg-primary",
    "data-[state=checked]:text-primary-foreground",

    // Focus
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring focus-visible:ring-offset-2",

    // Disabled
    "disabled:cursor-not-allowed disabled:opacity-50"
  )}
/>
```

### Select/Dropdown
```typescript
<Select>
  <SelectTrigger
    className={cn(
      "flex h-10 w-full items-center justify-between",
      "rounded-md border border-input bg-background",
      "px-3 py-2 text-sm",
      "transition-colors duration-150",

      // Hover
      "hover:border-ring",

      // Focus
      "focus:outline-none focus:ring-2 focus:ring-ring",

      // Disabled
      "disabled:cursor-not-allowed disabled:opacity-50"
    )}
  >
    <SelectValue />
  </SelectTrigger>
</Select>
```

### Switch/Toggle
```typescript
<Switch
  className={cn(
    "peer inline-flex h-6 w-11 shrink-0 cursor-pointer",
    "items-center rounded-full border-2 border-transparent",
    "transition-colors duration-200",

    // Unchecked
    "bg-input",

    // Checked
    "data-[state=checked]:bg-primary",

    // Focus
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring focus-visible:ring-offset-2",

    // Disabled
    "disabled:cursor-not-allowed disabled:opacity-50"
  )}
/>
```

---

## Link States

### Text Link
```typescript
<a
  href={href}
  className={cn(
    "text-primary underline-offset-4",
    "transition-colors duration-150",

    // Hover
    "hover:underline hover:text-primary/80",

    // Focus
    "focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring focus-visible:rounded-sm"
  )}
>
  {children}
</a>
```

### Card as Link
```typescript
<a href={href} className="group block">
  <Card
    className={cn(
      "transition-all duration-200",

      // Hover
      "group-hover:border-primary/50 group-hover:shadow-md",

      // Focus
      "group-focus-visible:ring-2 group-focus-visible:ring-ring"
    )}
  >
    <CardContent>...</CardContent>
  </Card>
</a>
```

### Nav Link
```typescript
<NavLink
  className={({ isActive }) =>
    cn(
      "px-3 py-2 rounded-md text-sm font-medium",
      "transition-colors duration-150",

      isActive
        ? "bg-primary text-primary-foreground"
        : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
    )
  }
>
  {label}
</NavLink>
```

---

## Touch Targets

### Minimum Sizes
- **Minimum**: 44x44px (Apple HIG / WCAG)
- **Recommended**: 48x48px (Material Design)

```typescript
// ❌ Too small
<button className="p-1">
  <Icon className="h-4 w-4" />  {/* ~24px total */}
</button>

// ✅ Adequate touch target
<button className="p-3">
  <Icon className="h-4 w-4" />  {/* 44px total */}
</button>

// ✅ Or use min-w/min-h
<button className="min-w-[44px] min-h-[44px] p-2">
  <Icon className="h-5 w-5" />
</button>
```

### Spacing Between Targets
```typescript
// ❌ Too close
<div className="flex gap-1">
  <IconButton />
  <IconButton />
</div>

// ✅ Adequate spacing
<div className="flex gap-2">
  <IconButton />
  <IconButton />
</div>
```

---

## Keyboard Navigation

### Focus Visible
```typescript
// Use focus-visible instead of focus
// Only shows for keyboard navigation

// ❌ Shows on click too
"focus:ring-2 focus:ring-ring"

// ✅ Only keyboard
"focus-visible:ring-2 focus-visible:ring-ring"
```

### Skip Link
```typescript
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute
             focus:top-4 focus:left-4 focus:z-50
             focus:px-4 focus:py-2 focus:bg-background
             focus:ring-2 focus:ring-ring"
>
  Skip to main content
</a>
```

### Focus Trap (Modals)
```typescript
// Use Radix/shadcn Dialog - handles focus trap automatically
<Dialog>
  <DialogContent>
    {/* Focus is trapped here while open */}
  </DialogContent>
</Dialog>
```

### Arrow Key Navigation
```typescript
// For custom components like tabs, menus
// Radix handles this automatically

<Tabs>
  <TabsList>
    <TabsTrigger value="a">A</TabsTrigger>  {/* Arrow keys work */}
    <TabsTrigger value="b">B</TabsTrigger>
    <TabsTrigger value="c">C</TabsTrigger>
  </TabsList>
</Tabs>
```

---

## Anti-Patterns

```typescript
// ❌ No hover state
<button className="bg-primary">Click</button>

// ❌ No focus indicator (accessibility fail)
<button className="focus:outline-none">Click</button>

// ❌ Hover on disabled
<button disabled className="hover:bg-primary/90">
  {/* Hover effect still shows when disabled */}
</button>

// ✅ Disable hover when disabled
<button
  disabled
  className="hover:bg-primary/90 disabled:hover:bg-primary"
>
```

---

## State Checklist

For each interactive element, verify:

- [ ] Hover state visible
- [ ] Focus ring visible (keyboard nav)
- [ ] Active/pressed state
- [ ] Disabled state (if applicable)
- [ ] Loading state (if applicable)
- [ ] Touch target >= 44px
- [ ] Cursor changes appropriately
- [ ] Color contrast sufficient

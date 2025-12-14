# Visual Hierarchy Guide

## Table of Contents
- [Typography Scale](#typography-scale)
- [Color Hierarchy](#color-hierarchy)
- [Focal Points](#focal-points)
- [Layout Hierarchy](#layout-hierarchy)
- [Common Patterns](#common-patterns)

---

## Typography Scale

### Tailwind Default Scale
| Class | Size | Use Case |
|-------|------|----------|
| `text-xs` | 12px | Labels, captions, fine print |
| `text-sm` | 14px | Secondary text, descriptions |
| `text-base` | 16px | Body text, default |
| `text-lg` | 18px | Lead paragraphs, emphasis |
| `text-xl` | 20px | Section headings |
| `text-2xl` | 24px | Card titles, H3 |
| `text-3xl` | 30px | Page sections, H2 |
| `text-4xl` | 36px | Page titles, H1 |

### Font Weights
```typescript
// Hierarchy through weight
font-normal   // 400 - Body text
font-medium   // 500 - Slight emphasis
font-semibold // 600 - Headings, labels
font-bold     // 700 - Strong emphasis
```

### Text Colors for Hierarchy
```typescript
// Primary content
"text-foreground"

// Secondary content
"text-muted-foreground"

// Disabled/placeholder
"text-muted-foreground/50"

// Accent/emphasis
"text-primary"
```

### Typography Patterns
```typescript
// Page header
<div className="space-y-1">
  <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
  <p className="text-muted-foreground">Welcome back, here's your overview.</p>
</div>

// Section header
<div className="space-y-1">
  <h2 className="text-xl font-semibold">Recent Activity</h2>
  <p className="text-sm text-muted-foreground">Last 7 days</p>
</div>

// Card content
<div>
  <h3 className="font-medium">Project Name</h3>
  <p className="text-sm text-muted-foreground">Updated 2 hours ago</p>
</div>
```

---

## Color Hierarchy

### shadcn/ui Color System
```typescript
// Background layers (light to dark)
"bg-background"      // Base page
"bg-muted"           // Elevated/grouped sections
"bg-card"            // Cards
"bg-accent"          // Hover states

// Text hierarchy
"text-foreground"         // Primary text
"text-muted-foreground"   // Secondary text
"text-primary"            // Links, emphasis

// Semantic colors
"text-destructive"   // Errors, destructive actions
"bg-destructive"     // Destructive buttons
```

### Creating Emphasis
```typescript
// ❌ Same visual weight everywhere
<Card>
  <p className="text-foreground">Primary info</p>
  <p className="text-foreground">Secondary info</p>
  <p className="text-foreground">Tertiary info</p>
</Card>

// ✅ Clear hierarchy
<Card>
  <p className="font-medium">Primary info</p>
  <p className="text-muted-foreground">Secondary info</p>
  <p className="text-sm text-muted-foreground">Tertiary info</p>
</Card>
```

### Color as Status
```typescript
// Success
"text-green-600 dark:text-green-400"
"bg-green-100 dark:bg-green-900/30"

// Warning
"text-yellow-600 dark:text-yellow-400"
"bg-yellow-100 dark:bg-yellow-900/30"

// Error
"text-destructive"
"bg-destructive/10"

// Info
"text-blue-600 dark:text-blue-400"
"bg-blue-100 dark:bg-blue-900/30"
```

---

## Focal Points

### One Primary Action per View
```typescript
// ❌ Competing focal points
<div className="flex gap-2">
  <Button>Save</Button>
  <Button>Preview</Button>
  <Button>Export</Button>
  <Button>Share</Button>
</div>

// ✅ Clear primary action
<div className="flex gap-2">
  <Button>Save Changes</Button>
  <Button variant="outline">Preview</Button>
  <Button variant="ghost">Export</Button>
</div>
```

### Visual Weight
Elements draw attention through:
1. **Size** - Larger = more important
2. **Color** - Saturated = more attention
3. **Contrast** - Higher = more prominent
4. **Position** - Top-left reads first (LTR)
5. **White space** - More space = more emphasis

```typescript
// Hero section with clear focal point
<section className="py-24 text-center space-y-6">
  {/* Largest, most attention */}
  <h1 className="text-4xl font-bold">Build faster</h1>

  {/* Secondary, supporting */}
  <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
    The modern development experience you deserve.
  </p>

  {/* Primary action - saturated color */}
  <Button size="lg">Get Started</Button>
</section>
```

### Z-Pattern and F-Pattern
```typescript
// F-Pattern for text-heavy pages
<article className="space-y-6">
  <h1 className="text-3xl font-bold">Title</h1>  {/* Eye starts here */}
  <p className="text-lg">Lead paragraph...</p>    {/* Scans right */}
  <h2 className="text-xl font-semibold">Section</h2>  {/* Back to left */}
  <p>Body text...</p>  {/* Scans right again */}
</article>

// Z-Pattern for landing pages
<section className="grid grid-cols-2 gap-8 items-center">
  <div>Logo</div>           {/* Top left */}
  <nav>Navigation</nav>      {/* Top right */}
  <div>Hero content</div>    {/* Bottom left */}
  <div>CTA Button</div>      {/* Bottom right */}
</section>
```

---

## Layout Hierarchy

### Card Hierarchy
```typescript
// Important card (elevated)
<Card className="border-2 shadow-lg">
  <CardContent className="p-6">
    Primary content
  </CardContent>
</Card>

// Standard card
<Card>
  <CardContent className="p-4">
    Regular content
  </CardContent>
</Card>

// Subtle card
<Card className="border-dashed bg-muted/50">
  <CardContent className="p-4">
    Secondary content
  </CardContent>
</Card>
```

### List Item Hierarchy
```typescript
<div className="flex items-center gap-4">
  {/* Visual indicator */}
  <Avatar className="h-10 w-10">
    <AvatarImage src={user.avatar} />
    <AvatarFallback>{user.initials}</AvatarFallback>
  </Avatar>

  {/* Text hierarchy */}
  <div className="flex-1 min-w-0">
    <p className="font-medium truncate">{user.name}</p>
    <p className="text-sm text-muted-foreground truncate">{user.email}</p>
  </div>

  {/* Secondary action */}
  <Button variant="ghost" size="sm">View</Button>
</div>
```

### Table Hierarchy
```typescript
<Table>
  <TableHeader>
    <TableRow>
      {/* Headers = smaller, muted, uppercase */}
      <TableHead className="text-xs font-medium text-muted-foreground uppercase tracking-wider">
        Name
      </TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    <TableRow>
      {/* Primary column = normal weight */}
      <TableCell className="font-medium">{item.name}</TableCell>
      {/* Secondary columns = muted */}
      <TableCell className="text-muted-foreground">{item.date}</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

---

## Common Patterns

### Stats/Metrics
```typescript
<div className="space-y-1">
  <p className="text-sm text-muted-foreground">Total Revenue</p>
  <p className="text-3xl font-bold">$45,231.89</p>
  <p className="text-sm text-green-600">+20.1% from last month</p>
</div>
```

### Form Labels
```typescript
<div className="space-y-2">
  <Label className="text-sm font-medium">
    Email address
    <span className="text-destructive ml-1">*</span>
  </Label>
  <Input />
  <p className="text-xs text-muted-foreground">
    We'll never share your email.
  </p>
</div>
```

### Empty State
```typescript
<div className="text-center py-12 space-y-4">
  <Icon className="h-12 w-12 mx-auto text-muted-foreground" />
  <div className="space-y-1">
    <h3 className="text-lg font-medium">No items yet</h3>
    <p className="text-sm text-muted-foreground">
      Get started by creating your first item.
    </p>
  </div>
  <Button>Create Item</Button>
</div>
```

### Navigation
```typescript
// Active vs inactive
<nav className="flex gap-4">
  <a className="text-foreground font-medium">Active</a>
  <a className="text-muted-foreground hover:text-foreground">Inactive</a>
</nav>
```

---

## Anti-Patterns

```typescript
// ❌ Everything same size/weight
<div>
  <p>Title</p>
  <p>Description</p>
  <p>Metadata</p>
</div>

// ❌ Too many font sizes
<div>
  <p className="text-3xl">Title</p>
  <p className="text-lg">Subtitle</p>
  <p className="text-base">Description</p>
  <p className="text-sm">Details</p>
  <p className="text-xs">Fine print</p>
  <p className="text-[11px]">Even smaller</p>  // Too many levels!
</div>

// ❌ Color without meaning
<p className="text-blue-500">Regular text in blue</p>
<p className="text-green-500">Another regular text</p>

// ✅ Color with semantic meaning
<p className="text-green-600">Success: Saved!</p>
<p className="text-destructive">Error: Failed to save</p>
```

---

## Hierarchy Checklist

- [ ] Page has clear H1
- [ ] Only one primary CTA
- [ ] Text uses max 3-4 size levels
- [ ] Secondary content is muted
- [ ] Important items have more visual weight
- [ ] Consistent heading hierarchy (H1 > H2 > H3)
- [ ] Color used semantically (status, emphasis)

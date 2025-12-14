# Loading States Guide

## Table of Contents
- [When to Use What](#when-to-use-what)
- [Skeleton Patterns](#skeleton-patterns)
- [Spinner Patterns](#spinner-patterns)
- [Progress Indicators](#progress-indicators)
- [Optimistic Updates](#optimistic-updates)

---

## When to Use What

| Scenario | Use | Example |
|----------|-----|---------|
| Content loading | Skeleton | Page load, list items |
| User action | Spinner | Button click, form submit |
| Long operation | Progress bar | File upload, data export |
| Quick update | Optimistic | Toggle, like button |

---

## Skeleton Patterns

### Basic Skeleton
```typescript
import { Skeleton } from "@/components/ui/skeleton";

// Text lines
<div className="space-y-2">
  <Skeleton className="h-4 w-[250px]" />
  <Skeleton className="h-4 w-[200px]" />
</div>

// Avatar + text
<div className="flex items-center space-x-4">
  <Skeleton className="h-12 w-12 rounded-full" />
  <div className="space-y-2">
    <Skeleton className="h-4 w-[150px]" />
    <Skeleton className="h-4 w-[100px]" />
  </div>
</div>
```

### Card Skeleton
```typescript
function CardSkeleton() {
  return (
    <Card>
      <CardHeader className="pb-2">
        <Skeleton className="h-5 w-1/2" />
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-4/5" />
          <Skeleton className="h-4 w-3/5" />
        </div>
      </CardContent>
    </Card>
  );
}
```

### Table Skeleton
```typescript
function TableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex gap-4 py-2 border-b">
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/4" />
      </div>
      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4 py-2">
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-4 w-1/4" />
          <Skeleton className="h-4 w-1/4" />
        </div>
      ))}
    </div>
  );
}
```

### Match Content Shape
```typescript
// ❌ Generic rectangles
<Skeleton className="h-20 w-full" />

// ✅ Match actual content structure
<div className="flex gap-4">
  <Skeleton className="h-16 w-16 rounded-lg" />  {/* Image */}
  <div className="flex-1 space-y-2">
    <Skeleton className="h-5 w-3/4" />  {/* Title */}
    <Skeleton className="h-4 w-1/2" />  {/* Subtitle */}
  </div>
</div>
```

---

## Spinner Patterns

### Button with Spinner
```typescript
import { Loader2 } from "lucide-react";

<Button disabled={isPending}>
  {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  {isPending ? 'Saving...' : 'Save'}
</Button>
```

### Inline Spinner
```typescript
<span className="inline-flex items-center gap-2 text-sm text-muted-foreground">
  <Loader2 className="h-3 w-3 animate-spin" />
  Loading...
</span>
```

### Full Page Spinner
```typescript
function PageLoader() {
  return (
    <div className="flex items-center justify-center min-h-[400px]">
      <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
    </div>
  );
}
```

### Overlay Spinner
```typescript
function LoadingOverlay({ show }: { show: boolean }) {
  if (!show) return null;

  return (
    <div className="absolute inset-0 bg-background/80 backdrop-blur-sm
                    flex items-center justify-center z-50">
      <Loader2 className="h-8 w-8 animate-spin" />
    </div>
  );
}

// Usage with relative container
<div className="relative">
  <Card>...</Card>
  <LoadingOverlay show={isLoading} />
</div>
```

---

## Progress Indicators

### Progress Bar
```typescript
import { Progress } from "@/components/ui/progress";

<div className="space-y-2">
  <div className="flex justify-between text-sm">
    <span>Uploading...</span>
    <span>{progress}%</span>
  </div>
  <Progress value={progress} />
</div>
```

### Step Progress
```typescript
function StepProgress({ current, total }: { current: number; total: number }) {
  return (
    <div className="flex gap-2">
      {Array.from({ length: total }).map((_, i) => (
        <div
          key={i}
          className={cn(
            "h-2 flex-1 rounded-full transition-colors",
            i < current ? "bg-primary" : "bg-muted"
          )}
        />
      ))}
    </div>
  );
}
```

---

## Optimistic Updates

### Toggle Example
```typescript
const [isEnabled, setIsEnabled] = useState(initialValue);
const [isPending, startTransition] = useTransition();

function handleToggle() {
  // Optimistically update UI
  setIsEnabled(!isEnabled);

  startTransition(async () => {
    try {
      await updateSetting(!isEnabled);
    } catch {
      // Revert on error
      setIsEnabled(isEnabled);
      toast.error("Failed to update");
    }
  });
}

return (
  <Switch
    checked={isEnabled}
    onCheckedChange={handleToggle}
    disabled={isPending}
  />
);
```

---

## Anti-Patterns

```typescript
// ❌ No loading indication
if (isLoading) return null;

// ❌ Layout shift on load
if (isLoading) return <Spinner />;
return <Content />;

// ✅ Consistent layout with skeleton
if (isLoading) return <ContentSkeleton />;
return <Content />;

// ✅ Or use Suspense
<Suspense fallback={<ContentSkeleton />}>
  <Content />
</Suspense>
```

---

## Duration Guidelines

| Content Type | Threshold | Action |
|-------------|-----------|--------|
| Immediate | <100ms | No indicator |
| Short | 100-300ms | Skeleton/spinner |
| Medium | 300ms-3s | Progress or detailed skeleton |
| Long | >3s | Progress bar + estimation |

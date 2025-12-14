# Empty States Guide

## Table of Contents
- [Anatomy of Empty State](#anatomy-of-empty-state)
- [Types of Empty States](#types-of-empty-states)
- [Component Patterns](#component-patterns)
- [Copy Guidelines](#copy-guidelines)

---

## Anatomy of Empty State

Every empty state should have:

1. **Visual** - Icon or illustration
2. **Headline** - What's empty
3. **Description** - Why it's empty + what to do
4. **Action** - Primary way to resolve (optional but recommended)

```typescript
<div className="flex flex-col items-center justify-center py-12 text-center">
  {/* Visual */}
  <Inbox className="h-12 w-12 text-muted-foreground mb-4" />

  {/* Headline */}
  <h3 className="text-lg font-medium mb-1">No messages yet</h3>

  {/* Description */}
  <p className="text-sm text-muted-foreground mb-4 max-w-sm">
    When you receive messages, they'll appear here.
  </p>

  {/* Action */}
  <Button>Compose Message</Button>
</div>
```

---

## Types of Empty States

### First Use / No Data Yet
User hasn't created anything yet.

```typescript
function FirstUseEmpty() {
  return (
    <EmptyState
      icon={<Sparkles className="h-12 w-12" />}
      title="Get started with projects"
      description="Create your first project to organize your work."
      action={<Button>Create Project</Button>}
    />
  );
}
```

### No Results
Search or filter returned nothing.

```typescript
function NoResultsEmpty({ query }: { query: string }) {
  return (
    <EmptyState
      icon={<Search className="h-12 w-12" />}
      title={`No results for "${query}"`}
      description="Try adjusting your search or filters."
      action={
        <Button variant="outline" onClick={clearFilters}>
          Clear Filters
        </Button>
      }
    />
  );
}
```

### Cleared / Completed
All items processed or deleted.

```typescript
function AllDoneEmpty() {
  return (
    <EmptyState
      icon={<CheckCircle className="h-12 w-12 text-green-500" />}
      title="All caught up!"
      description="You've completed all your tasks."
    />
  );
}
```

### Error State
Failed to load content.

```typescript
function ErrorEmpty({ onRetry }: { onRetry: () => void }) {
  return (
    <EmptyState
      icon={<AlertCircle className="h-12 w-12 text-destructive" />}
      title="Unable to load"
      description="Something went wrong. Please try again."
      action={
        <Button variant="outline" onClick={onRetry}>
          <RefreshCw className="mr-2 h-4 w-4" />
          Retry
        </Button>
      }
    />
  );
}
```

### Permission Denied
User lacks access.

```typescript
function NoAccessEmpty() {
  return (
    <EmptyState
      icon={<Lock className="h-12 w-12" />}
      title="Access restricted"
      description="You don't have permission to view this content."
      action={<Button variant="outline">Request Access</Button>}
    />
  );
}
```

---

## Component Patterns

### Reusable Empty State Component
```typescript
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
  className?: string;
}

function EmptyState({
  icon,
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center py-12 px-4 text-center",
        className
      )}
    >
      {icon && (
        <div className="mb-4 text-muted-foreground">{icon}</div>
      )}
      <h3 className="text-lg font-medium mb-1">{title}</h3>
      {description && (
        <p className="text-sm text-muted-foreground mb-4 max-w-sm">
          {description}
        </p>
      )}
      {action && <div>{action}</div>}
    </div>
  );
}
```

### Table Empty State
```typescript
function TableEmptyRow({ colSpan }: { colSpan: number }) {
  return (
    <TableRow>
      <TableCell colSpan={colSpan} className="h-24 text-center">
        <div className="flex flex-col items-center justify-center py-4">
          <FileX className="h-8 w-8 text-muted-foreground mb-2" />
          <p className="text-sm text-muted-foreground">No data found</p>
        </div>
      </TableCell>
    </TableRow>
  );
}
```

### Card Empty State
```typescript
function CardEmpty() {
  return (
    <Card className="border-dashed">
      <CardContent className="flex flex-col items-center justify-center py-8">
        <Plus className="h-8 w-8 text-muted-foreground mb-2" />
        <p className="text-sm text-muted-foreground">Add your first item</p>
      </CardContent>
    </Card>
  );
}
```

### Inline Empty (Small Spaces)
```typescript
function InlineEmpty() {
  return (
    <p className="text-sm text-muted-foreground py-4 text-center">
      No items to display
    </p>
  );
}
```

---

## Copy Guidelines

### Headlines
- Keep short (3-5 words)
- Be specific about what's empty
- Use sentence case

```
✅ "No projects yet"
✅ "No results found"
✅ "All tasks completed"

❌ "Nothing Here"
❌ "EMPTY"
❌ "There Are No Items In This List"
```

### Descriptions
- Explain why or what to do next
- Keep under 100 characters
- Don't blame the user

```
✅ "Create your first project to get started."
✅ "Try adjusting your search terms."

❌ "You haven't created any projects."
❌ "Your search didn't match anything because you typed wrong."
```

### Action Labels
- Start with verb
- Be specific

```
✅ "Create Project"
✅ "Upload File"
✅ "Invite Team"

❌ "Get Started"
❌ "Click Here"
❌ "Go"
```

---

## Icon Suggestions

| State | Icons |
|-------|-------|
| No data | `Inbox`, `FolderOpen`, `FileText` |
| No results | `Search`, `Filter`, `SearchX` |
| All done | `CheckCircle`, `PartyPopper`, `Sparkles` |
| Error | `AlertCircle`, `XCircle`, `AlertTriangle` |
| No access | `Lock`, `ShieldX`, `Ban` |
| Add new | `Plus`, `PlusCircle`, `FilePlus` |

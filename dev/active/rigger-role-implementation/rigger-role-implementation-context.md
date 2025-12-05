# Rigger Role Implementation - Context

**Last Updated**: 2025-12-05 (Plan Review Complete)
**Status**: PLAN REVIEWED - Critical fixes identified before Phase 1
**Branch**: `main` (rigger-jobs submodule)

## Project Overview

Adding role-based access control to rigger-jobs app with QR code rigger onboarding. Riggers get mobile-first interface for their assigned jobs only.

## Plan Review Summary (2025-12-05)

**Verdict**: Plan architecturally sound but has 4 critical issues to fix first.

### Critical Issues (Must Fix Before Phase 1)

| Issue | Problem | Fix |
|-------|---------|-----|
| Role Sync Gap | Convex `users.role` vs Clerk `publicMetadata` will drift | Read role from JWT claims only, sync to Convex as cache |
| JWT Config | No verification step, `sessionClaims?.metadata?.role` = undefined | Add Phase 1 test to log `ctx.auth.getUserIdentity()` |
| User Migration | ~50+ existing users have no role | Backfill script + default fallback to "office" |
| Schema Mismatch | Plan mentions `jobAssignments` table but codebase uses team-based | Stick with team-based model (`job.assignedTeamId`) |

### Missing Considerations (Should Fix)

| Gap | Fix |
|-----|-----|
| Photo upload permissions | Add rigger team check to `addPhotosToJob` |
| Team deletion with riggers | Block deletion if riggers assigned |
| Expired QR handling | Add error UI for expired/used tokens |
| Team reassignment mid-work | Show "team changed" banner |
| Rate limiting invites | 10 invites/hour/user |
| Token security | Hash tokens before storage |

### Key Code Fixes Required

**1. Auth helper (read from JWT, not DB)**:
```typescript
// convex/lib/auth.ts
export async function getUserRole(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();
  const role = (identity as any)?.metadata?.role;
  return role ?? "office"; // Safe default
}
```

**2. Update users.store (sync role)**:
```typescript
const role = (identity as any)?.metadata?.role ?? "office";
await ctx.db.patch(user._id, { ...existing, role });
```

**3. Photo upload protection**:
```typescript
if (role === "rigger" && job.assignedTeamId !== teamId) {
  throw new Error("Cannot add photos to jobs not assigned to your team");
}
```

## Current State

### Completed & Committed
- ✅ Schema updated with role + teamId fields - commit `0e46f58`
- ✅ TypeScript types created (types/roles.ts)
- ✅ Complete implementation guide (docs/my-jobs-feature.md)
- ✅ Plan review completed - critical issues identified

### Next: Phase 1.0 Critical Fixes (NEW)
- ⏳ Create `convex/lib/auth.ts` with JWT-based role helpers
- ⏳ Update `convex/users.ts` store to sync role from JWT
- ⏳ Configure Clerk JWT template + verification test
- ⏳ Create existing users backfill script

### Then: Phase 1.5 QR Code Invitation
- ⏳ Install qrcode.react + nanoid
- ⏳ Create invitations table + mutations (with token hashing)
- ⏳ Create InviteRiggerDialog component (with rate limiting)
- ⏳ Create /invite/[token] page (with error handling)

### Remaining Phase 1
- ⏳ Server role helpers (`lib/roles.ts`)
- ⏳ Client role hook (`hooks/useRole.ts`)
- ⏳ Middleware updates

## Key Decisions Made

| Decision | Rationale |
|----------|-----------|
| Clerk publicMetadata | Simple, no Organizations needed |
| Teams-only model | Keep existing team structure |
| office default | Safe for existing users |
| Three-layer security | Middleware + Layout + Convex |
| Route groups | Separate office/rigger layouts |
| **QR Code onboarding** | Easy rigger invite, no email needed |
| **Prioritize Phase 1.5** | Need QR to test rigger flow |

## Tech Stack

- **Auth**: Clerk (JWT with publicMetadata)
- **Database**: Convex (real-time, auth integration)
- **Frontend**: Next.js 16 App Router
- **Styling**: Tailwind CSS v4
- **Types**: TypeScript strict mode

### New Dependencies (Phase 1.5)
```bash
npm install qrcode.react nanoid
```

| Package | Purpose |
|---------|---------|
| `qrcode.react` | Render QR codes in React |
| `nanoid` | Generate secure, URL-safe tokens |

## Schema Changes

### Users Table (COMMITTED)
```typescript
users: defineTable({
  // Existing fields...
  role: v.optional(
    v.union(v.literal("office"), v.literal("rigger"), v.literal("admin"))
  ),
  teamId: v.optional(v.id("teams")),
})
  .index("by_token", ["tokenIdentifier"])
  .index("by_role", ["role"])
  .index("by_team", ["teamId"])
```

### Invitations Table (TO CREATE)
```typescript
invitations: defineTable({
  token: v.string(),
  teamId: v.id("teams"),
  createdBy: v.id("users"),
  expiresAt: v.number(),
  usedAt: v.optional(v.number()),
  usedBy: v.optional(v.id("users")),
}).index("by_token", ["token"])
```

## Files Reference

### Committed
- `convex/schema.ts` - role + teamId on users
- `types/roles.ts` - Role types, route config
- `docs/my-jobs-feature.md` - Full implementation guide

### To Create (Phase 1.5)
- `convex/invitations.ts` - Token CRUD + validation
- `components/InviteRiggerDialog.tsx` - QR generator UI
- `app/invite/[token]/page.tsx` - Acceptance/signup page

### To Create (Later)
- `lib/roles.ts` - Server helpers
- `hooks/useRole.ts` - Client hook
- `convex/lib/auth.ts` - Convex auth helpers
- `components/rigger/*.tsx` - Rigger mobile UI
- `app/(rigger)/*.tsx` - Rigger routes

## Architecture

### Three-Layer Security
```
1. Middleware → Route-level redirects (fast, no DB)
2. Layout → Server-side role checks (auth verification)
3. Convex → Data filtering + mutation protection (source of truth)
```

### Role Hierarchy
```
admin
  └─ Full access + user management
office (default)
  └─ Full job CRUD, no user management
rigger
  └─ View/update assigned team jobs only
```

### QR Code Invitation Flow
```
1. Admin → InviteRiggerDialog → selects team
2. nanoid generates token → stored in Convex
3. QRCode.react renders /invite/{token}
4. Rigger scans → mobile signup page
5. Clerk signup → token validated
6. User created with role=rigger + teamId
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Break existing functionality | Default all to office |
| Riggers see wrong jobs | Defense in depth (3 layers) |
| Offline updates lost | Convex retry + optimistic UI |
| Performance issues | Convex indexes on role/teamId |
| Token security | nanoid (21 chars), short expiry |

## Next Steps

1. Install dependencies: `npm install qrcode.react nanoid`
2. Update schema with invitations table
3. Create convex/invitations.ts mutations
4. Create InviteRiggerDialog.tsx component
5. Create app/invite/[token]/page.tsx
6. Update user store for invitation tokens
7. Test complete QR flow
8. Continue with remaining Phase 1 items

## Mobile UI Design Specifications

**Reference**: `ASCII-Layout-Specifications.md` (682 lines)

### Touch Target Sizes
| Component | Height |
|-----------|--------|
| Primary buttons (START, COMPLETE) | 56px |
| Secondary buttons (DETAILS) | 48px |
| Status tabs | 44px (pill shape) |
| Bottom nav items | 64px touch area |

### Status Badge Colors (Tailwind)
```
TO DO:       bg-blue-100   text-blue-800
IN PROGRESS: bg-green-100  text-green-800
DELAYED:     bg-orange-100 text-orange-800
DONE:        bg-gray-100   text-gray-600
URGENT:      bg-red-100    text-red-800
```

### Screen Components (Phase 3)

**1. My Jobs (main screen)**
- Header: Logo + "RiggOps" + user avatar
- Team banner: Team name, member count, active jobs
- Status tabs: TO DO | IN PROGRESS | DELAYED (pill buttons)
- Job cards: Status badge, priority, work nr, area, description, location
- Action buttons: START (56px) + DETAILS (48px)
- Bottom nav: My Jobs (active) | Profile

**2. Job Detail Page**
- Back navigation
- Work number + status + priority badges
- Description section
- Location section (NO maps button for MVP)
- Details: Requested by, Requested at, Required by
- Sticky action button at bottom

**3. Profile Page**
- Large avatar
- Name + Role badge ("Rigger")
- My Team section with members list
- Today's Stats (Completed, In Progress, Pending)
- Sign Out button

**4. Empty States**
- No jobs: "No jobs assigned" + coffee emoji
- All done: "All done for now!" + celebration emoji

**5. Loading States**
- Skeleton cards for initial load

### UX Principles
1. **Glove-friendly**: All buttons 48px+ height
2. **One-hand operation**: Bottom nav in thumb zone
3. **Maximum 3 taps**: Open app → See jobs → Tap START
4. **High contrast**: Works in bright sunlight
5. **Offline indicator**: (future enhancement)

### MVP Exclusions
- Maps/directions button (marked "DO NOT INCLUDE YET")

## Reference Docs

- `rigger-jobs/docs/my-jobs-feature.md` - Full implementation guide
- `rigger-jobs/types/roles.ts` - Type definitions
- `ASCII-Layout-Specifications.md` - Detailed UI wireframes
- `rigger-role-implementation-tasks.md` - Task list

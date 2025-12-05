# Session Handoff - Rigger Role Implementation
**Last Updated**: 2025-12-05 (Pre-Context Reset)
**Status**: PLAN REVIEWED - Critical fixes required before Phase 1
**Branch**: `main` (rigger-jobs submodule)
**Working Dir**: `/Users/ramunasnognys/Developer/workspace/prompt-improver/rigger-jobs`

---

## Quick Summary

Adding role-based access control with QR code rigger onboarding.

**Completed**:
- ✅ Schema (role + teamId on users) - commit `0e46f58`
- ✅ TypeScript types (types/roles.ts)
- ✅ Implementation guide (docs/my-jobs-feature.md)
- ✅ **Plan review completed** - critical issues identified
- ✅ Bootstrap workflow files - commit `1ed6d36`

**Next**: Phase 1.0 Critical Fixes (before QR code)

---

## CURRENT STATE (2025-12-05)

### Git Status in rigger-jobs submodule:
```
Untracked: CLAUDE.md (can ignore/delete)
Last commits:
  1ed6d36 feat: bootstrap workflow files for rigger role implementation
  0e46f58 feat: add role-based schema and type definitions
  e92cb89 fix: AddPhotosSection button styling
```

No uncommitted work-in-progress. Ready to start Phase 1.0.

---

## PLAN REVIEW FINDINGS (2025-12-05)

**Verdict**: Plan architecturally sound but has 4 critical issues.

### Critical Issues (Must Fix First)

| Issue | Problem | Fix |
|-------|---------|-----|
| **Role Sync Gap** | Convex `users.role` vs Clerk `publicMetadata` will drift | Read role from JWT claims only, sync to Convex as cache |
| **JWT Config** | No verification step | Add test to log `ctx.auth.getUserIdentity()` |
| **User Migration** | ~50+ existing users have no role | Backfill script + default to "office" |
| **Schema Mismatch** | Plan mentions `jobAssignments` but code uses team-based | Use existing team-based model |

### Additional Fixes Required

- Photo upload protection for riggers (team check)
- Team deletion protection (block if riggers assigned)
- Expired QR error handling (user-friendly messages)
- Rate limiting invites (10/hour/user)
- Token hashing (security)

### Full Review Location
- Summary: `~/.claude/plans/inherited-purring-crown.md`
- Details: `~/.claude/plans/inherited-purring-crown-agent-fa211d2e.md`

---

## Implementation Status

### Phase 1.0: Critical Fixes ⏳ NEXT
- [ ] Create `convex/lib/auth.ts` - JWT-based role helpers
- [ ] Update `convex/users.ts` - sync role from JWT
- [ ] Configure Clerk JWT + verification test
- [ ] Backfill existing users to role="office"

### Phase 1: Foundation
- [x] Schema: role + teamId fields ✅ COMMITTED
- [x] Types: types/roles.ts ✅ COMMITTED
- [x] Docs: my-jobs-feature.md ✅ COMMITTED
- [x] Plan review ✅ COMPLETED
- [ ] lib/roles.ts server helpers
- [ ] hooks/useRole.ts client hook
- [ ] middleware.ts role routing

### Phase 1.5: QR Code Invitation (after 1.0)
- [ ] Install qrcode.react + nanoid
- [ ] Create invitations table (with token hashing)
- [ ] Create mutations (with rate limiting)
- [ ] Create InviteRiggerDialog
- [ ] Create /invite/[token] page (with error handling)

### Phase 2-4: Not Started
See `rigger-role-implementation-tasks.md`

---

## Quick Resume Commands

```bash
cd ~/Developer/workspace/prompt-improver/rigger-jobs

# Dev server
npm run dev                    # localhost:3000
npx convex dev                 # Convex dashboard

# After Phase 1.0, install deps
npm install qrcode.react nanoid
```

---

## Key Architecture

### Three-Layer Security
1. **Middleware** - Route redirects based on role
2. **Layout** - Server-side role checks
3. **Convex** - Data filtering + mutation protection (**source of truth**)

### Critical: Role Reading
```typescript
// convex/lib/auth.ts - ALWAYS read from JWT, not DB
export async function getUserRole(ctx: QueryCtx) {
  const identity = await ctx.auth.getUserIdentity();
  const role = (identity as any)?.metadata?.role;
  return role ?? "office"; // Safe default
}
```

### Role Hierarchy
```
admin → Full access + user management
office (default) → Full job CRUD
rigger → View/update assigned team jobs only
```

### QR Code Flow (Phase 1.5)
```
Admin → InviteRiggerDialog → nanoid token → hash → Convex storage
  ↓
QRCode.react renders /invite/{token}
  ↓
Rigger scans → /invite/[token] page
  ↓
Clerk signup → token validated → role = rigger + teamId
```

---

## Files Reference

**Committed**:
- `convex/schema.ts` - role + teamId on users
- `types/roles.ts` - Role types
- `docs/my-jobs-feature.md` - Implementation guide

**To Create (Phase 1.0)**:
- `convex/lib/auth.ts` - JWT-based auth helpers
- `convex/debug.ts` - Temporary JWT verification

**To Create (Phase 1.5)**:
- `convex/invitations.ts` - Token CRUD + validation (with hashing)
- `components/InviteRiggerDialog.tsx` - QR generator
- `app/invite/[token]/page.tsx` - Acceptance page

**To Create (Later)**:
- `lib/roles.ts` - Server helpers
- `hooks/useRole.ts` - Client hook
- `components/rigger/*.tsx` - Rigger UI
- `app/(rigger)/*.tsx` - Rigger routes

---

## Next Steps (Exact Order)

### Phase 1.0 Critical Fixes

1. **Create Convex auth helpers**:
   ```typescript
   // convex/lib/auth.ts
   export async function getUserRole(ctx: QueryCtx) {
     const identity = await ctx.auth.getUserIdentity();
     const role = (identity as any)?.metadata?.role;
     return role ?? "office";
   }
   ```

2. **Update users.store()** to sync role from JWT

3. **Configure Clerk JWT**:
   - Dashboard → Sessions → Customize session token
   - Add: `{"metadata": "{{user.public_metadata}}"}`

4. **Verify JWT works**:
   ```typescript
   // convex/debug.ts (temporary)
   export const testJwtClaims = query({
     handler: async (ctx) => {
       const identity = await ctx.auth.getUserIdentity();
       return { identity };
     },
   });
   ```

5. **Backfill existing users** to role="office"

---

## Mobile UI Specifications

**Reference Document**: `ASCII-Layout-Specifications.md` (682 lines)

### Touch Target Sizes
| Component | Height |
|-----------|--------|
| Primary buttons (START, COMPLETE) | 56px |
| Secondary buttons (DETAILS) | 48px |
| Status tabs | 44px (pill shape) |
| Bottom nav items | 64px touch area |

### Status Badge Colors
- TO DO: `bg-blue-100 text-blue-800`
- IN PROGRESS: `bg-green-100 text-green-800`
- DELAYED: `bg-orange-100 text-orange-800`
- DONE: `bg-gray-100 text-gray-600`
- URGENT: `bg-red-100 text-red-800`

---

## Unresolved Questions (Answered)

1. Can riggers be invited without email? → **No** (Clerk requires email)
2. Can rigger belong to multiple teams? → **No** (single team)
3. Is there a team lead role? → **Yes** (future enhancement)
4. Who runs existing users backfill script? → **Admin via Clerk API**
5. Photo storage limits per rigger? → **5 per job**

---

**End of Handoff - Continue with Phase 1.0 Critical Fixes**

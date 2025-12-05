# Session Handoff - RiggOps App
**Last Updated**: 2025-12-05 (Pre-Context Reset)
**Status**: PRODUCTION + RIGGER ROLE IN PROGRESS
**Branch**: `matt/rigger-my-jobs-feature`
**Working Dir**: `/Users/ramunasnognys/Developer/workspace/prompt-improver/rigger-jobs`

---

## Quick Summary

RiggOps is production-ready mobile-first job tracking. Currently implementing rigger role feature.

**Core Features Complete**:
1. ✅ Job management (Create, view, update status, assign teams)
2. ✅ Kanban board with 4 status columns
3. ✅ Activity timeline with filtering
4. ✅ Daily handover summaries
5. ✅ Team management
6. ✅ Photo uploads (up to 5 per job)
7. ✅ Real-time updates (Convex subscriptions)
8. ✅ Mobile-responsive navigation
9. ✅ Offline handling
10. ✅ Professional sign-in/sign-up pages

**Current Work**: Rigger Role Implementation (Phase 1.0 Critical Fixes next)

---

## CURRENT STATE (2025-12-05)

### Git Status
```
Parent repo (prompt-improver):
  - Branch: matt/rigger-my-jobs-feature
  - Modified: dev docs (need commit)

Submodule (rigger-jobs):
  - Untracked: CLAUDE.md (can delete)
  - Last commit: 1ed6d36 (bootstrap workflow files)
```

**No uncommitted work-in-progress.** Ready to continue.

---

## Rigger Role Implementation Status

**Detailed docs**: `dev/active/rigger-role-implementation/`

### Phase 1.0: Critical Fixes ⏳ NEXT
Plan review identified 4 critical issues to fix first:
- [ ] Create `convex/lib/auth.ts` - JWT-based role helpers
- [ ] Update `convex/users.ts` - sync role from JWT
- [ ] Configure Clerk JWT + verification test
- [ ] Backfill existing users to role="office"

### Phase 1.1: Schema & Types ✅ COMMITTED
- [x] Schema: role + teamId on users (commit `0e46f58`)
- [x] Types: types/roles.ts
- [x] Docs: my-jobs-feature.md
- [x] Plan review completed

### Phase 1.2-1.4: Not Started
- [ ] Server role helpers (`lib/roles.ts`)
- [ ] Client hook (`hooks/useRole.ts`)
- [ ] Middleware routing

### Phase 1.5: QR Code Invitation
- [ ] Install qrcode.react + nanoid
- [ ] Create invitations table + mutations
- [ ] Create InviteRiggerDialog
- [ ] Create /invite/[token] page

### Phase 2-4: Not Started
See `rigger-role-implementation-tasks.md`

---

## Quick Commands

```bash
cd ~/Developer/workspace/prompt-improver/rigger-jobs

# Development
npm run dev                    # Start dev server (localhost:3000)
npx convex dev                 # Convex dev dashboard

# Git status
git status

# After Phase 1.0, install deps
npm install qrcode.react nanoid
```

---

## Architecture: Rigger Role

### Three-Layer Security:
1. **Middleware** - Route redirects based on role
2. **Layout** - Server-side role checks
3. **Convex** - Data filtering + mutation protection

### Role Hierarchy:
```
admin
  └─ Full access + user management
office (default for existing users)
  └─ Full job CRUD, no user management
rigger
  └─ View/update assigned team jobs only
```

### Team Assignment Model:
- Jobs → Teams (existing)
- Riggers → Teams (NEW: teamId field on users)
- Riggers see only jobs assigned to their team

---

## Critical Fixes Required (Plan Review)

| Issue | Problem | Fix |
|-------|---------|-----|
| **Role Sync Gap** | Convex vs Clerk roles drift | Read from JWT only |
| **JWT Config** | No verification | Add test query |
| **User Migration** | No role on existing users | Backfill to "office" |
| **Schema Mismatch** | Plan vs code differ | Use team-based model |

---

## Key Files Reference

**In rigger-jobs submodule**:
- `convex/schema.ts` - role + teamId on users
- `types/roles.ts` - Role types and route config
- `docs/my-jobs-feature.md` - Full implementation guide

**To Create**:
- `convex/lib/auth.ts` - JWT-based auth helpers
- `lib/roles.ts` - Server helpers
- `hooks/useRole.ts` - Client hook
- `app/(rigger)/` - Rigger route group

**To Modify**:
- `middleware.ts` - Add role-based routing
- `convex/users.ts` - Sync role from JWT
- `convex/jobs.ts` - Role-based filtering
- `components/AuthenticatedLayout.tsx` - Role check

---

## Next Steps (Resume Here)

1. **Start Phase 1.0 Critical Fixes**:
   - Create `convex/lib/auth.ts`
   - Update `convex/users.ts` store mutation

2. **Configure Clerk JWT** (requires Clerk Dashboard):
   - Sessions → Customize session token
   - Add `{"metadata": "{{user.public_metadata}}"}`

3. **Verify JWT works** with debug query

4. **Backfill existing users** to role="office"

---

## Build Status

**Build**: ✅ Passes (11 routes, 2.3s compile)
**Dev Server**: Port 3000
**Database**: Convex (deployed)
**Auth**: Clerk (configured)

---

**End of Handoff - Continue with Phase 1.0 Critical Fixes**

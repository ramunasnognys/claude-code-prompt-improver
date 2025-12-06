# Rigger Role Implementation - Context

**Last Updated**: 2025-12-06 05:50 UTC
**Status**: jwt-auth-foundation VERIFIED PASSING
**Branch**: `main` (rigger-jobs submodule)
**Working Directory**: `/Users/ramunasnognys/Developer/workspace/prompt-improver/rigger-jobs`
**Latest Commit**: `cda5a71` - chore: update Clerk domain to humble-magpie-34

## Session Summary (2025-12-06 - Latest Session)

### What Was Completed This Session

**JWT Auth Foundation - VERIFIED PASSING**

1. **JWT Template Configuration** - User configured in Clerk Dashboard
   - Added claim: `"metadata": "{{user.public_metadata}}"`
   - JWT now correctly exposes publicMetadata

2. **Clerk Domain Update**
   - Changed from `helping-pigeon-78.clerk.accounts.dev` to `humble-magpie-34.clerk.accounts.dev`
   - Updated `convex/auth.config.ts`

3. **Debug Verification** - All checks passing at `/debug`:
   - ✅ JWT contains metadata.role: `office`
   - ✅ Convex user has role: `office`
   - ✅ JWT role matches Convex role

4. **Created `/api/set-role` endpoint** - `app/api/set-role/route.ts`
   - Sets current user's publicMetadata.role to "office"
   - Used for backfilling existing users

### Files Modified/Created This Session

| File | Action | Purpose |
|------|--------|---------|
| `app/api/set-role/route.ts` | NEW | API to set user role in Clerk |
| `app/debug/page.tsx` | NEW | Debug page for JWT verification |
| `convex/debug.ts` | NEW | Debug query for JWT claims |
| `convex/auth.config.ts` | MODIFIED | Updated Clerk domain |
| `features.json` | MODIFIED | Updated feature statuses |
| `progress.md` | MODIFIED | Session documentation |

## Git Status

**All changes committed and pushed:**
```
cda5a71 chore: update Clerk domain to humble-magpie-34
f061ef0 feat: jwt-auth-foundation verified passing
3a6d47f feat: add set-role API + update features.json status
92cfd15 feat: add QR code invitation system for riggers
```

## Feature Status Summary

| Feature | Status | Notes |
|---------|--------|-------|
| jwt-auth-foundation | ✅ passing | JWT template configured, verified |
| existing-users-backfill | ✅ passing | /api/set-role works |
| role-helpers-middleware | ✅ passing | All helpers exist |
| qr-invitation-system | in_progress | Code complete, needs e2e test |
| convex-authorization | not_started | Next priority |
| rigger-mobile-navigation | not_started | After authorization |

## Key Decisions Made This Session

| Decision | Rationale |
|----------|-----------|
| Created /api/set-role endpoint | Simpler than Clerk admin scripts |
| Kept debug files for now | Still useful for verification |
| Changed Clerk domain | User switched to different Clerk instance |

## Critical Information for Next Session

### JWT Flow - NOW WORKING
```
Clerk publicMetadata → JWT template exposes as `metadata` → Convex reads from identity → Syncs to users table
```

### Verified Working Configuration
- **Clerk Domain**: `humble-magpie-34.clerk.accounts.dev`
- **JWT Template Name**: `convex`
- **JWT Template Claims**: `{"metadata": "{{user.public_metadata}}"}`
- **User ID**: `user_35cXgAhN6wi23wB09eIoReKe5Lq`
- **User Role**: `office` (set in both Clerk and Convex)

## Commands for Next Session

```bash
# Navigate to project
cd /Users/ramunasnognys/Developer/workspace/prompt-improver/rigger-jobs

# Start dev server
pnpm dev

# Verify JWT still working
# Visit http://localhost:3000/debug

# After done with debug:
rm app/debug/page.tsx convex/debug.ts
```

## Next Steps (Priority Order)

1. **Test QR invitation e2e** - Generate QR, new user signs up, verify role=rigger assigned
2. **Mark qr-invitation-system as passing** - After e2e test
3. **Start Phase 2: Convex Authorization**
   - Update listJobs with role filtering
   - Riggers see only their team's jobs
   - Office/admin see all jobs
4. **Delete debug files** - After confident auth works

## Reference Files

- `features.json` - Feature tracking (per CLAUDE.md protocol)
- `progress.md` - Session progress notes
- `types/roles.ts` - Role types, ROUTE_ACCESS, LANDING_PAGES
- `docs/my-jobs-feature.md` - Full implementation guide

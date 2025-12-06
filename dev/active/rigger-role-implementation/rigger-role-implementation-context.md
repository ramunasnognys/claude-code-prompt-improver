# Rigger Role Implementation - Context

**Last Updated**: 2025-12-06 08:45 UTC
**Status**: Phase 3 COMPLETE - Rigger mobile interface done
**Branch**: `main` (rigger-jobs submodule)
**Working Directory**: `/Users/ramunasnognys/Developer/workspace/prompt-improver/rigger-jobs`

---

## Session Summary (2025-12-06 - Current Session)

### What Was Completed This Session

**Phase 3: Rigger Mobile Interface - COMPLETE**

1. **Rigger Components** (`components/rigger/`):
   - `RiggerBottomNav.tsx` - 2-item nav (My Jobs, Profile), 64px touch areas
   - `TeamBanner.tsx` - Team name, member count, active jobs
   - `RiggerStatusTabs.tsx` - 3 tabs: TO DO | IN PROGRESS | DELAYED
   - `RiggerJobCard.tsx` - Action buttons (START/COMPLETE)

2. **Rigger Pages**:
   - `app/my-jobs/page.tsx` - Job list with status filtering, empty states
   - `app/my-jobs/[id]/page.tsx` - Job detail with sticky action button
   - `app/profile/page.tsx` - Role-based views (rigger vs office)

3. **Layout Integration**:
   - `AuthenticatedLayout.tsx` - Conditional layout for riggers (no sidebar)
   - `convex/users.ts` - Added `getCurrentUserWithTeam` query

4. **Edge Case Fix**:
   - `convex/jobs.ts` - Rigger without team sees empty list (not error)

### Files Modified/Created This Session

| File | Action | Purpose |
|------|--------|---------|
| `components/rigger/RiggerBottomNav.tsx` | NEW | 2-item bottom nav |
| `components/rigger/TeamBanner.tsx` | NEW | Team info display |
| `components/rigger/RiggerStatusTabs.tsx` | NEW | Status filter tabs |
| `components/rigger/RiggerJobCard.tsx` | NEW | Action-focused job card |
| `app/my-jobs/page.tsx` | NEW | Rigger job list page |
| `app/my-jobs/[id]/page.tsx` | NEW | Rigger job detail page |
| `app/profile/page.tsx` | MODIFIED | Added rigger profile view |
| `components/AuthenticatedLayout.tsx` | MODIFIED | Conditional rigger layout |
| `convex/users.ts` | MODIFIED | Added getCurrentUserWithTeam |
| `convex/jobs.ts` | MODIFIED | Fixed rigger no-team edge case |

---

## Git Status

**Commits in rigger-jobs submodule (ahead of origin by 7):**
```
0a9f5d3 chore: update project state files
370a6b4 fix: handle rigger without team in job queries
24d8d4e feat(rigger): add rigger mobile interface
90bd326 feat: block team deletion if riggers assigned
ba2d61c feat: add role-based authorization to job mutations
d3d0fb4 feat: add role-based filtering to job queries
[earlier commits...]
```

**Commits in parent repo:**
```
9f1e57e docs: update rigger tasks - Phase 3 complete
```

---

## Key Decisions Made This Session

| Decision | Rationale |
|----------|-----------|
| No "done" tab for riggers | User decided riggers focus on active work only |
| Simpler profile for riggers | Team info + stats instead of full Clerk UI |
| Action buttons on cards | START + DETAILS for new; full-width COMPLETE for in_progress |
| Rigger layout = mobile-only | No sidebar, just MobileHeader + RiggerBottomNav |

---

## Feature Status Summary

| Feature | Status | Notes |
|---------|--------|-------|
| jwt-auth-foundation | ✅ passing | JWT template configured |
| existing-users-backfill | ✅ passing | /api/set-role works |
| role-helpers-middleware | ✅ passing | All helpers exist |
| qr-invitation-system | ✅ passing | Needs e2e test |
| convex-authorization | ✅ passing | Role filtering complete |
| rigger-mobile-navigation | ✅ passing | Phase 3 complete |
| rigger-job-card | ✅ passing | Action buttons work |
| rigger-my-jobs-page | ✅ passing | List + empty states |
| rigger-job-detail-page | ✅ passing | Sticky action button |
| rigger-profile-page | ✅ passing | Team info + stats |

---

## Critical Information for Next Session

### Architecture - Role System
```
Clerk publicMetadata → JWT claims → Convex auth helpers → Query/Mutation filtering
                                  ↓
                          useRole() hook → Conditional UI rendering
```

### Key Files
- `types/roles.ts` - Route access config, role types, landing pages
- `hooks/useRole.ts` - Client-side role hook
- `convex/lib/auth.ts` - Server-side: getUserRole(), getUserTeamId()
- `middleware.ts` - Role-based route redirects
- `components/AuthenticatedLayout.tsx` - Conditional layout per role

### Mutation Parameter
**IMPORTANT**: Use `newStatus` not `status` when calling `updateJobStatus`:
```typescript
await updateStatus({
  jobId: job._id,
  newStatus: "in_progress", // NOT "status"
  expectedVersion: job.version,
});
```

---

## Pre-existing Issues (Not From This Session)

TypeScript errors - mismatch `waiting_for_scaffolder` vs `waiting_for_scaffolders`:
- `app/jobs/[id]/page.tsx:116`
- `components/JobCard.tsx:61,91`
- `components/StatusDropdown.tsx:117`

---

## Commands for Next Session

```bash
# Navigate to project
cd /Users/ramunasnognys/Developer/workspace/prompt-improver/rigger-jobs

# Check status
git status
git log --oneline -10

# Start dev server
npm run dev

# Push to remote when ready
git push origin main
```

---

## Testing Checklist

- [ ] Create rigger invitation (office user on /admin/teams)
- [ ] New user accepts invite via QR code
- [ ] Verify rigger redirects to /my-jobs
- [ ] Verify rigger sees only team's jobs
- [ ] Test START button on "new" job
- [ ] Test COMPLETE button on "in_progress" job
- [ ] Verify profile shows team info
- [ ] Verify today's stats in profile
- [ ] Test sign out from rigger profile

---

## Next Steps (Priority Order)

1. **Push changes** - `git push origin main` in rigger-jobs
2. **Test with real rigger account** - Create invite, new user accepts
3. **Delete debug files** - `app/debug/page.tsx`, `convex/debug.ts`
4. **Phase 4: Admin user management** (if needed)

---

## Reference Files

- `dev/active/rigger-role-implementation/rigger-role-implementation-tasks.md` - Task checklist
- `dev/active/rigger-role-implementation/ASCII-Layout-Specifications.md` - UI specs
- `rigger-jobs/features.json` - Feature tracking
- `rigger-jobs/docs/my-jobs-feature.md` - Full implementation guide

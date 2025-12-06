# Rigger Role Implementation - Tasks

**Last Updated**: 2025-12-06 08:30 UTC
**Status**: Phase 3 COMPLETE - Rigger mobile interface done

---

## Phase 1.0: Critical Fixes ✅ COMPLETE

**Purpose**: Address critical issues identified in plan review.

### 1.0.1 Create Convex Auth Helpers ✅
- [x] Create `convex/lib/auth.ts`
- [x] Implement `getUserRole(ctx)` - read from JWT claims
- [x] Implement `getUserTeamId(ctx)` - extract teamId from JWT claims
- [x] Add safe default: return "office" if role missing
- [x] Added `isRigger()`, `isOfficeOrAdmin()` helpers

### 1.0.2 Update User Store to Sync Role ✅
- [x] Update `convex/users.ts` store mutation
- [x] Extract role from JWT identity custom claims
- [x] Sync role to Convex on every store() call (cache only)

### 1.0.3 Clerk JWT Configuration ✅ VERIFIED WORKING
- [x] Created `convex/debug.ts` with test query
- [x] Created `app/debug/page.tsx` - verification UI
- [x] JWT template configured: `{"metadata": "{{user.public_metadata}}"}`
- [x] User publicMetadata set: `{"role": "office"}`
- [x] Verified all 3 checks passing on /debug page

### 1.0.4 Existing Users Backfill ✅
- [x] Create backfill script: `convex/migrations/backfillRoles.ts`
- [x] Created /api/set-role endpoint for individual user backfill
- [x] Current user role verified syncing via JWT

**Phase 1.0 Checkpoint**: ✅ COMPLETE AND VERIFIED

---

## Phase 1: Foundation ✅ COMPLETE

### 1.1 Schema & Types ✅
- [x] Update `convex/schema.ts` - Add role + teamId to users
- [x] Create `types/roles.ts` - Role types, route access config
- [x] Create `docs/my-jobs-feature.md` - Implementation guide

### 1.2 Server Role Helpers ✅
- [x] Create `lib/roles.ts`
- [x] Implement `getUserRole()`, `checkRole()`, `isRigger()`, `isOfficeWorker()`, `isAdmin()`, `getLandingPage()`

### 1.3 Client Role Hook ✅
- [x] Create `hooks/useRole.ts`
- [x] Extract role from Clerk publicMetadata

### 1.4 Update Middleware ✅
- [x] Update `middleware.ts` with role-based redirects
- [ ] Test redirects with rigger user (need rigger account)

**Phase 1 Checkpoint**: ✅ COMPLETE

---

## Phase 1.5: QR Code Invitation ✅ COMPLETE

### 1.5.1-1.5.7 All Tasks Complete ✅
- [x] Dependencies installed (qrcode.react, nanoid)
- [x] Schema updated with invitations table
- [x] Convex mutations created (createInvitation, validateInvitation, etc.)
- [x] InviteRiggerDialog component
- [x] Invitation acceptance page (/invite/[token])
- [x] API route (/api/accept-invite)
- [x] Teams page updated with "Invite Rigger" button

**Phase 1.5 Checkpoint**: ✅ CODE COMPLETE (needs e2e test with new user)

---

## Phase 2: Convex Authorization ✅ COMPLETE

### 2.1 Auth Helpers ✅
Already created in `convex/lib/auth.ts`

### 2.2 Update Job Queries ✅
- [x] Update `convex/jobs.ts` listJobs with role filtering
- [x] Filter by teamId for riggers
- [x] Office/admin see all jobs
- [x] Add getJob with access check
- [x] Update searchJobs with role filtering

### 2.3 Update Job Mutations ✅
- [x] Update updateJobStatus with team check for riggers
- [x] Update updateDelayReason with team check
- [x] Add photo upload protection (addPhotosToJob, addPhotosFromQueue)
- [x] Block riggers from assignTeam/unassignTeam

### 2.4 Team Deletion Protection ✅
- [x] Block deletion if riggers assigned to team

---

## Phase 3: Rigger Mobile Interface ✅ COMPLETE

### 3.1 Rigger Components ✅
- [x] `components/rigger/RiggerBottomNav.tsx` - 2-item nav (My Jobs, Profile)
- [x] `components/rigger/TeamBanner.tsx` - Team info with member count
- [x] `components/rigger/RiggerStatusTabs.tsx` - TO DO | IN PROGRESS | DELAYED
- [x] `components/rigger/RiggerJobCard.tsx` - Action-focused job card with START/COMPLETE buttons

### 3.2 Rigger Pages ✅
- [x] `app/my-jobs/page.tsx` - Main job list with status tabs and empty states
- [x] `app/my-jobs/[id]/page.tsx` - Job detail with sticky action button
- [x] `app/profile/page.tsx` - Updated with rigger-specific view (team info, stats)

### 3.3 Layout Integration ✅
- [x] `components/AuthenticatedLayout.tsx` - Conditional nav for riggers (no sidebar)
- [x] `convex/users.ts` - Added `getCurrentUserWithTeam` query

---

## Phase 4: Administration (Not Started)

- [ ] Admin user management page
- [ ] Role assignment UI
- [ ] Team assignment for riggers

---

## Files Created/Modified

| File | Status | Purpose |
|------|--------|---------|
| `convex/lib/auth.ts` | ✅ | Convex auth helpers |
| `convex/debug.ts` | ✅ TEMP | JWT verification query |
| `convex/migrations/backfillRoles.ts` | ✅ | Migration script |
| `convex/invitations.ts` | ✅ | QR invitation mutations |
| `convex/users.ts` | ✅ | Added getCurrentUserWithTeam |
| `app/debug/page.tsx` | ✅ TEMP | JWT debug UI |
| `app/invite/[token]/page.tsx` | ✅ | Invitation page |
| `app/my-jobs/page.tsx` | ✅ NEW | Rigger job list |
| `app/my-jobs/[id]/page.tsx` | ✅ NEW | Rigger job detail |
| `app/profile/page.tsx` | ✅ UPDATED | Role-based profile views |
| `app/api/accept-invite/route.ts` | ✅ | Accept invite API |
| `app/api/set-role/route.ts` | ✅ | Set user role API |
| `components/rigger/RiggerBottomNav.tsx` | ✅ NEW | Rigger bottom nav |
| `components/rigger/TeamBanner.tsx` | ✅ NEW | Team info banner |
| `components/rigger/RiggerStatusTabs.tsx` | ✅ NEW | Status filter tabs |
| `components/rigger/RiggerJobCard.tsx` | ✅ NEW | Action-focused job card |
| `components/AuthenticatedLayout.tsx` | ✅ UPDATED | Conditional rigger layout |
| `components/InviteRiggerDialog.tsx` | ✅ | QR code dialog |
| `lib/roles.ts` | ✅ | Server role helpers |
| `hooks/useRole.ts` | ✅ | Client role hook |
| `middleware.ts` | ✅ | Role-based redirects |
| `convex/auth.config.ts` | ✅ | Updated Clerk domain |
| `convex/jobs.ts` | ✅ | Role-based query/mutation filtering |
| `convex/teams.ts` | ✅ | Rigger deletion protection |

---

## Known Issues (Resolved)

### ~~Clerk User ID Mismatch~~ ✅ RESOLVED
- Now using `humble-magpie-34.clerk.accounts.dev`
- User ID: `user_35cXgAhN6wi23wB09eIoReKe5Lq`
- Role correctly syncing via JWT

### ~~JWT Claims Not Flowing~~ ✅ RESOLVED
- JWT template configured correctly
- All verification checks passing

---

## Next Session Actions

1. **Test QR invitation e2e** - Create invite, new user signs up as rigger
2. **Test rigger mobile interface** - Verify job list, actions, profile work
3. **Delete debug files** when confident auth works
4. **Start Phase 4** - Admin user management

---

## Session Handoff (2025-12-06 08:30 UTC)

### This Session Completed
- Phase 3.1: Created all rigger UI components
- Phase 3.2: Created my-jobs pages (list + detail)
- Phase 3.3: Updated profile page with role-based views
- Phase 3.4: Integrated rigger layout in AuthenticatedLayout

### Files Created
- `components/rigger/RiggerBottomNav.tsx`
- `components/rigger/TeamBanner.tsx`
- `components/rigger/RiggerStatusTabs.tsx`
- `components/rigger/RiggerJobCard.tsx`
- `app/my-jobs/page.tsx`
- `app/my-jobs/[id]/page.tsx`

### Files Modified
- `components/AuthenticatedLayout.tsx` - Added rigger layout branch
- `app/profile/page.tsx` - Added RiggerProfilePage component
- `convex/users.ts` - Added getCurrentUserWithTeam query

### Key Features Implemented
- 3-tab status filter (TO DO, IN PROGRESS, DELAYED)
- Action buttons: START (new jobs), MARK COMPLETE (in_progress/delayed)
- Team banner showing team name, member count, active jobs
- Rigger profile with team info and today's stats
- Empty states for no jobs / all done
- Sticky action button on detail page

### No TypeScript Errors in New Files
Pre-existing type mismatch in scaffolder naming (not from this session)

### Next Priority
Test the rigger interface with a real rigger user account

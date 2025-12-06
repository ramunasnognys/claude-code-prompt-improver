# Rigger Role Implementation - Tasks

**Last Updated**: 2025-12-06 05:50 UTC
**Status**: Phase 1.0-1.5 COMPLETE, JWT VERIFIED WORKING

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

## Phase 2: Convex Authorization (Next Priority)

### 2.1 Auth Helpers ✅
Already created in `convex/lib/auth.ts`

### 2.2 Update Job Queries
- [ ] Update `convex/jobs.ts` listJobs with role filtering
- [ ] Filter by teamId for riggers
- [ ] Office/admin see all jobs
- [ ] Add getJobById with access check

### 2.3 Update Job Mutations
- [ ] Update updateJobStatus with team check for riggers
- [ ] Add photo upload protection for riggers
- [ ] Ensure riggers can only update their team's jobs

### 2.4 Team Deletion Protection
- [ ] Block deletion if riggers assigned to team

---

## Phase 3: Rigger Mobile Interface (Not Started)

- [ ] BottomNavigation component
- [ ] MobileHeader component
- [ ] TeamBanner component
- [ ] StatusTabs component
- [ ] JobCard component (rigger version)
- [ ] My Jobs page
- [ ] Job detail page
- [ ] Profile page

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
| `app/debug/page.tsx` | ✅ TEMP | JWT debug UI |
| `app/invite/[token]/page.tsx` | ✅ | Invitation page |
| `app/api/accept-invite/route.ts` | ✅ | Accept invite API |
| `app/api/set-role/route.ts` | ✅ NEW | Set user role API |
| `components/InviteRiggerDialog.tsx` | ✅ | QR code dialog |
| `lib/roles.ts` | ✅ | Server role helpers |
| `hooks/useRole.ts` | ✅ | Client role hook |
| `middleware.ts` | ✅ | Role-based redirects |
| `convex/auth.config.ts` | ✅ | Updated Clerk domain |

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

1. ~~Verify JWT claims~~ ✅ DONE
2. **Test QR invitation e2e** - Create invite, new user signs up as rigger
3. **Start Phase 2** - Convex authorization (team-based job filtering)
4. **Delete debug files** when confident auth works

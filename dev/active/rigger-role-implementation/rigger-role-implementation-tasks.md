# Rigger Role Implementation - Tasks

**Last Updated**: 2025-12-05 (Post Plan Review)
**Status**: PLAN REVIEWED - Critical fixes required before Phase 1

---

## Phase 1.0: Critical Fixes (NEW - DO FIRST)

**Purpose**: Address critical issues identified in plan review.

### 1.0.1 Create Convex Auth Helpers
- [ ] Create `convex/lib/auth.ts`
- [ ] Implement `getUserRole(ctx)` - **read from JWT claims, NOT database**
- [ ] Implement `getUserTeamId(ctx)` - extract teamId from JWT claims
- [ ] Add safe default: return "office" if role missing

### 1.0.2 Update User Store to Sync Role
- [ ] Update `convex/users.ts` store mutation
- [ ] Extract role from JWT identity custom claims
- [ ] Sync role to Convex on every store() call (cache only)
- [ ] Test that role syncs correctly

### 1.0.3 Clerk JWT Configuration + Verification
- [ ] Open Clerk Dashboard
- [ ] Navigate to Sessions → Customize session token
- [ ] Add `{"metadata": "{{user.public_metadata}}"}`
- [ ] **VERIFICATION**: Create `convex/debug.ts` with test query
- [ ] Call test query and verify `metadata.role` appears in identity
- [ ] Delete debug.ts after verification

### 1.0.4 Existing Users Backfill
- [ ] Create backfill script (Clerk Backend API or Convex migration)
- [ ] Set all existing users to role="office" in Clerk publicMetadata
- [ ] Verify users.store() picks up the role on next login
- [ ] Confirm no users have undefined role

**Phase 1.0 Checkpoint**: JWT verified, role syncs, existing users have role

---

## Phase 1: Foundation

### 1.1 Schema & Types ✅ COMMITTED
- [x] Update `convex/schema.ts` - Add role + teamId to users
- [x] Create `types/roles.ts` - Role types, route access config
- [x] Create `docs/my-jobs-feature.md` - Implementation guide
- [x] Plan review completed - critical issues identified

**Commit**: `0e46f58` - feat: add role-based schema and type definitions

### 1.2 Server Role Helpers
- [ ] Create `lib/roles.ts`
- [ ] Implement `getUserRole()` - extract from sessionClaims
- [ ] Implement `checkRole(role)` - validate specific role
- [ ] Implement `isRigger()` - helper function
- [ ] Implement `isOfficeWorker()` - helper function

### 1.3 Client Role Hook
- [ ] Create `hooks/useRole.ts`
- [ ] Extract role from sessionClaims
- [ ] Return role + helpers (isRigger, isOfficeWorker, isAdmin)
- [ ] Test hook in component

### 1.4 Update Middleware
- [ ] Update `middleware.ts`
- [ ] Create route matchers (isOfficeRoute, isRiggerRoute, isPublicRoute)
- [ ] Add role-based redirects
- [ ] Test redirects manually

**Phase 1 Checkpoint**: Hook works, redirects work

---

## Phase 1.5: QR Code Invitation ⏳ NEXT (after Phase 1.0)

**Purpose**: Allow office workers to invite riggers via QR code.

### 1.5.1 Install Dependencies
- [ ] Run `npm install qrcode.react nanoid`
- [ ] Verify packages in package.json

### 1.5.2 Update Schema (with security improvements)
- [ ] Add invitations table to `convex/schema.ts`:
  ```typescript
  invitations: defineTable({
    tokenHash: v.string(),        // SHA-256 hash (not plaintext!)
    teamId: v.id("teams"),
    createdBy: v.id("users"),
    createdAt: v.number(),
    expiresAt: v.number(),        // 24-48h, not 7 days
    usedAt: v.optional(v.number()),
    usedBy: v.optional(v.id("users")),
  }).index("by_token_hash", ["tokenHash"])
  ```
- [ ] Run `npx convex dev` to apply schema

### 1.5.3 Create Invitation Mutations (with rate limiting)
- [ ] Create `convex/invitations.ts`
- [ ] Implement `createInvitation` mutation:
  - **Rate limit**: Max 10 invites per user per hour
  - Generate token with nanoid
  - Hash token with SHA-256 before storage
  - Store with teamId, createdBy, expiresAt (24h)
  - Return plaintext token (for QR code)
- [ ] Implement `validateInvitation` query:
  - Hash input token
  - Look up by tokenHash
  - Check not expired
  - Check not used
  - Return invitation data (team name, etc.)
- [ ] Implement `consumeInvitation` mutation:
  - Mark usedAt = now
  - Mark usedBy = userId
  - Return teamId for assignment

### 1.5.4 Create InviteRiggerDialog Component
- [ ] Create `components/InviteRiggerDialog.tsx`
- [ ] Add team selector dropdown
- [ ] Add "Generate Invitation" button
- [ ] Display QR code using qrcode.react
- [ ] Add "Copy Link" button
- [ ] Add expiry countdown/info
- [ ] Style for mobile + desktop

### 1.5.5 Create Invitation Acceptance Page (with error handling)
- [ ] Create `app/invite/[token]/page.tsx`
- [ ] Validate token on page load
- [ ] **Error handling with user-friendly messages**:
  - Expired: "This invitation has expired. Please request a new one."
  - Used: "This invitation has already been used."
  - Invalid: "Invalid invitation link."
- [ ] Show team info if valid
- [ ] Integrate Clerk SignUp component
- [ ] After signup, consume token + assign role

### 1.5.6 Update User Store
- [ ] Update `convex/users.ts` store mutation
- [ ] Accept optional invitationToken parameter
- [ ] If token valid, set role="rigger" + teamId
- [ ] If no token, default role="office"

### 1.5.7 Add Invite Button to Admin
- [ ] Add "Invite Rigger" button to teams page
- [ ] Wire up InviteRiggerDialog
- [ ] Test complete flow

**Phase 1.5 Checkpoint**: Can generate QR, rigger scans, signs up, gets role + team

---

## Phase 2: Convex Authorization (Team-Based Model)

**Note**: Using existing team-based model (`job.assignedTeamId`), NOT user-based assignments.

### 2.1 Auth Helpers (moved to Phase 1.0)
Auth helpers created in Phase 1.0 (`convex/lib/auth.ts`)

### 2.2 Update Job Queries
- [ ] Update `convex/jobs.ts` listJobs
- [ ] Add role check using `getUserRole(ctx)`
- [ ] Filter by teamId for riggers: `job.assignedTeamId === userTeamId`
- [ ] Rigger without team sees empty list
- [ ] Office/admin see all jobs
- [ ] Update getJob with access check
- [ ] Test query filtering

### 2.3 Update Job Mutations
- [ ] Update updateJobStatus with team check for riggers
- [ ] Update createJob (office only)
- [ ] Update assignTeam (office only)
- [ ] **Add photo upload protection for riggers**:
  ```typescript
  if (role === "rigger" && job.assignedTeamId !== teamId) {
    throw new Error("Cannot add photos to jobs not assigned to your team");
  }
  ```
- [ ] Add proper error messages
- [ ] Test permission checks

### 2.4 Team Deletion Protection (NEW)
- [ ] Update `convex/teams.ts` deleteTeam mutation
- [ ] Check for assigned riggers before deletion
- [ ] Block deletion if riggers assigned
- [ ] Return error with rigger count

**Phase 2 Checkpoint**: Queries filtered by team, photo uploads restricted, team deletion protected

---

## Phase 3: Rigger Mobile Interface

**Reference**: `ASCII-Layout-Specifications.md` (682 lines of detailed wireframes)

### Design Specs Summary
| Component | Size |
|-----------|------|
| Primary buttons (START, COMPLETE) | 56px height |
| Secondary buttons (DETAILS) | 48px height |
| Status tabs | 44px (pill shape) |
| Bottom nav items | 64px touch area |

**Status Badge Colors (Tailwind)**:
- TO DO: `bg-blue-100 text-blue-800`
- IN PROGRESS: `bg-green-100 text-green-800`
- DELAYED: `bg-orange-100 text-orange-800`
- DONE: `bg-gray-100 text-gray-600`
- URGENT: `bg-red-100 text-red-800`

---

### 3.1 Bottom Navigation
- [ ] Create `components/rigger/BottomNavigation.tsx`
- [ ] 2 items: My Jobs (📋) | Profile (👤)
- [ ] 64px touch area per item
- [ ] Active dot indicator
- [ ] Fixed to bottom of screen
- [ ] Test on mobile viewport

### 3.2 Mobile Header
- [ ] Create `components/rigger/MobileHeader.tsx`
- [ ] Left: Logo icon + "RiggOps" text
- [ ] Right: User avatar (Clerk UserButton)
- [ ] Sticky top position
- [ ] Safe area padding for notch

### 3.3 Team Banner
- [ ] Create `components/rigger/TeamBanner.tsx`
- [ ] 🔧 icon + Team name
- [ ] "X members • Y active jobs" subtitle
- [ ] Card styling with border

### 3.4 Status Tabs
- [ ] Create `components/rigger/StatusTabs.tsx`
- [ ] 3 tabs: TO DO | IN PROGRESS | DELAYED
- [ ] Pill shape (rounded-full), 44px height
- [ ] Show count in parentheses: `TO DO (3)`
- [ ] Active indicator (underline or bold)
- [ ] Horizontally scrollable on small screens

### 3.5 Job Card
- [ ] Create `components/rigger/JobCard.tsx`
- [ ] **Header row**: Status badge + Priority badge (if urgent)
- [ ] **Info section**: Work Nr (RF-1234) + Area code (DU010)
- [ ] **Description**: 2-line truncated text
- [ ] **Location**: 📍 icon + location text
- [ ] **Delay banner** (if DELAYED): Orange bg, ⏳ icon, reason text
- [ ] **Action buttons**:
  - TO DO: START (56px primary) + DETAILS (48px secondary)
  - IN PROGRESS: MARK COMPLETE (full-width 56px)
- [ ] Status update handlers with optimistic updates
- [ ] Test all three card states

### 3.6 Job Detail Page
- [ ] Create `app/(rigger)/my-jobs/[id]/page.tsx`
- [ ] Back navigation (← Back to jobs)
- [ ] Work number (large heading)
- [ ] Status + Priority badges
- [ ] **Description section**: Label + full text
- [ ] **Location section**: Label + 📍 area + location
  - ⚠️ NO maps button (per ASCII doc: "DO NOT INCLUDE YET")
- [ ] **Details section**: Requested by, Requested at, Required by
- [ ] **Timeline** (for in-progress jobs):
  - ○ Requested - timestamp
  - ● Started - timestamp (filled = current)
  - ○ Completed - --:--
- [ ] **Sticky action button** at bottom (56px height)

### 3.7 My Jobs Page
- [ ] Create `app/(rigger)/my-jobs/page.tsx`
- [ ] TeamBanner at top
- [ ] StatusTabs below banner
- [ ] Scrollable job card list
- [ ] Pull-to-refresh (Convex subscription handles real-time)
- [ ] **Empty state**: 📋 icon + "No jobs assigned" + friendly message
- [ ] **All done state**: 🎉 icon + "All done for now!" message

### 3.8 Profile Page
- [ ] Create `app/(rigger)/profile/page.tsx`
- [ ] Large avatar (centered)
- [ ] Name + "Rigger" role badge
- [ ] **My Team section**: Team name + member list (you highlighted)
- [ ] **Today's Stats section**:
  - Jobs Completed: X
  - Jobs In Progress: X
  - Jobs Pending: X
- [ ] Sign Out button (🚪 SIGN OUT)

### 3.9 Rigger Layout
- [ ] Create `app/(rigger)/layout.tsx`
- [ ] Flex column: header + main + bottom nav
- [ ] Main area scrolls independently
- [ ] BottomNavigation always visible
- [ ] MobileHeader sticky at top
- [ ] Safe area insets for iOS

### 3.10 Confirmation Dialogs
- [ ] Start Job confirmation dialog:
  - "Start Job?" heading
  - Job summary (Work Nr + description)
  - CANCEL + START buttons (side by side)
- [ ] Job Completed success toast:
  - ✓ icon + "Job completed successfully!"
  - Work Nr reference
  - Auto-dismiss after 3s

### 3.11 Loading States
- [ ] Create skeleton components for:
  - Team banner skeleton
  - Status tabs skeleton
  - Job card skeleton (multiple)
- [ ] Show during initial load

### 3.12 Update AuthenticatedLayout
- [ ] Update `components/AuthenticatedLayout.tsx`
- [ ] Add useRole hook
- [ ] If rigger → render minimal wrapper (no sidebar)
- [ ] If office → render existing layout with sidebar
- [ ] Test role-based rendering

**Phase 3 Checkpoint**: Riggers see mobile UI matching ASCII specs, all touch targets 48px+, status updates functional

---

## Phase 4: Administration

### 4.1 Create User Management Page
- [ ] Create `app/(office)/admin/users/page.tsx`
- [ ] Fetch users and teams
- [ ] Create table with name, email, role, team
- [ ] Add role dropdown
- [ ] Add team dropdown (riggers only)
- [ ] Implement role change handler
- [ ] Implement team assign handler
- [ ] Test UI

### 4.2 Add User Mutations
- [ ] Add `listUsers` query to `convex/users.ts`
- [ ] Add `updateUserRole` mutation
- [ ] Add `assignUserToTeam` mutation
- [ ] Add admin-only checks
- [ ] Test mutations

### 4.3 Protect Admin Routes
- [ ] Update `app/(office)/admin/teams/page.tsx`
- [ ] Add useRole check
- [ ] Redirect non-admins
- [ ] Add loading state
- [ ] Test protection

### 4.4 Update Sidebar
- [ ] Update `components/Sidebar.tsx`
- [ ] Add role to NAV_ITEMS
- [ ] Filter items by user role
- [ ] Add Users nav item (admin only)
- [ ] Test filtering

**Phase 4 Checkpoint**: Admins can manage users, non-admins redirected

---

## Testing & Validation

### Security Testing
- [ ] Try accessing /dashboard as rigger
- [ ] Try accessing /my-jobs as office worker
- [ ] Try querying unassigned jobs via console
- [ ] Try updating unassigned job status
- [ ] Try accessing admin pages as non-admin
- [ ] Try using expired invitation token
- [ ] Try reusing consumed invitation token

### Functional Testing
- [ ] Generate invitation QR code
- [ ] Scan QR as new user
- [ ] Complete Clerk signup
- [ ] Verify rigger role assigned
- [ ] Verify teamId assigned
- [ ] Verify rigger sees only team jobs
- [ ] Update status as rigger
- [ ] Add photo as rigger
- [ ] Verify office worker sees all jobs

### Mobile Testing
- [ ] Test QR scanning on iPhone
- [ ] Test QR scanning on Android
- [ ] Verify 48px+ targets
- [ ] Test bottom nav
- [ ] Test job cards
- [ ] Test offline mode

---

## Deployment

### Pre-Deployment
- [ ] Run `npx convex dev` to test migration
- [ ] Set default role for existing users
- [ ] Configure Clerk JWT in production
- [ ] Test with prod Clerk keys
- [ ] Verify environment variables

### Deployment
- [ ] Deploy Convex: `npx convex deploy --prod`
- [ ] Deploy Next.js: `vercel --prod`
- [ ] Verify auth flow in prod
- [ ] Create test invitation
- [ ] Test QR code flow in prod
- [ ] Verify rigger restrictions

### Post-Deployment
- [ ] Monitor Sentry for errors
- [ ] Check Convex logs
- [ ] Test all user flows
- [ ] Gather pilot feedback

---

## Success Criteria

- [ ] QR code invitation flow works end-to-end
- [ ] Riggers see only assigned team jobs
- [ ] Office workers see all jobs
- [ ] No unauthorized data access
- [ ] Status updates < 1s
- [ ] Page load < 5s
- [ ] 48px+ touch targets verified
- [ ] Zero auth errors in production

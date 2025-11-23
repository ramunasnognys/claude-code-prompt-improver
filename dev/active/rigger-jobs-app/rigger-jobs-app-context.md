# Rigger Job Management App - Context & Key Decisions

**Last Updated**: 2025-11-23 17:45 UTC (Phase 3.1-3.3 UI Components COMPLETE ✅)

## 🎯 Current Status: PHASE 3 UI COMPONENTS IN PROGRESS

**Phase**: Phase 3 (Core UI Components) - **3 of 6 COMPLETE** ✅
**Completed**: 3.1 JobCard, 3.2 StatusColumn, 3.3 TeamBadge
**In Progress**: Phase 3.4 QuickActionsModal (next task)
**Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`
**Git Branches**:
  - `main` - Component files (rigger-jobs repo)
  - `rigger` - Documentation updates (prompt-improver repo)
**Latest Commits (main)**:
- `4c33ae2` - feat: Phase 3.3 TeamBadge component
- `b0aab89` - feat: Phase 3.2 StatusColumn component
- `e781486` - feat: Phase 3.1 JobCard component
**Latest Commits (rigger)**:
- `65458d0` - docs: mark Phase 3.3 TeamBadge complete
- `422fded` - docs: mark Phase 3.2 StatusColumn complete
- `89fa9ec` - docs: mark Phase 3.1 JobCard complete

### Session Summary (2025-11-23 - PHASE 3.1-3.3 UI COMPONENTS)
**What Was Accomplished This Session**:
- ✅ Phase 3.1: JobCard component (mobile-optimized with React.memo, status colors, priority indicator)
- ✅ Phase 3.2: StatusColumn component (Kanban column with header, count, empty state, horizontal scroll)
- ✅ Phase 3.3: TeamBadge component (FREE/BUSY status colors, keyboard nav, accessibility)
- ✅ Created comprehensive test pages for all 3 components
- ✅ All components compiled successfully (TypeScript strict mode)
- ✅ All changes committed to git (6 commits total)
- ✅ **READY FOR PHASE 3.4** - QuickActionsModal (complex: bottom sheet + Radix Dialog)

**Previous Sessions**:
- ✅ Phase 2 (All Backend): Convex schema, mutations, queries, cron jobs
- ✅ Phase 1 (Bootstrap): Next.js + Convex + Clerk setup

**Previous Session (Phase 1)**:
- ✅ Phase 1.1: Next.js project initialized with TypeScript, Tailwind, App Router
- ✅ Phase 1.2: Convex setup complete and connected
- ✅ Phase 1.3: Clerk auth configured and working
- ✅ Phase 1.4: Clerk → Convex integration complete (user sync working)

**Stack Implemented**:
- Next.js 16.0.3 with App Router
- React 19.2.0
- Convex 1.29.3 (real-time backend)
- Clerk 6.35.4 (authentication)
- Tailwind 4.0 with mobile-first config
- TypeScript 5
- All core dependencies installed

### Files Modified/Created This Session (Phase 2)

**Convex Backend** (ALL COMPLETE ✅):
- `convex/schema.ts` - ✅ EXPANDED with jobRequests, teams, activityEvents tables + 10 indexes
- `convex/jobs.ts` - ✅ CREATED with 4 mutations + 3 queries (379 lines)
- `convex/teams.ts` - ✅ CREATED with 2 queries + 1 mutation (78 lines)
- `convex/activity.ts` - ✅ CREATED with 4 queries + 1 internal mutation + cron job (154 lines)
- `convex/handover.ts` - ✅ CREATED with getHandoverData query (143 lines)

**Configuration Files** (Phase 1):
- `package.json` - All dependencies installed (Next.js, Convex, Clerk, etc.)
- `middleware.ts` - Clerk auth middleware protecting routes
- `lib/env.ts` - Zod environment variable validation
- `lib/constants.ts` - ✅ Area codes CORRECT (24 specific codes), delay reasons, shift times, status enums
- `lib/utils.ts` - Utility functions (cn helper)

**Convex Backend** (Phase 1 + 2 - ALL COMPLETE):
- `convex/users.ts` - User store mutation for Clerk sync
- `convex/auth.config.ts` - Clerk auth configuration
- `convex/myFunctions.ts` - Sample query (testing)
- `convex/schema.ts` - Complete schema with 4 tables
- `convex/jobs.ts` - Job CRUD operations
- `convex/teams.ts` - Team operations
- `convex/activity.ts` - Activity queries + cron
- `convex/handover.ts` - Handover data aggregation

**React Components**:
- `app/layout.tsx` - Root layout with ConvexClientProvider + Navbar
- `app/ConvexClientProvider.tsx` - Convex + Clerk providers
- `app/page.tsx` - Homepage
- `app/dashboard/page.tsx` - Dashboard placeholder
- `app/jobs/page.tsx` - Jobs listing placeholder
- `app/profile/page.tsx` - Profile page
- `app/components/Navbar.tsx` - Navigation bar
- `app/components/UserMenu.tsx` - User menu component
- `components/ui/button.tsx` - shadcn button component

---

## 🎯 Phase 2 Implementation Details

### 2.1 Define Convex Schema (COMPLETE ✅)

**File**: `convex/schema.ts` (104 lines)

**Tables Defined**:
1. **users** (existing) - Clerk user sync
   - tokenIdentifier, name, email, image
   - Index: `by_token`

2. **teams** (NEW) - Rigger team management
   - name (string) - "Team 1", "Team 2", or custom
   - memberNames (array of strings)

3. **jobRequests** (NEW) - Main work tracking
   - Status: new, in_progress, delayed, done
   - Dates: requestedAt, requiredBy, startedAt, completedAt, lastStatusChangeAt
   - Details: requestedByName, area, exactLocation, description, priority
   - Team: assignedTeamId (optional)
   - Delay: delayReasonType (7 options), delayReasonNote
   - Users: createdByUserId, assignedByUserId, lastUpdatedByUserId
   - **Version field** for optimistic locking (concurrent edit protection)
   - Indexes: by_status, by_area, by_team, by_version, by_last_status_change

4. **activityEvents** (NEW) - Audit trail
   - timestamp, type (job_created, status_changed, etc.)
   - References: jobRequestId, teamId, userId
   - Change tracking: fromValue, toValue, note
   - **TTL field** for 30-day auto-archival
   - Indexes: by_timestamp_desc, by_job, by_team, by_user, by_ttl

**Key Decisions**:
- Version field on jobRequests prevents concurrent edit conflicts
- Activity events have TTL to prevent database bloat (30 days)
- All indexes created for query performance

### 2.2 Job Mutations (COMPLETE ✅)

**File**: `convex/jobs.ts` (Lines 1-281, mutations)

**Mutations Implemented**:

1. **createJob** (Lines 11-76)
   - Validates: requestedByName, area, exactLocation, description, priority, requiredBy
   - Creates job with version=0, status="new"
   - Sets timestamps: requestedAt, lastStatusChangeAt
   - Tracks user: createdByUserId, lastUpdatedByUserId
   - Creates activity event (type: "job_created", ttl: +30 days)
   - Returns: jobId

2. **updateJobStatus** (Lines 81-150)
   - Checks version for concurrent edit protection
   - Updates status + timestamps:
     - Sets startedAt when → "in_progress"
     - Sets completedAt when → "done"
     - Updates lastStatusChangeAt
   - Increments version
   - Creates activity event (type: "status_changed")
   - Returns: jobId

3. **assignTeam** (Lines 155-215)
   - Checks version
   - Validates team exists
   - Detects team swaps (existing → new team)
   - Updates assignedTeamId, assignedByUserId
   - Increments version
   - Creates activity event:
     - type: "team_assigned" (first assignment)
     - type: "team_swapped" (team change)
   - Returns: jobId

4. **updateDelayReason** (Lines 220-281)
   - Checks version
   - Updates delayReasonType (7 options) + delayReasonNote
   - Increments version
   - Creates activity event (type: "delay_updated")
   - Returns: jobId

**Pattern**: All mutations follow same structure:
1. Authenticate user
2. Fetch current job
3. Check version (throw if mismatch)
4. Update job fields
5. Increment version
6. Create activity event with TTL
7. Return jobId

### 2.3 Job Queries (COMPLETE ✅)

**File**: `convex/jobs.ts` (Lines 283-398, queries)

**Queries Implemented**:

1. **listJobs** (Lines 292-325)
   - Optional filters: status, area, teamId
   - Filters jobs by any combination
   - Orders by lastStatusChangeAt desc (newest first)
   - Returns array of jobs
   - Real-time subscriptions automatic

2. **getJob** (Lines 350-371)
   - Fetches single job by ID
   - Includes team details if assignedTeamId exists
   - Returns null if not found
   - Returns: { ...job, team }

3. **getJobsByTeam** (Lines 377-398)
   - Fetches all jobs for specific team
   - Filters to active jobs (new, in_progress, delayed)
   - Excludes completed (done)
   - Uses by_team index
   - Orders by lastStatusChangeAt desc
   - Returns array of active jobs

**TypeScript Issue Fixed**: Initial implementation tried to reassign query variable with `.withIndex()` which caused type errors. Fixed by collecting all jobs first, then filtering in-memory.

### 2.4 Team Queries & Mutations (COMPLETE ✅)

**File**: `convex/teams.ts` (78 lines)

**Queries Implemented**:

1. **listTeams** (Lines 10-18)
   - Fetches all teams
   - Sorts alphabetically by name
   - No filters (small dataset)
   - Returns array of teams

2. **getTeamStatus** (Lines 25-56)
   - Determines if team is FREE or BUSY
   - Queries jobs assigned to team via by_team index
   - Filters active jobs (new, in_progress, delayed)
   - Returns discriminated union:
     - `{ status: 'FREE' }` if no active jobs
     - `{ status: 'BUSY', area, jobId }` if has active jobs

**Mutations Implemented**:

3. **createTeam** (Lines 63-78)
   - Validates: name, memberNames array
   - Requires authentication
   - Supports "Team 1-20" or custom names
   - Returns: teamId

**Implementation Pattern**: Teams are simple entities (name + members), status computed on-the-fly from job assignments.

### 2.5 Activity Queries (COMPLETE ✅)

**File**: `convex/activity.ts` (154 lines)

**Queries Implemented**:

1. **getTodayActivity** (Lines 10-40)
   - Shift-aware: determines current shift based on time
   - Day shift (07:00-19:00): if currentHour < 19
   - Night shift (19:00-07:00): if currentHour >= 19
   - Queries events since shift start
   - Sorted by timestamp desc (newest first)

2. **getActivityByDate** (Lines 47-73)
   - Accepts date param (Unix timestamp)
   - Calculates start/end of day (00:00-23:59)
   - Queries events within date range
   - Sorted by timestamp desc

3. **getActivityByJob** (Lines 78-93)
   - Queries by jobRequestId using by_job index
   - Returns all events for specific job
   - Sorted by timestamp desc

4. **getActivityByTeam** (Lines 98-113)
   - Queries by teamId using by_team index
   - Returns all events for specific team
   - Sorted by timestamp desc

**Internal Mutation**:

5. **archiveOldEvents** (Lines 118-141)
   - Internal mutation (not exposed to client)
   - Queries events where ttl < now using by_ttl index
   - Deletes expired events
   - Returns count of deleted events

**Cron Job** (Lines 147-153):
- Schedule: Daily at 02:00 UTC
- Calls internal.activity.archiveOldEvents
- Auto-archives events older than 30 days

**Key Decision**: TTL field set by mutations in jobs.ts (30 days), cron job handles cleanup.

### 2.6 Handover Query (COMPLETE ✅)

**File**: `convex/handover.ts` (143 lines)

**Query Implemented**:

1. **getHandoverData** (Lines 10-126)
   - Optional date filter (defaults to today)
   - Fetches all jobs (or filtered by date range)
   - Fetches all teams for lookup
   - Groups jobs by:
     1. Module (DU/DP/DW) - extracted from area code prefix
     2. Area code (DU010, DP030, etc.)
     3. Status category (completed/inProgress/delayed/new)
   - Per area:
     - completed: status = 'done'
     - inProgress: status = 'in_progress'
     - delayed: status = 'delayed' (includes delay reasons)
     - new: status = 'new'
   - Includes counts per category
   - Includes team details via lookup
   - Sorts areas numerically within each module

**Return Structure**:
```ts
{
  modules: {
    DU: { areas: {
      DU010: {
        completed: JobWithTeam[],
        inProgress: JobWithTeam[],
        delayed: JobWithTeam[],
        new: JobWithTeam[],
        counts: { completed, inProgress, delayed, new, total }
      }
    }},
    DP: { areas: { ... }},
    DW: { areas: { ... }}
  }
}
```

**Performance**: Optimized for 50+ jobs across 24 areas:
- Single query for all jobs
- Single query for all teams
- In-memory grouping and sorting
- Map-based team lookup (O(1))

**Date Filter Logic**:
- If date provided: filters jobs active during that date
- Job is "active" if: requestedAt <= endOfDay AND (not completed OR completedAt >= startOfDay)

---

## 🎯 Phase 3 Implementation Details (UI Components)

### 3.1 JobCard Component (COMPLETE ✅)

**File**: `components/JobCard.tsx` (75 lines)
**Test Page**: `app/test-jobcard/page.tsx` (144 lines)

**Props Interface**:
```ts
interface JobCardProps {
  job: Doc<"jobRequests">;
  team?: Doc<"teams"> | null;
  onClick?: () => void;
}
```

**Key Features**:
- React.memo optimization for real-time performance (50+ jobs)
- Status-based left border colors (new=gray, in_progress=blue, delayed=red, done=green)
- Priority indicator: urgent = red AlertCircle icon
- Area badge + description truncation (line-clamp-2)
- Team badge shows team name if assigned
- Min 44px height for mobile tap targets
- Active scale feedback (0.98) on tap
- Full keyboard support (Enter/Space keys with onKeyDown handler)
- Comprehensive accessibility (aria-label with job context, role="button", tabIndex=0)
- Dark mode support

**Testing**: Test page with 4 mock jobs (all statuses, urgent/normal, with/without team)

### 3.2 StatusColumn Component (COMPLETE ✅)

**File**: `components/StatusColumn.tsx` (94 lines)
**Test Page**: `app/test-statuscolumn/page.tsx` (272 lines)

**Props Interface**:
```ts
interface StatusColumnProps {
  status: "new" | "in_progress" | "delayed" | "done";
  jobs: Array<Doc<"jobRequests">>;
  teams?: Array<Doc<"teams">>;
  onJobClick?: (job: Doc<"jobRequests">) => void;
}
```

**Key Features**:
- React.memo optimization
- Sticky header with status name + job count badge
- Status-specific header colors (matches JobCard border colors)
- Empty state with Inbox icon and message
- Fixed 320px width (optimal for mobile horizontal scroll)
- Vertical scroll within column (overflow-y-auto)
- Team lookup callback (useCallback) for JobCard team prop
- Dark mode support
- Parent configures horizontal scroll with `flex overflow-x-auto` pattern

**Testing**: Test page with full Kanban board (4 columns, 2 new, 3 in progress, 1 delayed, 2 done)

### 3.3 TeamBadge Component (COMPLETE ✅)

**File**: `components/TeamBadge.tsx` (86 lines)
**Test Page**: `app/test-teambadge/page.tsx` (255 lines)

**Props Interface**:
```ts
interface TeamBadgeProps {
  team: Doc<"teams">;
  activeJob?: Doc<"jobRequests"> | null;  // Parent computes first active job
  onClick?: () => void;
}
```

**Key Features**:
- React.memo optimization
- FREE (green) vs BUSY (blue) status colors derived from activeJob presence
- Team name with truncation support (long names)
- Member count display (singular/plural handling)
- FREE status: CheckCircle icon
- BUSY status: Shows area code + "In Progress" label
- Min 44px tap target
- Full keyboard navigation (Enter/Space keys with onKeyDown)
- Focus ring with status-specific colors (green for FREE, blue for BUSY)
- Comprehensive accessibility (aria-label, sr-only text, aria-hidden on icons)
- Text truncation handling (min-w-0 on flex containers)
- Dark mode support

**Design Decision**: Parent computes activeJob (first active job for team), component derives FREE/BUSY. This keeps component presentational and reusable.

**Testing**: Test page with 6 teams (3 FREE, 3 BUSY), grid layout, keyboard navigation instructions

---

### Current Implementation State

**What's Working** (Phase 1 + Phase 2 COMPLETE):
- ✅ Dev server runs (`npm run dev`)
- ✅ Convex connected and syncing
- ✅ Clerk auth flow working (sign-in/sign-up)
- ✅ User sync from Clerk → Convex users table
- ✅ Environment validation with Zod
- ✅ Tailwind CSS configured with mobile breakpoints (Tailwind v4 @theme)
- ✅ Area codes correct (24 specific facility codes)
- ✅ Basic navigation and layout
- ✅ **Convex schema complete** (jobRequests, teams, activityEvents, users)
- ✅ **Job mutations complete** (createJob, updateJobStatus, assignTeam, updateDelayReason)
- ✅ **Job queries complete** (listJobs, getJob, getJobsByTeam)
- ✅ **Team queries & mutations complete** (listTeams, getTeamStatus, createTeam)
- ✅ **Activity queries complete** (getTodayActivity, getActivityByDate, getActivityByJob, getActivityByTeam)
- ✅ **Activity archival complete** (archiveOldEvents internal mutation + daily cron job)
- ✅ **Handover query complete** (getHandoverData with module/area grouping)
- ✅ **ALL BACKEND FUNCTIONS DEPLOYED TO CONVEX** ✅

**What's Working** (Phase 3.1-3.3 COMPLETE):
- ✅ **JobCard component** (Phase 3.1) - Status colors, priority indicator, team badge, min 44px tap
- ✅ **StatusColumn component** (Phase 3.2) - Kanban column, header with count, empty state, horizontal scroll
- ✅ **TeamBadge component** (Phase 3.3) - FREE/BUSY colors, keyboard nav, accessibility
- ✅ Test pages for all 3 components with mock data
- ✅ TypeScript compilation successful (strict mode)
- ✅ All components use React.memo for performance
- ✅ Mobile-first responsive design with Tailwind v4

**What's Not Yet Implemented** (Phase 3.4+):
- ❌ QuickActionsModal component (Phase 3.4) - NEXT TASK
- ❌ TodayTeamsPanel component (Phase 3.5)
- ❌ ActivityEventCard component (Phase 3.6)
- ❌ Main Board page with Convex integration (Phase 4.1)
- ❌ New Job form (Phase 4.2)
- ❌ Real-time toast notifications (Phase 6.1)
- ❌ Optimistic UI updates (Phase 6.2)

### Critical Information for Next Session

**📍 Project Status**:
- Phase 1 COMPLETE ✅
- Phase 2 COMPLETE ✅ (All backend)
- **Phase 3 IN PROGRESS** - 3 of 6 components complete
- Project location: `~/Developer/workspace/prompt-improver/rigger-jobs/`
- Git branches:
  - `main` - Component files (rigger-jobs repo)
  - `rigger` - Documentation (prompt-improver repo)
- **All changes committed** ✅

**🎯 Next Actions**:
1. **CONTINUE PHASE 3.4**: QuickActionsModal Component
   - Bottom sheet on mobile (Radix Dialog)
   - Full modal on desktop
   - Actions: Change Status, Assign Team, Update Delay
   - Convex mutations with version check
   - Optimistic UI updates
   - Toast notifications
2. Phase 3.5: TodayTeamsPanel
3. Phase 3.6: ActivityEventCard
4. Phase 4: Main Board page with real Convex data

**⚠️ Critical Notes**:
- ✅ Area codes FIXED (24 specific codes in lib/constants.ts)
- ✅ Tailwind mobile breakpoints configured (Tailwind v4 @theme in globals.css)
- ✅ **ALL PHASE 2 BACKEND COMPLETE** - 4 Convex files deployed
- ✅ All changes committed to git
- ✅ Cron job configured for daily activity archival (02:00 UTC)

**📂 Backend Files Created (Phase 2 - ALL COMPLETE)**:
- `convex/schema.ts` - 4 tables + 10 indexes (105 lines)
- `convex/jobs.ts` - 4 mutations + 3 queries (379 lines)
- `convex/teams.ts` - 2 queries + 1 mutation (78 lines)
- `convex/activity.ts` - 4 queries + 1 internal mutation + cron (154 lines)
- `convex/handover.ts` - 1 query (143 lines)

**📂 Frontend Files Created (Phase 3.1-3.3 - COMPLETE)**:
- ✅ `components/JobCard.tsx` - Individual job card (75 lines)
- ✅ `components/StatusColumn.tsx` - Kanban column (94 lines)
- ✅ `components/TeamBadge.tsx` - Team status badge (86 lines)
- ✅ `app/test-jobcard/page.tsx` - Test page with mock data (144 lines)
- ✅ `app/test-statuscolumn/page.tsx` - Test page with Kanban layout (272 lines)
- ✅ `app/test-teambadge/page.tsx` - Test page with FREE/BUSY examples (255 lines)

**📂 Frontend Files to Create Next (Phase 3.4+)**:
- ❌ `components/QuickActionsModal.tsx` - Bottom sheet/modal for job actions (NEXT)
- ❌ `components/TodayTeamsPanel.tsx` - Team overview panel
- ❌ `components/ActivityEventCard.tsx` - Activity event display

### Important Context for Next Session
- **Project Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`
- **Next Step**: Phase 3.1 - Create JobCard component
- **All Phase 1 + Phase 2 tasks complete** - Backend fully functional, ready for UI

## Key Files & Their Purpose

### Project Root
- `~/Developer/workspace/prompt-improver/rigger-jobs/` - ✅ Created and initialized

### Core Application Files

**Next.js App Structure**:
- `app/layout.tsx` - ✅ Root layout with Clerk + Convex providers
- `app/ConvexClientProvider.tsx` - ✅ Convex + Clerk provider wrapper
- `app/page.tsx` - ✅ Homepage (will become main board/kanban)
- `app/dashboard/page.tsx` - ✅ Dashboard placeholder
- `app/jobs/page.tsx` - ✅ Jobs listing placeholder
- `app/jobs/new/page.tsx` - ❌ TO BE CREATED - New job form
- `app/activity/page.tsx` - ❌ TO BE CREATED - Activity timeline
- `app/handover/page.tsx` - ❌ TO BE CREATED - Daily handover
- `middleware.ts` - ✅ Clerk auth protection

**Convex Backend** (ALL COMPLETE ✅):
- `convex/schema.ts` - ✅ Complete schema (4 tables + 10 indexes)
- `convex/users.ts` - ✅ User store mutation (Clerk sync)
- `convex/auth.config.ts` - ✅ Clerk auth configuration
- `convex/jobs.ts` - ✅ Job CRUD (4 mutations + 3 queries)
- `convex/teams.ts` - ✅ Team management (2 queries + 1 mutation)
- `convex/activity.ts` - ✅ Activity queries + archival cron job
- `convex/handover.ts` - ✅ Handover data aggregation query
- `convex/http.ts` - ⚠️ Optional (Clerk webhook - can use Convex sync instead)

**React Components** (All to be created):
- `components/JobCard.tsx` - ❌ Individual job card
- `components/StatusColumn.tsx` - ❌ Column container for jobs
- `components/TeamBadge.tsx` - ❌ Team status indicator
- `components/QuickActionsModal.tsx` - ❌ Bottom sheet for job actions
- `components/TodayTeamsPanel.tsx` - ❌ Team overview panel
- `components/ActivityEventCard.tsx` - ❌ Activity event display
- `app/components/Navbar.tsx` - ✅ Navigation bar
- `app/components/UserMenu.tsx` - ✅ User menu
- `components/ui/button.tsx` - ✅ shadcn button

**Configuration**:
- `.env.local` - ✅ Environment variables configured
- `lib/env.ts` - ✅ Zod validation
- `lib/constants.ts` - ✅ Area codes, delay reasons, shift times (needs area code verification)
- `lib/utils.ts` - ✅ Utility functions (cn helper)
- `tailwind.config.ts` - ❌ Needs mobile breakpoints configuration
- `package.json` - ✅ All dependencies installed

---

## Architectural Decisions

### 1. Single-Tenant Architecture
**Decision**: Build for single office only, no multi-tenant support
**Rationale**:
- Simpler auth (no organization switching)
- Faster development
- Sufficient for current requirements
**Future Consideration**: If expanding to multiple offices, add Clerk organizations

### 2. Convex as Backend
**Decision**: Use Convex instead of traditional REST API or Supabase
**Rationale**:
- Built-in real-time subscriptions (critical for multi-user updates)
- TypeScript-first with automatic type inference
- Serverless (no database management)
- Mutations + queries replace traditional backend routes
**Trade-off**: Vendor lock-in, but migration path exists via Convex export

### 3. No Repository Pattern
**Decision**: Call Convex functions directly from components
**Rationale**:
- Convex functions ARE the data layer
- No need for abstraction (Repository, Service layers)
- Simpler codebase for small team
**Pattern**:
```tsx
const jobs = useQuery(api.jobs.listJobs, { status: "in_progress" });
const createJob = useMutation(api.jobs.createJob);
```

### 4. Mobile-First UI with Tailwind
**Decision**: Pure Tailwind CSS, minimal component library
**Rationale**:
- Mobile is primary use case (office staff on phones)
- Tailwind sufficient for simple UI
- Avoid MUI/Radix overhead (except date picker if needed)
**Layout Strategy**: Horizontal scroll for status columns on mobile

### 5. Toast Notifications with Sonner
**Decision**: Use `sonner` library for real-time notifications
**Rationale**:
- Lightweight (2.5kb vs react-toastify 15kb)
- Beautiful defaults
- Works seamlessly with Tailwind
**Pattern**: Subscribe to activityEvents, show toast for other users' actions

### 6. Optimistic UI Updates
**Decision**: Implement optimistic updates for all mutations
**Rationale**:
- Critical for mobile UX (feels instant)
- Convex supports optimistic updates natively
- Rollback on error
**Implementation**: Use Convex optimistic update API

### 7. Activity Logging Strategy
**Decision**: Create activityEvent for every mutation
**Rationale**:
- Audit trail for compliance
- Powers activity timeline
- Enables handover generation
**Events Logged**: job_created, status_changed, team_assigned, team_swapped, delay_updated
**Archival**: Events auto-archived after 30 days (TTL) to prevent database bloat

### 8. Concurrent Edit Protection
**Decision**: Use optimistic locking with version field
**Rationale**:
- Multiple users may edit same job simultaneously
- Last-write-wins causes data loss
- Version checking prevents conflicts
**Implementation**: Every mutation checks version, increments on success, shows toast warning if version mismatch

---

## Integration Points

### Clerk ↔ Convex User Sync
**Flow**:
1. User signs up/in via Clerk
2. Clerk webhook triggers on user.created
3. Convex HTTP endpoint receives webhook
4. Convex creates user record in `users` table
5. JWT includes userId for all subsequent requests

**Key Files**:
- `convex/http.ts` - Webhook handler
- `convex/users.ts` - User CRUD
- `middleware.ts` - Auth middleware

**Environment Variables**:
- `CLERK_WEBHOOK_SECRET` (in Convex dashboard)
- `NEXT_PUBLIC_CLERK_FRONTEND_API_URL` (both envs)

### Real-Time Updates Flow
**Pattern**:
1. User A changes job status
2. Convex mutation executes
3. Convex reactivity triggers
4. User B's `useQuery` auto-updates
5. User B sees new data + toast notification

**No polling required** - Convex uses WebSockets

---

## Data Model Decisions

### Job Status Enum
**Options**: `"new" | "in_progress" | "delayed" | "done"`
**Rationale**: Simple, covers all workflow states
**Future**: Could add "cancelled" or "on_hold"

### Delay Reason Types
**Predefined List**:
- waiting_for_crane
- waiting_for_scaffolder
- material_not_found
- cable_trace_in_progress
- waiting_for_other_discipline
- weather_safety
- other

**Rationale**: Structured data for analytics, with "other" escape hatch
**Storage**: Enum in schema + optional freetext note

### Area Names (24 Total)
**Format**: Three-letter prefix + three-digit number
**Areas**:
- **DU (Utility Module)**: DU010, DU110, DU120, DU310, DU320, DU410, DU420, DU510
- **DP (Processing Module)**: DP030, DP130, DP140, DP230, DP240, DP330, DP340, DP530, DP540, DP730, DP740
- **DW**: DW050, DW150, DW250, DW350
**Type**: String (not enum) for flexibility
**Rationale**: Matches facility layout exactly, allows easy expansion
**Storage**: Constants file for dropdown, validation

### Team Identification
**Pattern**: "Team 1" through "Team 20"
**Custom Names**: Supported (e.g., "A-Team", "Night Crew Alpha")
**Storage**: `teams` table with name + memberNames array

### Timestamps & Shift Times
**Format**: Unix timestamp (number)
**Timezone**: Norway time (Europe/Oslo)
**Shift Schedule**:
- Day shift: 07:00 - 19:00 (12 hours)
- Night shift: 19:00 - 07:00 next day (12 hours)
**"Today" Definition**: Current shift (if before 19:00, show day shift; if after 19:00, show night shift)
**Display**: Format with `date-fns` in UI

---

## Dependencies & Versions

### Core Stack
- **Next.js 15**: Latest with App Router, React 19 support
- **Convex 1.16+**: Real-time database
- **Clerk 6.0+**: Authentication
- **Tailwind 4.0**: Latest CSS framework
- **TypeScript 5.6**: Type safety

### UI Libraries
- **sonner**: Toast notifications
- **lucide-react**: Icons
- **date-fns**: Date formatting
- **react-hook-form + zod**: Form validation

### Why These Versions
- Next.js 15: Server components, improved performance
- Tailwind 4: Better DX, faster builds
- Convex 1.16+: Latest real-time features
- Clerk 6.0: Latest auth patterns

---

## Important Notes & Gotchas

### Phase 1 Implementation Learnings

**✅ What Worked Well**:
- Convex auth integration with Clerk was straightforward
- `convex/users.ts` store mutation pattern handles user sync automatically
- Environment validation with Zod caught missing env vars early
- Middleware pattern protects routes cleanly

**⚠️ Issues Encountered & Solutions**:
1. **Area Codes Mismatch**: Initial constants had 77 generic codes instead of 24 specific
   - Solution: Need to manually update `lib/constants.ts` with exact facility codes
2. **Tailwind Config**: Mobile breakpoints not configured yet
   - Solution: Add to `tailwind.config.ts` in Phase 2
3. **Convex Auth Setup**: Required specific JWT template name in Clerk dashboard
   - Solution: Create "convex" template, configure issuer URL correctly

### 1. Convex Schema Changes
**Issue**: Schema changes require migration
**Solution**: Use `npx convex run` scripts for data migrations
**Best Practice**: Test schema changes in dev environment first
**Phase 1 Status**: ✅ Basic users schema working, ready to expand

### 2. Clerk JWT Template
**Critical**: Must create "convex" JWT template in Clerk
**Gotcha**: Forgetting this breaks Convex auth
**Check**: Verify `NEXT_PUBLIC_CLERK_FRONTEND_API_URL` matches JWT issuer
**Phase 1 Status**: ✅ Configured and tested

### 3. Mobile Touch Targets
**Rule**: Minimum 44px × 44px for all tappable elements
**Why**: Apple/Google accessibility guidelines
**Check**: Test on real devices, not just browser resize
**Phase 1 Status**: Not yet applicable (no UI components created)

### 4. Real-Time Update Performance
**Concern**: With 50+ jobs across 24 areas, does board re-render lag?
**Target**: <1 second propagation with 6 concurrent users
**Mitigation**:
- Use React.memo for JobCard
- Index Convex queries by status, area, team
- Limit initial query to jobs from last 7 days
- Test with 6 simultaneous users before launch
**Phase 1 Status**: Infrastructure ready, will test in Phase 4+

### 5. Concurrent Edit Conflicts
**Issue**: Two users assign different teams to same job
**Solution**: Optimistic locking with version field
**UX**: Show warning toast "Job updated by {user}, please refresh"
**Critical**: Test this scenario thoroughly in Phase 7.4
**Phase 1 Status**: Pattern documented, will implement in Phase 2

### 6. Offline Handling
**Issue**: Convex requires connection for real-time
**Solution**: Show offline indicator, queue mutations when reconnected
**Future**: Add service worker for true offline support
**Phase 1 Status**: Connection working, offline handling for Phase 6+

### 7. Webhook Security
**Critical**: Verify Clerk webhook signature in Convex
**Pattern**: Use `svix` library (already in Convex)
**Gotcha**: Test webhook in prod (ngrok in dev)
**Phase 1 Status**: Not yet implemented (optional for Phase 1)

---

## Testing Strategy

### Unit Tests (Optional for MVP)
- Convex functions (mutations, queries)
- Utility functions (handover text generator)

### Integration Tests (Critical)
- Multi-user real-time updates
- Clerk → Convex user sync
- Form validation flows

### Manual Testing (Required)
- Test on iPhone + Android
- Multiple users simultaneously
- Network disconnection/reconnection
- Touch target sizes

---

## Deployment Checklist

### Before First Deploy
- [ ] Convex production project created
- [ ] Clerk production instance configured
- [ ] All env vars set in Vercel
- [ ] Webhook URLs updated to production domain
- [ ] Test user created in Clerk prod

### Post-Deploy Verification
- [ ] Auth flow works
- [ ] User sync from Clerk to Convex
- [ ] Real-time updates across devices
- [ ] Mobile responsive layout
- [ ] Toast notifications appear

---

## Future Enhancements (Post-MVP)

1. **Photo Attachments**: Add photos to job requests
2. **Push Notifications**: Native mobile notifications for urgent jobs
3. **Analytics Dashboard**: Job completion rates, team utilization
4. **Shift Management**: Define shift times, auto-archive old jobs
5. **Multi-Language**: Norwegian + English support
6. **Export**: CSV/PDF export of activity logs
7. **AI Features**: Parse job descriptions, generate handover summaries

---

## Reference Projects

**Similar Stack**:
- `~/Developer/workspace/elite-next-clerk-convex-starter/` - Next.js + Clerk + Convex template
- Reference for: Clerk setup, Convex config, middleware patterns

**Monorepo Example**:
- `~/Developer/workspace/offshore-mate/` - Previous project
- Reference for: Mobile-first patterns (if applicable)

---

## Environment Variables

### .env.local (Next.js)
```bash
# Convex
CONVEX_DEPLOYMENT=
NEXT_PUBLIC_CONVEX_URL=

# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_FRONTEND_API_URL=
NEXT_PUBLIC_CLERK_SIGN_IN_FORCE_REDIRECT_URL=/
NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL=/
```

### Convex Dashboard
```bash
CLERK_WEBHOOK_SECRET=whsec_...
NEXT_PUBLIC_CLERK_FRONTEND_API_URL=https://...clerk.accounts.dev
```

---

## Resolved Questions ✅

1. ✅ **Area Names**: 24 areas confirmed (DU: 8, DP: 11, DW: 4)
2. ✅ **Team Names**: "Team 1-20" + custom names supported
3. ✅ **Shift Times**: Day 07:00-19:00, Night 19:00-07:00 Norway time
4. ✅ **User Roles**: No permission differences (removed role field)

## Remaining Questions

1. **Photo Attachments**: Defer to post-MVP (add if requested during testing)
2. **Bottom Sheet Library**: Use Radix Dialog (decision made during refactor review)

---

## 📝 Session Handoff Notes (Context Reset Prep)

### Files Modified This Session (2025-11-23)

**Documentation Updates**:
1. **Updated**: `dev/active/rigger-jobs-app/rigger-jobs-app-context.md` (this file)
   - Updated status to "Phase 1 Complete"
   - Added current implementation state
   - Listed all created files with ✅/❌ status
   - Added critical notes about next steps

2. **Updated**: `dev/active/rigger-jobs-app/rigger-jobs-app-tasks.md`
   - ✅ Marked all Phase 1 tasks as complete

**Application Files Created** (in `~/Developer/workspace/prompt-improver/rigger-jobs/`):
- All Phase 1 files listed above in "Core Application Files" section
- Project fully initialized and working
- Dev server runs successfully
- Auth flow tested and working

### Git Status
- **Branch**: `rigger`
- **Working Directory**: `/Users/ramunasnognys/Developer/workspace/prompt-improver/`
- **Project Location**: `rigger-jobs/` subdirectory
- **Uncommitted Changes**:
  - Phase 1 task checkmarks in `dev/active/rigger-jobs-app/rigger-jobs-app-tasks.md`
  - Context updates in this file
  - Entire `rigger-jobs/` project directory (new files not yet committed)

### Critical Decisions Made This Session

1. **Facility Layout Confirmed**: User provided facility diagram showing exact area codes
   - DU (Utility): 8 areas (DU010, DU110, DU120, DU310, DU320, DU410, DU420, DU510)
   - DP (Processing): 11 areas (DP030, DP130, DP140, DP230, DP240, DP330, DP340, DP530, DP540, DP730, DP740)
   - DW: 4 areas (DW050, DW150, DW250, DW350)

2. **Shift Times Defined**: Day 07:00-19:00, Night 19:00-07:00 (12-hour shifts, Norway time)
   - "Today" = current shift (not calendar day)
   - Activity queries filter by shift start time

3. **Concurrent Edit Protection**: Optimistic locking with version field
   - Every mutation checks version before update
   - Version incremented on success
   - Toast warning shown if version mismatch (another user edited)

4. **Activity Event Archival**: 30-day TTL to prevent database bloat
   - Convex cron job archives old events
   - Prevents performance issues with 1000+ events/day

5. **No User Roles**: Foremen and assistants have identical permissions
   - Removed `role` field from users table
   - Simplifies auth logic

### Refactor Review Findings (All Fixed)

**Critical Issues Fixed**:
1. ✅ Reordered Phase 1.4 - user schema now created before webhook (dependency fix)
2. ✅ Added missing tasks: env.ts validation, constants.ts, ngrok, error boundaries
3. ✅ Added concurrent edit handling with version field
4. ✅ Specified Radix Dialog for bottom sheet (removed ambiguity)
5. ✅ Added activity event archival strategy
6. ✅ Enhanced testing requirements (6 users, <1s updates)

### Next Immediate Steps (Phase 3.1 - JobCard Component)

**Start Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`

**First Task**: Create `components/JobCard.tsx`:
1. Display job details (description, area, requestedByName, team)
2. Add priority indicator (urgent = red border/icon)
3. Add status-based border color
4. Min 44px tap target
5. Click handler to open QuickActionsModal

**Critical Points**:
- Import from `@/convex/_generated/dataModel` for types
- Use Tailwind for styling (mobile-first)
- Add Lucide React icons for priority/status
- Follow Phase 3.1 checklist in tasks.md

**Commands to run**:
```bash
cd ~/Developer/workspace/prompt-improver/rigger-jobs
npm run dev  # Start dev server
# Open http://localhost:3000
```

### Blockers: NONE

Phase 1 + 2 complete. All backend functions deployed and working. Ready for UI development.

### Testing Approach for Phase 1

- Phase 1.1: Verify `npm run dev` works after setup
- Phase 1.2: Check Convex dashboard shows connected project
- Phase 1.3: Test Clerk sign-in flow works
- Phase 1.4: Verify new Clerk user appears in Convex users table (use ngrok for webhook)

### Performance Targets

- Real-time updates: <1 second propagation
- Concurrent users: Test with 6 simultaneous users
- Initial load: <5 seconds on mobile
- Touch targets: Minimum 44px × 44px

### Reference Projects

- `~/Developer/workspace/elite-next-clerk-convex-starter/` - Similar stack, reference for Clerk+Convex setup
- Facility layout diagram provided by user (stored in session image, shows exact area codes)

### Commands for Next Session

**To view plan**:
```bash
cat dev/active/rigger-jobs-app/rigger-jobs-app-plan.md
```

**To view tasks checklist**:
```bash
cat dev/active/rigger-jobs-app/rigger-jobs-app-tasks.md
```

**To start Phase 1**:
```bash
cd ~/Developer/workspace
# Follow Phase 1.1 steps in tasks.md
```

### Unfinished Work: NONE

Planning phase complete. No partially completed features. Clean slate for implementation.

---

**🎯 HANDOFF SUMMARY FOR NEXT SESSION**:
- ✅ Phase 1 COMPLETE - Project initialized and working
- ✅ Phase 2 COMPLETE - All backend functions deployed
- 📂 Location: `~/Developer/workspace/prompt-improver/rigger-jobs/`
- 🚀 Next: Phase 3.1 - Create JobCard component
- ✅ Area codes correct (24 specific codes)
- ✅ Mobile breakpoints configured
- ✅ All Convex functions deployed (jobs, teams, activity, handover)
- 📋 Reference: See tasks.md for Phase 3 checklist

---

## Quick Reference Commands

**Development**:
```bash
cd ~/Developer/workspace/prompt-improver/rigger-jobs
npm run dev          # Start Next.js dev server (port 3000)
npx convex dev       # Start Convex sync (real-time backend)
npm run build        # Production build
npm run lint         # Run ESLint
```

**Testing**:
- Open browser: http://localhost:3000
- Test auth: Sign in/sign up flow
- Check Convex dashboard: https://dashboard.convex.dev

**Environment Variables** (already configured in `.env.local`):
- `NEXT_PUBLIC_CONVEX_URL` - Convex backend URL
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk auth public key
- `CLERK_SECRET_KEY` - Clerk secret (server-side)
- `NEXT_PUBLIC_CLERK_FRONTEND_API_URL` - Clerk issuer URL

---

## Phase 3 Quick Start Checklist

Before writing code for Phase 3:
1. ✅ Phase 2 backend complete - all queries/mutations working
2. 📖 Read `dev/active/rigger-jobs-app/rigger-jobs-app-tasks.md` Phase 3 section
3. 📖 Review Convex API exports in `convex/_generated/api.d.ts`
4. 📖 Review data types in `convex/_generated/dataModel.ts`
5. 🚀 Start with Phase 3.1: Create `components/JobCard.tsx`
6. 💡 Use `useQuery(api.jobs.listJobs, {...})` for data fetching
7. 💡 Use `useMutation(api.jobs.createJob)` for mutations

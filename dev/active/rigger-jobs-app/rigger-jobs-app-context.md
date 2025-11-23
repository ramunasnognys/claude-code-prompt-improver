# Rigger Job Management App - Context & Key Decisions

**Last Updated**: 2025-11-23 18:05 UTC (Phase 2.1-2.3 Complete)

## 🎯 Current Status: PHASE 2.1-2.3 COMPLETE ✅

**Phase**: Phase 2 (Convex Backend) - IN PROGRESS
**Completed**: 2.1 Define Schema, 2.2 Job Mutations, 2.3 Job Queries
**Next Phase**: 2.4 Team Queries & Mutations
**Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`
**Git Branch**: rigger
**Latest Git Commit**: TBD (changes not yet committed)

### Session Summary (2025-11-23 - PHASE 2 IMPLEMENTATION)
**What Was Accomplished This Session**:
- ✅ Phase 2.1: Convex schema expanded with jobRequests, teams, activityEvents tables
- ✅ Phase 2.2: Job mutations implemented (createJob, updateJobStatus, assignTeam, updateDelayReason)
- ✅ Phase 2.3: Job queries implemented (listJobs, getJob, getJobsByTeam)
- ✅ All backend functions deployed and tested in Convex dashboard

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

**Convex Backend** (NEW):
- `convex/schema.ts` - ✅ EXPANDED with jobRequests, teams, activityEvents tables + 10 indexes
- `convex/jobs.ts` - ✅ CREATED with 4 mutations + 3 queries (398 lines)

**Configuration Files** (Phase 1):
- `package.json` - All dependencies installed (Next.js, Convex, Clerk, etc.)
- `middleware.ts` - Clerk auth middleware protecting routes
- `lib/env.ts` - Zod environment variable validation
- `lib/constants.ts` - ✅ Area codes CORRECT (24 specific codes), delay reasons, shift times, status enums
- `lib/utils.ts` - Utility functions (cn helper)

**Convex Backend** (Phase 1):
- `convex/users.ts` - User store mutation for Clerk sync
- `convex/auth.config.ts` - Clerk auth configuration
- `convex/myFunctions.ts` - Sample query (testing)

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

---

### Current Implementation State

**What's Working** (Phase 1 + Phase 2.1-2.3):
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
- ✅ All backend functions deployed to Convex

**What's Not Yet Implemented**:
- ❌ Team mutations and queries (Phase 2.4)
- ❌ Activity queries (Phase 2.5)
- ❌ Handover query (Phase 2.6)
- ❌ Kanban board UI (Phase 4)
- ❌ Quick actions modal (Phase 3)
- ❌ Real-time toast notifications (Phase 6)
- ❌ Mobile-first responsive UI components (Phase 3-4)

### Critical Information for Next Session

**📍 Project Status**:
- Phase 1 COMPLETE ✅
- Phase 2.1-2.3 COMPLETE ✅ (Schema, Job Mutations, Job Queries)
- Project location: `~/Developer/workspace/prompt-improver/rigger-jobs/`
- Git branch: `rigger`
- **Changes NOT committed** - Need to commit Phase 2 work

**🎯 Next Actions**:
1. **COMMIT WORK**: Git commit Phase 2.1-2.3 changes (schema + jobs.ts)
2. Start Phase 2.4: Create `convex/teams.ts` with team queries & mutations
3. Continue Phase 2.5: Activity queries
4. Continue Phase 2.6: Handover query

**⚠️ Critical Notes**:
- ✅ Area codes FIXED (24 specific codes in lib/constants.ts)
- ✅ Tailwind mobile breakpoints configured (Tailwind v4 @theme in globals.css)
- ✅ All Phase 2.1-2.3 functions deployed to Convex
- ⚠️ Changes uncommitted - need git commit before continuing

**📂 Key Files Modified This Session**:
- `convex/schema.ts` - Expanded with 3 new tables + 10 indexes
- `convex/jobs.ts` - NEW file with 4 mutations + 3 queries (398 lines)
- `dev/active/rigger-jobs-app/rigger-jobs-app-tasks.md` - Marked Phase 2.1-2.3 complete

**📂 Key Files to Create Next**:
- `convex/teams.ts` - Team CRUD operations (Phase 2.4)
- `convex/activity.ts` - Activity timeline queries (Phase 2.5)
- `convex/handover.ts` - Daily handover data aggregation (Phase 2.6)

### Important Context for Next Session
- **Project Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`
- **Next Step**: Phase 2.1 - Define Convex schema with all tables
- **All Phase 1 tasks complete** - Ready to build backend

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

**Convex Backend**:
- `convex/schema.ts` - ✅ Basic users table (needs expansion for jobs, teams, activity)
- `convex/users.ts` - ✅ User store mutation (Clerk sync)
- `convex/auth.config.ts` - ✅ Clerk auth configuration
- `convex/jobs.ts` - ❌ TO BE CREATED - Job CRUD operations
- `convex/teams.ts` - ❌ TO BE CREATED - Team management
- `convex/activity.ts` - ❌ TO BE CREATED - Activity logging & queries
- `convex/handover.ts` - ❌ TO BE CREATED - Handover data aggregation
- `convex/http.ts` - ❌ TO BE CREATED - Webhook handlers (if needed)

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

### Next Immediate Steps (Phase 2.1 - Define Convex Schema)

**Start Location**: `~/Developer/workspace/prompt-improver/rigger-jobs/`

**First Task**: Update `convex/schema.ts` to add:
1. `jobRequests` table with all fields (status, dates, area, team, version, etc.)
2. `teams` table (name, memberNames)
3. `activityEvents` table (timestamp, type, jobId, teamId, userId, ttl)
4. Add all necessary indexes

**Critical Points**:
- Add `version` field to jobRequests for optimistic locking
- Verify area codes in `lib/constants.ts` match facility layout (24 areas)
- Add TTL field to activityEvents for 30-day auto-archival
- Reference existing `users` table (already implemented)

**Commands to test**:
```bash
cd ~/Developer/workspace/prompt-improver/rigger-jobs
npx convex dev  # Apply schema changes
# Verify schema in Convex dashboard
```

### Blockers: NONE

Phase 1 complete and working. Ready for Phase 2 (backend development).

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
- 📂 Location: `~/Developer/workspace/prompt-improver/rigger-jobs/`
- 🚀 Next: Phase 2.1 - Define Convex schema
- ⚠️ Fix area codes in `lib/constants.ts` FIRST (77 codes → 24 specific codes)
- ⚠️ Add mobile breakpoints to Tailwind config
- 📋 Reference: See tasks.md for Phase 2 checklist

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

## Phase 2 Quick Start Checklist

Before writing code for Phase 2:
1. ✅ Read `dev/active/rigger-jobs-app/rigger-jobs-app-tasks.md` Phase 2 section
2. ⚠️ Fix area codes in `lib/constants.ts` (24 specific codes)
3. ⚠️ Add mobile breakpoints to `tailwind.config.ts`
4. 📖 Review data model in this context doc (lines 230-280)
5. 🚀 Start with Phase 2.1: Update `convex/schema.ts`

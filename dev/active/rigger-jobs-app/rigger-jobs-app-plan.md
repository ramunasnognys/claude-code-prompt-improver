# Rigger Job Management App - Implementation Plan

**Last Updated**: 2025-11-15 (Updated with resolved questions & refactor review fixes)

## Executive Summary

Build mobile-first web app replacing paper book for tracking ~50 riggers across ~20 teams. Single-tenant system for 6 office staff (3 foremen + 3 assistants). Real-time job status, team assignments, activity tracking, end-of-day handover. Stack: Next.js 15 + Convex + Clerk + Tailwind.

**Project Directory**: `~/Developer/workspace/rigger-jobs`
**Estimated Timeline**: 3-4 weeks MVP
**Key Success Metric**: Zero paper book usage after week 1

**Shift Schedule**:
- Day shift: 07:00 - 19:00
- Night shift: 19:00 - 07:00

**Facility Areas** (24 total):
- **DU** (Utility Module): DU010, DU110, DU120, DU310, DU320, DU410, DU420, DU510
- **DP** (Processing Module): DP030, DP130, DP140, DP230, DP240, DP330, DP340, DP530, DP540, DP730, DP740
- **DW**: DW050, DW150, DW250, DW350

---

## Current State Analysis

**Pain Points**:
- Paper book often outdated with 6 simultaneous users
- No visibility into job status across shifts
- Unclear team availability (free vs busy)
- Manual handover notes prone to errors
- No activity history or audit trail

**Manual Processes Replaced**:
- ✅ Writing job requests in paper book
- ✅ Manually tracking team assignments
- ✅ Paper-based status updates
- ✅ Handwritten handover notes

---

## Proposed Future State

**Mobile-First Board View**:
- Kanban columns: New | In Progress | Delayed | Done
- Real-time updates across all devices
- One-tap status changes, team swaps
- Visual team availability dashboard

**Activity & Handover**:
- Complete event timeline (who did what, when)
- Filterable by team, job, date
- Auto-generated handover summaries by area
- Copy-paste ready for shift notes

---

## Implementation Phases

### Phase 1: Project Bootstrap (Days 1-2)
Initialize Next.js app, configure Convex + Clerk, setup dev environment

### Phase 2: Convex Backend (Days 3-5)
Schema, mutations, queries, real-time subscriptions, indexes

### Phase 3: Core UI Components (Days 6-9)
JobCard, StatusColumn, TeamBadge, QuickActionsModal, mobile layouts

### Phase 4: Main Features (Days 10-14)
Board view, team overview, new job form, status/team updates

### Phase 5: Activity & Handover (Days 15-17)
Timeline view, filtering, area-grouped handover, text generation

### Phase 6: Real-Time & Polish (Days 18-20)
Toast notifications, optimistic updates, loading states, touch optimizations

### Phase 7: Deploy & Test (Days 21-25)
Production deployment, multi-user testing, mobile device testing, training

---

## Detailed Task Breakdown

### PHASE 1: Project Bootstrap

**1.1 Initialize Next.js Project** (Effort: M)
- Create `~/Developer/workspace/rigger-jobs/`
- Run `npx create-next-app@latest` with TypeScript, Tailwind, App Router
- Install dependencies: `convex`, `@clerk/nextjs`, `react-hook-form`, `zod`, `sonner`, `date-fns`, `lucide-react`
- Configure `tailwind.config.ts` with mobile-first breakpoints: `screens: { xs: '375px', sm: '640px', md: '768px', lg: '1024px' }`
- Create `lib/env.ts` with Zod validation for environment variables
- Create `lib/constants.ts` with area codes, delay reasons, shift times
- **Acceptance**: `npm run dev` works, localhost:3000 loads, env validation passes

**1.2 Setup Convex** (Effort: S)
- Run `npx convex dev`, create account/project
- Copy deployment URL to `.env.local`
- Create `convex/tsconfig.json`
- Test connection with sample query
- **Acceptance**: Convex dashboard shows connected project

**1.3 Configure Clerk Auth** (Effort: M)
- Create Clerk app (single-tenant mode)
- Add env vars: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`
- Create JWT template "convex", copy issuer URL
- Setup `middleware.ts` for route protection
- Add Clerk providers to `app/layout.tsx`
- **Acceptance**: Sign-in works, dashboard route protected

**1.4 Connect Clerk → Convex** (Effort: M)
- Add `NEXT_PUBLIC_CLERK_FRONTEND_API_URL` to both envs
- Create `convex/users.ts` with basic user schema and CRUD functions
- Create Convex HTTP endpoint `/clerk-users-webhook` in `convex/http.ts`
- Setup ngrok for local webhook testing: `ngrok http 3000`
- Setup Clerk webhook for `user.created`, `user.updated`, `user.deleted` (use ngrok URL in dev)
- Add `CLERK_WEBHOOK_SECRET` to Convex env
- Test user sync (create user in Clerk, verify appears in Convex)
- **Acceptance**: New Clerk user appears in Convex `users` table

---

### PHASE 2: Convex Backend

**2.1 Define Schema** (Effort: L)
```typescript
// convex/schema.ts
jobRequests: {
  status: v.union(literal("new"), literal("in_progress"), literal("delayed"), literal("done")),
  requestedAt: v.number(), // Unix timestamp
  requiredBy: v.optional(v.number()),
  startedAt: v.optional(v.number()),
  completedAt: v.optional(v.number()),
  lastStatusChangeAt: v.number(),
  requestedByName: v.string(),
  area: v.string(), // DU010, DP030, DW050, etc. (24 area codes)
  exactLocation: v.string(), // e.g., "deck", "port side"
  description: v.string(),
  priority: v.union(literal("normal"), literal("urgent")),
  assignedTeamId: v.optional(v.id("teams")),
  delayReasonType: v.optional(v.union(
    literal("waiting_for_crane"),
    literal("waiting_for_scaffolder"),
    literal("material_not_found"),
    literal("cable_trace_in_progress"),
    literal("waiting_for_other_discipline"),
    literal("weather_safety"),
    literal("other")
  )),
  delayReasonNote: v.optional(v.string()),
  createdByUserId: v.id("users"),
  assignedByUserId: v.optional(v.id("users")),
  lastUpdatedByUserId: v.id("users"),
  version: v.number(), // For optimistic locking (concurrent edit protection)
}
teams: {
  name: v.string(), // "Team 1", "Team 2", or custom names
  memberNames: v.array(v.string()),
}
activityEvents: {
  timestamp: v.number(),
  type: v.string(), // "job_created", "status_changed", "team_assigned", etc.
  jobRequestId: v.id("jobRequests"),
  teamId: v.optional(v.id("teams")),
  userId: v.id("users"),
  fromValue: v.optional(v.string()),
  toValue: v.optional(v.string()),
  note: v.optional(v.string()),
  ttl: v.optional(v.number()), // Archive after 30 days
}
users: {
  clerkId: v.string(),
  name: v.string(),
  // No role field - foremen and assistants have same permissions
}
```
- Add indexes: `by_status`, `by_area`, `by_team`, `by_timestamp_desc`, `by_version`
- Note: Timestamps represent shift times (Day: 07:00-19:00, Night: 19:00-07:00 Norway time)
- **Acceptance**: Schema compiles, indexes created, matches facility layout

**2.2 Job Mutations** (Effort: L)
- `createJob`: Validate input (Zod), insert jobRequest with version=0, create activityEvent
- `updateJobStatus`: Check version (concurrent edit protection), change status, update timestamps, increment version, log activity
- `assignTeam`: Check version, set assignedTeamId, create swap event if team changed, increment version
- `updateDelayReason`: Check version, set reason + note, log activity, increment version
- Add optimistic updates support for all mutations
- Implement retry queue with local storage fallback for failed mutations
- **Acceptance**: All mutations work in Convex dashboard, concurrent edits handled gracefully

**2.3 Job Queries** (Effort: M)
- `listJobs`: Filter by status, area, team; order by lastStatusChangeAt desc
- `getJob(id)`: Single job with team details
- `getJobsByTeam(teamId)`: Active jobs for team
- Real-time subscriptions enabled
- **Acceptance**: Queries return expected data, auto-update on mutations

**2.4 Team Queries & Mutations** (Effort: S)
- `listTeams`: All teams ordered by name
- `createTeam(name, memberNames)`: Add new team (supports "Team 1" through "Team 20" or custom names)
- `getTeamStatus(teamId)`: Returns FREE or current job details
  - FREE = no jobs with status in ['new', 'in_progress', 'delayed']
  - BUSY = show area + job number for active job
- **Acceptance**: Teams CRUD works, status logic correct (tested with sample jobs)

**2.5 Activity Queries** (Effort: M)
- `getTodayActivity`: Events from current shift start to now
  - If before 19:00, show day shift (07:00-19:00)
  - If after 19:00, show night shift (19:00-07:00 next day)
- `getActivityByDate(date)`: Historical events
- `getActivityByJob(jobId)`: Job-specific timeline
- `getActivityByTeam(teamId)`: Team-specific events
- Implement activity event archival: TTL = 30 days (auto-delete old events)
- Add Convex cron job to archive events older than 30 days
- **Acceptance**: Filtering works, correct chronological order, archival tested

**2.6 Handover Query** (Effort: M)
- `getHandoverData(date)`: Group jobs by area code (DU010, DP030, DW050, etc.)
- Per area: completed today, in_progress, delayed (with reasons), new
- Include job counts, team assignments, area module type (DU/DP/DW)
- Group by module for better organization (all DU together, all DP together, etc.)
- **Acceptance**: Data structure matches handover mockup, covers all 24 areas

---

### PHASE 3: Core UI Components

**3.1 JobCard Component** (Effort: M)
```tsx
// components/JobCard.tsx
<JobCard job={job} onTap={() => openQuickActions(job)} />
```
- Show: description (truncated), area badge, requestedByName, team badge
- Priority indicator (urgent = red border/icon)
- Status-based border color
- Min 44px tap target
- **Acceptance**: Renders all job data, tap opens modal

**3.2 StatusColumn Component** (Effort: S)
```tsx
<StatusColumn status="in_progress" jobs={jobs} />
```
- Vertical list of JobCards
- Status header with count
- Horizontal scroll on mobile (columns side-by-side)
- Empty state message
- **Acceptance**: Displays jobs, scrollable on mobile

**3.3 TeamBadge Component** (Effort: S)
- Show team name, member count
- FREE vs BUSY status color
- Tap to filter board by team
- **Acceptance**: Correct status display, tap filters work

**3.4 QuickActionsModal Component** (Effort: L)
- Bottom sheet on mobile using Radix Dialog (full modal on desktop)
- Actions: Change Status (4 buttons), Assign Team (grid), Update Delay (form)
- Each action calls Convex mutation with version check (concurrent edit protection)
- Optimistic UI updates
- Close on success with toast
- Show warning toast if job was updated by another user (version mismatch)
- **Acceptance**: All actions work, UI updates instantly, concurrent edits handled

**3.5 TodayTeamsPanel Component** (Effort: M)
- Collapsible panel (default open on desktop, closed on mobile)
- Grid of team cards showing status
- Tap team → filter board to that team's jobs
- Tap job reference → scroll to job card
- **Acceptance**: Shows correct team status, tap navigation works

**3.6 ActivityEventCard Component** (Effort: S)
- Display: timestamp, user name, action description
- Color-coded by event type
- Example: "10:23 - Ramunas assigned Team 3 to Job #24 (PAU-1)"
- **Acceptance**: Renders event data clearly

---

### PHASE 4: Main Features

**4.1 Board Page** (Effort: L)
```tsx
// app/board/page.tsx or app/page.tsx
```
- Protect route with Clerk
- Fetch jobs with `useQuery` from Convex
- Four StatusColumn components (New, In Progress, Delayed, Done)
- TodayTeamsPanel at top
- QuickActionsModal state management
- Real-time updates (Convex reactivity)
- **Acceptance**: Board displays all jobs, updates in real-time

**4.2 New Job Form** (Effort: M)
```tsx
// app/jobs/new/page.tsx
```
- Fields:
  - requestedByName (text input)
  - area (dropdown with 24 areas: DU010-510, DP030-740, DW050-350)
  - exactLocation (text input, e.g., "deck", "port side")
  - description (textarea)
  - priority (toggle: normal/urgent)
  - requiredBy (optional date picker)
- Validation with Zod + react-hook-form
- Submit → Convex `createJob` mutation
- Redirect to board with success toast
- **Acceptance**: Form validates, creates job with version=0, redirects correctly

**4.3 Top Navigation** (Effort: S)
- Logo/app name
- "Today's Teams" toggle button (mobile)
- "+ New Job" button → /jobs/new
- User menu (Clerk UserButton)
- **Acceptance**: All navigation works, responsive

**4.4 Bottom Navigation (Mobile)** (Effort: S)
- Tabs: Board | Activity | Handover
- Fixed position on mobile
- Hidden on desktop (use sidebar or top nav)
- Active state indication
- **Acceptance**: Navigation works, correct active state

---

### PHASE 5: Activity & Handover

**5.1 Activity Timeline Page** (Effort: M)
```tsx
// app/activity/page.tsx
```
- Date picker (default today)
- Filter dropdowns: team, job search
- List of ActivityEventCards
- Infinite scroll / pagination for past days
- Real-time updates for today
- **Acceptance**: Filters work, displays events correctly

**5.2 Handover Overview Page** (Effort: L)
```tsx
// app/handover/page.tsx
```
- Date selector (default today)
- Area sections (PAU-1, PAU-2, etc.)
- Per area: Completed (green), In Progress (blue), Delayed (red), New (gray)
- Show job number, description, team, delay reason
- "Copy All" button → copies formatted text
- **Acceptance**: Displays correct data, copy function works

**5.3 Handover Text Generator** (Effort: M)
- Function to convert handover data → formatted text
- Group by module type (DU, DP, DW) for clarity
```
UTILITY MODULE (DU):
  DU010:
    Completed: Job #23 (Install pipes, Team 5)
    In Progress: Job #24 (Cable routing, Team 3, continue tomorrow)
  DU110:
    Delayed: Job #25 (Waiting for crane, Team 1)

PROCESSING MODULE (DP):
  DP030:
    New: Job #28 (Valve replacement, unassigned)
  ...
```
- Plain text format (easy to copy/paste into shift log)
- **Acceptance**: Generated text covers all 24 areas, matches handover structure

---

### PHASE 6: Real-Time & Polish

**6.1 Toast Notifications** (Effort: M)
- Install `sonner` (lightweight toast library)
- Subscribe to activityEvents where userId ≠ current user
- Show toast: "{userName} {action} on Job #{id} ({area})"
- Max 3 toasts visible
- Auto-dismiss after 5 seconds
- **Acceptance**: Toasts appear for other users' actions

**6.2 Optimistic UI Updates** (Effort: M)
- Implement optimistic mutations in Convex
- Update local cache before server confirms
- Rollback on error
- Show loading indicators during mutations
- **Acceptance**: UI updates feel instant, errors handled gracefully

**6.3 Loading States** (Effort: S)
- Skeleton cards for initial job list load
- Spinner for form submissions
- Disabled states on buttons during mutations
- **Acceptance**: No blank screens, clear loading feedback

**6.4 Mobile Touch Optimizations** (Effort: S)
- Min 44px tap targets
- Swipe gestures (optional): swipe job card right/left to change status
- Prevent accidental taps (debounce)
- Touch ripple effects
- **Acceptance**: All actions easy to tap on phone

**6.5 Error Handling** (Effort: S)
- Add React error boundary to `app/layout.tsx`
- Offline indicator when Convex disconnected
- Error toasts for failed mutations
- Retry mechanism for network errors (with exponential backoff)
- Manual user sync button in admin panel (fallback if Clerk webhook fails)
- **Acceptance**: Errors communicated clearly, error boundary catches crashes, retry works

---

### PHASE 7: Deploy & Test

**7.1 Convex Production Deploy** (Effort: S)
- Run `npx convex deploy`
- Set production env vars in Convex dashboard
- Update Clerk webhook to production URL
- **Acceptance**: Prod Convex instance works

**7.2 Clerk Production Config** (Effort: S)
- Switch Clerk to production instance
- Add production domain to allowed origins
- Update JWT template issuer URL
- Test auth flow in prod
- **Acceptance**: Auth works in production

**7.3 Vercel Deployment** (Effort: S)
- Connect GitHub repo to Vercel
- Set env vars in Vercel dashboard
- Deploy to production
- Test prod URL
- **Acceptance**: App accessible at production URL

**7.4 Multi-User Testing** (Effort: M)
- Test with 6 simultaneous users (matches office staff count)
- Verify real-time updates propagate <1 second
- Test concurrent edits (two users editing same job)
- Test team swaps, status changes
- Check toast notifications appear for other users' actions
- Verify Convex backup schedule configured
- **Acceptance**: All users see updates <1 second, concurrent edits show warning toast

**7.5 Mobile Device Testing** (Effort: M)
- Test on iPhone, Android phones
- Check touch targets, scrolling
- Test quick actions modal on mobile
- Verify responsive layouts
- **Acceptance**: All features work smoothly on mobile

**7.6 Data Seeding & Training** (Effort: S)
- Create initial teams (Team 1-20 via Convex mutations)
- Verify area codes in constants match facility layout (24 areas: DU/DP/DW)
- Create 10-15 sample jobs across different areas for demo
- Create 2-minute onboarding video walkthrough
- Train 1-2 office staff (foremen/assistants)
- **Acceptance**: Real data ready, staff can create/update jobs independently

---

## Technology Decisions

**Why Convex over Supabase**:
- Built-in real-time (no manual subscriptions)
- TypeScript-first, type-safe queries
- Serverless (no DB management)
- Better DX for React integration

**Why Single-Tenant**:
- Simpler auth (no org switching)
- Faster development
- Sufficient for one office

**Why No Repository Pattern**:
- Convex functions ARE the data layer
- No need for abstraction overhead
- Simpler codebase

**Why Sonner for Toasts**:
- Lightweight (vs react-toastify)
- Beautiful defaults
- Works great with Tailwind

---

## Risk Assessment & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Real-time updates fail with many users | High | Low | Load test with 10+ simultaneous users before launch |
| Mobile performance poor on older phones | Medium | Medium | Test on iPhone 12, Samsung Galaxy A series |
| Users forget to update job status | Medium | High | Add daily reminder notifications (future) |
| Convex free tier limits hit | Low | Low | Monitor usage, upgrade plan if needed ($25/mo) |
| Clerk auth issues during shift change | High | Low | Test auth flow thoroughly, add error recovery |
| Handover text format not useful | Medium | Medium | Iterate with foremen feedback during testing |

---

## Success Metrics

**Week 1**:
- [ ] All 6 office staff using app daily
- [ ] >80% of jobs tracked in app vs paper
- [ ] Real-time updates working

**Week 2**:
- [ ] 100% of jobs in app, zero paper book usage
- [ ] <5 second load time on mobile
- [ ] Handover generated daily

**Month 1**:
- [ ] Average <10 seconds to create new job
- [ ] Team swap takes <5 taps
- [ ] >90% user satisfaction

---

## Required Resources

**Development**:
- Convex account (free tier → $25/mo if needed)
- Clerk account (free tier, 10k MAUs)
- Vercel account (free hobby tier OK)

**Testing**:
- 2-3 test users (foremen/assistants)
- iPhone + Android test devices
- 20 sample teams, 50+ sample jobs

**Skills to Activate**:
- `frontend-dev-guidelines` - React/Next.js patterns
- `backend-dev-guidelines` - If adding custom API routes (unlikely)

---

## Dependencies

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "convex": "^1.16.0",
    "@clerk/nextjs": "^6.0.0",
    "react-hook-form": "^7.53.0",
    "zod": "^3.23.0",
    "sonner": "^1.5.0",
    "date-fns": "^4.1.0",
    "lucide-react": "^0.460.0"
  },
  "devDependencies": {
    "typescript": "^5.6.0",
    "tailwindcss": "^4.0.0",
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0"
  }
}
```

---

## Resolved Questions ✅

- ✅ **Area names**: 24 facility areas confirmed
  - DU (Utility): DU010, DU110, DU120, DU310, DU320, DU410, DU420, DU510
  - DP (Processing): DP030, DP130, DP140, DP230, DP240, DP330, DP340, DP530, DP540, DP730, DP740
  - DW: DW050, DW150, DW250, DW350
- ✅ **Team naming**: "Team 1" through "Team 20" (support for custom names)
- ✅ **Shift times**: Day shift 07:00-19:00, Night shift 19:00-07:00 (Norway time)
- ✅ **User permissions**: No difference between foreman and assistant roles

## Remaining Questions (Can Defer)

- Photo attachments for jobs? (Post-MVP, add if requested during testing)
- Multi-site expansion? (Single office now, plan architecture allows future expansion)

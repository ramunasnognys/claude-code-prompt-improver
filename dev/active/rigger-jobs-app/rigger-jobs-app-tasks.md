# Rigger Job Management App - Task Checklist

**Last Updated**: 2025-11-15 (Updated with resolved questions, reordered tasks, added missing items)

---

## PHASE 1: Project Bootstrap

### 1.1 Initialize Next.js Project
- [x] Create directory `~/Developer/workspace/rigger-jobs/`
- [x] Run `npx create-next-app@latest rigger-jobs` (TypeScript, Tailwind, App Router, no src/)
- [x] Install core dependencies: `npm install convex @clerk/nextjs react-hook-form zod sonner date-fns lucide-react`
- [x] Configure `tailwind.config.ts` with mobile-first breakpoints: `screens: { xs: '375px', sm: '640px', md: '768px', lg: '1024px' }`
- [x] Create `lib/env.ts` with Zod validation for environment variables
- [x] Create `lib/constants.ts` with 24 area codes (DU/DP/DW), delay reasons, shift times (07:00-19:00, 19:00-07:00)
- [x] Test dev server: `npm run dev` loads at localhost:3000, env validation passes

### 1.2 Setup Convex
- [x] Run `npx convex dev` to initialize
- [x] Create Convex account/project (or use existing)
- [x] Copy `CONVEX_DEPLOYMENT` and `NEXT_PUBLIC_CONVEX_URL` to `.env.local`
- [x] Create `convex/tsconfig.json`
- [x] Test connection: create sample query, verify in dashboard

### 1.3 Configure Clerk Auth
- [x] Create Clerk application (single-tenant mode)
- [x] Add env vars to `.env.local`: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`
- [x] Create JWT template "convex" in Clerk dashboard
- [x] Copy issuer URL to `NEXT_PUBLIC_CLERK_FRONTEND_API_URL`
- [x] Create `middleware.ts` for route protection
- [x] Add `ClerkProvider` to `app/layout.tsx`
- [x] Test: sign-in flow works

### 1.4 Connect Clerk → Convex
- [x] Add `NEXT_PUBLIC_CLERK_FRONTEND_API_URL` to Convex dashboard env vars
- [x] Create basic `convex/schema.ts` with `users` table (clerkId, name)
- [x] Create `convex/users.ts` with basic user CRUD functions
- [x] Create `convex/http.ts` with webhook endpoint `/clerk-users-webhook`
- [x] Setup ngrok for local webhook testing: `ngrok http 3000`
- [x] Setup Clerk webhook in Clerk dashboard for `user.created`, `user.updated`, `user.deleted` (use ngrok URL in dev)
- [x] Add `CLERK_WEBHOOK_SECRET` to Convex dashboard
- [x] Test: create Clerk user, verify appears in Convex `users` table

---

## PHASE 2: Convex Backend

### 2.1 Define Schema
- [x] Update `convex/schema.ts` (already has basic users table from Phase 1.4)
- [x] Define `jobRequests` table with all fields:
  - status, dates (requestedAt, requiredBy, startedAt, completedAt, lastStatusChangeAt)
  - requestedByName, area (string for 24 codes), exactLocation, description, priority
  - assignedTeamId, delayReasonType (7 options), delayReasonNote
  - userId fields (createdBy, assignedBy, lastUpdatedBy)
  - **version** field (number) for optimistic locking
- [x] Define `teams` table (name, memberNames array)
- [x] Define `activityEvents` table (timestamp, type, jobRequestId, teamId, userId, from/to values, note, ttl)
- [x] Update `users` table (remove role field - foremen/assistants have same permissions)
- [x] Add indexes: `by_status`, `by_area`, `by_team`, `by_timestamp_desc`, `by_version`
- [x] Run `npx convex dev` to apply schema
- [x] Verify schema in Convex dashboard matches 24 facility areas

### 2.2 Job Mutations
- [x] Create `convex/jobs.ts`
- [x] Implement `createJob` mutation (validate, insert job with version=0, create activity event)
- [x] Implement `updateJobStatus` mutation (check version, change status, update timestamps, increment version, log activity)
- [x] Implement `assignTeam` mutation (check version, set team, create swap event if applicable, increment version)
- [x] Implement `updateDelayReason` mutation (check version, set reason/note, log activity, increment version)
- [x] Test all mutations in Convex dashboard
- [x] Add optimistic update support for all mutations
- [x] Implement retry queue with local storage fallback for failed mutations

### 2.3 Job Queries
- [x] Implement `listJobs` query (filter by status, area, team; order by lastStatusChangeAt desc)
- [x] Implement `getJob` query (single job by ID with team details)
- [x] Implement `getJobsByTeam` query (active jobs for specific team)
- [x] Test queries return expected data
- [x] Verify real-time subscriptions work (update data, check query auto-updates)

### 2.4 Team Queries & Mutations
- [x] Create `convex/teams.ts`
- [x] Implement `listTeams` query (all teams ordered by name)
- [x] Implement `createTeam` mutation (supports "Team 1-20" or custom names)
- [x] Implement `getTeamStatus` query:
  - FREE = no jobs with status in ['new', 'in_progress', 'delayed']
  - BUSY = return area + job number for active job
- [x] Test team CRUD operations
- [x] Verify status logic with sample jobs

### 2.5 Activity Queries
- [ ] Create `convex/activity.ts`
- [ ] Implement `getTodayActivity` query (events from current shift start):
  - If before 19:00, show day shift (07:00-19:00)
  - If after 19:00, show night shift (19:00-07:00 next day)
- [ ] Implement `getActivityByDate` query (historical events for specific date)
- [ ] Implement `getActivityByJob` query (job-specific timeline)
- [ ] Implement `getActivityByTeam` query (team-specific events)
- [ ] Implement activity event archival: TTL = 30 days (auto-delete old events)
- [ ] Add Convex cron job to archive events older than 30 days
- [ ] Test filtering works correctly
- [ ] Verify chronological order (newest first), archival tested

### 2.6 Handover Query
- [ ] Create `convex/handover.ts`
- [ ] Implement `getHandoverData` query (group jobs by area code: DU010, DP030, etc.)
- [ ] Per area: separate completed, in_progress, delayed (with reasons), new jobs
- [ ] Include job counts, team assignments, area module type (DU/DP/DW)
- [ ] Group by module for better organization (all DU together, all DP together, etc.)
- [ ] Test data structure matches handover mockup
- [ ] Verify performance with 50+ jobs across 24 areas

---

## PHASE 3: Core UI Components

### 3.1 JobCard Component
- [ ] Create `components/JobCard.tsx`
- [ ] Display: description (truncated), area badge, requestedByName, team badge
- [ ] Add priority indicator (urgent = red border/icon)
- [ ] Add status-based border color
- [ ] Ensure min 44px tap target
- [ ] Add tap handler to open QuickActionsModal
- [ ] Test rendering with sample data

### 3.2 StatusColumn Component
- [ ] Create `components/StatusColumn.tsx`
- [ ] Display status header with count
- [ ] Render vertical list of JobCards
- [ ] Add empty state message
- [ ] Make horizontal scrollable on mobile (flexbox)
- [ ] Test with various job counts

### 3.3 TeamBadge Component
- [ ] Create `components/TeamBadge.tsx`
- [ ] Show team name, member count
- [ ] Color code FREE (green) vs BUSY (blue)
- [ ] Add tap handler to filter board
- [ ] Test status display logic

### 3.4 QuickActionsModal Component
- [ ] Create `components/QuickActionsModal.tsx`
- [ ] Implement bottom sheet on mobile using Radix Dialog (full modal on desktop)
- [ ] Add "Change Status" section (4 buttons: New, In Progress, Delayed, Done)
- [ ] Add "Assign Team" section (grid of team buttons)
- [ ] Add "Update Delay" section (dropdown with 7 reasons + textarea for note)
- [ ] Connect to Convex mutations with version check (concurrent edit protection)
- [ ] Implement optimistic UI updates
- [ ] Show success toast on completion
- [ ] Show warning toast if job was updated by another user (version mismatch)
- [ ] Test all actions, including concurrent edits

### 3.5 TodayTeamsPanel Component
- [ ] Create `components/TodayTeamsPanel.tsx`
- [ ] Implement collapsible panel (default open on desktop, closed on mobile)
- [ ] Display grid of team cards with status
- [ ] Add tap handlers: tap team → filter board, tap job → scroll to card
- [ ] Test team status logic (FREE vs BUSY)

### 3.6 ActivityEventCard Component
- [ ] Create `components/ActivityEventCard.tsx`
- [ ] Display timestamp, user name, action description
- [ ] Color-code by event type (create=green, status=blue, delay=red, etc.)
- [ ] Test with sample events

---

## PHASE 4: Main Features

### 4.1 Board Page
- [ ] Create `app/page.tsx` (or `app/board/page.tsx`)
- [ ] Protect route with Clerk auth
- [ ] Fetch jobs using `useQuery(api.jobs.listJobs)`
- [ ] Render four StatusColumn components (New, In Progress, Delayed, Done)
- [ ] Add TodayTeamsPanel at top
- [ ] Implement QuickActionsModal state management
- [ ] Test real-time updates (open two browser windows, change job in one)

### 4.2 New Job Form
- [ ] Create `app/jobs/new/page.tsx`
- [ ] Add form fields:
  - requestedByName (text input)
  - area (dropdown with 24 areas: DU010-510, DP030-740, DW050-350)
  - exactLocation (text input, e.g., "deck", "port side")
  - description (textarea)
  - priority (toggle: normal/urgent)
  - requiredBy (optional date picker)
- [ ] Setup react-hook-form with Zod validation
- [ ] Connect to `createJob` mutation
- [ ] Redirect to board on success with toast
- [ ] Test form validation, creates job with version=0, redirects correctly

### 4.3 Top Navigation
- [ ] Create `components/TopNav.tsx` (or add to layout)
- [ ] Add logo/app name
- [ ] Add "Today's Teams" toggle button (mobile only)
- [ ] Add "+ New Job" button → /jobs/new
- [ ] Add Clerk UserButton
- [ ] Test responsive behavior

### 4.4 Bottom Navigation (Mobile)
- [ ] Create `components/BottomNav.tsx`
- [ ] Add tabs: Board | Activity | Handover
- [ ] Make fixed position on mobile, hidden on desktop
- [ ] Add active state styling
- [ ] Test navigation between pages

---

## PHASE 5: Activity & Handover

### 5.1 Activity Timeline Page
- [ ] Create `app/activity/page.tsx`
- [ ] Add date picker (default today)
- [ ] Add filter dropdowns: team, job search
- [ ] Fetch activity using `useQuery(api.activity.getTodayActivity)`
- [ ] Render list of ActivityEventCards
- [ ] Implement infinite scroll / pagination for past days
- [ ] Test filters and real-time updates

### 5.2 Handover Overview Page
- [ ] Create `app/handover/page.tsx`
- [ ] Add date selector (default today)
- [ ] Fetch handover data using `useQuery(api.handover.getHandoverData)`
- [ ] Render area sections (PAU-1, PAU-2, etc.)
- [ ] Color-code job lists: Completed (green), In Progress (blue), Delayed (red), New (gray)
- [ ] Add "Copy All" button
- [ ] Test data display and copy function

### 5.3 Handover Text Generator
- [ ] Create `lib/handoverFormatter.ts`
- [ ] Implement function to convert handover data → formatted text
- [ ] Format: Area → Completed/In Progress/Delayed/New jobs with details
- [ ] Test with sample data
- [ ] Integrate with "Copy All" button

---

## PHASE 6: Real-Time & Polish

### 6.1 Toast Notifications
- [ ] Install `sonner` if not already installed
- [ ] Add `Toaster` component to `app/layout.tsx`
- [ ] Subscribe to `activityEvents` where userId ≠ current user
- [ ] Show toast: "{userName} {action} on Job #{id} ({area})"
- [ ] Configure max 3 toasts, auto-dismiss after 5 seconds
- [ ] Test with two users making changes

### 6.2 Optimistic UI Updates
- [ ] Implement optimistic mutations in Convex
- [ ] Update local cache before server confirms
- [ ] Add rollback logic on error
- [ ] Show loading indicators during mutations
- [ ] Test error handling (simulate network failure)

### 6.3 Loading States
- [ ] Create skeleton cards for initial job list load
- [ ] Add spinner for form submissions
- [ ] Add disabled states on buttons during mutations
- [ ] Test loading feedback on slow connections

### 6.4 Mobile Touch Optimizations
- [ ] Audit all tap targets (min 44px)
- [ ] Add touch ripple effects (optional)
- [ ] Prevent accidental double-taps (debounce)
- [ ] (Optional) Implement swipe gestures for status change
- [ ] Test on real phone

### 6.5 Error Handling
- [ ] Add React error boundary to `app/layout.tsx`
- [ ] Add offline indicator when Convex disconnected
- [ ] Show error toasts for failed mutations
- [ ] Implement retry mechanism for network errors (with exponential backoff)
- [ ] Add manual user sync button in admin panel (fallback if Clerk webhook fails)
- [ ] Test error boundary catches crashes
- [ ] Test offline/online transitions, retry works

---

## PHASE 7: Deploy & Test

### 7.1 Convex Production Deploy
- [ ] Run `npx convex deploy` to production
- [ ] Set production env vars in Convex dashboard (`CLERK_WEBHOOK_SECRET`, `NEXT_PUBLIC_CLERK_FRONTEND_API_URL`)
- [ ] Update Clerk webhook URL to production domain
- [ ] Test Convex functions in prod dashboard

### 7.2 Clerk Production Config
- [ ] Create Clerk production instance (or switch existing app to prod mode)
- [ ] Add production domain to allowed origins
- [ ] Update JWT template issuer URL
- [ ] Test auth flow in production

### 7.3 Vercel Deployment
- [ ] Connect GitHub repo to Vercel
- [ ] Set all env vars in Vercel dashboard
- [ ] Deploy to production
- [ ] Test production URL loads correctly

### 7.4 Multi-User Testing
- [ ] Create 6 test users in Clerk prod (matches office staff count)
- [ ] Test simultaneous usage with 6 browsers/devices
- [ ] Verify real-time updates propagate <1 second
- [ ] Test concurrent edits (two users editing same job)
- [ ] Test team swaps, status changes
- [ ] Check toast notifications appear for other users' actions
- [ ] Verify Convex backup schedule configured

### 7.5 Mobile Device Testing
- [ ] Test on iPhone (Safari)
- [ ] Test on Android (Chrome)
- [ ] Check touch targets, scrolling
- [ ] Test QuickActionsModal on mobile
- [ ] Verify responsive layouts work

### 7.6 Data Seeding & Training
- [ ] Create initial teams (Team 1-20 via Convex mutations)
- [ ] Verify area codes in constants match facility layout (24 areas: DU/DP/DW)
- [ ] Create 10-15 sample jobs across different areas for demo
- [ ] Create 2-minute onboarding video walkthrough
- [ ] Train 1-2 office staff (foremen/assistants)
- [ ] Gather feedback for immediate fixes
- [ ] Verify staff can create/update jobs independently

---

## Post-MVP Improvements (Future)

- [ ] Add photo attachments to jobs
- [ ] Implement push notifications for urgent jobs
- [ ] Build analytics dashboard (job completion rates, team utilization)
- [ ] Add shift management (define shift times, auto-archive)
- [ ] Support multi-language (Norwegian + English)
- [ ] Add CSV/PDF export of activity logs
- [ ] Integrate AI for job description parsing (optional)
- [ ] Integrate AI for handover summary generation (optional)

---

## Success Criteria

### Week 1
- [ ] All 6 office staff using app daily
- [ ] >80% of jobs tracked in app vs paper
- [ ] Real-time updates working reliably

### Week 2
- [ ] 100% of jobs in app, zero paper book usage
- [ ] <5 second load time on mobile
- [ ] Handover generated daily

### Month 1
- [ ] Average <10 seconds to create new job
- [ ] Team swap takes <5 taps
- [ ] >90% user satisfaction (informal feedback)

# Rigger Job Management App - Context & Key Decisions

**Last Updated**: 2025-11-15 (Updated with resolved questions & facility layout)

## Key Files & Their Purpose

### Project Root
- `~/Developer/workspace/rigger-jobs/` - NEW project directory (not yet created)

### Core Application Files (To Be Created)

**Next.js App Structure**:
- `app/layout.tsx` - Root layout with Clerk + Convex providers
- `app/page.tsx` - Main board view (kanban)
- `app/jobs/new/page.tsx` - New job creation form
- `app/activity/page.tsx` - Activity timeline
- `app/handover/page.tsx` - Daily handover overview
- `middleware.ts` - Clerk auth protection

**Convex Backend**:
- `convex/schema.ts` - Database schema definition
- `convex/jobs.ts` - Job CRUD operations
- `convex/teams.ts` - Team management
- `convex/activity.ts` - Activity logging & queries
- `convex/handover.ts` - Handover data aggregation
- `convex/users.ts` - User sync from Clerk
- `convex/http.ts` - Webhook handlers

**React Components**:
- `components/JobCard.tsx` - Individual job card
- `components/StatusColumn.tsx` - Column container for jobs
- `components/TeamBadge.tsx` - Team status indicator
- `components/QuickActionsModal.tsx` - Bottom sheet for job actions
- `components/TodayTeamsPanel.tsx` - Team overview panel
- `components/ActivityEventCard.tsx` - Activity event display

**Configuration**:
- `.env.local` - Environment variables
- `lib/env.ts` - Environment variable validation with Zod
- `tailwind.config.ts` - Tailwind configuration with mobile breakpoints
- `lib/constants.ts` - 24 facility area codes, delay reasons, shift times

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

### 1. Convex Schema Changes
**Issue**: Schema changes require migration
**Solution**: Use `npx convex run` scripts for data migrations
**Best Practice**: Test schema changes in dev environment first

### 2. Clerk JWT Template
**Critical**: Must create "convex" JWT template in Clerk
**Gotcha**: Forgetting this breaks Convex auth
**Check**: Verify `NEXT_PUBLIC_CLERK_FRONTEND_API_URL` matches JWT issuer

### 3. Mobile Touch Targets
**Rule**: Minimum 44px × 44px for all tappable elements
**Why**: Apple/Google accessibility guidelines
**Check**: Test on real devices, not just browser resize

### 4. Real-Time Update Performance
**Concern**: With 50+ jobs across 24 areas, does board re-render lag?
**Target**: <1 second propagation with 6 concurrent users
**Mitigation**:
- Use React.memo for JobCard
- Index Convex queries by status, area, team
- Limit initial query to jobs from last 7 days
- Test with 6 simultaneous users before launch

### 5. Concurrent Edit Conflicts
**Issue**: Two users assign different teams to same job
**Solution**: Optimistic locking with version field
**UX**: Show warning toast "Job updated by {user}, please refresh"
**Critical**: Test this scenario thoroughly in Phase 7.4

### 5. Offline Handling
**Issue**: Convex requires connection for real-time
**Solution**: Show offline indicator, queue mutations when reconnected
**Future**: Add service worker for true offline support

### 6. Webhook Security
**Critical**: Verify Clerk webhook signature in Convex
**Pattern**: Use `svix` library (already in Convex)
**Gotcha**: Test webhook in prod (ngrok in dev)

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

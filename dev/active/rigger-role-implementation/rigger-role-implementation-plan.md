# Rigger Role Implementation Plan

**Last Updated**: 2025-12-05 (Post-Review)

## Executive Summary

Add restricted rigger role to rigger-jobs app using Clerk publicMetadata, Convex authorization, and Next.js route groups. Riggers get mobile-first interface showing only assigned team jobs with full interaction (view/add photos, update status/delays). Office workers keep current desktop experience with full access.

**Risk**: Low - incremental changes, existing functionality preserved
**Complexity**: Medium - multiple layers (Clerk, Convex, Next.js)

---

## Plan Review Summary (2025-12-05)

**Verdict**: Plan architecturally sound but has critical issues to address first.

### Critical Issues Identified

| Issue | Problem | Required Fix |
|-------|---------|--------------|
| **Role Sync Gap** | Convex `users.role` vs Clerk `publicMetadata` will drift | Always read role from JWT claims, sync to Convex as cache only |
| **JWT Config** | No verification step in plan | Add test to log `ctx.auth.getUserIdentity()` before proceeding |
| **User Migration** | ~50+ existing users have no role | Backfill script + default fallback to "office" |
| **Schema Mismatch** | Plan mentions `jobAssignments` table | Use existing team-based model (`job.assignedTeamId`) |

### Additional Fixes Required

| Gap | Fix |
|-----|-----|
| Photo upload permissions | Add rigger team check to `addPhotosToJob` mutation |
| Team deletion | Block deletion if riggers assigned to team |
| Expired QR handling | Add error UI for expired/used tokens |
| Rate limiting | 10 invites/hour/user max |
| Token security | Hash tokens before storage in Convex |

### Alternatives Confirmed

| Decision | Choice | Verdict |
|----------|--------|---------|
| Role storage | publicMetadata | Correct (simpler than Organizations) |
| Route structure | Route groups | Correct (cleaner separation) |
| Token storage | Convex table | Correct (QR-only flow, no email required) |

---

## Key Decisions

1. **Role Model**: Clerk publicMetadata with 3 roles (admin, office_worker, rigger)
2. **Assignment**: Keep existing team model - riggers belong to teams, jobs assigned to teams
3. **Rigger Permissions**: Full job interaction (photos, delays, status) for assigned team jobs
4. **Default Role**: Existing users → office_worker (safe, maintains access)
5. **Offline Handling**: Optimistic updates with Convex retry (built-in)
6. **Route Strategy**: (office) and (rigger) groups with separate layouts

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Clerk JWT Claims                                           │
│  • publicMetadata.role: "admin" | "office_worker" | "rigger"│
│  • userId synced to Convex users table                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Next.js Middleware (Route Protection)                      │
│  • Riggers → /my-jobs (redirect from office routes)        │
│  • Office → /dashboard (redirect from rigger routes)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  AuthenticatedLayout (Conditional Rendering)                │
│  • Riggers: BottomNav only, no sidebar                     │
│  • Office: Sidebar + BottomNav (current)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Convex Authorization (Data Layer)                          │
│  • Queries: Filter jobs by team membership for riggers     │
│  • Mutations: Validate role + team assignment              │
│  • Auth helpers: getCurrentUserWithRole, canEditJob         │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1.0: Critical Fixes (NEW - Do First)

### Goal
Address critical issues from plan review before proceeding

### Tasks

1. **Create Convex Auth Helpers** (`convex/lib/auth.ts`)
   ```typescript
   // Always read role from JWT claims, not from DB
   export async function getUserRole(ctx: QueryCtx) {
     const identity = await ctx.auth.getUserIdentity();
     const role = (identity as any)?.metadata?.role;
     return role ?? "office"; // Safe default for existing users
   }

   export async function getUserTeamId(ctx: QueryCtx) {
     const identity = await ctx.auth.getUserIdentity();
     const teamId = (identity as any)?.metadata?.teamId;
     return teamId ? (teamId as Id<"teams">) : null;
   }
   ```

2. **Update User Store** (`convex/users.ts`)
   - Sync role from JWT claims to Convex on every store() call
   - This keeps Convex in sync for queries (not authorization)

3. **Clerk JWT Configuration + Verification**
   - Clerk Dashboard → Sessions → Customize session token
   - Add: `{"metadata": "{{user.public_metadata}}"}`
   - **VERIFICATION**: Create debug query to log identity:
   ```typescript
   // convex/debug.ts (temporary)
   export const testJwtClaims = query({
     handler: async (ctx) => {
       const identity = await ctx.auth.getUserIdentity();
       return { identity };
     },
   });
   ```

4. **Existing Users Backfill**
   - Create script to set all existing users to role="office"
   - Run via Clerk Backend API or Convex migration

### Testing Checkpoint
- [ ] JWT contains metadata.role (verified via debug query)
- [ ] users.store() syncs role from JWT
- [ ] Existing users have role="office"

---

## Phase 1: Foundation

### Goal
TypeScript types, role helpers, basic middleware

### Tasks

1. **Create TypeScript Types** (`types/globals.d.ts`)
2. **Create Server Role Helpers** (`lib/roles.ts`)
3. **Create Client Role Hook** (`hooks/useRole.ts`)
4. **Update Middleware** (`middleware.ts`)

### Testing Checkpoint
- [ ] useRole() hook works
- [ ] Middleware redirects correctly

---

## Phase 2: Convex Authorization

### Goal
Implement Convex authorization using team-based model (NOT user-based)

### Tasks

1. **Update Job Queries** (`convex/jobs.ts`)
   ```typescript
   export const listJobs = query({
     handler: async (ctx, args) => {
       const role = await getUserRole(ctx);
       const teamId = await getUserTeamId(ctx);

       if (role === "rigger") {
         if (!teamId) return []; // Rigger without team sees nothing
         return await ctx.db
           .query("jobRequests")
           .withIndex("by_team", (q) => q.eq("assignedTeamId", teamId))
           .collect();
       }
       // Office/admin see all
       return await ctx.db.query("jobRequests").collect();
     },
   });
   ```

2. **Update Job Mutations** - Permission checks
3. **Add Photo Upload Protection** (`convex/jobs.ts`)
   ```typescript
   export const addPhotosToJob = mutation({
     handler: async (ctx, args) => {
       const role = await getUserRole(ctx);
       const teamId = await getUserTeamId(ctx);
       const job = await ctx.db.get(args.jobId);

       if (role === "rigger" && job.assignedTeamId !== teamId) {
         throw new Error("Cannot add photos to jobs not assigned to your team");
       }
       // ... rest of implementation
     },
   });
   ```

4. **Add Team Deletion Protection** (`convex/teams.ts`)
   ```typescript
   // Block deletion if riggers assigned
   const assignedRiggers = await ctx.db
     .query("users")
     .withIndex("by_team", (q) => q.eq("teamId", args.teamId))
     .collect();
   if (assignedRiggers.length > 0) {
     throw new Error(`Cannot delete: ${assignedRiggers.length} rigger(s) assigned`);
   }
   ```

### Testing Checkpoint
- [ ] Rigger queries filtered by team
- [ ] Rigger photo uploads restricted to team jobs
- [ ] Team deletion blocked with assigned riggers
- [ ] Unauthorized access blocked

---

## Phase 3: Rigger Mobile Interface (Days 8-12)

### Goal
Mobile-first rigger experience with /my-jobs route

### Tasks

1. **Create Bottom Navigation** (`components/rigger/BottomNavigation.tsx`)
2. **Create Mobile Header** (`components/rigger/MobileHeader.tsx`)
3. **Create Job Card** (`components/rigger/JobCard.tsx`)
4. **Create My Jobs Page** (`app/(rigger)/my-jobs/page.tsx`)
5. **Create Rigger Layout** (`app/(rigger)/layout.tsx`)
6. **Update AuthenticatedLayout** - Role-based rendering

### Testing Checkpoint
- [ ] Rigger sees bottom nav only
- [ ] Job cards have 48px+ buttons
- [ ] Status updates work
- [ ] Shows only assigned jobs

---

## Phase 4: Rigger Onboarding (QR Code Invitations)

### Goal
Admin invite system with QR codes for field worker onboarding

### Onboarding Flow
```
Foreman → Admin Panel → Teams → "Invite Rigger" → Generate Link/QR
                                                          ↓
                                          Rigger scans QR or clicks link
                                                          ↓
                                          /invite/[token] → Clerk signup
                                                          ↓
                                          Auto-assigned: role=rigger, teamId=xyz
```

### Schema Addition (with security improvements)
```typescript
invitations: defineTable({
  tokenHash: v.string(),          // SHA-256 hash of token (security)
  teamId: v.id("teams"),
  createdBy: v.id("users"),
  createdAt: v.number(),
  expiresAt: v.number(),          // 24-48 hours (not 7 days)
  usedAt: v.optional(v.number()),
  usedBy: v.optional(v.id("users")),
}).index("by_token_hash", ["tokenHash"])
```

### Tasks

1. **Add invitations to Schema** (`convex/schema.ts`)
2. **Create Invite Mutations** (`convex/invitations.ts`)
   - `createInvitation(teamId)` - admin/office only, **with rate limiting**
   - `validateInvitation(token)` - public
   - `consumeInvitation(token)` - after signup
   - `listTeamInvitations(teamId)` - admin only
   - `revokeInvitation(invitationId)` - admin only

   **Rate Limiting**: Max 10 invites per user per hour
   ```typescript
   const recentInvites = await ctx.db
     .query("invitations")
     .filter((q) =>
       q.and(
         q.eq(q.field("createdBy"), userId),
         q.gt(q.field("createdAt"), Date.now() - 3600000)
       )
     )
     .collect();
   if (recentInvites.length >= 10) {
     throw new Error("Rate limit: max 10 invites per hour");
   }
   ```

3. **Create Invite Page** (`app/invite/[token]/page.tsx`)
   - Validate token (not expired, not used)
   - **Error handling for expired/used tokens**:
     - Expired: "This invitation has expired. Please request a new one."
     - Used: "This invitation has already been used."
     - Invalid: "Invalid invitation link."
   - Show team name: "Joining Team Alpha"
   - Clerk `<SignUp />` component
   - Post-signup: call `consumeInvitation` mutation

4. **Add Invite UI to Teams Page**
   - "Invite Rigger" button per team
   - Modal with QR code + copyable link
   - List active invites with revoke option

5. **QR Code Component** (`components/InviteQRCode.tsx`)
   - Use `qrcode.react` with `level="H"` for high error correction
   - Display: `{baseUrl}/invite/{token}`

### Clerk Auth Methods for Riggers
- Email + password
- Phone SMS (ideal for field workers)
- Google OAuth (personal Gmail)

### Testing Checkpoint
- [ ] Admin can generate invite for team
- [ ] QR code renders correctly
- [ ] Token validates on /invite page
- [ ] Expired tokens show user-friendly error
- [ ] Used tokens show user-friendly error
- [ ] Rate limiting blocks excessive invite generation
- [ ] Signup creates user with role=rigger, teamId set
- [ ] Invite marked as used after redemption

---

## Phase 5: Administration UI (Days 17-18)

### Goal
Role management, user-team assignment for existing users

### Tasks

1. **Create User Management Page** (`app/(office)/admin/users/page.tsx`)
2. **Add User Mutations** - Role/team assignment
3. **Protect Admin Routes** - Add auth checks
4. **Update Sidebar** - Role-based filtering

### Testing Checkpoint
- [ ] Admin can manage users
- [ ] Non-admin redirected
- [ ] Sidebar filters by role

---

## Deployment Checklist

### Pre-Deployment
- [ ] Schema migration (users + inviteTokens)
- [ ] Set default roles for existing users
- [ ] Configure Clerk JWT with publicMetadata
- [ ] Install qrcode.react package
- [ ] Test with prod keys

### Deployment
1. Deploy Convex: `npx convex deploy --prod`
2. Deploy Next.js: `vercel --prod`
3. Assign roles to existing users
4. Generate first invite tokens for teams
5. Test rigger onboarding flow

### Post-Deployment
- [ ] Monitor errors
- [ ] Test all flows (invite → signup → access)
- [ ] Gather feedback from foremen and riggers

---

## Success Metrics

- [ ] Riggers see only assigned jobs
- [ ] Office workers keep full access
- [ ] Zero unauthorized access
- [ ] Invite → signup → access <2 min
- [ ] <1s status updates
- [ ] <5s page load
- [ ] Zero auth errors

---

## Package Dependencies

```bash
# QR code generation for invite links
npm install qrcode.react

# Unique token generation
npm install nanoid
```

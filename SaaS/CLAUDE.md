# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Next.js SaaS starter with Supabase (auth + database) and Stripe (payments). Uses magic link authentication, subscription management, and local development environment.

## Development Commands

```bash
# Development
npm run dev              # Start Next.js dev server (http://localhost:3000)
npm run build            # Build for production
npm run lint             # Run ESLint

# Supabase (local)
supabase start           # Start local Supabase (Docker required)
supabase stop            # Stop local services
supabase status          # Check running services
supabase db reset        # Reset DB and apply migrations

# Stripe (local)
stripe listen --forward-to localhost:3000/api/webhooks/stripe  # Webhook listener
stripe listen --print-secret                                     # Get webhook secret
```

## Environment Configuration

All services use `.env` for local development with easy prod switching:

- **Supabase**: Local instance runs on `http://localhost:3000` (must use localhost, not 127.0.0.1 for cookie compatibility)
- **Stripe**: Test keys pre-configured, webhook secret needs update after running `stripe listen --print-secret`
- **Local email testing**: Inbucket at http://127.0.0.1:54424

When adding new environment variables, update both `.env` and `.env.example`.

## Architecture

### Authentication Flow

**Magic Link Pattern** (passwordless):
1. User submits email → `supabase.auth.signInWithOtp()`
2. Email sent (local: Inbucket, prod: SMTP configured in Supabase Dashboard)
3. User clicks link → `/app/auth/callback/route.ts` exchanges code for session
4. Middleware (`middleware.ts`) auto-refreshes sessions on all routes

**Supabase Client Pattern**:
- Client Components: Use `lib/supabase/client.ts` (browser client)
- Server Components/API Routes: Use `lib/supabase/server.ts` (server client with cookie handling)
- Middleware: Uses `lib/supabase/middleware.ts` for session refresh

### Database Schema

Three main tables extending `auth.users`:

```
profiles          - User profile data (auto-created via trigger)
customers         - Stripe customer mapping (user_id → stripe_customer_id)
subscriptions     - Subscription status (plan, interval, period dates)
```

**Key helper functions** (callable via `supabase.rpc()`):
- `get_user_plan(user_uuid)` - Returns 'free' | 'pro' | 'enterprise'
- `has_active_subscription(user_uuid)` - Boolean check for active/trialing status
- `upsert_customer()` - Sync Stripe customer from webhook
- `upsert_subscription()` - Sync Stripe subscription from webhook
- `cancel_subscription()` - Cancel user subscription

**RLS policies**: Users can read/update own records only. Service role has full access for webhooks.

See `supabase/README.md` for full schema details and `supabase/STRIPE_WEBHOOK_GUIDE.md` for webhook integration.

### Stripe Integration

**Required webhooks** to handle:
- `customer.created` - Create customer record
- `customer.subscription.created/updated` - Sync subscription status
- `customer.subscription.deleted` - Cancel subscription

**User ID mapping**: Store Supabase user_id in Stripe customer metadata as `supabase_user_id` for webhook processing.

**Environment variables**:
- `STRIPE_SECRET_KEY` - Server-side operations
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Client-side Checkout/Elements
- `STRIPE_WEBHOOK_SECRET` - Webhook signature verification
- Price IDs for monthly/yearly plans

### Route Structure

```
app/
├── (auth)/              - Auth route group
│   ├── login/           - Magic link entry (email-only form)
│   └── signup/          - Same as login (unified flow)
├── auth/callback/       - Magic link verification route
├── dashboard/           - Protected route, shows subscription status
└── page.tsx             - Public homepage (auth-aware)
```

**Protected routes**: Check auth in Server Component, redirect to `/login` if not authenticated. Example in `app/dashboard/page.tsx`.

### Component Patterns

- **Auth components** in `/components/auth/`:
  - `AuthForm.tsx` - Email-only magic link form
  - `LogoutButton.tsx` - Client component with loading state

- **Client vs Server components**:
  - Forms/interactive UI → `'use client'` + browser Supabase client
  - Data fetching/auth checks → Server Component + server Supabase client

## Local Development Setup

1. **Docker must be running** for Supabase local
2. Ensure dev server runs on `http://localhost:3000` (not 127.0.0.1) for cookie compatibility
3. Check Inbucket (http://127.0.0.1:54424) for magic link emails during testing
4. Update `STRIPE_WEBHOOK_SECRET` in `.env` after first `stripe listen --print-secret`

## Database Migrations

Located in `supabase/migrations/`:
1. `20250126000001_create_profiles.sql` - Profiles + auto-create trigger
2. `20250126000002_create_customers.sql` - Stripe customer mapping
3. `20250126000003_create_subscriptions.sql` - Subscription tracking
4. `20250126000004_create_helpers.sql` - RPC functions for webhooks

Migrations are idempotent. Apply with `supabase db reset`.

## Production Deployment

**Environment variables to replace**:
- Supabase: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL`
- Stripe: All keys (live mode), price IDs (live products), webhook secret (from dashboard)

**Supabase**:
```bash
supabase link --project-ref <your-ref>
supabase db push  # Push migrations to prod
```

**Stripe**: Configure SMTP in Dashboard > Authentication > Email Templates for production magic links.

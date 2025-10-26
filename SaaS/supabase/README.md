# Supabase Database Schema

## Quick Start

```bash
supabase start           # Start local instance
supabase db reset        # Apply migrations
supabase studio          # Open Studio UI
```

## Schema Overview

```
auth.users (Supabase Auth)
    ↓
profiles (1:1)           customers (1:1)         subscriptions (1:1)
- id                     - id                    - user_id
- email                  - stripe_customer_id    - stripe_subscription_id
- full_name                                      - stripe_price_id
- avatar_url                                     - status (enum)
                                                 - plan (enum)
                                                 - interval (enum)
                                                 - period dates
                                                 - trial dates
```

## Enums

**subscription_status**: active | canceled | incomplete | incomplete_expired | past_due | paused | trialing | unpaid

**pricing_plan**: free | pro | enterprise

**billing_interval**: month | year

## Migrations

1. `20250126000001_create_profiles.sql` - Profiles table + auto-create trigger
2. `20250126000002_create_customers.sql` - Stripe customer mapping
3. `20250126000003_create_subscriptions.sql` - Subscription tracking + helper queries
4. `20250126000004_create_helpers.sql` - Webhook processing functions

## Key Functions

- `handle_new_user()` - Auto-creates profile on signup
- `upsert_customer()` - Sync Stripe customer
- `upsert_subscription()` - Sync Stripe subscription
- `cancel_subscription()` - Cancel user subscription
- `get_user_plan()` - Get current plan (defaults to 'free')
- `has_active_subscription()` - Check active status
- `get_subscription_claims()` - Get JWT claims data

## RLS Policies

All tables enforce:
- Users can read/update own records
- Service role has full access
- Profiles auto-created via trigger

## Stripe Integration

See [STRIPE_WEBHOOK_GUIDE.md](./STRIPE_WEBHOOK_GUIDE.md) for:
- Webhook event handling
- User ID mapping
- Application usage examples
- Production deployment

## Local URLs

- Studio: http://127.0.0.1:54423
- API: http://127.0.0.1:54421
- DB: postgresql://postgres:postgres@127.0.0.1:54422/postgres

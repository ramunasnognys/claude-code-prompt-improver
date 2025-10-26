# Stripe Webhook Integration Guide

## Overview

Schema supports Stripe subscription management via webhook processing.

## Database Schema

### Tables

#### `profiles`
Extends auth.users with custom fields
- `id` (UUID, PK) - References auth.users
- `email` (TEXT)
- `full_name` (TEXT)
- `avatar_url` (TEXT)
- `created_at`, `updated_at` (TIMESTAMPTZ)

#### `customers`
Links users to Stripe customers
- `id` (UUID, PK) - References auth.users
- `stripe_customer_id` (TEXT, unique)
- `created_at`, `updated_at` (TIMESTAMPTZ)

#### `subscriptions`
Tracks subscription status and billing
- `id` (UUID, PK)
- `user_id` (UUID, unique) - One sub per user
- `stripe_subscription_id` (TEXT, unique)
- `stripe_price_id` (TEXT)
- `status` (ENUM) - active, canceled, past_due, etc.
- `plan` (ENUM) - free, pro, enterprise
- `interval` (ENUM) - month, year
- `current_period_start`, `current_period_end` (TIMESTAMPTZ)
- `cancel_at_period_end` (BOOLEAN)
- `canceled_at`, `trial_start`, `trial_end` (TIMESTAMPTZ)

### RLS Policies

All tables:
- Users: Read/update own records
- Service role: Full access

### Helper Functions

#### `upsert_customer(user_uuid, stripe_customer_id)`
Create/update customer record

#### `upsert_subscription(...)`
Create/update subscription from webhook data
- Parameters: user_id, subscription_id, price_id, status, plan, interval, period dates, trial dates

#### `cancel_subscription(user_uuid)`
Mark subscription as canceled

#### `get_user_plan(user_uuid) → pricing_plan`
Returns user's current plan (defaults to 'free')

#### `has_active_subscription(user_uuid) → boolean`
Checks if user has active/trialing subscription

#### `get_subscription_claims(user_uuid) → jsonb`
Returns subscription data for JWT claims

## Webhook Processing

### Required Stripe Webhooks

1. **customer.created**
   ```typescript
   await supabase.rpc('upsert_customer', {
     user_uuid: userId,
     stripe_customer: customer.id
   })
   ```

2. **customer.subscription.created/updated**
   ```typescript
   await supabase.rpc('upsert_subscription', {
     user_uuid: userId,
     stripe_sub_id: subscription.id,
     stripe_price: subscription.items.data[0].price.id,
     sub_status: subscription.status,
     sub_plan: mapPriceToPlan(priceId), // 'pro' | 'enterprise'
     sub_interval: subscription.items.data[0].price.recurring.interval,
     period_start: new Date(subscription.current_period_start * 1000),
     period_end: new Date(subscription.current_period_end * 1000),
     cancel_at_end: subscription.cancel_at_period_end,
     trial_start_time: subscription.trial_start ? new Date(subscription.trial_start * 1000) : null,
     trial_end_time: subscription.trial_end ? new Date(subscription.trial_end * 1000) : null
   })
   ```

3. **customer.subscription.deleted**
   ```typescript
   await supabase.rpc('cancel_subscription', {
     user_uuid: userId
   })
   ```

### User ID Mapping

Store user ID in Stripe metadata:
```typescript
const customer = await stripe.customers.create({
  email: user.email,
  metadata: {
    supabase_user_id: user.id
  }
})
```

Retrieve in webhooks:
```typescript
const userId = customer.metadata.supabase_user_id
```

## Usage in Application

### Check subscription status
```typescript
const { data } = await supabase
  .from('subscriptions')
  .select('status, plan')
  .eq('user_id', userId)
  .single()

const isActive = data?.status === 'active' || data?.status === 'trialing'
```

### Get user plan
```typescript
const { data } = await supabase.rpc('get_user_plan', {
  user_uuid: userId
})
// Returns: 'free' | 'pro' | 'enterprise'
```

### Check if has active subscription
```typescript
const { data } = await supabase.rpc('has_active_subscription', {
  user_uuid: userId
})
// Returns: boolean
```

## Local Development

Migrations applied. Run:
```bash
supabase db reset  # Reset and apply all migrations
supabase start     # Start local instance
```

Studio: http://127.0.0.1:54423

## Production Deployment

```bash
supabase link --project-ref your-project-ref
supabase db push  # Push migrations to production
```

## Security Notes

- All functions use SECURITY DEFINER
- RLS enforced on all tables
- Service role required for webhook processing
- Users can only read own data

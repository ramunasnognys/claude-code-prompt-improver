# Database Usage Examples

## TypeScript Types

```typescript
// types/database.ts
export type SubscriptionStatus =
  | 'active'
  | 'canceled'
  | 'incomplete'
  | 'incomplete_expired'
  | 'past_due'
  | 'paused'
  | 'trialing'
  | 'unpaid'

export type PricingPlan = 'free' | 'pro' | 'enterprise'

export type BillingInterval = 'month' | 'year'

export interface Profile {
  id: string
  email: string
  full_name: string | null
  avatar_url: string | null
  created_at: string
  updated_at: string
}

export interface Subscription {
  id: string
  user_id: string
  stripe_subscription_id: string | null
  stripe_price_id: string | null
  status: SubscriptionStatus
  plan: PricingPlan
  interval: BillingInterval | null
  current_period_start: string | null
  current_period_end: string | null
  cancel_at_period_end: boolean
  canceled_at: string | null
  trial_start: string | null
  trial_end: string | null
}
```

## Client-Side Usage

### Get User Profile

```typescript
// hooks/useProfile.ts
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import type { Profile } from '@/types/database'

export function useProfile(userId?: string) {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) return

    const fetchProfile = async () => {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()

      if (!error) setProfile(data)
      setLoading(false)
    }

    fetchProfile()
  }, [userId])

  return { profile, loading }
}
```

### Update Profile

```typescript
// lib/profile.ts
export async function updateProfile(
  userId: string,
  updates: Partial<Pick<Profile, 'full_name' | 'avatar_url'>>
) {
  const { data, error } = await supabase
    .from('profiles')
    .update(updates)
    .eq('id', userId)
    .select()
    .single()

  return { data, error }
}
```

### Get User Subscription

```typescript
// hooks/useSubscription.ts
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import type { Subscription } from '@/types/database'

export function useSubscription(userId?: string) {
  const [subscription, setSubscription] = useState<Subscription | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) return

    const fetchSubscription = async () => {
      const { data, error } = await supabase
        .from('subscriptions')
        .select('*')
        .eq('user_id', userId)
        .single()

      if (!error) setSubscription(data)
      setLoading(false)
    }

    fetchSubscription()

    // Subscribe to realtime changes
    const channel = supabase
      .channel('subscription-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'subscriptions',
          filter: `user_id=eq.${userId}`
        },
        (payload) => {
          setSubscription(payload.new as Subscription)
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [userId])

  const isPro = subscription?.plan === 'pro' &&
    ['active', 'trialing'].includes(subscription.status)

  return { subscription, loading, isPro }
}
```

### Check Access

```typescript
// lib/access.ts
export async function hasProAccess(userId: string): Promise<boolean> {
  const { data } = await supabase.rpc('has_active_subscription', {
    user_uuid: userId
  })
  return data ?? false
}

export async function getUserPlan(userId: string): Promise<PricingPlan> {
  const { data } = await supabase.rpc('get_user_plan', {
    user_uuid: userId
  })
  return data ?? 'free'
}
```

## Server-Side Usage (API Routes)

### Stripe Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
import { headers } from 'next/headers'
import { stripe } from '@/lib/stripe'
import { createClient } from '@supabase/supabase-js'

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // Service role key
)

export async function POST(req: Request) {
  const body = await req.text()
  const signature = headers().get('stripe-signature')!

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    return new Response('Webhook signature verification failed', { status: 400 })
  }

  switch (event.type) {
    case 'customer.created': {
      const customer = event.data.object
      const userId = customer.metadata.supabase_user_id

      await supabaseAdmin.rpc('upsert_customer', {
        user_uuid: userId,
        stripe_customer: customer.id
      })
      break
    }

    case 'customer.subscription.created':
    case 'customer.subscription.updated': {
      const subscription = event.data.object
      const customer = await stripe.customers.retrieve(subscription.customer as string)
      const userId = (customer as Stripe.Customer).metadata.supabase_user_id

      const priceId = subscription.items.data[0].price.id
      const plan = mapPriceToPlan(priceId)

      await supabaseAdmin.rpc('upsert_subscription', {
        user_uuid: userId,
        stripe_sub_id: subscription.id,
        stripe_price: priceId,
        sub_status: subscription.status,
        sub_plan: plan,
        sub_interval: subscription.items.data[0].price.recurring?.interval,
        period_start: new Date(subscription.current_period_start * 1000).toISOString(),
        period_end: new Date(subscription.current_period_end * 1000).toISOString(),
        cancel_at_end: subscription.cancel_at_period_end,
        trial_start_time: subscription.trial_start
          ? new Date(subscription.trial_start * 1000).toISOString()
          : null,
        trial_end_time: subscription.trial_end
          ? new Date(subscription.trial_end * 1000).toISOString()
          : null
      })
      break
    }

    case 'customer.subscription.deleted': {
      const subscription = event.data.object
      const customer = await stripe.customers.retrieve(subscription.customer as string)
      const userId = (customer as Stripe.Customer).metadata.supabase_user_id

      await supabaseAdmin.rpc('cancel_subscription', {
        user_uuid: userId
      })
      break
    }
  }

  return new Response(JSON.stringify({ received: true }), { status: 200 })
}

function mapPriceToPlan(priceId: string): PricingPlan {
  const priceMap: Record<string, PricingPlan> = {
    [process.env.STRIPE_PRICE_PRO_MONTHLY!]: 'pro',
    [process.env.STRIPE_PRICE_PRO_YEARLY!]: 'pro',
    [process.env.STRIPE_PRICE_ENTERPRISE_MONTHLY!]: 'enterprise',
    [process.env.STRIPE_PRICE_ENTERPRISE_YEARLY!]: 'enterprise',
  }
  return priceMap[priceId] ?? 'free'
}
```

### Create Checkout Session

```typescript
// app/api/checkout/route.ts
import { stripe } from '@/lib/stripe'
import { createClient } from '@supabase/supabase-js'

export async function POST(req: Request) {
  const { priceId, userId } = await req.json()

  // Get or create Stripe customer
  let customerId: string

  const supabaseAdmin = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const { data: customer } = await supabaseAdmin
    .from('customers')
    .select('stripe_customer_id')
    .eq('id', userId)
    .single()

  if (customer?.stripe_customer_id) {
    customerId = customer.stripe_customer_id
  } else {
    const { data: profile } = await supabaseAdmin
      .from('profiles')
      .select('email')
      .eq('id', userId)
      .single()

    const stripeCustomer = await stripe.customers.create({
      email: profile?.email,
      metadata: { supabase_user_id: userId }
    })

    await supabaseAdmin.rpc('upsert_customer', {
      user_uuid: userId,
      stripe_customer: stripeCustomer.id
    })

    customerId = stripeCustomer.id
  }

  const session = await stripe.checkout.sessions.create({
    customer: customerId,
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/pricing`,
  })

  return Response.json({ sessionId: session.id })
}
```

## Component Examples

### Subscription Guard

```typescript
// components/SubscriptionGuard.tsx
'use client'

import { useSubscription } from '@/hooks/useSubscription'
import { useAuth } from '@/hooks/useAuth'

export function SubscriptionGuard({
  children,
  fallback
}: {
  children: React.ReactNode
  fallback?: React.ReactNode
}) {
  const { user } = useAuth()
  const { subscription, loading } = useSubscription(user?.id)

  if (loading) return <div>Loading...</div>

  const hasAccess = subscription?.status === 'active' ||
                    subscription?.status === 'trialing'

  if (!hasAccess) {
    return fallback ?? <div>Upgrade required</div>
  }

  return <>{children}</>
}
```

### Usage

```typescript
// app/dashboard/page.tsx
<SubscriptionGuard fallback={<UpgradePrompt />}>
  <ProFeature />
</SubscriptionGuard>
```

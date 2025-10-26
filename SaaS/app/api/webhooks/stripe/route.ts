import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@supabase/supabase-js'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
})

// Use service role for webhooks
const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
)

// Price ID to plan mapping
const PRICE_TO_PLAN: Record<string, { plan: string; interval: string }> = {
  [process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_MONTHLY || '']: {
    plan: 'pro',
    interval: 'month',
  },
  [process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_YEARLY || '']: {
    plan: 'pro',
    interval: 'year',
  },
  [process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_MONTHLY || '']: {
    plan: 'enterprise',
    interval: 'month',
  },
  [process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_YEARLY || '']: {
    plan: 'enterprise',
    interval: 'year',
  },
}

export async function POST(request: NextRequest) {
  const body = await request.text()
  const signature = request.headers.get('stripe-signature')

  if (!signature) {
    return NextResponse.json(
      { error: 'Missing stripe-signature header' },
      { status: 400 }
    )
  }

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (error) {
    console.error('Webhook signature verification failed:', error)
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 })
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session
        await handleCheckoutComplete(session)
        break
      }

      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription
        await handleSubscriptionUpdate(subscription)
        break
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription
        await handleSubscriptionDeleted(subscription)
        break
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice
        await handlePaymentFailed(invoice)
        break
      }

      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    return NextResponse.json({ received: true })
  } catch (error) {
    console.error('Webhook handler error:', error)
    return NextResponse.json(
      { error: 'Webhook handler failed' },
      { status: 500 }
    )
  }
}

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const customerId = session.customer as string
  const userId = session.metadata?.supabase_user_id

  if (!userId) {
    console.error('No supabase_user_id in session metadata')
    return
  }

  // Store customer if not exists
  const { error: customerError } = await supabaseAdmin.rpc('upsert_customer', {
    user_uuid: userId,
    stripe_customer: customerId,
  })

  if (customerError) {
    console.error('Error upserting customer:', customerError)
  }

  // If subscription is in the session, fetch it
  if (session.subscription) {
    const subscription = await stripe.subscriptions.retrieve(
      session.subscription as string
    )
    await handleSubscriptionUpdate(subscription)
  }
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  const customerId = subscription.customer as string
  const priceId = subscription.items.data[0]?.price.id

  if (!priceId) {
    console.error('No price ID in subscription')
    return
  }

  // Get user ID from customer
  const customer = await stripe.customers.retrieve(customerId)
  if (customer.deleted) {
    console.error('Customer deleted')
    return
  }

  const userId = customer.metadata?.supabase_user_id

  if (!userId) {
    console.error('No supabase_user_id in customer metadata')
    return
  }

  // Map price to plan
  const planInfo = PRICE_TO_PLAN[priceId]
  if (!planInfo) {
    console.error('Unknown price ID:', priceId)
    return
  }

  // Upsert subscription
  const { error } = await supabaseAdmin.rpc('upsert_subscription', {
    user_uuid: userId,
    stripe_sub_id: subscription.id,
    stripe_price: priceId,
    sub_status: subscription.status,
    sub_plan: planInfo.plan,
    sub_interval: planInfo.interval,
    period_start: subscription.current_period_start
      ? new Date(subscription.current_period_start * 1000).toISOString()
      : null,
    period_end: subscription.current_period_end
      ? new Date(subscription.current_period_end * 1000).toISOString()
      : null,
    cancel_at_end: subscription.cancel_at_period_end,
    canceled: subscription.canceled_at
      ? new Date(subscription.canceled_at * 1000).toISOString()
      : null,
    trial_start_time: subscription.trial_start
      ? new Date(subscription.trial_start * 1000).toISOString()
      : null,
    trial_end_time: subscription.trial_end
      ? new Date(subscription.trial_end * 1000).toISOString()
      : null,
  })

  if (error) {
    console.error('Error upserting subscription:', error)
  }
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription) {
  const customerId = subscription.customer as string

  // Get user ID from customer
  const customer = await stripe.customers.retrieve(customerId)
  if (customer.deleted) {
    console.error('Customer deleted')
    return
  }

  const userId = customer.metadata?.supabase_user_id

  if (!userId) {
    console.error('No supabase_user_id in customer metadata')
    return
  }

  // Cancel subscription in DB
  const { error } = await supabaseAdmin.rpc('cancel_subscription', {
    user_uuid: userId,
  })

  if (error) {
    console.error('Error canceling subscription:', error)
  }
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  const customerId = invoice.customer as string
  const subscriptionId = invoice.subscription as string

  if (!subscriptionId) {
    return
  }

  // Get subscription to update status
  const subscription = await stripe.subscriptions.retrieve(subscriptionId)
  await handleSubscriptionUpdate(subscription)
}

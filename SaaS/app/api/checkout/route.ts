import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
})

// Price mapping
const PRICE_IDS = {
  pro_monthly: process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_MONTHLY!,
  pro_yearly: process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_YEARLY!,
  enterprise_monthly: process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_MONTHLY!,
  enterprise_yearly: process.env.NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_YEARLY!,
}

export async function POST(request: NextRequest) {
  try {
    const supabase = await createClient()

    // Check auth
    const { data: { user }, error: userError } = await supabase.auth.getUser()

    if (userError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    // Parse request body
    const body = await request.json()
    const { plan, interval } = body

    // Validate inputs
    if (!plan || !interval) {
      return NextResponse.json(
        { error: 'Missing plan or interval' },
        { status: 400 }
      )
    }

    if (!['pro', 'enterprise'].includes(plan)) {
      return NextResponse.json({ error: 'Invalid plan' }, { status: 400 })
    }

    if (!['monthly', 'yearly'].includes(interval)) {
      return NextResponse.json({ error: 'Invalid interval' }, { status: 400 })
    }

    // Get price ID
    const priceKey = `${plan}_${interval}` as keyof typeof PRICE_IDS
    const priceId = PRICE_IDS[priceKey]

    if (!priceId || priceId === 'price_xxx') {
      return NextResponse.json(
        { error: 'Price ID not configured' },
        { status: 500 }
      )
    }

    // Get or create customer
    const { data: customer } = await supabase
      .from('customers')
      .select('stripe_customer_id')
      .eq('id', user.id)
      .single()

    let customerId = customer?.stripe_customer_id

    // Create customer if doesn't exist
    if (!customerId) {
      const stripeCustomer = await stripe.customers.create({
        email: user.email!,
        metadata: {
          supabase_user_id: user.id,
        },
      })
      customerId = stripeCustomer.id

      // Store customer in DB
      await supabase
        .from('customers')
        .upsert({
          id: user.id,
          stripe_customer_id: customerId,
        })
    }

    // Create checkout session
    const origin = request.headers.get('origin') || process.env.NEXT_PUBLIC_SUPABASE_URL
    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'subscription',
      success_url: `${origin}/dashboard?success=true`,
      cancel_url: `${origin}/dashboard?canceled=true`,
      metadata: {
        supabase_user_id: user.id,
      },
    })

    return NextResponse.json({ url: session.url })
  } catch (error) {
    console.error('Checkout error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

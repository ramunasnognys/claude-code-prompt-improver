# Stripe Payment System Setup

Complete Stripe integration for SaaS subscription management.

## Features

- 3 pricing tiers: Free, Pro ($14.99/mo or $143.90/yr), Enterprise ($99.99/mo or $959.90/yr)
- Checkout flow with customer creation
- Webhook handling for all subscription events
- Customer portal for billing management
- Subscription cancellation
- Pricing grid UI component
- Dashboard subscription management

## Setup Instructions

### 1. Install Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Login to Stripe
stripe login
```

### 2. Create Stripe Products

Run the setup script to create products and prices:

```bash
bash scripts/setup-stripe-products.sh
```

This creates:
- Pro Plan product with monthly/yearly prices
- Enterprise Plan product with monthly/yearly prices

Copy the output price IDs to your `.env` file.

### 3. Configure Environment Variables

Update `.env` with the price IDs from step 2:

```bash
NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_MONTHLY=price_xxx
NEXT_PUBLIC_STRIPE_PRICE_ID_PRO_YEARLY=price_xxx
NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_MONTHLY=price_xxx
NEXT_PUBLIC_STRIPE_PRICE_ID_ENTERPRISE_YEARLY=price_xxx
```

### 4. Set Up Webhook Secret

Start Stripe webhook forwarding:

```bash
stripe listen --forward-to http://localhost:3000/api/webhooks/stripe
```

Copy the webhook signing secret from the output and update `.env`:

```bash
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## Testing

### Test Checkout Flow

1. Start dev server:
```bash
npm run dev
```

2. Start webhook listener in another terminal:
```bash
stripe listen --forward-to http://localhost:3000/api/webhooks/stripe
```

3. Navigate to dashboard and test:
   - Click upgrade button
   - Complete checkout with test card: `4242 4242 4242 4242`
   - Verify subscription appears in dashboard
   - Check webhook events in terminal

### Test Stripe Events

Trigger events manually:

```bash
# Test successful subscription
stripe trigger checkout.session.completed

# Test subscription update
stripe trigger customer.subscription.updated

# Test payment failure
stripe trigger invoice.payment_failed

# Test subscription cancellation
stripe trigger customer.subscription.deleted
```

### Test Flows

**Free → Pro (Monthly)**
1. Login as free user
2. Click "Subscribe to Pro"
3. Select "Monthly"
4. Complete checkout
5. Verify plan updated in dashboard

**Free → Pro (Yearly)**
1. Login as free user
2. Click "Subscribe to Pro"
3. Select "Yearly"
4. Verify 20% discount shown
5. Complete checkout

**Pro → Enterprise (Upgrade)**
1. Login as Pro user
2. Click "Subscribe to Enterprise"
3. Complete checkout
4. Verify upgrade in dashboard

**Cancel Subscription**
1. Login as paid user
2. Click "Cancel Subscription"
3. Confirm cancellation
4. Verify "cancel at period end" message

**Manage Billing (Portal)**
1. Login as paid user
2. Click "Manage Billing"
3. Verify portal opens
4. Test changing payment method

## API Routes

- `POST /api/checkout` - Create checkout session
- `POST /api/webhooks/stripe` - Handle webhook events
- `POST /api/create-portal-session` - Create customer portal session
- `POST /api/cancel-subscription` - Cancel subscription at period end

## Webhook Events Handled

- `checkout.session.completed` - Create customer & subscription
- `customer.subscription.created` - Initial subscription
- `customer.subscription.updated` - Updates, renewals, upgrades
- `customer.subscription.deleted` - Cancellations
- `invoice.payment_failed` - Payment issues

## Database Schema

Uses existing Supabase helper functions:
- `upsert_customer(user_uuid, stripe_customer)` - Store customer
- `upsert_subscription(...)` - Store/update subscription
- `cancel_subscription(user_uuid)` - Mark subscription canceled

## Components

**Pricing**
- `PricingGrid` - Display all pricing tiers
- `PricingCard` - Individual pricing card with monthly/yearly toggle

**Dashboard**
- `ManageSubscriptionButton` - Opens customer portal
- `CancelSubscriptionButton` - Cancels subscription with confirmation

## Production Deployment

1. Update `.env` with live Stripe keys
2. Configure webhook endpoint in Stripe Dashboard:
   - URL: `https://yourdomain.com/api/webhooks/stripe`
   - Events: Select all subscription & invoice events
3. Copy webhook signing secret to production env
4. Test with live mode test cards before going live

## Test Cards

- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Requires auth: `4000 0025 0000 3155`

Use any future expiry date and any CVC.

## Troubleshooting

**Webhook signature verification failed**
- Ensure `STRIPE_WEBHOOK_SECRET` matches CLI output
- Restart webhook listener after env changes

**Price ID not configured**
- Verify all 4 price IDs are in `.env`
- Check for typos in price IDs

**No subscription found**
- Check webhook events processed successfully
- Verify customer metadata has `supabase_user_id`
- Check Supabase logs for RPC errors

**Checkout session not redirecting**
- Verify `NEXT_PUBLIC_SUPABASE_URL` is set
- Check browser console for errors

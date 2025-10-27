# Stripe Subscription Upgrade Debug Report

**Date:** 2025-10-27
**Issue:** User completed Stripe checkout but subscription remained "free" instead of upgrading to paid plan

---

## Root Cause

**PORT MISMATCH between Stripe webhook listener and Next.js dev server**

- Stripe webhook listener was forwarding to: `http://localhost:3002/api/webhooks/stripe`
- Next.js dev server was actually running on: `http://localhost:3003`
- Webhooks were created in Stripe but never reached the application
- No customer/subscription records were created in database

---

## Evidence

### 1. Stripe Events Created Successfully
- Event: `evt_1SMijXG3aHdr0luRjLaWcrZn` (checkout.session.completed)
- Event: `evt_1SMijXG3aHdr0luRHYPaFy8a` (customer.subscription.updated)
- Customer: `cus_TJLPtZBgVP9g3R`
- Subscription: `sub_1SMijUG3aHdr0luRRGawNh59`
- Price: `price_1SMMwTG3aHdr0luRXi8HKono` (Enterprise Monthly)
- User: `6a427a1d-77d8-440f-b0c9-e027b1e2304b`

### 2. Database State Before Fix
```sql
SELECT * FROM customers;  -- 0 rows
SELECT * FROM subscriptions;  -- 0 rows
```

### 3. Webhook Listener Output Before Fix
- Listener running with correct webhook secret
- NO forwarded events shown in output
- Endpoint check returned 405 (method not allowed for GET, but endpoint exists)

### 4. Database State After Fix
```sql
-- Customer created
SELECT * FROM customers;
id: 6a427a1d-77d8-440f-b0c9-e027b1e2304b
stripe_customer_id: cus_TJLPtZBgVP9g3R

-- Subscription synced
SELECT * FROM subscriptions;
user_id: 6a427a1d-77d8-440f-b0c9-e027b1e2304b
stripe_subscription_id: sub_1SMijUG3aHdr0luRRGawNh59
status: active
plan: enterprise
interval: month

-- RPC functions verified
SELECT get_user_plan('6a427a1d-77d8-440f-b0c9-e027b1e2304b'::uuid);
-- Returns: "enterprise"

SELECT has_active_subscription('6a427a1d-77d8-440f-b0c9-e027b1e2304b'::uuid);
-- Returns: true
```

### 5. Webhook Listener Output After Fix
```
2025-10-27 07:19:12   --> checkout.session.completed [evt_1SMijXG3aHdr0luRjLaWcrZn]
2025-10-27 07:19:13  <--  [200] POST http://localhost:3003/api/webhooks/stripe
2025-10-27 07:20:27   --> customer.subscription.updated [evt_1SMijXG3aHdr0luRHYPaFy8a]
2025-10-27 07:20:28  <--  [200] POST http://localhost:3003/api/webhooks/stripe
```

---

## Fix Applied

1. Killed webhook listener on wrong port: `stripe listen --forward-to http://localhost:3002/api/webhooks/stripe`
2. Started listener on correct port: `stripe listen --forward-to http://localhost:3003/api/webhooks/stripe`
3. Resent original webhook events using Stripe CLI:
   - `stripe events resend evt_1SMijXG3aHdr0luRjLaWcrZn` (checkout.session.completed)
   - `stripe events resend evt_1SMijXG3aHdr0luRHYPaFy8a` (customer.subscription.updated)
4. Verified database records created successfully
5. Verified RPC functions return correct values

---

## Verification

All components verified working:

- [x] Supabase local instance running (port 54421)
- [x] Next.js dev server running (port 3003)
- [x] Stripe webhook listener running on correct port (3003)
- [x] Webhook secret configured correctly in .env
- [x] Price IDs configured correctly in .env
- [x] RPC functions exist in database:
  - `upsert_customer`
  - `upsert_subscription`
  - `get_user_plan`
  - `has_active_subscription`
  - `cancel_subscription`
- [x] Customer record created
- [x] Subscription record created with correct plan (enterprise) and interval (month)
- [x] User plan returns "enterprise"
- [x] Active subscription check returns true

---

## Prevention

### Immediate Actions Required

1. **Document the correct port** in project setup docs
2. **Add port check** to webhook listener startup script
3. **Add health check** endpoint that logs webhook reception

### Recommended Improvements

1. **Environment variable for dev server port**
   ```bash
   # .env.local
   PORT=3003
   ```

2. **Startup script** to ensure consistent port usage:
   ```bash
   # scripts/start-dev.sh
   #!/bin/bash
   PORT=3003
   npm run dev -- -p $PORT &
   stripe listen --forward-to http://localhost:$PORT/api/webhooks/stripe
   ```

3. **Add webhook logging** to webhook handler:
   ```typescript
   export async function POST(request: NextRequest) {
     console.log('[Webhook] Received event:', {
       signature: request.headers.get('stripe-signature')?.substring(0, 20) + '...',
       timestamp: new Date().toISOString()
     })
     // ... rest of handler
   }
   ```

4. **Add health check endpoint** (`app/api/webhooks/stripe/health/route.ts`):
   ```typescript
   export async function GET() {
     return NextResponse.json({
       status: 'ok',
       timestamp: new Date().toISOString()
     })
   }
   ```

5. **Update CLAUDE.md** with port requirements:
   ```markdown
   ## Critical: Port Configuration
   - Dev server MUST run on same port as webhook listener
   - Default: port 3003
   - Webhook listener command: stripe listen --forward-to http://localhost:3003/api/webhooks/stripe
   - NEVER use 127.0.0.1 - use localhost for Supabase cookie compatibility
   ```

---

## Test Approach for Future Upgrades

### Pre-checkout Verification
```bash
# 1. Verify all services running
supabase status
lsof -i :3003  # Check Next.js dev server port
ps aux | grep "stripe listen"  # Check webhook listener

# 2. Verify webhook listener port matches dev server
# Look for: "forward-to http://localhost:3003"

# 3. Test webhook endpoint
curl http://localhost:3003/api/webhooks/stripe
# Should return 405 (method not allowed), not connection refused
```

### Post-checkout Verification
```bash
# 1. Check webhook listener output for forwarded events
# Should see: "--> checkout.session.completed"
# Should see: "<-- [200] POST http://localhost:3003/api/webhooks/stripe"

# 2. Query database
docker exec supabase_db_SaaS psql -U postgres -d postgres -c \
  "SELECT * FROM customers WHERE id = '<user_id>';"

docker exec supabase_db_SaaS psql -U postgres -d postgres -c \
  "SELECT * FROM subscriptions WHERE user_id = '<user_id>';"

# 3. Verify RPC functions
docker exec supabase_db_SaaS psql -U postgres -d postgres -c \
  "SELECT get_user_plan('<user_id>'::uuid);"
# Should return: 'pro' or 'enterprise', not 'free'
```

### Manual Webhook Resend (if needed)
```bash
# 1. Get event ID from Stripe CLI
stripe events list --limit 5

# 2. Resend specific event
stripe events resend evt_<event_id>

# 3. Verify in webhook listener output
# Should see successful 200 response
```

---

## Summary

**What happened:** User paid for enterprise plan, but webhooks never reached app due to port mismatch.

**Immediate fix:** Restarted webhook listener on correct port (3003), resent webhook events.

**Current status:** Subscription fully synced, user showing enterprise plan.

**Long-term fix:** Document port requirements, add startup script, add webhook logging/health checks.

-- Helper functions for Stripe webhook processing

-- Function to upsert customer record
CREATE OR REPLACE FUNCTION public.upsert_customer(
  user_uuid UUID,
  stripe_customer TEXT
)
RETURNS void AS $$
BEGIN
  INSERT INTO public.customers (id, stripe_customer_id)
  VALUES (user_uuid, stripe_customer)
  ON CONFLICT (id)
  DO UPDATE SET
    stripe_customer_id = EXCLUDED.stripe_customer_id,
    updated_at = NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to upsert subscription record from Stripe webhook
CREATE OR REPLACE FUNCTION public.upsert_subscription(
  user_uuid UUID,
  stripe_sub_id TEXT,
  stripe_price TEXT,
  sub_status TEXT,
  sub_plan TEXT,
  sub_interval TEXT DEFAULT NULL,
  period_start TIMESTAMPTZ DEFAULT NULL,
  period_end TIMESTAMPTZ DEFAULT NULL,
  cancel_at_end BOOLEAN DEFAULT FALSE,
  canceled TIMESTAMPTZ DEFAULT NULL,
  trial_start_time TIMESTAMPTZ DEFAULT NULL,
  trial_end_time TIMESTAMPTZ DEFAULT NULL
)
RETURNS void AS $$
BEGIN
  INSERT INTO public.subscriptions (
    user_id,
    stripe_subscription_id,
    stripe_price_id,
    status,
    plan,
    interval,
    current_period_start,
    current_period_end,
    cancel_at_period_end,
    canceled_at,
    trial_start,
    trial_end
  )
  VALUES (
    user_uuid,
    stripe_sub_id,
    stripe_price,
    sub_status::subscription_status,
    sub_plan::pricing_plan,
    sub_interval::billing_interval,
    period_start,
    period_end,
    cancel_at_end,
    canceled,
    trial_start_time,
    trial_end_time
  )
  ON CONFLICT (user_id)
  DO UPDATE SET
    stripe_subscription_id = EXCLUDED.stripe_subscription_id,
    stripe_price_id = EXCLUDED.stripe_price_id,
    status = EXCLUDED.status,
    plan = EXCLUDED.plan,
    interval = EXCLUDED.interval,
    current_period_start = EXCLUDED.current_period_start,
    current_period_end = EXCLUDED.current_period_end,
    cancel_at_period_end = EXCLUDED.cancel_at_period_end,
    canceled_at = EXCLUDED.canceled_at,
    trial_start = EXCLUDED.trial_start,
    trial_end = EXCLUDED.trial_end,
    updated_at = NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to cancel subscription
CREATE OR REPLACE FUNCTION public.cancel_subscription(user_uuid UUID)
RETURNS void AS $$
BEGIN
  UPDATE public.subscriptions
  SET
    status = 'canceled'::subscription_status,
    canceled_at = NOW(),
    updated_at = NOW()
  WHERE user_id = user_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get subscription details for JWT claims
CREATE OR REPLACE FUNCTION public.get_subscription_claims(user_uuid UUID)
RETURNS jsonb AS $$
DECLARE
  claims jsonb;
BEGIN
  SELECT jsonb_build_object(
    'subscription_status', status,
    'subscription_plan', plan,
    'subscription_interval', interval
  ) INTO claims
  FROM public.subscriptions
  WHERE user_id = user_uuid
  LIMIT 1;

  -- Return default free plan if no subscription
  RETURN COALESCE(
    claims,
    jsonb_build_object(
      'subscription_status', 'active',
      'subscription_plan', 'free',
      'subscription_interval', null
    )
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

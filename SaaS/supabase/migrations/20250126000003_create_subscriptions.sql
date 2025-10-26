-- Create subscriptions table for Stripe subscription management
-- Tracks subscription status, plan type, and billing period

-- Create subscription status enum
DO $$ BEGIN
  CREATE TYPE subscription_status AS ENUM (
    'active',
    'canceled',
    'incomplete',
    'incomplete_expired',
    'past_due',
    'paused',
    'trialing',
    'unpaid'
  );
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- Create pricing plan enum
DO $$ BEGIN
  CREATE TYPE pricing_plan AS ENUM (
    'free',
    'pro',
    'enterprise'
  );
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

-- Create billing interval enum
DO $$ BEGIN
  CREATE TYPE billing_interval AS ENUM (
    'month',
    'year'
  );
EXCEPTION
  WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS public.subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_subscription_id TEXT UNIQUE,
  stripe_price_id TEXT,
  status subscription_status NOT NULL DEFAULT 'incomplete',
  plan pricing_plan NOT NULL DEFAULT 'free',
  interval billing_interval,
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  canceled_at TIMESTAMPTZ,
  trial_start TIMESTAMPTZ,
  trial_end TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Ensure one active subscription per user
  CONSTRAINT unique_user_subscription UNIQUE(user_id)
);

-- Enable RLS
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;

-- RLS Policies for subscriptions
-- Users can view their own subscription
DROP POLICY IF EXISTS "Users can view own subscription" ON public.subscriptions;
CREATE POLICY "Users can view own subscription"
  ON public.subscriptions
  FOR SELECT
  USING (auth.uid() = user_id);

-- Service role can manage all subscriptions
DROP POLICY IF EXISTS "Service role can manage all subscriptions" ON public.subscriptions;
CREATE POLICY "Service role can manage all subscriptions"
  ON public.subscriptions
  FOR ALL
  USING (auth.jwt()->>'role' = 'service_role')
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

-- Add updated_at trigger
DROP TRIGGER IF EXISTS on_subscription_updated ON public.subscriptions;
CREATE TRIGGER on_subscription_updated
  BEFORE UPDATE ON public.subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_updated_at();

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS subscriptions_user_id_idx ON public.subscriptions(user_id);
CREATE INDEX IF NOT EXISTS subscriptions_stripe_subscription_id_idx ON public.subscriptions(stripe_subscription_id);
CREATE INDEX IF NOT EXISTS subscriptions_status_idx ON public.subscriptions(status);

-- Create function to get user's current subscription plan
CREATE OR REPLACE FUNCTION public.get_user_plan(user_uuid UUID)
RETURNS pricing_plan AS $$
DECLARE
  user_plan pricing_plan;
BEGIN
  SELECT plan INTO user_plan
  FROM public.subscriptions
  WHERE user_id = user_uuid
    AND status IN ('active', 'trialing')
  LIMIT 1;

  -- Default to free if no active subscription
  RETURN COALESCE(user_plan, 'free'::pricing_plan);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to check if user has active subscription
CREATE OR REPLACE FUNCTION public.has_active_subscription(user_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1
    FROM public.subscriptions
    WHERE user_id = user_uuid
      AND status IN ('active', 'trialing')
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

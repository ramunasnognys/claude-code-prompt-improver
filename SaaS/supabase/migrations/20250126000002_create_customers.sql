-- Create customers table for Stripe integration
-- Links Supabase users to Stripe customer IDs

CREATE TABLE IF NOT EXISTS public.customers (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_customer_id TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.customers ENABLE ROW LEVEL SECURITY;

-- RLS Policies for customers
-- Users can view their own customer record
DROP POLICY IF EXISTS "Users can view own customer" ON public.customers;
CREATE POLICY "Users can view own customer"
  ON public.customers
  FOR SELECT
  USING (auth.uid() = id);

-- Service role can manage all customers
DROP POLICY IF EXISTS "Service role can manage all customers" ON public.customers;
CREATE POLICY "Service role can manage all customers"
  ON public.customers
  FOR ALL
  USING (auth.jwt()->>'role' = 'service_role')
  WITH CHECK (auth.jwt()->>'role' = 'service_role');

-- Add updated_at trigger
DROP TRIGGER IF EXISTS on_customer_updated ON public.customers;
CREATE TRIGGER on_customer_updated
  BEFORE UPDATE ON public.customers
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_updated_at();

-- Create index for Stripe customer ID lookups
CREATE INDEX IF NOT EXISTS customers_stripe_customer_id_idx ON public.customers(stripe_customer_id);

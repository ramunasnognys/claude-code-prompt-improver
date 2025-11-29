-- Fix RLS policy for email_signups to allow service role access
--
-- Problem: The previous policy used `auth.uid() is null` which doesn't work
-- because service role has a valid uid (all zeros). This blocked service role
-- from reading email_signups for admin operations like exports.
--
-- Solution: Check for service_role JWT claim instead

-- Drop the broken policy
drop policy if exists "Service role can read email signups" on public.email_signups;

-- Create corrected policy that properly detects service role
create policy "Service role can read email signups"
  on public.email_signups
  for select
  using (
    (current_setting('request.jwt.claims', true)::json->>'role') = 'service_role'
  );

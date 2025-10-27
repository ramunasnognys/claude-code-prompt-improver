-- Create email_signups table for landing page email captures
create table if not exists public.email_signups (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  source_page text, -- which landing page they signed up from
  created_at timestamptz not null default now(),
  unique(email)
);

-- Enable RLS
alter table public.email_signups enable row level security;

-- Allow anyone to insert (for landing page forms)
create policy "Anyone can insert email signups"
  on public.email_signups
  for insert
  with check (true);

-- Only service role can read (for admin purposes)
create policy "Service role can read email signups"
  on public.email_signups
  for select
  using (auth.uid() is null); -- Service role doesn't have uid

-- Create index for faster queries
create index email_signups_email_idx on public.email_signups(email);
create index email_signups_created_at_idx on public.email_signups(created_at desc);

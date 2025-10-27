-- Create usage_tracking table
create table if not exists public.usage_tracking (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  month integer not null,
  year integer not null,
  image_count integer not null default 0,
  last_reset timestamptz not null default now(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(user_id, month, year)
);

-- Enable RLS
alter table public.usage_tracking enable row level security;

-- RLS policies: users can only read their own usage
create policy "Users can view own usage tracking"
  on public.usage_tracking
  for select
  using (auth.uid() = user_id);

create policy "Users can insert own usage tracking"
  on public.usage_tracking
  for insert
  with check (auth.uid() = user_id);

create policy "Users can update own usage tracking"
  on public.usage_tracking
  for update
  using (auth.uid() = user_id);

-- Create index for faster queries
create index usage_tracking_user_id_idx on public.usage_tracking(user_id);
create index usage_tracking_month_year_idx on public.usage_tracking(year, month);

-- Function to get current usage for a user
create or replace function get_current_usage(user_uuid uuid)
returns table(image_count integer, month integer, year integer) as $$
declare
  current_month integer := extract(month from now());
  current_year integer := extract(year from now());
begin
  return query
  select ut.image_count, ut.month, ut.year
  from usage_tracking ut
  where ut.user_id = user_uuid
    and ut.month = current_month
    and ut.year = current_year;
end;
$$ language plpgsql security definer;

-- Function to increment usage
create or replace function increment_usage(user_uuid uuid)
returns void as $$
declare
  current_month integer := extract(month from now());
  current_year integer := extract(year from now());
begin
  insert into usage_tracking (user_id, month, year, image_count, last_reset, updated_at)
  values (user_uuid, current_month, current_year, 1, now(), now())
  on conflict (user_id, month, year)
  do update set
    image_count = usage_tracking.image_count + 1,
    updated_at = now();
end;
$$ language plpgsql security definer;

-- Function to check if user can generate (returns usage limit based on plan)
create or replace function check_generation_limit(user_uuid uuid)
returns table(can_generate boolean, current_count integer, limit_count integer, plan_name text) as $$
declare
  user_plan text;
  usage_count integer := 0;
  plan_limit integer;
  current_month integer := extract(month from now());
  current_year integer := extract(year from now());
begin
  -- Get user plan
  select get_user_plan(user_uuid) into user_plan;

  -- Set limits based on plan
  case user_plan
    when 'free' then plan_limit := 10;
    when 'pro' then plan_limit := 300;
    when 'enterprise' then plan_limit := 999999; -- unlimited
    else plan_limit := 10; -- default to free
  end case;

  -- Get current usage
  select coalesce(ut.image_count, 0) into usage_count
  from usage_tracking ut
  where ut.user_id = user_uuid
    and ut.month = current_month
    and ut.year = current_year;

  -- If no record found, usage_count will be NULL, so set to 0
  usage_count := coalesce(usage_count, 0);

  -- Return result
  return query
  select (usage_count < plan_limit), usage_count, plan_limit, user_plan;
end;
$$ language plpgsql security definer;

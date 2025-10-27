-- Create image_generations table
create table if not exists public.image_generations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  prompt text not null,
  image_url text,
  model_used text not null default 'google/gemini-2.5-flash-image',
  created_at timestamptz not null default now()
);

-- Enable RLS
alter table public.image_generations enable row level security;

-- RLS policies: users can only read their own generations
create policy "Users can view own image generations"
  on public.image_generations
  for select
  using (auth.uid() = user_id);

create policy "Users can insert own image generations"
  on public.image_generations
  for insert
  with check (auth.uid() = user_id);

-- Create index for faster queries
create index image_generations_user_id_idx on public.image_generations(user_id);
create index image_generations_created_at_idx on public.image_generations(created_at desc);

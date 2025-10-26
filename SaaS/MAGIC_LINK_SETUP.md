# Magic Link Authentication Setup

## Overview
Passwordless authentication using Supabase magic links. Users receive email with secure link to sign in.

## Local Testing

### 1. Start Dev Server
```bash
npm run dev
```

### 2. Access Sign In
Navigate to: http://localhost:3000/login or http://localhost:3000/signup (both use same form)

### 3. Enter Email
Submit any email address (e.g., test@example.com)

### 4. Check Inbucket
Open: http://127.0.0.1:54424

- All local emails appear in Inbucket inbox
- Click email to view magic link
- Click "Confirm your signup" link to authenticate
- Redirects to homepage on success

## Flow

1. User enters email → `signInWithOtp()` called
2. Supabase sends email with magic link
3. Link contains auth code → routes to `/auth/callback`
4. Callback exchanges code for session
5. User redirected to homepage (authenticated)

## Files Modified

### `/components/auth/AuthForm.tsx`
- Removed password field
- Uses `signInWithOtp()` instead of `signInWithPassword()`
- Shows "Check your email" state after submission
- Single form for both login/signup

### `/app/auth/callback/route.ts` (NEW)
- Handles magic link verification
- Exchanges code for session
- Redirects authenticated users

### `/app/(auth)/login/page.tsx`
- Updated to use new passwordless AuthForm

### `/app/(auth)/signup/page.tsx`
- Updated to use same passwordless AuthForm

### `/.env`
- Added Inbucket notes for local testing
- Added production email config instructions

## Production Setup

### Supabase Dashboard
1. Go to Authentication > Email Templates
2. Configure SMTP provider (SendGrid, AWS SES, etc.)
3. Customize magic link email template
4. Set `auth.email.enable_confirmations = true`

### Email Template Variables
- `{{ .ConfirmationURL }}` - Magic link URL
- `{{ .SiteURL }}` - Your site URL
- `{{ .Email }}` - User's email

## Security

- Links expire in 1 hour (default)
- One-time use only
- PKCE flow for additional security
- No password storage/management needed

## Benefits

- Better UX (no password to remember)
- Reduced security risk (no password leaks)
- Faster signup/login flow
- Mobile-friendly

import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { cookies } from 'next/headers'

export async function GET(request: Request) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')
  const next = requestUrl.searchParams.get('next') ?? '/'

  if (code) {
    const cookieStore = await cookies()
    const supabase = await createClient()

    const { error } = await supabase.auth.exchangeCodeForSession(code)

    if (!error) {
      // Redirect to home or specified page
      return NextResponse.redirect(new URL(next, requestUrl.origin))
    }
  }

  // If no code or error, redirect to login
  return NextResponse.redirect(new URL('/login', requestUrl.origin))
}

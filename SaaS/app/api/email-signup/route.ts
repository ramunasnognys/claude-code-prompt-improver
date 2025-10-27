import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function POST(request: Request) {
  try {
    const { email, sourcePage } = await request.json();

    if (!email || typeof email !== 'string') {
      return NextResponse.json(
        { error: 'Email is required' },
        { status: 400 }
      );
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Invalid email address' },
        { status: 400 }
      );
    }

    const supabase = await createClient();

    // Insert email signup (will silently fail if duplicate due to unique constraint)
    const { error } = await supabase
      .from('email_signups')
      .insert({
        email: email.toLowerCase(),
        source_page: sourcePage || null
      });

    // Ignore duplicate errors
    if (error && !error.message.includes('duplicate')) {
      console.error('Email signup error:', error);
      return NextResponse.json(
        { error: 'Failed to save email' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Email saved successfully'
    });

  } catch (error: any) {
    console.error('Email signup error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to save email' },
      { status: 500 }
    );
  }
}

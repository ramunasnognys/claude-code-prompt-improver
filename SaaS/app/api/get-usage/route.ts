import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function GET() {
  try {
    const supabase = await createClient();

    // Check auth
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get usage limits
    const { data: limitData, error: limitError } = await supabase
      .rpc('check_generation_limit', { user_uuid: user.id })
      .single();

    if (limitError) {
      console.error('Limit check error:', limitError);
      return NextResponse.json(
        { error: 'Failed to check usage limits' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      current: limitData.current_count,
      limit: limitData.limit_count,
      plan: limitData.plan_name,
      can_generate: limitData.can_generate
    });

  } catch (error: any) {
    console.error('Get usage error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to get usage' },
      { status: 500 }
    );
  }
}

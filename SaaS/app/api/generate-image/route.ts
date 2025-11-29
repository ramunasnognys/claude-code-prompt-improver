import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: "https://openrouter.ai/api/v1",
  apiKey: process.env.OPENROUTER_API_KEY,
});

export async function POST(request: Request) {
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

    const { prompt } = await request.json();

    if (!prompt || typeof prompt !== 'string') {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      );
    }

    // Check usage limits
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

    if (!limitData.can_generate) {
      return NextResponse.json(
        {
          error: 'Usage limit reached',
          current_count: limitData.current_count,
          limit_count: limitData.limit_count,
          plan_name: limitData.plan_name
        },
        { status: 429 }
      );
    }

    // Generate image using OpenRouter
    // IMPORTANT: Must include modalities parameter to get image output
    const completion = await openai.chat.completions.create({
      model: "google/gemini-2.5-flash-image",
      messages: [
        {
          role: "user",
          content: prompt
        }
      ],
      // @ts-ignore - OpenRouter-specific parameter
      modalities: ["text", "image"]
    });

    // Debug: Log the entire response to see structure
    console.log('OpenRouter API Response:', JSON.stringify(completion, null, 2));

    // Extract image URL from response
    // Gemini Flash Image returns base64 data URL in message.images array
    const message = completion.choices[0]?.message as any;

    console.log('Message object:', JSON.stringify(message, null, 2));
    console.log('Has images array?', !!message?.images);
    console.log('Images array:', message?.images);

    const imageUrl = message?.images?.[0]?.image_url?.url;

    if (!imageUrl) {
      console.error('No image in response. Full message:', JSON.stringify(message, null, 2));
      console.error('Message content:', message?.content);
      return NextResponse.json(
        { error: 'No image generated', debug: { message, hasImages: !!message?.images, images: message?.images } },
        { status: 500 }
      );
    }

    console.log('Successfully extracted image URL (length):', imageUrl?.length);

    // Save generation to database
    const { data: generation, error: saveError } = await supabase
      .from('image_generations')
      .insert({
        user_id: user.id,
        prompt: prompt,
        image_url: imageUrl, // Store the base64 data URL
        model_used: 'google/gemini-2.5-flash-image'
      })
      .select()
      .single();

    if (saveError) {
      console.error('Save error:', saveError);
      return NextResponse.json(
        { error: 'Failed to save generation' },
        { status: 500 }
      );
    }

    // Increment usage count
    const { error: incrementError } = await supabase
      .rpc('increment_usage', { user_uuid: user.id });

    if (incrementError) {
      console.error('Increment error:', incrementError);
      return NextResponse.json(
        { error: 'Failed to update usage count' },
        { status: 500 }
      );
    }

    // Query actual usage after increment to ensure UI shows correct count
    const { data: updatedLimit, error: limitError } = await supabase
      .rpc('check_generation_limit', { user_uuid: user.id })
      .single();

    if (limitError || !updatedLimit) {
      console.error('Failed to query updated usage:', limitError);
      // Fallback to optimistic count if query fails
      return NextResponse.json({
        success: true,
        generation: generation,
        usage: {
          current: limitData.current_count + 1,
          limit: limitData.limit_count,
          plan: limitData.plan_name
        }
      });
    }

    return NextResponse.json({
      success: true,
      generation: generation,
      usage: {
        current: updatedLimit.current_count,
        limit: updatedLimit.limit_count,
        plan: updatedLimit.plan_name
      }
    });

  } catch (error: any) {
    console.error('Image generation error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to generate image' },
      { status: 500 }
    );
  }
}

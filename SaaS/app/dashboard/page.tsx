import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { LogoutButton } from '@/components/auth/LogoutButton'
import { DashboardClient } from '@/components/image-gen/DashboardClient'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = await createClient()

  // Check auth
  const { data: { user }, error: userError } = await supabase.auth.getUser()

  if (userError || !user) {
    redirect('/login')
  }

  // Fetch image generations
  const { data: generations } = await supabase
    .from('image_generations')
    .select('*')
    .eq('user_id', user.id)
    .order('created_at', { ascending: false })
    .limit(20)

  // Get usage data
  const { data: usageData } = await supabase
    .rpc('check_generation_limit', { user_uuid: user.id })
    .single()

  const usage = {
    current: usageData?.current_count || 0,
    limit: usageData?.limit_count || 10,
    plan: usageData?.plan_name || 'free'
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b-2 border-gray-200 bg-white/90 backdrop-blur-md sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">NB</span>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Nano Banana
            </h1>
          </div>
          <nav className="flex gap-4 items-center">
            <Link
              href="/"
              className="text-gray-700 hover:text-purple-600 font-semibold px-4 py-2 transition-colors"
            >
              Home
            </Link>
            <Link
              href="/pricing"
              className="text-gray-700 hover:text-purple-600 font-semibold px-4 py-2 transition-colors"
            >
              Pricing
            </Link>
            <span className="text-gray-600 text-sm">{user.email}</span>
            <LogoutButton />
          </nav>
        </div>
      </header>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Welcome Section */}
        <div className="mb-12 text-center">
          <h2 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent mb-4">
            Create Amazing AI Art
          </h2>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Transform your ideas into stunning visuals with the power of AI. Just describe what you imagine.
          </p>
        </div>

        {/* Dashboard Client Component */}
        <DashboardClient
          initialGenerations={generations || []}
          initialUsage={usage}
        />
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white/50 backdrop-blur-sm mt-24">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-gray-600">
          <p>&copy; 2025 Nano Banana. Powered by AI.</p>
        </div>
      </footer>
    </main>
  )
}

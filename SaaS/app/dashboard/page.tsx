import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { LogoutButton } from '@/components/auth/LogoutButton'
import Link from 'next/link'

export default async function DashboardPage() {
  const supabase = await createClient()

  // Check auth
  const { data: { user }, error: userError } = await supabase.auth.getUser()

  if (userError || !user) {
    redirect('/login')
  }

  // Fetch subscription data
  const { data: subscription } = await supabase
    .from('subscriptions')
    .select('plan, status, current_period_end')
    .eq('user_id', user.id)
    .single()

  const plan = subscription?.plan || 'free'
  const status = subscription?.status || 'active'
  const periodEnd = subscription?.current_period_end

  // Plan badge colors
  const planColors = {
    free: 'bg-gray-100 border-gray-300 text-gray-800',
    pro: 'bg-blue-100 border-blue-300 text-blue-800',
    enterprise: 'bg-purple-100 border-purple-300 text-purple-800'
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b border-gray-300 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">SaaS App</h1>
          <nav className="flex gap-4 items-center">
            <Link
              href="/"
              className="text-gray-800 hover:text-blue-600 font-semibold px-4 py-2 transition-colors"
            >
              Home
            </Link>
            <span className="text-gray-700">{user.email}</span>
            <LogoutButton />
          </nav>
        </div>
      </header>

      {/* Dashboard Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-4xl font-extrabold text-gray-900 mb-2">
            Welcome back!
          </h2>
          <p className="text-gray-700 text-lg">
            Logged in as <span className="font-semibold">{user.email}</span>
          </p>
        </div>

        {/* Subscription Card */}
        <div className="bg-white rounded-lg shadow-md border border-gray-300 p-8 mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Subscription Details</h3>

          <div className="space-y-4">
            {/* Current Plan */}
            <div className="flex items-center justify-between pb-4 border-b border-gray-200">
              <div>
                <p className="text-sm text-gray-600 mb-1">Current Plan</p>
                <div className="flex items-center gap-3">
                  <span className={`px-4 py-2 rounded-lg border-2 font-bold text-lg uppercase ${planColors[plan as keyof typeof planColors]}`}>
                    {plan}
                  </span>
                  <span className="text-sm text-gray-600">
                    Status: <span className="font-semibold capitalize">{status}</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Period End (if applicable) */}
            {periodEnd && (
              <div className="pb-4 border-b border-gray-200">
                <p className="text-sm text-gray-600 mb-1">Current Period Ends</p>
                <p className="text-gray-900 font-semibold">
                  {new Date(periodEnd).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </p>
              </div>
            )}

            {/* Plan Features */}
            <div className="pt-2">
              <p className="text-sm text-gray-600 mb-3">Plan Includes</p>
              <ul className="space-y-2">
                {plan === 'free' && (
                  <>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> Basic features
                    </li>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> Community support
                    </li>
                  </>
                )}
                {plan === 'pro' && (
                  <>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> All basic features
                    </li>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> Advanced analytics
                    </li>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> Priority support
                    </li>
                  </>
                )}
                {plan === 'enterprise' && (
                  <>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> All pro features
                    </li>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> Custom integrations
                    </li>
                    <li className="flex items-center text-gray-700">
                      <span className="mr-2">✓</span> Dedicated support
                    </li>
                  </>
                )}
              </ul>
            </div>

            {/* Upgrade CTA for Free Users */}
            {plan === 'free' && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <p className="text-gray-700 mb-4">
                  Upgrade to unlock more features and capabilities
                </p>
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors shadow-md">
                  Upgrade Plan
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Dashboard Content Placeholder */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md border border-gray-300 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Quick Stats</h3>
            <p className="text-gray-700">Dashboard analytics coming soon...</p>
          </div>

          <div className="bg-white rounded-lg shadow-md border border-gray-300 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Recent Activity</h3>
            <p className="text-gray-700">Activity feed coming soon...</p>
          </div>

          <div className="bg-white rounded-lg shadow-md border border-gray-300 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Settings</h3>
            <p className="text-gray-700">Account settings coming soon...</p>
          </div>

          <div className="bg-white rounded-lg shadow-md border border-gray-300 p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Resources</h3>
            <p className="text-gray-700">Documentation and guides coming soon...</p>
          </div>
        </div>
      </div>
    </main>
  )
}

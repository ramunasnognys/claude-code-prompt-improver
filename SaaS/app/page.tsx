import { createClient } from '@/lib/supabase/server'
import { LogoutButton } from '@/components/auth/LogoutButton'
import Link from 'next/link'

export default async function Home() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="border-b border-gray-300 bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">SaaS App</h1>
          <nav className="flex gap-4 items-center">
            {user ? (
              <>
                <span className="text-gray-700">
                  {user.email}
                </span>
                <LogoutButton />
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="text-gray-800 hover:text-blue-600 font-semibold px-4 py-2 transition-colors"
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg transition-colors"
                >
                  Sign up
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-5xl font-extrabold text-gray-900 mb-6 leading-tight">
            Build your SaaS product faster
          </h2>
          <p className="text-xl text-gray-700 mb-8 leading-relaxed">
            Next.js + Supabase starter with authentication, database, and payments ready to go.
            Start building features instead of boilerplate.
          </p>

          {user ? (
            <div className="space-y-4">
              <div className="bg-green-100 border border-green-400 text-green-700 px-6 py-4 rounded-lg inline-block">
                You&apos;re logged in! Default tier: Free
              </div>
              <div className="flex gap-4 justify-center">
                <Link
                  href="/dashboard"
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-lg text-lg transition-colors shadow-md"
                >
                  Go to Dashboard
                </Link>
              </div>
            </div>
          ) : (
            <div className="flex gap-4 justify-center">
              <Link
                href="/signup"
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-4 rounded-lg text-lg transition-colors shadow-md"
              >
                Get started free
              </Link>
              <Link
                href="/login"
                className="bg-white hover:bg-gray-100 border-2 border-gray-400 text-gray-800 font-semibold px-8 py-4 rounded-lg text-lg transition-colors"
              >
                Sign in
              </Link>
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-300">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Authentication</h3>
            <p className="text-gray-700">
              Secure auth with Supabase. Email/password, magic links, and OAuth ready.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-300">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Database</h3>
            <p className="text-gray-700">
              PostgreSQL database with row-level security and real-time subscriptions.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-300">
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Subscription Tiers</h3>
            <p className="text-gray-700">
              Free, Pro, and Enterprise tiers built in. Ready for Stripe integration.
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}

import { createClient } from '@/lib/supabase/server'
import { LogoutButton } from '@/components/auth/LogoutButton'
import Link from 'next/link'
import { ReactNode } from 'react'

export async function LandingLayout({ children }: { children: ReactNode }) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b-2 border-gray-200 bg-white/90 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl flex items-center justify-center">
              <span className="text-white font-bold text-xl">NB</span>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Nano Banana
            </h1>
          </Link>
          <nav className="flex gap-4 items-center">
            <Link href="/features" className="text-gray-700 hover:text-purple-600 font-semibold px-4 py-2 transition-colors">
              Features
            </Link>
            <Link href="/pricing" className="text-gray-700 hover:text-purple-600 font-semibold px-4 py-2 transition-colors">
              Pricing
            </Link>
            {user ? (
              <>
                <Link href="/dashboard" className="text-gray-700 hover:text-purple-600 font-semibold px-4 py-2 transition-colors">
                  Dashboard
                </Link>
                <LogoutButton />
              </>
            ) : (
              <>
                <Link href="/login" className="text-gray-800 hover:text-purple-600 font-semibold px-4 py-2 transition-colors">
                  Login
                </Link>
                <Link href="/signup" className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold px-6 py-2 rounded-lg transition-all shadow-md">
                  Sign up
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      {children}

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white/50 backdrop-blur-sm mt-20">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">NB</span>
                </div>
                <span className="font-bold text-gray-900">Nano Banana</span>
              </div>
              <p className="text-gray-600 text-sm">AI-powered image generation</p>
            </div>

            <div>
              <h4 className="font-bold text-gray-900 mb-4">Product</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/features" className="text-gray-600 hover:text-purple-600">Features</Link></li>
                <li><Link href="/pricing" className="text-gray-600 hover:text-purple-600">Pricing</Link></li>
                <li><Link href="/examples" className="text-gray-600 hover:text-purple-600">Examples</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold text-gray-900 mb-4">Use Cases</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/for-creators" className="text-gray-600 hover:text-purple-600">For Creators</Link></li>
                <li><Link href="/for-businesses" className="text-gray-600 hover:text-purple-600">For Businesses</Link></li>
                <li><Link href="/use-cases" className="text-gray-600 hover:text-purple-600">All Use Cases</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-bold text-gray-900 mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/ai-art" className="text-gray-600 hover:text-purple-600">About AI Art</Link></li>
                <li><Link href="/fast-generation" className="text-gray-600 hover:text-purple-600">Technology</Link></li>
                <li><Link href="/unlimited-creativity" className="text-gray-600 hover:text-purple-600">Enterprise</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-300 mt-8 pt-8 text-center text-gray-600 text-sm">
            <p>&copy; 2025 Nano Banana. Powered by AI.</p>
          </div>
        </div>
      </footer>
    </main>
  )
}

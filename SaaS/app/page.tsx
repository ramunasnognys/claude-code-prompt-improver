import { createClient } from '@/lib/supabase/server'
import { LogoutButton } from '@/components/auth/LogoutButton'
import { EmailCapture } from '@/components/landing/EmailCapture'
import Link from 'next/link'

export default async function Home() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      {/* Header */}
      <header className="border-b-2 border-gray-200 bg-white/90 backdrop-blur-md sticky top-0 z-50">
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

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="text-center max-w-4xl mx-auto">
          <h2 className="text-6xl font-extrabold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent mb-6 leading-tight">
            Transform Words into Stunning AI Art
          </h2>
          <p className="text-xl text-gray-700 mb-12 leading-relaxed max-w-2xl mx-auto">
            Create breathtaking images from simple text descriptions. No design skills needed.
            Powered by cutting-edge AI technology.
          </p>

          {user ? (
            <Link
              href="/dashboard"
              className="inline-block bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold px-10 py-5 rounded-xl text-lg transition-all shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
            >
              Start Creating
            </Link>
          ) : (
            <div className="flex flex-col items-center gap-6">
              <EmailCapture sourcePage="homepage-hero" buttonText="Start Free" />
              <p className="text-sm text-gray-600">
                No credit card required • 10 free images monthly
              </p>
            </div>
          )}
        </div>

        {/* Feature Preview */}
        <div className="mt-20 grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Lightning Fast</h3>
            <p className="text-gray-600">Generate images in seconds with our optimized AI models</p>
          </div>

          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Professional Quality</h3>
            <p className="text-gray-600">Create stunning visuals perfect for any project</p>
          </div>

          <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 hover:shadow-xl transition-shadow">
            <div className="w-12 h-12 bg-gradient-to-br from-pink-500 to-pink-600 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Unlimited Creativity</h3>
            <p className="text-gray-600">Enterprise plan offers unlimited image generation</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-purple-600 to-blue-600 py-20">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h3 className="text-4xl font-bold text-white mb-6">
            Ready to Create Something Amazing?
          </h3>
          <p className="text-xl text-purple-100 mb-8">
            Join thousands of creators using Nano Banana to bring their ideas to life
          </p>
          {!user && (
            <div className="flex justify-center">
              <Link
                href="/signup"
                className="bg-white hover:bg-gray-100 text-purple-600 font-bold px-10 py-4 rounded-xl text-lg transition-all shadow-xl transform hover:-translate-y-1"
              >
                Get Started Free
              </Link>
            </div>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold">NB</span>
                </div>
                <span className="font-bold text-gray-900">Nano Banana</span>
              </div>
              <p className="text-gray-600 text-sm">AI-powered image generation for everyone</p>
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

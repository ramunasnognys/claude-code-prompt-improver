import { LandingLayout } from '@/components/landing/LandingLayout'
import { EmailCapture } from '@/components/landing/EmailCapture'
import Link from 'next/link'

export default async function UnlimitedCreativityPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            Unlimited Creativity Awaits
          </h1>
          <p className="text-xl text-gray-700">Enterprise plan removes all limits. Create without boundaries.</p>
        </div>

        <div className="bg-white rounded-2xl shadow-2xl border-2 border-purple-200 p-12 mb-16">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Enterprise Plan</h2>
            <div className="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600 mb-4">
              Unlimited
            </div>
            <p className="text-xl text-gray-700">Images per month</p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 mb-12">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Everything Included:</h3>
              <ul className="space-y-3">
                {[
                  'Unlimited image generations',
                  'Priority processing queue',
                  'Dedicated account manager',
                  'Custom model training',
                  'API access',
                  'Advanced analytics',
                  'Team collaboration tools',
                  '24/7 premium support'
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-3">
                    <svg className="w-6 h-6 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-800 font-semibold">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Perfect For:</h3>
              <ul className="space-y-3">
                {[
                  'Marketing agencies',
                  'Large creative teams',
                  'E-commerce platforms',
                  'Publishing companies',
                  'Design studios',
                  'Enterprise organizations'
                ].map((type, i) => (
                  <li key={i} className="flex items-center gap-3">
                    <span className="w-2 h-2 bg-purple-600 rounded-full"></span>
                    <span className="text-gray-800">{type}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="text-center">
            <Link
              href="/pricing"
              className="inline-block bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-bold px-10 py-4 rounded-xl text-lg transition-all shadow-xl transform hover:-translate-y-1"
            >
              View Pricing
            </Link>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Ready to Go Unlimited?</h2>
          <p className="text-xl text-purple-100 mb-8">Contact us for custom enterprise pricing</p>
          <div className="flex justify-center">
            <EmailCapture sourcePage="unlimited-creativity" buttonText="Contact Sales" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}

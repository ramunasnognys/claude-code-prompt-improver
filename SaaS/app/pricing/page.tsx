import { LandingLayout } from '@/components/landing/LandingLayout'
import { PricingGrid } from '@/components/pricing/PricingGrid'

export default async function PricingPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-gray-700">Choose the plan that fits your creative needs</p>
        </div>

        <div className="mb-16">
          <PricingGrid currentPlan="free" />
        </div>

        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">What's Included in All Plans</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              'High-quality AI image generation',
              'Image history & saved generations',
              'Usage tracking dashboard',
              'Download generated images',
              'Commercial usage rights',
              'Regular model updates'
            ].map((feature, i) => (
              <div key={i} className="flex items-center gap-3">
                <svg className="w-6 h-6 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-gray-800">{feature}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">Need a Custom Plan?</h2>
          <p className="text-xl text-purple-100 mb-8">Contact us for enterprise solutions tailored to your organization</p>
        </div>
      </section>
    </LandingLayout>
  )
}

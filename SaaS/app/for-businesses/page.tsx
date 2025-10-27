import { LandingLayout } from '@/components/landing/LandingLayout'
import { EmailCapture } from '@/components/landing/EmailCapture'

export default async function ForBusinessesPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            Enterprise AI Image Generation
          </h1>
          <p className="text-xl text-gray-700">Scale your marketing and design operations with unlimited AI-powered visuals</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {[
            { title: 'Unlimited Generation', desc: 'No limits on Enterprise plan. Create as much as you need.' },
            { title: 'Team Collaboration', desc: 'Multiple team members can access and create together.' },
            { title: 'Priority Support', desc: 'Dedicated support team to help your business succeed.' },
            { title: 'Usage Analytics', desc: 'Track team usage and ROI with detailed analytics.' },
            { title: 'API Access', desc: 'Integrate directly into your existing workflows.' },
            { title: 'Custom Solutions', desc: 'Tailored plans and features for large organizations.' }
          ].map((feature, i) => (
            <div key={i} className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
              <p className="text-gray-600">{feature.desc}</p>
            </div>
          ))}
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Transform Your Business</h2>
          <p className="text-xl text-purple-100 mb-8">Contact us for custom enterprise pricing</p>
          <div className="flex justify-center">
            <EmailCapture sourcePage="for-businesses" buttonText="Contact Sales" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}

import { LandingLayout } from '@/components/landing/LandingLayout'
import { EmailCapture } from '@/components/landing/EmailCapture'

export default async function FastGenerationPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            Lightning-Fast AI Image Generation
          </h1>
          <p className="text-xl text-gray-700">From prompt to image in seconds, not minutes</p>
        </div>

        <div className="grid md:grid-cols-2 gap-12 mb-16">
          <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Why Speed Matters</h2>
            <div className="space-y-4">
              <p className="text-gray-700">In today's fast-paced world, waiting for images is lost productivity. Nano Banana delivers professional-quality images in seconds, keeping your workflow moving.</p>
              <div className="bg-purple-50 border-2 border-purple-200 rounded-lg p-6">
                <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600 mb-2">
                  &lt; 10s
                </div>
                <p className="text-gray-700 font-semibold">Average generation time</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-xl p-8 border border-gray-200">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Optimized Technology</h2>
            <ul className="space-y-4">
              {[
                'Powered by Google Gemini 2.5 Flash',
                'Optimized cloud infrastructure',
                'Parallel processing capabilities',
                'Global CDN for instant delivery',
                'Real-time generation monitoring'
              ].map((item, i) => (
                <li key={i} className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Experience the Speed</h2>
          <div className="flex justify-center">
            <EmailCapture sourcePage="fast-generation" buttonText="Try Now" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}

import { LandingLayout } from '@/components/landing/LandingLayout'
import { EmailCapture } from '@/components/landing/EmailCapture'

export default async function AIArtPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            The Future of Art is AI
          </h1>
          <p className="text-xl text-gray-700">Democratizing creativity through advanced artificial intelligence</p>
        </div>

        <div className="prose prose-lg max-w-3xl mx-auto mb-16">
          <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200 mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">What is AI Art?</h2>
            <p className="text-gray-700 leading-relaxed">
              AI art is created using machine learning models trained on millions of images. These models understand patterns, styles, and compositions, allowing them to generate entirely new images from text descriptions.
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200 mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Nano Banana?</h2>
            <p className="text-gray-700 leading-relaxed mb-4">
              We use cutting-edge Google Gemini models to deliver professional-quality images at lightning speed. Our platform makes AI art accessible to everyone, from beginners to professionals.
            </p>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-center gap-2">
                <span className="text-purple-600">✓</span> State-of-the-art AI models
              </li>
              <li className="flex items-center gap-2">
                <span className="text-purple-600">✓</span> Simple text-to-image interface
              </li>
              <li className="flex items-center gap-2">
                <span className="text-purple-600">✓</span> No technical knowledge required
              </li>
              <li className="flex items-center gap-2">
                <span className="text-purple-600">✓</span> Commercial usage rights included
              </li>
            </ul>
          </div>
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Experience AI Art Today</h2>
          <div className="flex justify-center">
            <EmailCapture sourcePage="ai-art" buttonText="Get Started" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}

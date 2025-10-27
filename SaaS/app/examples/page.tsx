import { LandingLayout } from '@/components/landing/LandingLayout'
import { EmailCapture } from '@/components/landing/EmailCapture'

const examples = [
  'A serene mountain landscape at sunset with vibrant purple and orange skies',
  'Futuristic city with neon lights and flying cars in cyberpunk style',
  'Portrait of a wise old wizard with long beard and magical staff',
  'Abstract geometric patterns in blue and gold metallic tones',
  'Cute cartoon banana character with sunglasses relaxing on beach',
  'Professional product photo of luxury watch on marble surface'
]

export default async function ExamplesPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            Inspiration Gallery
          </h1>
          <p className="text-xl text-gray-700">See what's possible with Nano Banana</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {examples.map((example, i) => (
            <div key={i} className="bg-gradient-to-br from-purple-100 to-blue-100 rounded-xl p-8 border-2 border-purple-200 min-h-[250px] flex items-center justify-center">
              <p className="text-gray-800 text-center italic">"{example}"</p>
            </div>
          ))}
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Create Your Own Masterpiece</h2>
          <div className="flex justify-center">
            <EmailCapture sourcePage="examples" buttonText="Get Started" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}

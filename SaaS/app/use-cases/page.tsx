import { LandingLayout } from '@/components/landing/LandingLayout'
import { EmailCapture } from '@/components/landing/EmailCapture'
import Link from 'next/link'

export default async function UseCasesPage() {
  return (
    <LandingLayout>
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-5xl font-extrabold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-6">
            AI Art for Every Need
          </h1>
          <p className="text-xl text-gray-700">Discover how Nano Banana powers creativity across industries</p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {[
            { title: 'Social Media Content', desc: 'Eye-catching visuals for posts, stories, and ads', icon: '📱' },
            { title: 'Marketing Materials', desc: 'Professional graphics for campaigns and presentations', icon: '📊' },
            { title: 'Product Design', desc: 'Concept art and mockups for product development', icon: '🎨' },
            { title: 'Website Graphics', desc: 'Hero images, backgrounds, and visual elements', icon: '🌐' },
            { title: 'Book Covers', desc: 'Stunning covers for novels, eBooks, and guides', icon: '📚' },
            { title: 'Personal Projects', desc: 'Art for hobbies, gifts, and creative expression', icon: '💡' }
          ].map((useCase, i) => (
            <div key={i} className="bg-white rounded-xl shadow-lg p-8 border border-gray-200 hover:shadow-xl transition-shadow">
              <div className="text-5xl mb-4">{useCase.icon}</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">{useCase.title}</h3>
              <p className="text-gray-600">{useCase.desc}</p>
            </div>
          ))}
        </div>

        <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-12 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Ready to Transform Your Workflow?</h2>
          <div className="flex justify-center">
            <EmailCapture sourcePage="use-cases" buttonText="Start Now" />
          </div>
        </div>
      </section>
    </LandingLayout>
  )
}

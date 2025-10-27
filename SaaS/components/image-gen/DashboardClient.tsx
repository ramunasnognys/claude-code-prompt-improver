'use client'

import { useState, useEffect } from 'react'
import { ImageGenerator } from './ImageGenerator'
import { ImageDisplay } from './ImageDisplay'
import { UsageTracker } from './UsageTracker'
import { ImageHistory } from './ImageHistory'

interface Generation {
  id: string
  prompt: string
  image_url: string
  created_at: string
}

interface DashboardClientProps {
  initialGenerations: Generation[]
  initialUsage: {
    current: number
    limit: number
    plan: string
  }
}

export function DashboardClient({ initialGenerations, initialUsage }: DashboardClientProps) {
  const [generations, setGenerations] = useState<Generation[]>(initialGenerations)
  const [usage, setUsage] = useState(initialUsage)
  const [isGenerating, setIsGenerating] = useState(false)
  const [currentImage, setCurrentImage] = useState<string | null>(null)
  const [currentPrompt, setCurrentPrompt] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async (prompt: string) => {
    setIsGenerating(true)
    setError(null)

    try {
      const response = await fetch('/api/generate-image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
      })

      const data = await response.json()

      if (!response.ok) {
        if (response.status === 429) {
          setError(`Usage limit reached! You've used ${data.current_count}/${data.limit_count} images on the ${data.plan_name} plan.`)
        } else {
          setError(data.error || 'Failed to generate image')
        }
        return
      }

      // Update current display
      setCurrentImage(data.generation.image_url)
      setCurrentPrompt(data.generation.prompt)

      // Add to history
      setGenerations([data.generation, ...generations])

      // Update usage
      setUsage({
        current: data.usage.current,
        limit: data.usage.limit,
        plan: data.usage.plan
      })

    } catch (err: any) {
      setError(err.message || 'Failed to generate image')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleSelectGeneration = (generation: Generation) => {
    setCurrentImage(generation.image_url)
    setCurrentPrompt(generation.prompt)
  }

  return (
    <div className="space-y-8">
      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-2 border-red-200 rounded-xl p-4">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div>
              <h4 className="font-bold text-red-900">Error</h4>
              <p className="text-red-800 text-sm mt-1">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="ml-auto text-red-600 hover:text-red-800"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Usage Tracker */}
      <UsageTracker current={usage.current} limit={usage.limit} plan={usage.plan} />

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Left Column: Generator */}
        <div>
          <ImageGenerator onGenerate={handleGenerate} isGenerating={isGenerating} />
        </div>

        {/* Right Column: Display */}
        <div>
          <ImageDisplay imageUrl={currentImage} prompt={currentPrompt} />
        </div>
      </div>

      {/* History */}
      <ImageHistory generations={generations} onSelectGeneration={handleSelectGeneration} />
    </div>
  )
}

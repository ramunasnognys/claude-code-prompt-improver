'use client'

import { useState } from 'react'
import { PricingCard } from './PricingCard'

interface PricingGridProps {
  currentPlan?: string
}

export function PricingGrid({ currentPlan }: PricingGridProps) {
  const [loading, setLoading] = useState(false)

  const handleSubscribe = async (plan: string, interval: 'monthly' | 'yearly') => {
    setLoading(true)

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ plan, interval }),
      })

      const data = await response.json()

      if (data.url) {
        window.location.href = data.url
      } else {
        console.error('No checkout URL returned')
        setLoading(false)
      }
    } catch (error) {
      console.error('Subscription error:', error)
      setLoading(false)
    }
  }

  return (
    <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
      <PricingCard
        plan="free"
        currentPlan={currentPlan}
        loading={loading}
      />
      <PricingCard
        plan="pro"
        currentPlan={currentPlan}
        onSubscribe={handleSubscribe}
        loading={loading}
      />
      <PricingCard
        plan="enterprise"
        currentPlan={currentPlan}
        onSubscribe={handleSubscribe}
        loading={loading}
      />
    </div>
  )
}

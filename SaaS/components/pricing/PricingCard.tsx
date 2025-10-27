'use client'

import { useState } from 'react'

interface PricingCardProps {
  plan: 'free' | 'pro' | 'enterprise'
  currentPlan?: string
  onSubscribe?: (plan: string, interval: 'monthly' | 'yearly') => void
  loading?: boolean
}

const PLAN_DATA = {
  free: {
    name: 'Free',
    monthlyPrice: 0,
    yearlyPrice: 0,
    features: ['10 images per month', 'High-quality AI generation', 'Image history', 'Commercial usage rights'],
  },
  pro: {
    name: 'Pro',
    monthlyPrice: 14.99,
    yearlyPrice: 143.90,
    features: [
      '300 images per month',
      'Priority generation queue',
      'Advanced image settings',
      'Premium support',
      'Download all formats',
    ],
  },
  enterprise: {
    name: 'Enterprise',
    monthlyPrice: 99.99,
    yearlyPrice: 959.90,
    features: [
      'Unlimited image generation',
      'Highest priority queue',
      'Custom model training',
      'API access',
      'Dedicated account manager',
      '24/7 premium support',
    ],
  },
}

export function PricingCard({
  plan,
  currentPlan,
  onSubscribe,
  loading,
}: PricingCardProps) {
  const [interval, setInterval] = useState<'monthly' | 'yearly'>('monthly')
  const planData = PLAN_DATA[plan]
  const price = interval === 'monthly' ? planData.monthlyPrice : planData.yearlyPrice
  const isCurrentPlan = currentPlan === plan
  const isFree = plan === 'free'

  const handleSubscribe = () => {
    if (onSubscribe && !isFree && !isCurrentPlan) {
      onSubscribe(plan, interval)
    }
  }

  const discount = interval === 'yearly' && !isFree ? '20% off' : null

  return (
    <div
      className={`bg-white rounded-lg shadow-md border-2 p-8 ${
        plan === 'pro' ? 'border-blue-500' : 'border-gray-300'
      }`}
    >
      {plan === 'pro' && (
        <div className="bg-blue-500 text-white text-xs font-bold uppercase px-3 py-1 rounded-full inline-block mb-4">
          Popular
        </div>
      )}

      <h3 className="text-2xl font-bold text-gray-900 mb-2">{planData.name}</h3>

      {!isFree && (
        <div className="mb-4">
          <div className="flex gap-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setInterval('monthly')}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-semibold transition-colors ${
                interval === 'monthly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setInterval('yearly')}
              className={`flex-1 py-2 px-4 rounded-md text-sm font-semibold transition-colors ${
                interval === 'yearly'
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600'
              }`}
            >
              Yearly
            </button>
          </div>
        </div>
      )}

      <div className="mb-6">
        <div className="flex items-baseline">
          <span className="text-5xl font-extrabold text-gray-900">
            ${price.toFixed(2)}
          </span>
          {!isFree && (
            <span className="text-gray-600 ml-2">
              /{interval === 'monthly' ? 'mo' : 'yr'}
            </span>
          )}
        </div>
        {discount && (
          <p className="text-green-600 font-semibold text-sm mt-1">{discount}</p>
        )}
      </div>

      <ul className="space-y-3 mb-8">
        {planData.features.map((feature, index) => (
          <li key={index} className="flex items-start text-gray-700">
            <svg
              className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
            {feature}
          </li>
        ))}
      </ul>

      <button
        onClick={handleSubscribe}
        disabled={loading || isCurrentPlan || isFree}
        className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
          isCurrentPlan
            ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
            : isFree
            ? 'bg-gray-200 text-gray-700 cursor-default'
            : plan === 'pro'
            ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-md'
            : 'bg-purple-600 hover:bg-purple-700 text-white shadow-md'
        }`}
      >
        {loading
          ? 'Processing...'
          : isCurrentPlan
          ? 'Current Plan'
          : isFree
          ? 'Free Forever'
          : `Subscribe to ${planData.name}`}
      </button>
    </div>
  )
}

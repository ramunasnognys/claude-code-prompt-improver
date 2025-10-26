'use client'

import { useState } from 'react'

interface CancellationData {
  plan: string
  interval: string
  current_period_end: string
  cancel_at: number
}

export function CancelSubscriptionButton() {
  const [loading, setLoading] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const [cancellationData, setCancellationData] = useState<CancellationData | null>(null)

  const handleCancel = async () => {
    setLoading(true)

    try {
      const response = await fetch('/api/cancel-subscription', {
        method: 'POST',
      })

      const data = await response.json()

      if (data.success) {
        setCancellationData({
          plan: data.plan,
          interval: data.interval,
          current_period_end: data.current_period_end,
          cancel_at: data.cancel_at,
        })
        setShowConfirm(false)
        setLoading(false)
      } else {
        console.error('Cancel failed')
        setLoading(false)
      }
    } catch (error) {
      console.error('Cancel error:', error)
      setLoading(false)
    }
  }

  const handleCloseModal = () => {
    setCancellationData(null)
    window.location.reload()
  }

  // Success modal
  if (cancellationData) {
    const endDate = new Date(cancellationData.current_period_end).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4 shadow-2xl">
          <div className="text-center">
            <div className="mb-4">
              <svg
                className="mx-auto h-12 w-12 text-green-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Subscription Cancelled
            </h2>
            <p className="text-gray-600 mb-6">
              Your cancellation has been processed successfully
            </p>

            <div className="bg-gray-50 rounded-lg p-4 mb-6 text-left">
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Plan:</span>
                  <span className="font-semibold text-gray-900 capitalize">
                    {cancellationData.plan}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Billing:</span>
                  <span className="font-semibold text-gray-900 capitalize">
                    {cancellationData.interval}ly
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Access until:</span>
                  <span className="font-semibold text-gray-900">
                    {endDate}
                  </span>
                </div>
              </div>
            </div>

            <p className="text-sm text-gray-500 mb-6">
              You'll continue to have access to all {cancellationData.plan} features until {endDate}.
              After that, you'll be downgraded to the free plan.
            </p>

            <button
              onClick={handleCloseModal}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
            >
              Got it, thanks!
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (showConfirm) {
    return (
      <div className="flex gap-2">
        <button
          onClick={handleCancel}
          disabled={loading}
          className="bg-red-600 hover:bg-red-700 text-white font-semibold px-4 py-2 rounded-lg transition-colors shadow-md disabled:opacity-50"
        >
          {loading ? 'Canceling...' : 'Confirm Cancel'}
        </button>
        <button
          onClick={() => setShowConfirm(false)}
          disabled={loading}
          className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold px-4 py-2 rounded-lg transition-colors"
        >
          Keep Plan
        </button>
      </div>
    )
  }

  return (
    <button
      onClick={() => setShowConfirm(true)}
      className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-6 py-2 rounded-lg transition-colors"
    >
      Cancel Subscription
    </button>
  )
}

'use client'

import { useState } from 'react'

export function CancelSubscriptionButton() {
  const [loading, setLoading] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const handleCancel = async () => {
    setLoading(true)

    try {
      const response = await fetch('/api/cancel-subscription', {
        method: 'POST',
      })

      const data = await response.json()

      if (data.success) {
        window.location.reload()
      } else {
        console.error('Cancel failed')
        setLoading(false)
      }
    } catch (error) {
      console.error('Cancel error:', error)
      setLoading(false)
    }
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

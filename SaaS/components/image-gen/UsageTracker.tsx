'use client'

interface UsageTrackerProps {
  current: number
  limit: number
  plan: string
}

export function UsageTracker({ current, limit, plan }: UsageTrackerProps) {
  const percentage = (current / limit) * 100
  const isUnlimited = limit > 900000 // Enterprise plan

  const planColors = {
    free: 'from-gray-400 to-gray-500',
    pro: 'from-blue-500 to-blue-600',
    enterprise: 'from-purple-500 to-purple-600'
  }

  const gradient = planColors[plan as keyof typeof planColors] || planColors.free

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-gray-900">Usage This Month</h3>
        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase bg-gradient-to-r ${gradient} text-white`}>
          {plan}
        </span>
      </div>

      {isUnlimited ? (
        <div className="text-center py-4">
          <p className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-600 mb-2">
            Unlimited
          </p>
          <p className="text-sm text-gray-600">
            {current} images generated this month
          </p>
        </div>
      ) : (
        <>
          <div className="mb-2 flex justify-between text-sm">
            <span className="font-semibold text-gray-700">{current} / {limit} images</span>
            <span className="text-gray-600">{Math.round(percentage)}%</span>
          </div>

          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full bg-gradient-to-r ${gradient} rounded-full transition-all duration-500`}
              style={{ width: `${Math.min(percentage, 100)}%` }}
            />
          </div>

          {current >= limit && (
            <p className="mt-3 text-sm text-red-600 font-semibold">
              Limit reached! Upgrade to generate more images.
            </p>
          )}

          {current >= limit * 0.8 && current < limit && (
            <p className="mt-3 text-sm text-orange-600 font-semibold">
              {limit - current} images remaining
            </p>
          )}
        </>
      )}
    </div>
  )
}

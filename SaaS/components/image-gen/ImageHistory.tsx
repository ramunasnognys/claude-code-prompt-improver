'use client'

interface Generation {
  id: string
  prompt: string
  image_url: string
  created_at: string
}

interface ImageHistoryProps {
  generations: Generation[]
  onSelectGeneration: (generation: Generation) => void
}

export function ImageHistory({ generations, onSelectGeneration }: ImageHistoryProps) {
  if (generations.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md border border-gray-200 p-8">
        <h3 className="text-xl font-bold text-gray-900 mb-4">Recent Generations</h3>
        <p className="text-gray-600 text-center py-8">No images generated yet. Create your first one!</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-md border border-gray-200 p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-6">Recent Generations</h3>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
        {generations.map((gen) => (
          <button
            key={gen.id}
            onClick={() => onSelectGeneration(gen)}
            className="group relative aspect-square rounded-lg overflow-hidden border-2 border-gray-300 hover:border-purple-500 transition-all hover:shadow-lg"
          >
            <img
              src={gen.image_url}
              alt={gen.prompt}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all flex items-center justify-center">
              <svg
                className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}

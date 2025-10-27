'use client'

interface ImageDisplayProps {
  imageUrl: string | null
  prompt: string | null
}

export function ImageDisplay({ imageUrl, prompt }: ImageDisplayProps) {
  if (!imageUrl) {
    return (
      <div className="bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl shadow-md border-2 border-dashed border-gray-300 p-12 flex flex-col items-center justify-center min-h-[400px]">
        <svg
          className="w-24 h-24 text-gray-400 mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        <p className="text-gray-600 font-semibold text-lg">Your generated image will appear here</p>
        <p className="text-gray-500 text-sm mt-2">Enter a prompt and click Generate</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-2xl shadow-xl border border-gray-200 p-6">
      <div className="mb-4">
        <h3 className="text-lg font-bold text-gray-900 mb-2">Generated Image</h3>
        {prompt && (
          <p className="text-sm text-gray-600 italic">"{prompt}"</p>
        )}
      </div>

      <div className="rounded-xl overflow-hidden bg-gray-100">
        <img
          src={imageUrl}
          alt={prompt || 'Generated image'}
          className="w-full h-auto"
        />
      </div>

      <div className="mt-4 flex gap-3">
        <button
          onClick={() => navigator.clipboard.writeText(imageUrl)}
          className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg transition-colors"
        >
          Copy
        </button>
        <button
          onClick={() => {
            const a = document.createElement('a')
            a.href = imageUrl
            a.download = `generated-image-${Date.now()}.png`
            a.click()
          }}
          className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
        >
          Download
        </button>
      </div>
    </div>
  )
}

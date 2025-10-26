import { AuthForm } from '@/components/auth/AuthForm'
import Link from 'next/link'

export default function LoginPage() {
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <div className="mb-8">
        <Link href="/" className="text-blue-600 hover:text-blue-700 font-semibold text-lg">
          ← Back to home
        </Link>
      </div>
      <AuthForm />
    </main>
  )
}

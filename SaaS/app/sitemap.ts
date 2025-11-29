import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://nanobanana.com'

  // Static routes
  const routes = [
    '',
    '/features',
    '/pricing',
    '/use-cases',
    '/examples',
    '/for-creators',
    '/for-businesses',
    '/ai-art',
    '/fast-generation',
    '/unlimited-creativity',
    '/login',
    '/signup',
  ]

  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date(),
    changeFrequency: route === '' ? 'daily' : 'weekly',
    priority: route === '' ? 1.0 : route === '/pricing' || route === '/features' ? 0.8 : 0.6,
  }))
}

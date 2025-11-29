---
name: seo-specialist
description: SEO optimization guidance including meta tags, Open Graph tags, Twitter cards, structured data (schema.org, JSON-LD), sitemaps (XML), robots.txt, canonical URLs, image alt text, semantic HTML, Core Web Vitals, mobile optimization, and accessibility. Use when implementing SEO, optimizing pages for search engines, adding metadata, creating sitemaps, or improving search visibility.
---

# SEO Specialist

## Purpose

Comprehensive guidance for implementing SEO best practices in web applications, including meta tags, structured data, social media optimization, and technical SEO requirements.

## When to Use

Activate when:
- Implementing meta tags (title, description, keywords)
- Adding Open Graph or Twitter card tags
- Creating structured data (JSON-LD, schema.org)
- Generating sitemaps or robots.txt
- Optimizing for search engines
- Improving social media sharing
- Adding canonical URLs
- Implementing semantic HTML
- Optimizing Core Web Vitals
- Ensuring mobile-friendliness
- Improving accessibility for SEO

---

## Core SEO Elements

### 1. Essential Meta Tags

**Basic Meta Tags:**
```html
<head>
  <!-- Primary Meta Tags -->
  <title>Page Title | Site Name</title>
  <meta name="title" content="Page Title | Site Name" />
  <meta name="description" content="Clear, concise description (150-160 chars)" />
  <meta name="keywords" content="keyword1, keyword2, keyword3" />

  <!-- Viewport for Mobile -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <!-- Canonical URL -->
  <link rel="canonical" href="https://example.com/page" />

  <!-- Language -->
  <html lang="en">
</head>
```

**Best Practices:**
- ✅ Title: 50-60 characters, include primary keyword
- ✅ Description: 150-160 characters, compelling, includes CTA
- ✅ Unique per page
- ✅ Include brand name in title
- ✅ Keywords: 5-10 relevant terms (deprecated but some engines still use)

### 2. Open Graph Tags (Social Media)

**Facebook/LinkedIn/Most Platforms:**
```html
<!-- Open Graph / Facebook -->
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Description for social sharing" />
<meta property="og:image" content="https://example.com/image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:site_name" content="Site Name" />
<meta property="og:locale" content="en_US" />
```

**Image Requirements:**
- Recommended: 1200x630px (1.91:1 ratio)
- Minimum: 600x315px
- Format: JPG or PNG
- Max file size: 8MB
- Include text overlay for context

### 3. Twitter Card Tags

```html
<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:url" content="https://example.com/page" />
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="Description for Twitter" />
<meta name="twitter:image" content="https://example.com/image.jpg" />
<meta name="twitter:site" content="@username" />
<meta name="twitter:creator" content="@username" />
```

**Card Types:**
- `summary`: Small image (120x120px)
- `summary_large_image`: Large image (2:1 ratio, 300x157px min)
- `app`: Mobile app
- `player`: Video/audio

### 4. Structured Data (JSON-LD)

**Website/Organization:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/username",
    "https://linkedin.com/company/name"
  ]
}
</script>
```

**Article/Blog Post:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "Article description",
  "image": "https://example.com/article-image.jpg",
  "datePublished": "2025-01-15T08:00:00+00:00",
  "dateModified": "2025-01-16T09:00:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/author/name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
}
</script>
```

**Breadcrumb:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://example.com/category"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Page",
      "item": "https://example.com/category/page"
    }
  ]
}
</script>
```

**Product (E-commerce):**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": "https://example.com/product.jpg",
  "description": "Product description",
  "brand": {
    "@type": "Brand",
    "name": "Brand Name"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/product",
    "priceCurrency": "USD",
    "price": "99.99",
    "availability": "https://schema.org/InStock"
  }
}
</script>
```

**More Schema Types:**
- `WebPage` - Generic web page
- `FAQPage` - FAQ pages
- `HowTo` - Step-by-step guides
- `Recipe` - Recipes
- `Event` - Events
- `LocalBusiness` - Local businesses
- `Review` - Reviews/ratings

### 5. Technical SEO

**Robots Meta Tag:**
```html
<!-- Allow indexing (default) -->
<meta name="robots" content="index, follow" />

<!-- Prevent indexing -->
<meta name="robots" content="noindex, nofollow" />

<!-- Allow index but don't follow links -->
<meta name="robots" content="index, nofollow" />
```

**Robots.txt:**
```txt
# Allow all bots
User-agent: *
Allow: /

# Disallow specific paths
Disallow: /admin/
Disallow: /private/
Disallow: /api/

# Sitemap location
Sitemap: https://example.com/sitemap.xml
```

**XML Sitemap:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2025-01-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Priority Guidelines:**
- Homepage: 1.0
- Main category pages: 0.8
- Sub-pages: 0.6
- Blog posts: 0.5
- Archive pages: 0.4

**Canonical URLs:**
```html
<!-- Prevent duplicate content issues -->
<link rel="canonical" href="https://example.com/page" />

<!-- When paginated -->
<link rel="prev" href="https://example.com/page?p=1" />
<link rel="next" href="https://example.com/page?p=3" />
```

### 6. Performance & Core Web Vitals

**Key Metrics:**
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1

**Optimization Techniques:**
```html
<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin />
<link rel="preload" href="/images/hero.jpg" as="image" />

<!-- Preconnect to external domains -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="dns-prefetch" href="https://analytics.example.com" />

<!-- Lazy load images -->
<img src="image.jpg" alt="Description" loading="lazy" />

<!-- Responsive images -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 900px) 800px, 1200px"
  alt="Description"
/>
```

### 7. Semantic HTML & Accessibility

**Proper HTML Structure:**
```html
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Main Heading (only one per page)</h1>
    <h2>Section Heading</h2>
    <h3>Subsection Heading</h3>

    <p>Content...</p>

    <figure>
      <img src="image.jpg" alt="Descriptive alt text" />
      <figcaption>Image caption</figcaption>
    </figure>
  </article>
</main>

<aside>
  <section>
    <h2>Related Content</h2>
  </section>
</aside>

<footer>
  <p>&copy; 2025 Company Name</p>
</footer>
```

**Heading Hierarchy:**
- ✅ One `<h1>` per page (usually page title)
- ✅ Don't skip levels (h1 → h2 → h3, not h1 → h3)
- ✅ Use headings for structure, not styling
- ✅ Screen readers use headings for navigation

**Alt Text Best Practices:**
```html
<!-- Descriptive alt text -->
<img src="sunset.jpg" alt="Golden sunset over mountain range" />

<!-- Decorative images -->
<img src="decoration.svg" alt="" role="presentation" />

<!-- Complex images -->
<figure>
  <img src="chart.png" alt="Sales chart showing 25% growth" />
  <figcaption>
    Detailed description: Sales increased from $100k to $125k in Q4...
  </figcaption>
</figure>
```

### 8. Mobile Optimization

**Viewport Configuration:**
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="theme-color" content="#0066cc" />
<meta name="mobile-web-app-capable" content="yes" />
```

**Responsive Design Checklist:**
- ✅ Mobile-first approach
- ✅ Touch targets ≥ 48x48px
- ✅ Readable font sizes (16px minimum)
- ✅ No horizontal scrolling
- ✅ Fast load times on 3G
- ✅ Test on real devices

### 9. Additional SEO Elements

**Favicons & App Icons:**
```html
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
```

**Web App Manifest (site.webmanifest):**
```json
{
  "name": "App Name",
  "short_name": "App",
  "icons": [
    {
      "src": "/android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

**Language & Internationalization:**
```html
<html lang="en">
<head>
  <!-- Alternate language versions -->
  <link rel="alternate" hreflang="en" href="https://example.com/en/page" />
  <link rel="alternate" hreflang="es" href="https://example.com/es/page" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/page" />
</head>
```

---

## Implementation Patterns

### React/Next.js Example

```tsx
import Head from 'next/head';

interface SEOProps {
  title: string;
  description: string;
  canonical?: string;
  ogImage?: string;
  ogType?: 'website' | 'article';
  publishedTime?: string;
  modifiedTime?: string;
}

export function SEO({
  title,
  description,
  canonical,
  ogImage = '/default-og-image.jpg',
  ogType = 'website',
  publishedTime,
  modifiedTime,
}: SEOProps) {
  const fullTitle = `${title} | Site Name`;
  const url = canonical || `https://example.com`;
  const fullOgImage = ogImage.startsWith('http')
    ? ogImage
    : `https://example.com${ogImage}`;

  return (
    <Head>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={url} />

      {/* Open Graph */}
      <meta property="og:type" content={ogType} />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={fullOgImage} />

      {/* Twitter */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullOgImage} />

      {/* Article specific */}
      {ogType === 'article' && publishedTime && (
        <meta property="article:published_time" content={publishedTime} />
      )}
      {ogType === 'article' && modifiedTime && (
        <meta property="article:modified_time" content={modifiedTime} />
      )}
    </Head>
  );
}
```

### Dynamic Sitemap Generation (Next.js)

```typescript
// pages/sitemap.xml.ts
import { GetServerSideProps } from 'next';

export const getServerSideProps: GetServerSideProps = async ({ res }) => {
  const baseUrl = 'https://example.com';

  // Fetch your pages/posts
  const pages = await fetchAllPages();

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${pages.map(page => `
  <url>
    <loc>${baseUrl}${page.url}</loc>
    <lastmod>${page.updatedAt}</lastmod>
    <changefreq>${page.changeFreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>
  `).join('')}
</urlset>`;

  res.setHeader('Content-Type', 'text/xml');
  res.write(sitemap);
  res.end();

  return { props: {} };
};

export default function Sitemap() {
  return null;
}
```

---

## Testing & Validation

### Tools

**Google Tools:**
- [Google Search Console](https://search.google.com/search-console)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [PageSpeed Insights](https://pagespeed.web.dev/)

**Social Media Validators:**
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

**Schema Validation:**
- [Schema.org Validator](https://validator.schema.org/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)

### SEO Checklist

**On-Page SEO:**
- [ ] Unique, descriptive title (50-60 chars)
- [ ] Compelling meta description (150-160 chars)
- [ ] One H1 heading per page
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Descriptive alt text for all images
- [ ] Internal linking to related content
- [ ] Canonical URL set
- [ ] Mobile responsive design
- [ ] Fast page load time (< 3s)
- [ ] HTTPS enabled

**Technical SEO:**
- [ ] Robots.txt configured
- [ ] XML sitemap generated and submitted
- [ ] Structured data implemented
- [ ] Open Graph tags configured
- [ ] Twitter cards configured
- [ ] 404 page exists
- [ ] 301 redirects for moved pages
- [ ] No broken links
- [ ] Clean URL structure

**Content SEO:**
- [ ] Unique, high-quality content
- [ ] Target keyword in title, H1, first paragraph
- [ ] Related keywords throughout
- [ ] Content length > 300 words
- [ ] Regular content updates
- [ ] External links to authoritative sources

---

## Common Pitfalls

❌ **Duplicate content**: Use canonical tags
❌ **Missing alt text**: Screen readers and SEO need it
❌ **Keyword stuffing**: Write naturally for humans
❌ **Slow page speed**: Optimize images, use CDN
❌ **Not mobile-friendly**: Test on devices
❌ **Broken links**: Check regularly
❌ **Missing structured data**: Implement JSON-LD
❌ **Poor URL structure**: Use clean, descriptive URLs
❌ **No sitemap**: Generate and submit
❌ **Ignoring Core Web Vitals**: Monitor and optimize

---

**Status**: Production-ready ✅
**Line Count**: < 500 ✅
**Best Practices**: Following Anthropic guidelines ✅

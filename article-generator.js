#!/usr/bin/env node

/**
 * Oscillot America Article Generator
 * Generates 15 SEO-optimized articles in English and Spanish
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Jina AI API configuration
const JINA_API_KEY = 'jina_d1114b7bbf404c72851738f87b9d7343XV5OHbxgIx0fqHw7yPBnkhgdO404';
const JINA_BASE_URL = 'https://r.jina.ai/';

// Load topics
const topics = require('./article-topics.json').topics;

// Product and collection data (scraped from sitemaps)
const PRODUCTS_BASE = 'https://oscillotamerica.com/products/';
const COLLECTIONS_BASE = 'https://oscillotamerica.com/collections/';

/**
 * Fetch URL content using Jina AI
 */
function fetchWithJina(url) {
  try {
    const cmd = `curl -s "${JINA_BASE_URL}${url}" -H "Authorization: Bearer ${JINA_API_KEY}"`;
    const result = execSync(cmd, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
    return result;
  } catch (error) {
    console.error(`Error fetching ${url}:`, error.message);
    return null;
  }
}

/**
 * Create article directory structure
 */
function createArticleDirectory(slug) {
  const articleDir = path.join(__dirname, 'articles', slug);
  if (!fs.existsSync(articleDir)) {
    fs.mkdirSync(articleDir, { recursive: true });
  }
  return articleDir;
}

/**
 * Generate article metadata
 */
function generateMetadata(topic) {
  return {
    title: topic.title,
    slug: topic.slug,
    keywords: topic.keywords,
    author: 'Oscillot America',
    publishDate: new Date().toISOString(),
    targetProducts: topic.target_products,
    targetCollections: topic.target_collections,
    description: topic.description
  };
}

/**
 * Save article file
 */
function saveArticle(articleDir, filename, content) {
  const filePath = path.join(articleDir, filename);
  fs.writeFileSync(filePath, content, 'utf-8');
  console.log(`✓ Saved: ${filename}`);
}

/**
 * Main generation function
 */
async function generateArticles() {
  console.log('🚀 Oscillot America Article Generator');
  console.log('=====================================\n');
  console.log(`Generating ${topics.length} articles in English and Spanish...\n`);

  for (let i = 0; i < topics.length; i++) {
    const topic = topics[i];
    console.log(`\n[${i + 1}/${topics.length}] Processing: ${topic.title}`);
    console.log('─'.repeat(80));

    // Create directory
    const articleDir = createArticleDirectory(topic.slug);

    // Generate metadata
    const metadata = generateMetadata(topic);
    saveArticle(articleDir, 'metadata.json', JSON.stringify(metadata, null, 2));

    // Save topic info for subagent
    const topicInfo = {
      ...topic,
      metadata,
      jinaApiKey: JINA_API_KEY,
      productsBase: PRODUCTS_BASE,
      collectionsBase: COLLECTIONS_BASE,
      sitemapUrls: {
        products: 'https://oscillotamerica.com/sitemap_products_1.xml?from=7552589267169&to=8003189735649',
        collections: 'https://oscillotamerica.com/sitemap_collections_1.xml?from=58566541363&to=412846031073',
        blogs: 'https://oscillotamerica.com/sitemap_blogs_1.xml'
      }
    };

    saveArticle(articleDir, 'topic-config.json', JSON.stringify(topicInfo, null, 2));

    console.log(`✓ Created directory and config for: ${topic.slug}`);
    console.log(`  Directory: ./articles/${topic.slug}/`);
  }

  console.log('\n\n✅ All article directories and configurations created!');
  console.log('\n📝 Next Steps:');
  console.log('Each article directory now contains a topic-config.json file.');
  console.log('Use Claude Code Task agents to generate the actual article content.\n');
}

// Run the generator
generateArticles().catch(console.error);

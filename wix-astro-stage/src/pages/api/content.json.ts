import { items } from '@wix/data';

export const prerender = false;
const allowedPages = new Set(['home', 'compositions', 'reconstruction', 'cds-and-books', 'academic']);
const allowedLanguages = new Set(['zh', 'en']);

export async function GET({ url }: { url: URL }) {
  const pageKey = url.searchParams.get('pageKey') ?? '';
  const language = url.searchParams.get('language') ?? '';
  if (!allowedPages.has(pageKey) || !allowedLanguages.has(language)) {
    return new Response(JSON.stringify({ error: 'Invalid content request' }), { status: 400, headers: { 'content-type': 'application/json' } });
  }
  try {
    let query = items.query('WebsiteContent')
      .eq('pageKey', pageKey)
      .eq('language', language)
      .eq('published', true)
      .limit(100);
    query = query.descending('sortOrder');
    const result = await query.find();
    return new Response(JSON.stringify({ items: result.items }), {
      headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
    });
  } catch (error) {
    console.error('Unable to read WebsiteContent', error);
    return new Response(JSON.stringify({ error: 'CMS temporarily unavailable' }), { status: 503, headers: { 'content-type': 'application/json' } });
  }
}

/**
 * pre-launch-check.mjs — go-live checks against a live URL.
 *
 * Mirrors the checklist's SEO + security + go-live items:
 *   status, security headers, noindex leaks (header + meta), title,
 *   meta description, canonical, OG tags, and robots.txt.
 *
 * Usage:
 *   node pre-launch-check.mjs https://staging.example.com
 *
 * Zero dependencies — Node 20+ fetch only. Exit code 0 only if every
 * High-risk check passes; Medium/Low failures print but don't fail.
 */

const SECURITY_HEADERS = [
  'strict-transport-security',
  'x-frame-options',
  'x-content-type-options',
  'referrer-policy',
  'content-security-policy',
];

export function checkHeaders(headers) {
  const h = new Map([...headers.entries()].map(([k, v]) => [k.toLowerCase(), v]));
  const out = [];
  for (const name of SECURITY_HEADERS) {
    out.push({ name, pass: h.has(name), risk: 'High', detail: h.get(name) || 'missing' });
  }
  const robotsTag = h.get('x-robots-tag') || '';
  out.push({
    name: 'x-robots-tag noindex leak',
    pass: !/noindex/i.test(robotsTag),
    risk: 'High',
    detail: robotsTag || 'not set (ok)',
  });
  return out;
}

export function checkHtml(html, pageUrl) {
  const out = [];
  const pick = (re) => (html.match(re) || [])[1];

  const metaRobots = pick(/<meta[^>]+name=["']robots["'][^>]+content=["']([^"']*)/i) || '';
  out.push({ name: 'meta robots noindex leak', pass: !/noindex/i.test(metaRobots), risk: 'High', detail: metaRobots || 'index (ok)' });

  const title = pick(/<title[^>]*>([^<]*)<\/title>/i) || '';
  out.push({ name: 'title present and <=60 chars', pass: title.trim().length > 0 && title.trim().length <= 60, risk: 'High', detail: `${title.trim().length} chars` });

  const desc = pick(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)/i) || '';
  out.push({ name: 'meta description 120-160 chars', pass: desc.length >= 120 && desc.length <= 160, risk: 'Medium', detail: `${desc.length} chars` });

  const canonical = pick(/<link[^>]+rel=["']canonical["'][^>]+href=["']([^"']*)/i) || '';
  const sameCanonical = canonical.replace(/\/$/, '') === pageUrl.replace(/\/$/, '');
  out.push({ name: 'canonical self-referencing', pass: sameCanonical, risk: 'High', detail: canonical || 'missing' });

  for (const prop of ['og:title', 'og:description', 'og:image']) {
    const present = new RegExp(`<meta[^>]+property=["']${prop}["']`, 'i').test(html);
    out.push({ name: `${prop} present`, pass: present, risk: 'Medium', detail: present ? 'set' : 'missing' });
  }
  return out;
}

export function checkRobotsTxt(robotsTxt, pageOrigin) {
  const blocksAll = /user-agent:\s*\*[\s\S]*?disallow:\s*\/\s*(\n|$)/i.test(robotsTxt);
  return [{
    name: 'robots.txt allows crawling',
    pass: !blocksAll,
    risk: 'High',
    detail: blocksAll ? 'Disallow: / blocks everything' : 'allows crawling',
  }];
}

function report(url, checks) {
  let failed = false;
  for (const c of checks) {
    const mark = c.pass ? 'PASS' : 'FAIL';
    if (!c.pass && c.risk === 'High') failed = true;
    console.log(`${mark}  [${c.risk}] ${c.name} — ${c.detail}`);
  }
  console.log(`\n${url}: ${failed ? 'HIGH-RISK FAILURES — do not launch' : 'no High-risk failures'}`);
  return failed;
}

const isMain = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1].replace(/\\/g, '/')}`).href;
if (isMain) {
  const url = process.argv[2];
  if (!url) {
    console.error('usage: node pre-launch-check.mjs <url>');
    process.exit(2);
  }
  const origin = new URL(url).origin;
  const [pageRes, robotsRes] = await Promise.all([
    fetch(url, { redirect: 'follow' }),
    fetch(`${origin}/robots.txt`).catch(() => null),
  ]);
  const checks = [
    { name: 'HTTP 200', pass: pageRes.status === 200, risk: 'High', detail: `status ${pageRes.status}` },
    ...checkHeaders(pageRes.headers),
    ...checkHtml(await pageRes.text(), pageRes.url),
    ...checkRobotsTxt(robotsRes ? await robotsRes.text() : '', origin),
  ];
  process.exit(report(pageRes.url, checks) ? 1 : 0);
}

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { checkHeaders, checkHtml, checkRobotsTxt } from '../pre-launch-check.mjs';

const hdrs = (obj) => new Map(Object.entries(obj));

const GOOD_HEADERS = hdrs({
  'strict-transport-security': 'max-age=63072000; includeSubDomains',
  'x-frame-options': 'DENY',
  'x-content-type-options': 'nosniff',
  'referrer-policy': 'strict-origin-when-cross-origin',
  'content-security-policy': "default-src 'self'",
});

const GOOD_HTML = `
<html><head>
<title>Acme - Quality Widgets</title>
<meta name="description" content="${'a'.repeat(140)}">
<link rel="canonical" href="https://example.com/">
<meta name="robots" content="index,follow">
<meta property="og:title" content="Acme">
<meta property="og:description" content="desc">
<meta property="og:image" content="https://example.com/og.png">
</head><body>ok</body></html>`;

test('all security headers present passes', () => {
  const r = checkHeaders(GOOD_HEADERS);
  assert.equal(r.filter(c => !c.pass).length, 0);
});

test('missing headers fail as High risk', () => {
  const r = checkHeaders(hdrs({ 'x-frame-options': 'DENY' }));
  const fails = r.filter(c => !c.pass);
  assert.ok(fails.length >= 4);
  assert.ok(fails.every(c => c.risk === 'High'));
});

test('x-robots-tag noindex is caught as a leak', () => {
  const r = checkHeaders(hdrs({ ...Object.fromEntries(GOOD_HEADERS), 'x-robots-tag': 'noindex' }));
  const leak = r.find(c => c.name.includes('noindex'));
  assert.equal(leak.pass, false);
});

test('clean HTML passes every check', () => {
  const r = checkHtml(GOOD_HTML, 'https://example.com/');
  assert.equal(r.filter(c => !c.pass).length, 0);
});

test('meta robots noindex in HTML is a High-risk fail', () => {
  const html = GOOD_HTML.replace('index,follow', 'noindex,nofollow');
  const leak = checkHtml(html, 'https://example.com/').find(c => c.name.includes('noindex'));
  assert.equal(leak.pass, false);
  assert.equal(leak.risk, 'High');
});

test('canonical pointing elsewhere fails', () => {
  const html = GOOD_HTML.replace('https://example.com/', 'https://example.com/other');
  const c = checkHtml(html, 'https://example.com/').find(c => c.name.includes('canonical'));
  assert.equal(c.pass, false);
});

test('robots.txt Disallow:/ for * fails as High', () => {
  const [r] = checkRobotsTxt('User-agent: *\nDisallow: /\n', 'https://example.com');
  assert.equal(r.pass, false);
  assert.equal(r.risk, 'High');
});

test('robots.txt with sitemap and no blanket block passes', () => {
  const [r] = checkRobotsTxt('User-agent: *\nDisallow: /admin\nSitemap: https://example.com/sitemap.xml\n', 'https://example.com');
  assert.equal(r.pass, true);
});

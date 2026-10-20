#!/usr/bin/env node
/**
 * check-email-html.js — pre-send checks for exported campaign HTML.
 *
 * Catches the mechanical failures that slip through visual review:
 *   - unresolved merge tags ({{name}}, *|NAME|*, %name%)
 *   - links missing UTM parameters on external URLs
 *   - <img> without alt text
 *   - HTML over 102 KB (Gmail clips and can cut the CTA)
 *   - missing unsubscribe link
 *
 * Usage:
 *   node check-email-html.js campaign-export.html
 *   node check-email-html.js campaign-export.html --utm-required=utm_campaign,utm_source
 *
 * Zero dependencies — Node 20+. Regex-based on purpose: email HTML
 * is messy by nature and a DOM parser won't save you from VML blocks.
 */

'use strict';

const fs = require('fs');

const file = process.argv[2];
if (!file) {
  console.error('usage: node check-email-html.js <campaign.html> [--utm-required=a,b]');
  process.exit(2);
}

const utmArg = process.argv.find((a) => a.startsWith('--utm-required='));
const requiredUtms = utmArg ? utmArg.slice('--utm-required='.length).split(',') : ['utm_campaign'];

const html = fs.readFileSync(file, 'utf8');
const lines = html.split('\n');
const issues = [];

const lineOf = (index) => html.slice(0, index).split('\n').length;
const report = (msg) => issues.push(msg);

// 1. Unresolved merge tags — {{var}}, *|VAR|* (Mailchimp), %var%, [var]-style ESP tokens
const mergePatterns = [
  /\{\{\s*[\w.]+\s*\}\}/g,
  /\*\|[A-Z_]+\|\*/g,
  /%[a-z_]{3,}%/g,
];
for (const re of mergePatterns) {
  for (const m of html.matchAll(re)) {
    report(`unresolved merge tag: ${m[0]} (line ${lineOf(m.index)})`);
  }
}

// 2. External links missing required UTM params
for (const m of html.matchAll(/<a\s[^>]*href=["']([^"']+)["']/gi)) {
  const href = m[1];
  if (/^(mailto:|tel:|#|\/)/.test(href)) continue;
  if (!/^https?:\/\//.test(href)) continue;
  for (const param of requiredUtms) {
    if (!href.includes(param + '=')) {
      report(`link missing ${param}: ${href} (line ${lineOf(m.index)})`);
      break; // one warning per link is enough
    }
  }
}

// 3. <img> without alt text
for (const m of html.matchAll(/<img\s[^>]*>/gi)) {
  const tag = m[0];
  const src = (tag.match(/src=["']([^"']+)["']/) || [null, 'image'])[1];
  if (!/alt=["'][^"']*["']/.test(tag)) {
    report(`img without alt: ${src} (line ${lineOf(m.index)})`);
  }
}

// 4. Gmail clipping — 102 KB of HTML source
const sizeKb = Buffer.byteLength(html, 'utf8') / 1024;
if (sizeKb > 100) {
  report(`HTML size ${sizeKb.toFixed(0)} KB — Gmail clips at 102 KB and can cut the CTA or footer links`);
}

// 5. Unsubscribe link present (CAN-SPAM / GDPR hygiene)
if (!/unsubscribe|desuscrib|baja|opt.?out/i.test(html)) {
  report('no unsubscribe link found — required in marketing email');
}

// 6. Plain-text sibling check (informational)
const sibling = file.replace(/\.html?$/i, '') + '.txt';
if (!fs.existsSync(sibling)) {
  report(`no plain text version found next to the HTML (expected ${sibling})`);
}

if (issues.length === 0) {
  console.log('OK — no mechanical issues found. Visual rendering still needs a seed send.');
} else {
  for (const issue of issues) console.log(`  ${issue}`);
  console.log(`\n${issues.length} issue(s) — fix before sending.`);
  process.exit(1);
}

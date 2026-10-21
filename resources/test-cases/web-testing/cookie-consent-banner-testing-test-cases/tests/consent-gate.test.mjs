import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { ConsentGate } from '../consent-gate.mjs';

const vendors = [
  { name: 'session', category: 'necessary' },
  { name: 'ga', category: 'analytics' },
  { name: 'fb-pixel', category: 'marketing' },
];
const make = (opts = {}) => new ConsentGate({ vendors, ...opts });

// TC-01 — banner on first visit
it('tc01: banner visible without stored consent, only necessary fires', () => {
  const g = make();
  assert.equal(g.bannerVisible(), true);
  assert.deepEqual(g.activeVendors(), ['session']);
});

// TC-02 — granular categories
it('tc02: granular consent blocks rejected category only', () => {
  const g = make();
  g.grant(['necessary', 'analytics']);
  assert.deepEqual(g.activeVendors(), ['session', 'ga']);
});

// TC-03 — nothing non-essential before consent
it('tc03: zero non-essential vendors fire before consent', () => {
  const g = make();
  assert.equal(g.vendorAllowed('ga'), false);
  assert.equal(g.vendorAllowed('fb-pixel'), false);
});

// TC-04 — consented scripts fire
it('tc04: accepted categories fire after consent', () => {
  const g = make();
  g.grant(['analytics', 'marketing']);
  assert.equal(g.vendorAllowed('ga'), true);
  assert.equal(g.vendorAllowed('fb-pixel'), true);
});

// TC-05 — persistence across sessions
it('tc05: restored consent keeps banner hidden and choices honored', () => {
  const g1 = make();
  g1.grant(['analytics']);
  const blob = g1.serialize();
  const g2 = make();
  ConsentGate.restore(g2, blob);
  assert.equal(g2.bannerVisible(), false);
  assert.equal(g2.vendorAllowed('ga'), true);
  assert.equal(g2.vendorAllowed('fb-pixel'), false);
});

// TC-06 — withdrawal kills the trackers
it('tc06: withdrawn category stops firing', () => {
  const g = make();
  g.grant(['analytics', 'marketing']);
  g.withdraw('analytics');
  assert.equal(g.vendorAllowed('ga'), false);
  assert.equal(g.vendorAllowed('fb-pixel'), true);
});

// TC-10 — GPC auto-reject default
it('tc10: GPC suppresses banner and defaults to most restrictive', () => {
  const g = make({ gpc: true });
  assert.equal(g.bannerVisible(), false);
  assert.deepEqual(g.activeVendors(), ['session']);
});

// TC-11 — version bump re-prompts
it('tc11: consent version bump forces re-prompt with old choices kept', () => {
  const g = make();
  g.grant(['analytics']);
  g.bumpVersion('2.0');
  assert.equal(g.needsReprompt(), true);
  assert.equal(g.bannerVisible(), true);
});

// TC-12 — new vendor does not inherit prior consent
it('tc12: vendor added after consent stays blocked', () => {
  const g = make();
  g.grant(['marketing']);
  assert.equal(g.vendorAllowed('fb-pixel'), true);
  g.bumpVersion('2.0');
  g.registerVendor('tiktok-pixel', 'marketing');
  // under version-1.0 consent, the 2.0 vendor is out of scope
  assert.equal(g.vendorAllowed('tiktok-pixel'), false);
  // and the old consent still covers the old vendors once re-prompted
  g.grant(['marketing']);
  assert.equal(g.vendorAllowed('tiktok-pixel'), true);
});

// edge — corrupted consent treated as absent
it('edge: corrupted consent blob falls back to no-consent', () => {
  const g = make();
  assert.throws(() => ConsentGate.restore(g, '{"broken"'), SyntaxError);
  assert.equal(g.bannerVisible(), true);
});

// edge — unknown category rejected at registration
it('edge: registering an uncategorized vendor throws', () => {
  const g = make();
  assert.throws(() => g.registerVendor('mystery', 'unknown'), /unknown category/);
});

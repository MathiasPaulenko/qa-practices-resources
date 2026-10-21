import { test } from 'node:test';
import assert from 'node:assert/strict';
import { evaluateStage } from '../evaluate-stage.mjs';

const baseline = { errorRate: 0.0028, p95Ms: 120, requests: 48000 };

test('healthy canary within deltas promotes', () => {
  const r = evaluateStage(baseline, { errorRate: 0.0031, p95Ms: 128, requests: 1250 });
  assert.equal(r.decision, 'PROMOTE');
});

test('error-rate delta above +0.5% rolls back', () => {
  const r = evaluateStage(baseline, { errorRate: 0.0091, p95Ms: 128, requests: 1250 });
  assert.equal(r.decision, 'ROLLBACK');
  assert.match(r.reason, /delta/);
});

test('p95 delta above +50ms rolls back', () => {
  const r = evaluateStage(baseline, { errorRate: 0.0031, p95Ms: 190, requests: 1250 });
  assert.equal(r.decision, 'ROLLBACK');
});

test('absolute floor catches a broken baseline that deltas would pass', () => {
  const badBaseline = { errorRate: 0.018, p95Ms: 460, requests: 48000 };
  const r = evaluateStage(badBaseline, { errorRate: 0.021, p95Ms: 505, requests: 1250 });
  assert.equal(r.decision, 'ROLLBACK');
  assert.match(r.reason, /floor/);
});

test('missing metric data fails closed, never passes', () => {
  const r = evaluateStage(baseline, { errorRate: null, p95Ms: 128, requests: 1250 });
  assert.equal(r.decision, 'ROLLBACK');
  assert.match(r.reason, /missing/);
});

test('low-traffic canary holds instead of promoting on noise', () => {
  const r = evaluateStage(baseline, { errorRate: 0.0031, p95Ms: 128, requests: 320 });
  assert.equal(r.decision, 'HOLD');
  assert.match(r.reason, /extend/);
});

test('canary better than baseline promotes', () => {
  const r = evaluateStage(baseline, { errorRate: 0.0019, p95Ms: 112, requests: 1250 });
  assert.equal(r.decision, 'PROMOTE');
});

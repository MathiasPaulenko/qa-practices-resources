/**
 * evaluate-stage.mjs — stage-gate evaluator for canary releases.
 *
 * Mirrors the checklist's gate logic:
 *   - missing metric data counts as a FAILED gate, never a pass
 *   - the canary is compared against a same-window stable baseline (deltas)
 *   - an absolute floor applies even when the delta looks fine
 *   - a minimum request volume makes low-traffic canaries fail closed
 *
 * Usage:
 *   node evaluate-stage.mjs baseline.json canary.json
 *
 * Both files look like: { "errorRate": 0.0028, "p95Ms": 120, "requests": 1250 }
 * Prints one of: PROMOTE | HOLD (not enough data yet) | ROLLBACK (+reason)
 */

const FLOORS = { errorRateMax: 0.02, p95MaxMs: 500, minRequests: 1000 };
const DELTAS = { errorRate: 0.005, p95Ms: 50 };

export function evaluateStage(baseline, canary, { minRequests = FLOORS.minRequests } = {}) {
  if (canary.errorRate == null || canary.p95Ms == null) {
    return { decision: 'ROLLBACK', reason: 'metric data missing — a gap is not a pass' };
  }
  if (canary.requests < minRequests) {
    return { decision: 'HOLD', reason: `${canary.requests} requests < ${minRequests} minimum — extend the stage` };
  }
  if (canary.errorRate > FLOORS.errorRateMax || canary.p95Ms > FLOORS.p95MaxMs) {
    return { decision: 'ROLLBACK', reason: 'absolute floor breached' };
  }
  const errDelta = canary.errorRate - baseline.errorRate;
  const latDelta = canary.p95Ms - baseline.p95Ms;
  if (errDelta > DELTAS.errorRate || latDelta > DELTAS.p95Ms) {
    return {
      decision: 'ROLLBACK',
      reason: `delta breached (errorRate ${(errDelta * 100).toFixed(2)}%, p95 ${Math.round(latDelta)}ms over baseline)`
    };
  }
  return { decision: 'PROMOTE', reason: 'within deltas and floors' };
}

const isMain = process.argv[1] && import.meta.url === new URL(`file://${process.argv[1].replace(/\\/g, '/')}`).href;
if (isMain) {
  const [, , baseFile, canaryFile] = process.argv;
  const { readFileSync } = await import('node:fs');
  const baseline = JSON.parse(readFileSync(baseFile, 'utf8'));
  const canary = JSON.parse(readFileSync(canaryFile, 'utf8'));
  const r = evaluateStage(baseline, canary);
  console.log(`${r.decision} — ${r.reason}`);
  process.exit(r.decision === 'PROMOTE' ? 0 : 1);
}

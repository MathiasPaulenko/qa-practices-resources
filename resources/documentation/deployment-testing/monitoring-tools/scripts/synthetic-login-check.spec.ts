// Synthetic login health check (@playwright/test 1.65.1).
// Run on a cron (every 5 min) or via Grafana k6 / Datadog Synthetics.
// Credentials come from env vars — use a dedicated synthetic account on
// staging, never a real user.
//
//   SYNTH_URL=https://staging.example.internal SYNTH_USER=... SYNTH_PASS=... \
//     npx playwright test synthetic-login-check.spec.ts

import { test, expect } from '@playwright/test';

const baseUrl = process.env.SYNTH_URL ?? 'http://localhost:3000';

test('login flow stays healthy', async ({ page }) => {
  const started = Date.now();

  await page.goto(`${baseUrl}/login`);
  await page.fill('[data-testid="email"]', process.env.SYNTH_USER!);
  await page.fill('[data-testid="password"]', process.env.SYNTH_PASS!);
  await page.click('[data-testid="login-button"]');

  await expect(page.locator('[data-testid="dashboard"]')).toBeVisible({
    timeout: 10_000,
  });

  const elapsed = Date.now() - started;
  // Latency budget: the whole journey should finish under 8s.
  // Expose `elapsed` to your collector (custom metric, log line or annotation).
  console.log(`synthetic_login_duration_ms=${elapsed}`);
  expect(elapsed).toBeLessThan(8_000);
});

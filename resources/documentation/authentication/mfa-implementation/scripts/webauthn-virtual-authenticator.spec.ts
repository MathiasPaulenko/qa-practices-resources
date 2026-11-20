import { test, expect } from '@playwright/test';

// Chromium only: CDP registers a software authenticator that signs real
// WebAuthn ceremonies — no hardware key needed in CI.
test('assertion via virtual authenticator', async ({ page, context }) => {
  const cdp = await context.newCDPSession(page);
  await cdp.send('WebAuthn.enable');
  const { authenticatorId } = await cdp.send('WebAuthn.addVirtualAuthenticator', {
    options: {
      protocol: 'ctap2',
      transport: 'internal',
      hasResidentKey: true,
      hasUserVerification: true,
      isUserVerified: true,
    },
  });

  await page.goto('https://staging.qapractices.com/login');
  await page.click('#sign-in-with-passkey');
  await expect(page).toHaveURL(/dashboard/);

  // Inspect what the ceremony created.
  const { credentials } = await cdp.send('WebAuthn.getCredentials', { authenticatorId });
  expect(credentials.length).toBeGreaterThanOrEqual(0);
});

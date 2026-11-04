import { test as base, type APIRequestContext } from '@playwright/test';

type AppFixtures = {
  apiContext: APIRequestContext;
  testUser: { email: string; password: string };
  cleanDb: void;
};

export const test = base.extend<AppFixtures>({
  testUser: async ({}, use) => {
    await use({
      email: `test-${Date.now()}@playwright.test`,
      password: 'TestPass123!',
    });
  },
  apiContext: async ({ playwright }, use) => {
    const ctx = await playwright.request.newContext({
      baseURL: process.env.API_BASE_URL ?? 'http://localhost:3000',
      extraHTTPHeaders: {
        Authorization: `Bearer ${process.env.API_TOKEN}`,
        'Content-Type': 'application/json',
      },
    });
    await use(ctx);
    await ctx.dispose();
  },
  cleanDb: async ({ apiContext }, use) => {
    await use();
    await apiContext.post('/api/test/reset');
  },
});

export { expect } from '@playwright/test';

import { test as base, expect, type Page } from '@playwright/test';

// Shared setup via test.extend: authenticated page + scoped test data
// created through the API, torn down in the fixture (not in the test body).

interface TestData {
  projectId: string;
  cleanup: () => Promise<void>;
}

async function apiRequest(page: Page, method: string, path: string, body?: unknown) {
  const res = await page.request.fetch(`${process.env.API_URL}${path}`, {
    method,
    data: body,
  });
  if (!res.ok()) throw new Error(`${method} ${path} -> ${res.status()}`);
  return res.json();
}

export const test = base.extend<{ data: TestData; authedPage: Page }>({
  // Reuses the session saved by the setup project (storageState),
  // no UI login per test.
  authedPage: async ({ page }, use) => {
    await page.goto('/');
    await expect(page.getByRole('navigation')).toBeVisible();
    await use(page);
  },

  // Each test gets its own project record; nothing is shared.
  data: async ({ request }, use) => {
    const project = await request
      .post(`${process.env.API_URL}/projects`, { data: { name: `pw-${Date.now()}` } })
      .then((r) => r.json());
    await use({
      projectId: project.id,
      cleanup: () => request.delete(`${process.env.API_URL}/projects/${project.id}`).then(() => {}),
    });
  },
});

export { expect } from '@playwright/test';

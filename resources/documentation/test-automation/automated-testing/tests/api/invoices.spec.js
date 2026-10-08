// Playwright 1.44 API test against Postgres 15 test container
import { test, expect } from '@playwright/test';

test('POST /invoices creates a draft', async ({ request }) => {
  const response = await request.post('/api/invoices', {
    data: { customerId: 'cust-123', amount: 1000, currency: 'EUR' },
    headers: { Authorization: 'Bearer test-token-ledgerflow' }
  });
  expect(response.status()).toBe(201);
  const body = await response.json();
  expect(body).toHaveProperty('id');
  expect(body.status).toBe('draft');
});

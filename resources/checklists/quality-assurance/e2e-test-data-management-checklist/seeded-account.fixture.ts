// Worker-scoped fixture: seeds an account via API and always deletes it,
// even when the test fails. Requires Playwright 1.49+.
import { test as base } from '@playwright/test';
import { createUser } from './user.factory';

interface SeededAccount {
  id: string;
  email: string;
}

export const test = base.extend<{ seededAccount: SeededAccount }>({
  seededAccount: async ({ request }, use) => {
    const res = await request.post('/api/accounts', { data: createUser() });
    if (!res.ok()) throw new Error(`Seeding failed: ${res.status()}`);
    const account = (await res.json()) as SeededAccount;
    await use(account);
    await request.delete(`/api/accounts/${account.id}`);
  },
});

export { expect } from '@playwright/test';

import { test, expect } from '@playwright/test';

test('fetch user and update role', async ({ request }) => {
  const query = await request.post('/graphql', {
    data: {
      query: `query { user(id: "1") { id email role } }`
    }
  });
  expect(query.ok()).toBeTruthy();
  const user = (await query.json()).data.user;
  expect(user.role).toBe('admin');

  const mutation = await request.post('/graphql', {
    data: {
      query: `mutation { updateRole(id: "1", role: "editor") { id role } }`
    }
  });
  expect(mutation.ok()).toBeTruthy();
});

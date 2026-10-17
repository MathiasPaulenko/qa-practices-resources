// Unique test data per invocation — safe for parallel workers.
import type { APIRequestContext } from '@playwright/test';

export interface User {
  email: string;
  firstName: string;
  lastName: string;
  role: 'qa' | 'admin' | 'viewer';
}

let seq = 0;

export function createUser(overrides: Partial<User> = {}): User {
  seq += 1;
  return {
    email: `qa-${Date.now()}-${seq}@test.qapractices.dev`,
    firstName: 'Ada',
    lastName: 'Lovelace',
    role: 'qa',
    ...overrides,
  };
}

export async function cleanupUser(api: APIRequestContext, userId: string): Promise<void> {
  await api.delete(`/users/${userId}`);
}

// math.test.ts
import { describe, it, expect, vi } from 'vitest';
import { sum, asyncFetch } from './math';
vi.mock('./api', () => ({
  fetchData: vi.fn(() => Promise.resolve({ id: 1 })),
}));
describe('math utilities', () => {
  it('sums two numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });
  it('mocks async fetch', async () => {
    const data = await asyncFetch();
    expect(data.id).toBe(1);
  });
});

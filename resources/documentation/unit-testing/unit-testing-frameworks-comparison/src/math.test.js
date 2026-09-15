// math.test.js
import { sum, asyncFetch } from './math';
jest.mock('./api', () => ({
  fetchData: jest.fn(() => Promise.resolve({ id: 1 })),
}));
beforeEach(() => {
  jest.clearAllMocks();
});
test('sums two numbers', () => {
  expect(sum(2, 3)).toBe(5);
});
test('mocks async fetch', async () => {
  const data = await asyncFetch();
  expect(data.id).toBe(1);
});

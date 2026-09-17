// Uses the '@/src' alias — resolved by moduleNameMapper under Jest
// (via babel-jest) and by resolve.alias under Vitest, from the same
// import specifier.
import { totalPrice, applyDiscount } from '@/cart';

describe('cart', () => {
  test('sums item prices', () => {
    const items = [
      { price: 25, qty: 2 },
      { price: 10, qty: 1 },
    ];
    expect(totalPrice(items)).toBe(60);
  });

  test('applies a percentage discount', () => {
    expect(applyDiscount(200, 15)).toBe(170);
  });

  test('rejects a discount above 100%', () => {
    expect(() => applyDiscount(200, 120)).toThrow('Discount must be between 0 and 100');
  });
});

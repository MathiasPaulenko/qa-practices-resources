// calculateTotal.test.js
// Unit test for cart discount logic — Test Pyramid layer: Unit
// Run with: npx jest src/calculateTotal.test.js

function calculateTotal(cart, discountThreshold = 100, discountRate = 0.1) {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price, 0);
  const discount = subtotal >= discountThreshold ? subtotal * discountRate : 0;
  return Math.round((subtotal - discount) * 100) / 100;
}

test('applies 10% discount for orders over $100', () => {
  const cart = { items: [{ price: 60 }, { price: 50 }] };
  expect(calculateTotal(cart)).toBe(99);
});

test('does not apply discount under the threshold', () => {
  const cart = { items: [{ price: 30 }, { price: 20 }] };
  expect(calculateTotal(cart)).toBe(50);
});

test('handles empty cart', () => {
  const cart = { items: [] };
  expect(calculateTotal(cart)).toBe(0);
});

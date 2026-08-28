const { add, divide } = require('../src/calculator');

describe('calculator', () => {
  describe('add', () => {
    it('adds two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('handles negative numbers', () => {
      expect(add(-2, -3)).toBe(-5);
    });
  });

  describe('divide', () => {
    it('throws on division by zero', () => {
      expect(() => divide(10, 0)).toThrow('Cannot divide by zero');
    });

    it('divides two numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });
  });
});

import { describe, it, expect } from '@jest/globals';
import { calculateTax } from '../../src/tax/calculateTax.js';

describe('calculateTax', () => {
  it('applies 21% VAT to a 100 EUR invoice', () => {
    expect(calculateTax({ amount: 100, rate: 0.21, region: 'ES' })).toBe(21);
  });

  it('returns 0 for zero-rated exports', () => {
    expect(calculateTax({ amount: 250, rate: 0, region: 'ES-export' })).toBe(0);
  });
});

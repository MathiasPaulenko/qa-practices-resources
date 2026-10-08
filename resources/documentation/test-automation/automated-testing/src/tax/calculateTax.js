export function calculateTax({ amount, rate, region }) {
  if (region.endsWith('-export')) {
    return 0;
  }
  return Math.round(amount * rate * 100) / 100;
}

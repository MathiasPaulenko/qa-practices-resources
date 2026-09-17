function totalPrice(items) {
  return items.reduce((sum, item) => sum + item.price * item.qty, 0);
}

function applyDiscount(total, percent) {
  if (percent < 0 || percent > 100) {
    throw new Error('Discount must be between 0 and 100');
  }
  return Math.round(total * (1 - percent / 100) * 100) / 100;
}

module.exports = { totalPrice, applyDiscount };

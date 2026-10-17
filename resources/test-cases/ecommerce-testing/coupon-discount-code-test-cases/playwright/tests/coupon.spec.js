const { test, expect } = require('@playwright/test');

// Self-contained coupon field fixture rendered inline — no store backend needed.
// Mirrors TC001 (percentage), TC026 (fixed capped at total), TC019 (no stacking).

const COUPONS = {
  SAVE10: { type: 'percent', value: 10 },
  DOLLAR50: { type: 'fixed', value: 50 },
  SPEND50: { type: 'percent', value: 15, minSpend: 50 },
};

function cartHtml(cartTotal = 100) {
  return `<!doctype html><html><body>
    <input id="coupon" data-testid="coupon-input" />
    <button id="apply" data-testid="apply-coupon">Apply</button>
    <div id="error" data-testid="coupon-error" style="display:none"></div>
    <div id="discount" data-testid="discount-line"></div>
    <div id="total" data-testid="cart-total">$${cartTotal.toFixed(2)}</div>
    <script>
      const coupons = ${JSON.stringify(COUPONS)};
      let applied = null;
      const base = ${cartTotal};
      document.getElementById('apply').addEventListener('click', () => {
        const code = document.getElementById('coupon').value.trim().toUpperCase();
        const err = document.getElementById('error');
        const c = coupons[code];
        if (applied) { err.textContent = 'Only one coupon per order.'; err.style.display = 'block'; return; }
        if (!c) { err.textContent = 'Invalid coupon code.'; err.style.display = 'block'; return; }
        if (c.minSpend && base < c.minSpend) { err.textContent = 'Minimum spend $' + c.minSpend + ' required.'; err.style.display = 'block'; return; }
        applied = c;
        const d = c.type === 'percent' ? Math.min(base * c.value / 100, base) : Math.min(c.value, base);
        const total = Math.max(base - d, 0);
        document.getElementById('discount').textContent = 'Discount: -$' + d.toFixed(2);
        document.getElementById('total').textContent = '$' + total.toFixed(2);
      });
    </script>
  </body></html>`;
}

test('TC001: percentage discount reduces total by 10%', async ({ page }) => {
  await page.setContent(cartHtml(100));
  await page.fill('[data-testid="coupon-input"]', 'SAVE10');
  await page.click('[data-testid="apply-coupon"]');
  await expect(page.locator('[data-testid="discount-line"]')).toContainText('-$10.00');
  await expect(page.locator('[data-testid="cart-total"]')).toHaveText('$90.00');
});

test('TC026: fixed discount caps at cart total, never negative', async ({ page }) => {
  await page.setContent(cartHtml(30));
  await page.fill('[data-testid="coupon-input"]', 'DOLLAR50');
  await page.click('[data-testid="apply-coupon"]');
  await expect(page.locator('[data-testid="cart-total"]')).toHaveText('$0.00');
});

test('TC018: below minimum spend is rejected', async ({ page }) => {
  await page.setContent(cartHtml(35));
  await page.fill('[data-testid="coupon-input"]', 'SPEND50');
  await page.click('[data-testid="apply-coupon"]');
  await expect(page.locator('[data-testid="coupon-error"]')).toContainText('Minimum spend');
});

test('TC019: second coupon rejected when stacking disabled', async ({ page }) => {
  await page.setContent(cartHtml(100));
  await page.fill('[data-testid="coupon-input"]', 'SAVE10');
  await page.click('[data-testid="apply-coupon"]');
  await page.fill('[data-testid="coupon-input"]', 'DOLLAR50');
  await page.click('[data-testid="apply-coupon"]');
  await expect(page.locator('[data-testid="coupon-error"]')).toContainText('Only one coupon');
  await expect(page.locator('[data-testid="cart-total"]')).toHaveText('$90.00');
});

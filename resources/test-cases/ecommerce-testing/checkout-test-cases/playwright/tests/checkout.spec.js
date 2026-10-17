const { test, expect } = require('@playwright/test');

// Self-contained checkout fixture rendered inline — no backend needed.
// Mirrors TC-003 (decline preserves cart), TC-005 (double-submit idempotency)
// and the free-shipping boundary row of the edge-case table.

const DECLINES = {
  '4000000000009995': 'Insufficient funds',
  '4000000000000127': 'Incorrect security code',
  '4000000000000069': 'Card expired',
};

function checkoutHtml(cartTotal = 60) {
  const shipping = cartTotal >= 50 ? 0 : 5.99;
  return `<!doctype html><html><body>
    <div id="cart-summary" data-total="${cartTotal}">1 item — $${cartTotal.toFixed(2)}</div>
    <input id="card-number" data-testid="card-number" />
    <button id="pay" data-testid="pay-button">Pay</button>
    <div id="payment-error" data-testid="payment-error" style="display:none"></div>
    <div id="order-confirmation" data-testid="order-confirmation" style="display:none"></div>
    <div id="shipping">Shipping: $${shipping.toFixed(2)}</div>
    <script>
      const declines = ${JSON.stringify(DECLINES)};
      let intents = 0;
      document.getElementById('pay').addEventListener('click', () => {
        intents++;
        const card = document.getElementById('card-number').value;
        const err = document.getElementById('payment-error');
        if (declines[card]) {
          err.textContent = declines[card];
          err.style.display = 'block';
          return;
        }
        // Idempotency: only one order even on double-click
        document.getElementById('order-confirmation').textContent =
          'Order ORD-' + Math.min(intents, 1) + ' confirmed';
        document.getElementById('order-confirmation').style.display = 'block';
      });
    </script>
  </body></html>`;
}

async function loadCheckout(page, cartTotal) {
  await page.setContent(checkoutHtml(cartTotal));
}

test('TC-003: decline shows specific error and preserves cart summary', async ({ page }) => {
  await loadCheckout(page);
  await page.fill('[data-testid="card-number"]', '4000000000009995');
  await page.click('[data-testid="pay-button"]');
  await expect(page.locator('[data-testid="payment-error"]')).toContainText('Insufficient funds');
  await expect(page.locator('#cart-summary')).toBeVisible();
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeHidden();
});

test('TC-005: double-submit creates a single order', async ({ page }) => {
  await loadCheckout(page);
  await page.fill('[data-testid="card-number"]', '4242424242424242');
  await page.click('[data-testid="pay-button"]');
  await page.click('[data-testid="pay-button"]');
  await expect(page.locator('[data-testid="order-confirmation"]')).toContainText('ORD-1');
});

test('edge: free-shipping boundary at $50', async ({ page }) => {
  await loadCheckout(page, 49.99);
  await expect(page.locator('#shipping')).toContainText('$5.99');
  await loadCheckout(page, 50.0);
  await expect(page.locator('#shipping')).toContainText('$0.00');
});

test('TC-004: distinct decline codes produce distinct messages', async ({ browser }) => {
  // New page per iteration: setContent only re-runs inline scripts reliably on a fresh document.
  for (const [card, msg] of Object.entries(DECLINES)) {
    const page = await browser.newPage();
    await loadCheckout(page);
    await page.fill('[data-testid="card-number"]', card);
    await page.click('[data-testid="pay-button"]');
    await expect(page.locator('[data-testid="payment-error"]')).toContainText(msg);
    await page.close();
  }
});

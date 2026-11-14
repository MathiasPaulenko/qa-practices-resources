# Example Output — Generated Playwright Suite Fragment

```typescript
// tests/checkout/checkout.spec.ts
import { test, expect } from './fixtures/base-test';
import { testUsers } from './fixtures/test-data';

test.describe('Checkout Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/checkout');
  });

  test('successful checkout with valid payment', async ({ page }) => {
    const checkout = new CheckoutPage(page);
    await checkout.fillShippingInfo(testUsers.standard);
    await checkout.selectPaymentMethod('credit_card');
    await checkout.fillCardDetails({
      number: '4111111111111111',
      expiry: '12/25',
      cvv: '123',
    });
    await checkout.submitOrder();

    await expect(page).toHaveURL(/\/order-confirmation/);
    await expect(checkout.confirmationMessage).toBeVisible();
    await expect(checkout.orderId).toMatch(/ORD-\d{6}/);
  });

  test('checkout with empty cart shows error', async ({ page }) => {
    const checkout = new CheckoutPage(page);
    await checkout.submitOrder();

    await expect(checkout.errorMessage).toBeVisible();
    await expect(checkout.errorMessage).toHaveText('Your cart is empty');
  });
});```

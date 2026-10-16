---
resourceType: checklists
slug: ecommerce-checkout-testing-checklist
title: 'E-commerce Checkout Testing Checklist: Payments & Orders'
description: 'Checkout is where revenue lives or dies. This checklist walks the whole purchase flow — cart, auth, shipping, tax, discounts, payments, fraud and order confirmation.'
metaDescription: 'E-commerce checkout testing checklist: 50+ items across cart, shipping, tax, payments, fraud and confirmation — plus Playwright and webhook examples.'
difficulty: intermediate
topics:
- ecommerce-testing
tags:
- ecommerce-checkout
- fraud-prevention
- order-confirmation
- payment-testing
- shipping
- shopping-cart
- tax-calculation
relatedResources:
- /checklists/ecommerce-testing-checklist
- /checklists/payment-gateway-integration-testing-checklist
- /checklists/web-testing-checklist
- /test-cases/ecommerce-checkout-test-cases
- /documentation/e-commerce-checkout-flow-testing-guide
- /documentation/ecommerce-security
ogImage: /assets/og-images/ecommerce-checkout-testing-checklist.png
lastUpdated: '2026-10-16'
created: '2026-01-02'
author: Mathias Paulenko
featured: false
seo:
  metaDescription: 'E-commerce checkout testing checklist: 50+ items across cart, shipping, tax, payments, fraud and confirmation — plus Playwright and webhook examples.'
  keywords:
  - ecommerce checkout testing checklist
  - checkout testing checklist
  - payment flow testing
  - shopping cart testing
  - ecommerce
  - order confirmation testing
---
# E-commerce Checkout Testing Checklist: Payments & Orders

## Overview

Every other page in an e-commerce store can afford a bug — checkout can't. A broken payment step doesn't produce a 500 page, it produces abandoned carts and orders that never existed. This checklist covers the whole purchase flow end to end: cart behavior, authentication, shipping, taxes, discounts, payment processing, fraud controls, order confirmation, and the edge cases that only appear when things go wrong mid-transaction.

Run it before any release that touches the checkout path, and before peak season. For the broader storefront scope, see the [E-commerce Testing Checklist](/checklists/ecommerce-testing-checklist); for executable test scenarios, pair it with the [Ecommerce Checkout Test Cases](/test-cases/ecommerce-checkout-test-cases) and the [Checkout Flow Testing Guide](/documentation/e-commerce-checkout-flow-testing-guide).

![Checkout validation funnel: cart, authentication, shipping, tax and discounts, payment with a fraud-check branch, and order confirmation — where each failure mode gets caught](/assets/images/diagrams/checkout-testing-validation-funnel.svg)

## When to Use

- **Before launching a new store:** run the full list before go-live — a broken checkout on day one is a revenue emergency.
- **After payment gateway changes:** a new processor config, API version or webhook handler means re-testing the whole flow.
- **Before peak shopping seasons:** Black Friday and holiday sales stress the checkout infrastructure; run this with a load test about two weeks out.
- **After cart or checkout redesigns:** UI changes introduce new edge cases; re-test end to end after any visual or structural change.

## Cart Management

- [ ] **Add to cart** — products can be added from product pages, category pages and search results; the count badge updates immediately.
  - **Risk:** Medium
- [ ] **Cart persistence** — contents survive logout and return; guest carts persist via cookie or local storage for 30+ days.
  - **Risk:** Medium
- [ ] **Quantity updates** — increase, decrease and remove all work, and totals recalculate instantly.
  - **Risk:** Low
- [ ] **Out-of-stock handling** — items that sell out while in the cart get flagged, checkout is blocked for them, and alternatives are offered.
  - **Risk:** High
- [ ] **Price change reflection** — if a price changes mid-session, the cart shows the current price and warns the user.
  - **Risk:** Medium
- [ ] **Cart merge on login** — a guest cart merges with the account cart on login; nothing is lost and duplicates combine quantities.
  - **Risk:** Medium
- [ ] **Cart limits** — maximum item count or total value limits are enforced with a clear error message.
  - **Risk:** Low

## User Authentication

- [ ] **Guest checkout** — purchase completes without an account; account creation is offered after, never forced.
  - **Risk:** Medium
- [ ] **Mid-checkout login** — returning users can log in mid-flow without losing the cart and land back on the correct step.
  - **Risk:** Medium
- [ ] **Social login** — Google, Apple and Facebook sign-in work and return to checkout without data loss.
  - **Risk:** Low
- [ ] **Password reset** — users can reset a forgotten password without leaving checkout; the reset email arrives within a minute.
  - **Risk:** High

## Shipping and Fulfillment

- [ ] **Address validation** — addresses verify against postal APIs, invalid ones get correction suggestions, PO boxes follow shipping rules.
  - **Risk:** Medium
- [ ] **Shipping methods** — all options (standard, express, overnight, pickup) display with correct rates and delivery estimates.
  - **Risk:** Low
- [ ] **Rate calculation** — shipping costs match the carrier API, and free-shipping thresholds trigger at the right subtotal.
  - **Risk:** High
- [ ] **International orders** — foreign addresses are accepted where supported, customs and duties are calculated or disclosed, country restrictions hold.
  - **Risk:** Medium
- [ ] **Address autocomplete** — suggestions speed up entry and populate every field correctly.
  - **Risk:** Low
- [ ] **Restricted products** — hazmat and age-restricted items show warnings and can't ship to prohibited regions.
  - **Risk:** High

## Tax Calculation

- [ ] **Jurisdiction rates** — sales tax, VAT and GST calculate correctly per shipping address against current tax tables.
  - **Risk:** High
- [ ] **Tax on shipping** — where applicable, shipping costs are taxed too; rules vary by jurisdiction, verify each one you sell into.
  - **Risk:** Medium
- [ ] **Tax-exempt orders** — B2B customers with exemption status can buy tax-free; certificates are validated and stored.
  - **Risk:** High
- [ ] **Digital products** — downloads, subscriptions and services follow their own tax rules, different from physical goods in many jurisdictions.
  - **Risk:** Medium
- [ ] **Tax visible before payment** — the tax amount shows on the order summary before card details are entered; no surprise charges.
  - **Risk:** High

## Discounts and Promotions

- [ ] **Coupon application** — valid codes apply the right discount (percentage, fixed, free shipping); invalid or expired codes get clear errors.
  - **Risk:** Medium
- [ ] **Stacking rules** — non-combinable coupons can't stack; where stacking is allowed, combined discounts calculate correctly.
  - **Risk:** Medium
- [ ] **Minimum purchase** — threshold coupons only apply when the subtotal qualifies, checked after other discounts if configured.
  - **Risk:** Low
- [ ] **Exclusions** — category and product exclusions hold; discounts calculate only on eligible items.
  - **Risk:** Low
- [ ] **Usage limits** — single-use codes can't be reused, per-user limits hold, and total caps stop the coupon at the limit.
  - **Risk:** Medium
- [ ] **Automatic promotions** — BOGO, free-gift and tiered discounts trigger on their own; no manual code entry needed.
  - **Risk:** Low
- [ ] **Expired promotions** — ended promos stop applying and no stale discount amount shows in the cart.
  - **Risk:** Low

## Payment Processing

- [ ] **Card payments** — Visa, Mastercard, Amex and Discover process correctly; card numbers are tokenized, never stored (see PCI DSS in References).
  - **Risk:** High
- [ ] **Digital wallets** — Apple Pay, Google Pay and PayPal complete checkout in minimal steps, with shipping and billing populated from the wallet.
  - **Risk:** High
- [ ] **Decline handling** — declined cards show the processor's reason, and users can retry with another method without re-entering shipping info.
  - **Risk:** High
- [ ] **3D Secure / SCA** — Strong Customer Authentication triggers when the issuer requires it; the challenge completes and the order processes.
  - **Risk:** High
- [ ] **Regional payment methods** — methods display by user location: iDEAL in the Netherlands, Klarna in Scandinavia, PIX in Brazil, and so on.
  - **Risk:** Medium
- [ ] **Split payments** — gift card plus credit card splits calculate correctly, and the gift card balance updates after purchase.
  - **Risk:** Medium
- [ ] **Refund flow** — full and partial refunds process through the gateway and sync status back to the OMS.
  - **Risk:** Medium
- [ ] **Webhook handling** — gateway webhooks (success, failure, dispute) are received and processed; idempotency prevents duplicate orders on retries.
  - **Risk:** High

## Fraud Prevention

- [ ] **AVS checks** — billing address verifies against the card issuer; mismatches trigger review or decline per risk settings.
  - **Risk:** Medium
- [ ] **CVV required** — CVV is validated on every card payment and failed checks block the transaction.
  - **Risk:** High
- [ ] **Velocity rules** — repeat orders from the same IP, device or card in a short window get flagged.
  - **Risk:** Medium
- [ ] **Device fingerprinting** — fraud services (Sift, Signifyd, Riskified) score device and behavioral signals; high-risk orders hold for review.
  - **Risk:** Medium
- [ ] **BIN country match** — card BIN country compares against shipping and billing countries; mismatches trigger extra verification.
  - **Risk:** Medium

## Order Confirmation

- [ ] **Confirmation page** — shows order number, items, totals and estimated delivery after successful payment; printable.
  - **Risk:** Medium
- [ ] **Confirmation email** — arrives within ~2 minutes with order details, tracking link where available, and a support contact.
  - **Risk:** Low
- [ ] **SMS notification** — if enabled, the confirmation text sends; opted-out users never receive it.
  - **Risk:** Low
- [ ] **Order in account** — the order appears in user history with the right status (pending, processing, paid).
  - **Risk:** Medium
- [ ] **Inventory decrement** — stock drops by the purchased quantity, and out-of-stock alerts fire at zero.
  - **Risk:** High
- [ ] **ERP/OMS sync** — order number, items, totals and customer data sync correctly to the order management system.
  - **Risk:** Medium

## Edge Cases and Error Handling

- [ ] **Session timeout mid-checkout** — an expired session prompts re-authentication and preserves the cart.
  - **Risk:** Medium
- [ ] **Network drop during payment** — on reconnection the system checks the payment status; no duplicate charges.
  - **Risk:** High
- [ ] **Concurrent checkouts** — the same user on two devices produces one order, not two; the second attempt gets a clear message.
  - **Risk:** Medium
- [ ] **Browser back button** — pressing back after payment doesn't resubmit; the user sees the confirmation or an "order already placed" message.
  - **Risk:** Medium
- [ ] **Empty cart** — checkout can't proceed with an empty cart; the button is disabled or routes back to the cart.
  - **Risk:** Low

## From the Field

The bug that taught me to take split payments seriously: a rounding error in the gift-card-plus-card flow charged customers one cent less than the order total, then the payment gateway rejected the capture as an amount mismatch. It shipped on a Friday, and over the weekend 47 orders went into a "paid but unfilled" limbo — no alerts, because nothing technically failed.

Two items from this list would have caught it in staging: the split-payment calculation under Payment Processing, and the inventory/OMS sync under Order Confirmation. We added both to the release gate after that weekend, and the refund path got its own smoke test — partial refunds were where the next bug was hiding anyway.

## Best Practices

1. **Test in the gateway's sandbox.** Never run live credentials through a checkout test. Stripe test cards, PayPal sandbox and the processor's test environment cover success and every decline code.
2. **Test declines, not just approvals.** Run each card decline code the gateway documents (insufficient funds, expired card, do_not_honor) and verify the message, the retry path and that no order gets created.
3. **Test on a real phone.** Over 60% of e-commerce traffic is mobile — a real device catches keyboard behavior, autofill and wallet-sheet issues that responsive dev tools miss.
4. **Watch the funnel.** Track conversion per checkout step; a sharp drop at the payment step usually means friction or trust problems, not a marketing issue.
5. **Replay webhooks.** Stripe CLI or a captured payload lets you replay success, failure and dispute events — out of order, duplicated, delayed — to prove idempotency.
6. **Use realistic data.** Long names, special characters, international addresses and edge formats find input bugs that "Test Test" never will.

## Common Mistakes

1. **Testing tax only on the default rate.** Cross-state and cross-border rules are where tax engines break — test addresses in several jurisdictions, including digital goods.
2. **Forgetting gift cards and store credit.** Balance checks, partial redemption and combining with other payment methods are their own flows — tested last, broken first.
3. **Trusting webhook order.** Payment webhooks arrive out of order, duplicated and delayed; without idempotency you get duplicate orders or missed fulfillments.
4. **Skipping the load test.** Checkout hits payment APIs, tax engines and inventory at once — it needs a 100+ concurrent-user test before peak season, not a guess.
5. **Only testing the happy payment path.** Approvals are the easy case; declines, timeouts and mid-payment retries are where orders get duplicated or lost.
6. **Never testing the refund.** The refund flow is part of checkout — partial refunds and gateway-to-OMS sync break quietly until a customer calls.

## Automation Examples

### Playwright Checkout Test

A guest checkout with a coupon, end to end (Playwright 1.x, TypeScript):

```typescript
test('completes guest checkout with discount', async ({ page }) => {
  await page.goto('/product/headphones');
  await page.click('[data-testid="add-to-cart"]');
  await page.goto('/checkout');
  await page.fill('[data-testid="email"]', 'guest@example.com');
  await page.fill('[data-testid="shipping-address"]', '123 Main St');
  await page.click('[data-testid="apply-coupon"]');
  await page.fill('[data-testid="coupon-code"]', 'SUMMER20');
  await page.click('[data-testid="place-order"]');
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
});
```

### Stripe Webhook Replay

Replaying a captured webhook payload against the local endpoint (replace the signature with a real captured one or use `stripe listen --forward-to`):

```bash
curl -X POST https://staging.your-store.com/webhooks/stripe \
  -H "Content-Type: application/json" \
  -H "Stripe-Signature: t=...,v1=..." \
  -d '{
    "id": "evt_3O...",
    "type": "payment_intent.succeeded",
    "data": { "object": { "id": "pi_3O...", "amount": 2999, "currency": "usd" } }
  }'
```

### Order Summary Assertion

The shape an order summary should assert against after payment:

```json
{
  "orderId": "ord_9x2A",
  "status": "paid",
  "items": [{ "sku": "hp-001", "qty": 1, "price": 29.99 }],
  "tax": 2.10,
  "shipping": 5.00,
  "discount": 6.00,
  "total": 31.09
}
```

## Frequently Asked Questions

### Should checkout testing ever use real card numbers?

Never. Every major gateway publishes test card numbers for exactly this — Stripe's `4242 4242 4242 4242` covers the success path, and there are dedicated numbers for each decline code. Real card data in a test environment is also a PCI DSS scope violation.

### What is the minimum checkout smoke test before a release?

Five checks: add to cart, guest checkout with one card payment, discount application, confirmation email received, and inventory decremented. That covers the revenue path end to end in under ten minutes; everything else is depth on top of it.

### How do you test payment declines?

Each gateway documents test cards or triggers per decline code — insufficient funds, expired card, do_not_honor, lost card. Run the full set and verify three things per decline: the user sees a clear reason, they can retry with another method without re-entering everything, and no order gets created in limbo.

### When does 3D Secure have to trigger?

In the EEA and UK, Strong Customer Authentication is legally required for most online card payments under PSD2 — issuers decide whether to show a challenge or approve frictionlessly. Test both paths: the 3DS challenge completing, and the low-risk exemption passing without one.

### How do you load test a checkout flow?

On staging, with the gateway in sandbox mode — never against the live payment API. k6 or JMeter driving concurrent checkouts will surface the real bottleneck, which is usually the tax calculation or the payment call, not your servers. Run it about two weeks before any expected traffic peak.

## References

- [PCI Security Standards Council — PCI DSS](https://www.pcisecuritystandards.org/document_library)
- [EMVCo — 3-D Secure Specifications](https://www.emvco.com/emv-technologies/3-d-secure/)
- [Stripe — Testing documentation and test cards](https://docs.stripe.com/testing)
- [Stripe CLI — webhook forwarding and replay](https://docs.stripe.com/stripe-cli)

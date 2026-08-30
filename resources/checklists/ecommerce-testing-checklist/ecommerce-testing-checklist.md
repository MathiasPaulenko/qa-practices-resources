# Ecommerce Testing Checklist

> Printable companion for QAPractices.com

## --- Checklist

## Product Catalog Checklist
- [ ] Product pages display correct images, prices, stock status and descriptions.
  - **Risk:** High
- [ ] Search returns relevant results for exact names, partial names and common typos.
  - **Risk:** Medium
- [ ] Filters and sorting work with realistic product volumes (category, price, brand, rating).
  - **Risk:** Medium
- [ ] Product variants update price, SKU and stock when size or color changes.
  - **Risk:** High
- [ ] Out-of-stock products are clearly marked or hidden according to business rules.
  - **Risk:** High
- [ ] Reviews and ratings load and respect moderation/approval workflows.
  - **Risk:** Low
- [ ] Pagination and infinite scroll work without duplicated or missing items.
  - **Risk:** Low

## Shopping Cart Checklist
- [ ] Items can be added from product page, listing page and recently viewed.
  - **Risk:** Medium
- [ ] Cart badge updates immediately and matches line-item count.
  - **Risk:** Low
- [ ] Quantity can be changed and subtotal recalculates with taxes and discounts.
  - **Risk:** High
- [ ] Items can be removed and the cart shows an empty state.
  - **Risk:** Low
- [ ] Guest cart merges with user cart after login without losing items.
  - **Risk:** High
- [ ] Cart persists across sessions for logged-in users.
  - **Risk:** High
- [ ] Abandoned-cart email triggers within the configured delay (1–24 hours).
  - **Risk:** Medium

## Checkout Checklist
- [ ] Guest checkout and registered checkout both work end-to-end.
  - **Risk:** Medium
- [ ] Shipping address validates against supported regions and carrier rules.
  - **Risk:** Medium
- [ ] Shipping options and costs update when the address changes.
  - **Risk:** Medium
- [ ] Tax calculations are accurate for state, province and VAT rules.
  - **Risk:** High
- [ ] Promo and coupon codes apply, stack correctly and respect expiration.
  - **Risk:** High
- [ ] Minimum order value and free-shipping thresholds calculate correctly.
  - **Risk:** Medium
- [ ] Order total, line items, shipping and tax appear before payment.
  - **Risk:** High

## Payment Checklist
- [ ] Card payments complete successfully with the production gateway's sandbox.
  - **Risk:** High
- [ ] Declined cards, 3D Secure and OTP flows show clear, actionable errors.
  - **Risk:** High
- [ ] Partial payments (gift card + card, store credit + card) process correctly.
  - **Risk:** High
- [ ] Refund and cancellation flows return funds and restore inventory.
  - **Risk:** High
- [ ] Payment confirmation is received by the customer and the order service.
  - **Risk:** High
- [ ] PCI-compliant tokenization is used; raw card data never hits the server.
  - **Risk:** High

## Order & Inventory Checklist
- [ ] Order confirmation email includes order number, items, total and shipping address.
  - **Risk:** High
- [ ] Order status updates correctly from placed to shipped to delivered.
  - **Risk:** High
- [ ] Inventory decrements only after a successful order, not on add-to-cart.
  - **Risk:** High
- [ ] Low-stock alerts fire before the product sells out.
  - **Risk:** High
- [ ] Order cancellation by customer and admin updates stock and refund status.
  - **Risk:** High
- [ ] Return/refund process updates order totals, inventory and customer balance.
  - **Risk:** High

## Security & Compliance Checklist
- [ ] HTTPS is enforced and there's no mixed content on checkout pages.
  - **Risk:** High
- [ ] Customer PII and payment tokens are encrypted at rest.
  - **Risk:** High
- [ ] Admin panel requires MFA and role-based access control.
  - **Risk:** High
- [ ] Session tokens expire after a reasonable timeout and rotate on privilege change.
  - **Risk:** High
- [ ] CSRF tokens validate on cart, checkout, account and payment forms.
  - **Risk:** High
- [ ] SQL injection and XSS protections cover search, reviews and product fields.
  - **Risk:** High
- [ ] Rate limiting protects login, password reset and coupon endpoints.
  - **Risk:** High
- [ ] Security headers (CSP, X-Frame-Options, X-Content-Type-Options) are present.
  - **Risk:** High

## Performance & Mobile Checklist
- [ ] Checkout completes within 5 seconds including payment processing.
  - **Risk:** High
- [ ] Product images use WebP, lazy loading and responsive `srcset`.
  - **Risk:** Low
- [ ] Search returns results within 2 seconds on typical queries.
  - **Risk:** Medium
- [ ] Site handles peak traffic (Black Friday, flash sales) without errors.
  - **Risk:** Medium
- [ ] Full checkout flow works on iOS and Android with real payment options.
  - **Risk:** High
- [ ] Touch targets, input zoom and mobile keyboards don't break payment forms.
  - **Risk:** High

## Notifications & SEO Checklist
- [ ] Order, shipping and password-reset emails include correct data and tracking links.
  - **Risk:** High
- [ ] Promotional emails include an unsubscribe link and pass SPF/DKIM/DMARC.
  - **Risk:** Low
- [ ] Product pages have unique titles, meta descriptions and valid Product schema.
  - **Risk:** Low
- [ ] Canonical URLs and sitemap prevent duplicate product and category pages.
  - **Risk:** Low
- [ ] Analytics events fire on add-to-cart, checkout, purchase and refund.
  - **Risk:** High

## Accessibility Checklist
- [ ] Add-to-cart, filters and checkout fields are keyboard accessible.
  - **Risk:** Low
- [ ] Product images have meaningful alt text or are marked decorative.
  - **Risk:** Low
- [ ] Form fields in checkout have associated labels and error announcements.
  - **Risk:** Medium
- [ ] Color contrast meets WCAG 2.2 AA for prices, badges and error states.
  - **Risk:** Low
- [ ] Focus order follows the logical checkout flow.
  - **Risk:** Low

## Edge Cases & Negative Checks Checklist
- [ ] Pay with an expired card and verify the payment is rejected with a clear message.
  - **Risk:** High
- [ ] Pay with insufficient funds and confirm the user can retry without double-charging.
  - **Risk:** High
- [ ] Submit payment with a missing or short CVV and verify validation blocks it.
  - **Risk:** High
- [ ] Apply an already-used, expired or region-locked coupon and verify rejection.
  - **Risk:** High
- [ ] Attempt to buy more units than available stock and verify oversell protection.
  - **Risk:** High
- [ ] Change currency after cart is loaded and confirm prices recalculate or warn.
  - **Risk:** Medium
- [ ] Complete checkout with a shipping address the carrier doesn't serve.
  - **Risk:** Medium

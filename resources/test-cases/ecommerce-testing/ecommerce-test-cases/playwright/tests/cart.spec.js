const { test, expect } = require('@playwright/test');

// Self-contained fixtures rendered inline — no store backend needed.
// Mirrors TC-001..005 (cart), TC-032 (stock) and TC-034 (coupon math)
// from the QAPractices e-commerce test cases suite.

const PRODUCTS = [
  { sku: 'SKU-1001', name: 'Wireless headphones', price: 29.99, stock: 3 },
  { sku: 'SKU-2005', name: 'USB-C cable', price: 14.5, stock: 10 },
  { sku: 'SKU-3007', name: 'Webcam 4K', price: 89.0, stock: 0 },
];

function storeHtml(cart = []) {
  const items = cart
    .map(
      (c) =>
        `<li data-sku="${c.sku}">${c.name} — qty ${c.qty} — $${(c.price * c.qty).toFixed(2)}
          <button class="remove" data-remove="${c.sku}">remove</button>
          <button class="qtyplus" data-qtyplus="${c.sku}">+</button></li>`
    )
    .join('');
  const subtotal = cart.reduce((s, c) => s + c.price * c.qty, 0);
  return `<!doctype html><html><body>
    <span id="badge">${cart.reduce((s, c) => s + c.qty, 0)}</span>
    <ul id="products">${PRODUCTS.map(
      (p) => `<li>${p.name} $${p.price}
        <button data-add="${p.sku}" ${p.stock === 0 ? 'disabled' : ''}>
          ${p.stock === 0 ? 'Out of stock' : 'Add to Cart'}</button></li>`
    ).join('')}</ul>
    <ul id="cart">${items}</ul>
    <div id="subtotal">$${subtotal.toFixed(2)}</div>
    <input id="coupon" />
    <button id="apply-coupon">Apply</button>
    <div id="total"></div>
    <script>
      let cart = ${JSON.stringify(cart)};
      const money = (n) => '$' + n.toFixed(2);
      function render() {
        document.getElementById('badge').textContent = cart.reduce((s, c) => s + c.qty, 0);
        document.getElementById('cart').innerHTML = cart.map((c) =>
          '<li data-sku="' + c.sku + '">' + c.name + ' — qty ' + c.qty + ' — ' + money(c.price * c.qty) +
          ' <button data-remove="' + c.sku + '">remove</button>' +
          ' <button data-qtyplus="' + c.sku + '">+</button></li>').join('');
        document.getElementById('subtotal').textContent =
          money(cart.reduce((s, c) => s + c.price * c.qty, 0));
      }
      const prods = ${JSON.stringify(PRODUCTS)};
      document.body.addEventListener('click', (e) => {
        if (e.target.dataset.add) {
          const p = prods.find((x) => x.sku === e.target.dataset.add);
          const row = cart.find((x) => x.sku === p.sku);
          row ? row.qty++ : cart.push({ ...p, qty: 1 });
          render();
        }
        if (e.target.dataset.remove) {
          cart = cart.filter((x) => x.sku !== e.target.dataset.remove);
          render();
        }
        if (e.target.dataset.qtyplus) {
          cart.find((x) => x.sku === e.target.dataset.qtyplus).qty++;
          render();
        }
      });
      document.getElementById('apply-coupon').addEventListener('click', () => {
        const code = document.getElementById('coupon').value;
        const sub = cart.reduce((s, c) => s + c.price * c.qty, 0);
        document.getElementById('total').textContent =
          code === 'SUMMER20' ? money(sub * 0.8) : 'Invalid coupon';
      });
      render();
    </script></body></html>`;
}

test('TC-001/002: adding two products updates badge, lines and subtotal', async ({ page }) => {
  await page.setContent(storeHtml());
  await page.click('[data-add="SKU-1001"]');
  await page.click('[data-add="SKU-2005"]');
  await expect(page.locator('#badge')).toHaveText('2');
  await expect(page.locator('#cart li')).toHaveCount(2);
  await expect(page.locator('#subtotal')).toHaveText('$44.49');
});

test('TC-003: raising quantity recalculates line total and subtotal', async ({ page }) => {
  await page.setContent(
    storeHtml([{ ...PRODUCTS[0], qty: 1 }])
  );
  await page.click('[data-qtyplus="SKU-1001"]');
  await page.click('[data-qtyplus="SKU-1001"]');
  await expect(page.locator('#badge')).toHaveText('3');
  await expect(page.locator('#subtotal')).toHaveText('$89.97');
});

test('TC-004: removing an item keeps the other and fixes subtotal', async ({ page }) => {
  await page.setContent(
    storeHtml([{ ...PRODUCTS[0], qty: 1 }, { ...PRODUCTS[1], qty: 1 }])
  );
  await page.click('[data-remove="SKU-2005"]');
  await expect(page.locator('#cart li')).toHaveCount(1);
  await expect(page.locator('#subtotal')).toHaveText('$29.99');
  await expect(page.locator('#badge')).toHaveText('1');
});

test('TC-032: zero-stock product disables the add button', async ({ page }) => {
  await page.setContent(storeHtml());
  const btn = page.locator('[data-add="SKU-3007"]');
  await expect(btn).toBeDisabled();
  await expect(btn).toHaveText('Out of stock');
});

test('TC-034: SUMMER20 applies 20% off and invalid code fails', async ({ page }) => {
  await page.setContent(
    storeHtml([{ ...PRODUCTS[0], qty: 1 }, { ...PRODUCTS[1], qty: 1 }])
  );
  await page.fill('#coupon', 'SUMMER20');
  await page.click('#apply-coupon');
  await expect(page.locator('#total')).toHaveText('$35.59');
  await page.fill('#coupon', 'NOPE10');
  await page.click('#apply-coupon');
  await expect(page.locator('#total')).toHaveText('Invalid coupon');
});

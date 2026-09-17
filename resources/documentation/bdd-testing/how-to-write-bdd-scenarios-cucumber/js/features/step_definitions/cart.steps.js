const { Given, When, Then } = require('@cucumber/cucumber');
const assert = require('node:assert/strict');

class Shop {
  constructor() {
    this.catalog = new Map();
    this.cart = new Map();
  }

  stockProduct(name, price, units) {
    this.catalog.set(name, price);
  }

  clearCart() {
    this.cart.clear();
  }

  addToCart(name) {
    this.cart.set(name, (this.cart.get(name) || 0) + 1);
  }

  itemCount() {
    return [...this.cart.values()].reduce((a, b) => a + b, 0);
  }

  createOrder(rows) {
    this.cart.clear();
    for (const row of rows) {
      this.cart.set(row.product, (this.cart.get(row.product) || 0) + Number(row.quantity));
    }
  }

  total() {
    let sum = 0;
    for (const [name, qty] of this.cart) {
      sum += (this.catalog.get(name) || 0) * qty;
    }
    return sum;
  }

  totalFormatted() {
    return `$${this.total()}.00`;
  }
}

Given('I am logged in as a registered user', function () {
  this.shop = new Shop();
});

Given('I have an empty shopping cart', function () {
  this.shop.clearCart();
});

Given('the following products exist:', function (dataTable) {
  for (const row of dataTable.hashes()) {
    this.shop.stockProduct(row.name, Number(row.price), Number(row.stock));
  }
});

When('I add {string} to the cart', function (name) {
  this.shop.addToCart(name);
});

When('I create an order with:', function (dataTable) {
  this.shop.createOrder(dataTable.hashes());
});

Then('the cart should contain {int} item', function (count) {
  assert.equal(this.shop.itemCount(), count);
});

Then('the cart total should be {string}', function (expected) {
  assert.equal(this.shop.totalFormatted(), expected);
});

Then('the order total should be {string}', function (expected) {
  assert.equal(this.shop.totalFormatted(), expected);
});

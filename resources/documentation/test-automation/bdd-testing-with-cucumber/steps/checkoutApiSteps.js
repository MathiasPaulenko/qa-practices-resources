// steps/checkoutApiSteps.js
const { Given, When, Then } = require('@cucumber/cucumber');
const axios = require('axios');
const { expect } = require('@playwright/test');

const API_BASE = process.env.API_BASE_URL || 'https://api.qa.local';

Given('a cart with product SKU {string}', async function (sku) {
  if (sku) {
    this.cartId = await createCart(sku);
  } else {
    this.cartId = 'cart-empty';
  }
});

When('the user requests checkout for cart {string}', async function (cartId) {
  try {
    this.response = await axios.post(`${API_BASE}/checkout`, { cartId }, {
      headers: { Authorization: `Bearer ${process.env.API_TOKEN}` }
    });
  } catch (error) {
    this.response = error.response;
  }
});

Then('the checkout response status should be {int}', async function (status) {
  expect(this.response.status).toBe(status);
});

Then('the order total should be {float}', async function (total) {
  expect(parseFloat(this.response.data.order.total)).toBe(total);
});

async function createCart(sku) {
  const response = await axios.post(`${API_BASE}/carts`, { sku }, {
    headers: { Authorization: `Bearer ${process.env.API_TOKEN}` }
  });
  return response.data.cartId;
}

import { test as base } from './base.fixture';

type DataFixtures = {
  testProduct: { id: string; name: string; price: number };
  createdOrder: { id: string; status: string };
};

export const test = base.extend<DataFixtures>({
  testProduct: async ({ apiContext }, use) => {
    const res = await apiContext.post('/api/products', {
      data: { name: `Fixture Product ${Date.now()}`, price: 99.99 },
    });
    const product = await res.json();
    await use(product);
    await apiContext.delete(`/api/products/${product.id}`);
  },
  createdOrder: async ({ apiContext, testProduct }, use) => {
    const res = await apiContext.post('/api/orders', {
      data: { productId: testProduct.id, quantity: 2 },
    });
    const order = await res.json();
    await use(order);
    await apiContext.delete(`/api/orders/${order.id}`);
  },
});

export { expect } from '@playwright/test';

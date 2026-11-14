const request = require('supertest'); // supertest 7.x
const { faker } = require('@faker-js/faker'); // @faker-js/faker 9.x
const app = require('./app'); // Express 5 app, exported without .listen()

const TEST_PASSWORD = process.env.TEST_USER_PASSWORD || 'test-password';
const ADMIN_PASSWORD = process.env.TEST_ADMIN_PASSWORD || 'test-password';

describe('User API integration', () => {
  test('create user -> get user -> delete user', async () => {
    const createRes = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@test.dev' })
      .expect(201);

    const userId = createRes.body.id;

    const getRes = await request(app)
      .get(`/api/users/${userId}`)
      .expect(200);

    expect(getRes.body.name).toBe('John');
    expect(getRes.body.email).toBe('john@test.dev');

    await request(app)
      .delete(`/api/users/${userId}`)
      .expect(204);

    await request(app)
      .get(`/api/users/${userId}`)
      .expect(404);
  });
});

let authToken;

beforeAll(async () => {
  const res = await request(app)
    .post('/api/auth/login')
    .send({ email: 'test.user@test.dev', password: TEST_PASSWORD });

  authToken = res.body.token;
});

describe('Authenticated endpoints', () => {
  test('get profile with a valid token', async () => {
    const res = await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(res.body.email).toBe('test.user@test.dev');
  });

  test('reject the same request without a token', async () => {
    await request(app)
      .get('/api/profile')
      .expect(401);
  });
});

describe('per-test data setup', () => {
  let testUserId;

  beforeEach(async () => {
    const res = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: 'Test User', email: faker.internet.email() });

    testUserId = res.body.id;
  });

  afterEach(async () => {
    if (testUserId) {
      await request(app)
        .delete(`/api/users/${testUserId}`)
        .set('Authorization', `Bearer ${authToken}`);
    }
  });

  test('each test gets a fresh user', async () => {
    const res = await request(app)
      .get(`/api/users/${testUserId}`)
      .expect(200);

    expect(res.body.id).toBe(testUserId);
  });
});

describe('contract assertions', () => {
  test('create order returns the expected contract', async () => {
    const res = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${authToken}`)
      .send({
        items: [
          { productId: 1, quantity: 2 },
          { productId: 3, quantity: 1 },
        ],
        shippingAddress: '123 Test St',
      })
      .expect(201);

    expect(res.body).toMatchObject({
      id: expect.any(Number),
      status: 'pending',
      total: expect.any(Number),
    });

    expect(res.body.items).toHaveLength(2);
    expect(res.body.items[0]).toEqual({
      productId: 1,
      quantity: 2,
      price: expect.any(Number),
    });
  });
});

describe('chained flow', () => {
  test('full e-commerce flow', async () => {
    const user = await request(app)
      .post('/api/auth/login')
      .send({ email: 'buyer@test.dev', password: TEST_PASSWORD });

    const token = user.body.token;

    const admin = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@test.dev', password: ADMIN_PASSWORD });

    const product = await request(app)
      .post('/api/products')
      .set('Authorization', `Bearer ${admin.body.token}`)
      .send({ name: 'Widget', price: 9.99 })
      .expect(201);

    const order = await request(app)
      .post('/api/orders')
      .set('Authorization', `Bearer ${token}`)
      .send({ items: [{ productId: product.body.id, quantity: 3 }] })
      .expect(201);

    const fetched = await request(app)
      .get(`/api/orders/${order.body.id}`)
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(fetched.body.total).toBeCloseTo(29.97);
    expect(fetched.body.status).toBe('pending');
  });
});

describe('error scenarios', () => {
  test('validation error on create', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: '' })
      .expect(400);

    expect(res.body.error.code).toBe('VALIDATION_ERROR');
    expect(res.body.error.details).toContain('name is required');
  });

  test('not found', async () => {
    await request(app)
      .get('/api/users/99999')
      .expect(404);
  });

  test('conflict on duplicate email', async () => {
    const email = faker.internet.email();

    await request(app)
      .post('/api/users')
      .send({ name: 'Dup User', email })
      .expect(201);

    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Dup User', email })
      .expect(409);

    expect(res.body.error.code).toBe('EMAIL_CONFLICT');
  });
});

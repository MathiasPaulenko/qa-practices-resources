const express = require('express');

const app = express();
app.use(express.json());

// In-memory stores — this companion exists for tests, not production.
const users = new Map();
const products = new Map();
const orders = new Map();
let nextId = 1;

const TEST_USERS = {
  'test.user@test.dev': { role: 'user' },
  'buyer@test.dev': { role: 'user' },
  'admin@test.dev': { role: 'admin' },
};

function auth(req, res, next) {
  const header = req.headers.authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : '';
  if (!token.startsWith('test-token:')) {
    return res.status(401).json({
      error: { code: 'UNAUTHORIZED', details: ['missing or invalid token'] },
    });
  }
  req.userEmail = token.slice('test-token:'.length);
  next();
}

function adminOnly(req, res, next) {
  if (req.userEmail !== 'admin@test.dev') {
    return res.status(403).json({
      error: { code: 'FORBIDDEN', details: ['admin role required'] },
    });
  }
  next();
}

app.post('/api/auth/login', (req, res) => {
  const { email, password } = req.body || {};
  if (!email || !password || !TEST_USERS[email]) {
    return res.status(401).json({
      error: { code: 'INVALID_CREDENTIALS', details: ['unknown user or empty password'] },
    });
  }
  res.json({ token: `test-token:${email}` });
});

app.get('/api/profile', auth, (req, res) => {
  res.json({ email: req.userEmail });
});

app.post('/api/users', (req, res) => {
  const { name, email } = req.body || {};
  const details = [];
  if (!name) details.push('name is required');
  if (!email) details.push('email is required');
  if (details.length) {
    return res.status(400).json({ error: { code: 'VALIDATION_ERROR', details } });
  }
  for (const user of users.values()) {
    if (user.email === email) {
      return res.status(409).json({
        error: { code: 'EMAIL_CONFLICT', details: ['email already registered'] },
      });
    }
  }
  const user = { id: nextId++, name, email };
  users.set(user.id, user);
  res.status(201).json(user);
});

app.get('/api/users/:id', (req, res) => {
  const user = users.get(Number(req.params.id));
  if (!user) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', details: ['user not found'] } });
  }
  res.json(user);
});

app.put('/api/users/:id', (req, res) => {
  const user = users.get(Number(req.params.id));
  if (!user) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', details: ['user not found'] } });
  }
  Object.assign(user, req.body);
  res.json(user);
});

app.delete('/api/users/:id', (req, res) => {
  if (!users.delete(Number(req.params.id))) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', details: ['user not found'] } });
  }
  res.status(204).end();
});

app.post('/api/products', auth, adminOnly, (req, res) => {
  const { name, price } = req.body || {};
  if (!name || typeof price !== 'number') {
    return res.status(400).json({
      error: { code: 'VALIDATION_ERROR', details: ['name and numeric price are required'] },
    });
  }
  const product = { id: nextId++, name, price };
  products.set(product.id, product);
  res.status(201).json(product);
});

app.post('/api/orders', auth, (req, res) => {
  const { items, shippingAddress } = req.body || {};
  if (!Array.isArray(items) || !items.length) {
    return res.status(400).json({
      error: { code: 'VALIDATION_ERROR', details: ['items are required'] },
    });
  }
  const orderItems = items.map((item) => {
    const product = products.get(item.productId);
    return {
      productId: item.productId,
      quantity: item.quantity,
      price: product ? product.price : 0,
    };
  });
  const total = orderItems.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const order = {
    id: nextId++,
    userId: req.userEmail,
    items: orderItems,
    total: Math.round(total * 100) / 100,
    status: 'pending',
    shippingAddress: shippingAddress || null,
  };
  orders.set(order.id, order);
  res.status(201).json(order);
});

app.get('/api/orders/:id', auth, (req, res) => {
  const order = orders.get(Number(req.params.id));
  if (!order) {
    return res.status(404).json({ error: { code: 'NOT_FOUND', details: ['order not found'] } });
  }
  res.json(order);
});

module.exports = app;

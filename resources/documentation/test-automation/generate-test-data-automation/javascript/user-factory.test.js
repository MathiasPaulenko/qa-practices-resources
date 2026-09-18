import { describe, test } from 'node:test';
import assert from 'node:assert/strict';
import { faker } from '@faker-js/faker';
import { UserFactory } from './user-factory.js';

describe('UserFactory', () => {
  test('creates a user with realistic defaults', () => {
    const user = UserFactory.create();
    assert.match(user.id, /^[0-9a-f-]{36}$/);
    assert.ok(user.email.includes('@'));
    assert.equal(user.role, 'user');
    assert.equal(user.isActive, true);
  });

  test('overrides win over defaults', () => {
    const admin = UserFactory.createAdmin({ name: 'Super Admin' });
    assert.equal(admin.name, 'Super Admin');
    assert.equal(admin.role, 'admin');
  });

  test('createBatch produces N unique users', () => {
    const users = UserFactory.createBatch(50);
    assert.equal(users.length, 50);
    assert.equal(new Set(users.map((u) => u.id)).size, 50);
  });
});

describe('deterministic seeds', () => {
  test('same seed produces identical data across runs', () => {
    faker.seed(12345);
    const first = faker.person.fullName();
    faker.seed(12345);
    assert.equal(faker.person.fullName(), first);
  });
});

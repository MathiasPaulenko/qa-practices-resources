import { faker } from '@faker-js/faker';

export class UserFactory {
  static create(overrides = {}) {
    return {
      id: faker.string.uuid(),
      name: faker.person.fullName(),
      email: faker.internet.email(),
      password: 'Test123!',
      role: 'user',
      isActive: true,
      createdAt: faker.date.past(),
      ...overrides,
    };
  }

  static createAdmin(overrides = {}) {
    return this.create({ role: 'admin', ...overrides });
  }

  static createBatch(count, overrides = {}) {
    return Array.from({ length: count }, () => this.create(overrides));
  }
}

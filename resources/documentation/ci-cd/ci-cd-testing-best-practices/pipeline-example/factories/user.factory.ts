// factories/user.factory.ts — @faker-js/faker v9
import { faker } from '@faker-js/faker';

export const createUser = (overrides?: Partial<User>) => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  firstName: faker.person.firstName(),
  lastName: faker.person.lastName(),
  role: 'user',
  createdAt: new Date(),
  ...overrides,
});

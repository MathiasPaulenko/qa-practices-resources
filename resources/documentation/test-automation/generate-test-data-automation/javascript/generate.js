// Steps 6-7 of the guide: generate CSV and JSON test data files.
// Usage: node generate.js
import fs from 'fs';
import { faker } from '@faker-js/faker';

faker.seed(12345); // deterministic output — same files on every run

// --- JSON ---
const testData = Array.from({ length: 100 }, () => ({
  id: faker.string.uuid(),
  name: faker.person.fullName(),
  email: faker.internet.email(),
  phone: faker.phone.number(),
  address: {
    street: faker.location.streetAddress(),
    city: faker.location.city(),
    zipCode: faker.location.zipCode(),
  },
  orders: Array.from({ length: faker.number.int({ min: 1, max: 5 }) }, () => ({
    orderId: faker.string.uuid(),
    product: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price()),
    date: faker.date.recent().toISOString(),
  })),
}));
fs.writeFileSync('test-data.json', JSON.stringify(testData, null, 2));

// --- CSV ---
const header = 'name,email,phone,city,age';
const rows = Array.from({ length: 100 }, () =>
  [
    `"${faker.person.fullName()}"`,
    faker.internet.email(),
    `"${faker.phone.number()}"`,
    `"${faker.location.city()}"`,
    faker.number.int({ min: 18, max: 80 }),
  ].join(',')
);
fs.writeFileSync('test_users.csv', [header, ...rows].join('\n') + '\n');

console.log(`Generated test-data.json (${testData.length} records) and test_users.csv (${rows.length} rows)`);

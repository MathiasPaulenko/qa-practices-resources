// Validate an API response against the OpenAPI-derived JSON schema.
// Requires: ajv 8
const Ajv = require('ajv');
const request = require('./api-client'); // supertest agent
const paymentSchema = require('./payment-schema.json');

const ajv = new Ajv({ strict: true, allErrors: true });

test('payment response matches OpenAPI schema', async () => {
  const response = await request.get('/api/payments/123')
    .set('Authorization', `Bearer ${token}`);

  const validate = ajv.compile(paymentSchema);
  const valid = validate(response.body);

  if (!valid) {
    console.error('Schema errors:', ajv.errorsText(validate.errors));
  }
  expect(valid).toBe(true);
});

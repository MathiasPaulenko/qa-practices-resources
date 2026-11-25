// UUID-namespaced test data so parallel workers never collide (uuid 11.x)
const { v4: uuidv4 } = require('uuid');

describe('Contact sync integration', () => {
  const testId = uuidv4();
  const testEmail = `test-${testId}@synctest.com`;

  afterAll(async () => {
    // Clean up all records created by this test
    await deleteContactByEmail(testEmail);
  });

  it('should create and sync a contact', async () => {
    const contact = await createContact({ email: testEmail, name: `Test ${testId}` });
    expect(contact.id).toBeDefined();
  });
});

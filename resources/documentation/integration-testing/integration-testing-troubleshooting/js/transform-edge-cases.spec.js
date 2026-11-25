// Dedicated tests for the Stripe -> Salesforce transformation layer.
// Edge cases live here, not inside connector tests.
const { transformStripeToSalesforce } = require('./transform');

describe('Stripe to Salesforce field transformation', () => {
  it('should handle null fields gracefully', () => {
    const stripeCustomer = { name: null, email: 'test@test.com' };
    const salesforceContact = transformStripeToSalesforce(stripeCustomer);
    expect(salesforceContact.Name).toBe('');
    expect(salesforceContact.Email).toBe('test@test.com');
  });

  it('should normalize timezone to UTC', () => {
    const stripeCustomer = { created: 1690000000 }; // Unix timestamp
    const result = transformStripeToSalesforce(stripeCustomer);
    expect(result.CreatedDate).toBe('2023-07-22T02:13:20.000Z');
  });

  it('should handle empty strings and empty arrays', () => {
    const stripeCustomer = { name: '', metadata: {}, subscriptions: [] };
    const result = transformStripeToSalesforce(stripeCustomer);
    expect(result.Name).toBe('');
    expect(result.Subscriptions__c).toBeUndefined();
  });
});

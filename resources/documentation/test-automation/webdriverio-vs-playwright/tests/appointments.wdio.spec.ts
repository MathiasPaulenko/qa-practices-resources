describe('VitaCare appointment booking', () => {
  let paymentMock: WebdriverIO.Mock;

  before(async () => {
    // register the mock in a before hook (requires WebDriver BiDi)
    paymentMock = await browser.mock('**/v1/payments/authorize', { method: 'post' });
  });

  it('patient can book a telehealth slot', async () => {
    paymentMock.respond(
      { authorized: true, transactionId: 'mock-123' },
      { statusCode: 200 }
    );

    await browser.url('https://staging.vitacare.io/login');
    await $('#email').setValue('qa-patient@vitacare.io'); // seeded test account
    await $('#password').setValue(process.env.E2E_PASSWORD ?? 'local-dev-password');
    await $('button[type=submit]').click();

    await browser.url('https://staging.vitacare.io/appointments');
    const slots = await $$('.time-slot');
    const slot = slots[2];
    await slot.waitForClickable();
    await slot.click();

    await $('button#confirm-booking').click();
    await $('.booking-confirmation').waitForDisplayed();
    const confirmation = await $('.booking-confirmation').getText();
    expect(confirmation).toContain('Your appointment is confirmed');
  });
});

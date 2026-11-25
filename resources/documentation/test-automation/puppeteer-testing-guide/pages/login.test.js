// tests/login.test.js
const LoginPage = require('./pages/LoginPage');

describe('Login with Page Object', () => {
  let loginPage;

  beforeEach(async () => {
    loginPage = new LoginPage(page);
    await loginPage.navigate();
  });

  it('logs in successfully', async () => {
    await loginPage.login('jane@staging.myapp.com', 'validpass123');
    const heading = await loginPage.getDashboardHeading();
    expect(heading).toBe('Dashboard');
  });
});

const loginPage = require('./pages/LoginPage')

describe('Login', () => {
  beforeAll(async () => {
    await device.launchApp()
  })

  beforeEach(async () => {
    await device.reloadReactNative()
  })

  it('should login with valid credentials', async () => {
    await element(by.id('email-input')).typeText('jane.qa@acme-shop.io') // test account on the staging build
    await element(by.id('password-input')).typeText('validpass123')
    await element(by.id('login-button')).tap()

    await expect(element(by.text('Welcome, Jane'))).toBeVisible()
  })

  it('should show error on invalid credentials', async () => {
    await element(by.id('email-input')).typeText('jane.qa@acme-shop.io')
    await element(by.id('password-input')).typeText('wrongpass')
    await element(by.id('login-button')).tap()

    await expect(element(by.text('Invalid credentials'))).toBeVisible()
  })

  it('logs in through the Page Object', async () => {
    await loginPage.login('jane.qa@acme-shop.io', 'validpass123')
    await loginPage.expectWelcomeVisible()
  })
})

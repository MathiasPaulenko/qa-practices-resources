// pages/LoginPage.ts
import type { Page } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  async open() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.getByTestId('email-input').fill(email);
    await this.page.getByTestId('password-input').fill(password);
    await this.page.getByTestId('sign-in-button').click();
  }

  async getErrorMessage(): Promise<string> {
    return this.page.getByTestId('login-error').innerText();
  }
}

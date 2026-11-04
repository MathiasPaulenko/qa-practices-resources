import { test as base, type Page } from '@playwright/test';

export class DashboardPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/dashboard');
  }

  async getMetric(name: string) {
    return this.page.locator(`[data-testid="metric-${name}"]`).textContent();
  }

  async waitForChartLoad() {
    await this.page.waitForSelector('[data-testid="chart-canvas"]', { state: 'visible' });
  }
}

export const test = base.extend<{ dashboardPage: DashboardPage }>({
  dashboardPage: async ({ page }, use) => {
    const dashboard = new DashboardPage(page);
    await dashboard.goto();
    await use(dashboard);
  },
});

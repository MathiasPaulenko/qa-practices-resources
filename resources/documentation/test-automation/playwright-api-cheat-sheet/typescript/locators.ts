// @playwright/test 1.x — locators: prefer getBy* over raw CSS
page.locator('#elementId');
page.locator('.className');
page.locator('[data-testid="submit"]');
page.locator('input[name="email"]');
page.getByText('Welcome');
page.getByRole('button', { name: 'Save' });
page.getByLabel('Email');
page.getByPlaceholder('Enter email');
page.getByAltText('Logo');
page.getByTitle('Submit form');

// Chaining and filtering
page.locator('ul > li').first();
page.locator('ul > li').last();
page.locator('ul > li').nth(2);
page.locator('li').filter({ hasText: 'Active' });
page.locator('div').filter({ has: page.locator('span.error') });

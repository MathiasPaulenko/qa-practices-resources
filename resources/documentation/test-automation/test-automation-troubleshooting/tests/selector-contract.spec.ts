import { expect, test } from '@playwright/test';

test('locates the save action by its accessible name', async ({ page }) => {
  await page.setContent(`
    <button class="button button-primary">Save changes</button>
    <p data-testid="save-status">Not saved</p>
    <script>
      document.querySelector('button').addEventListener('click', () => {
        document.querySelector('[data-testid="save-status"]').textContent = 'Saved';
      });
    </script>
  `);

  await page.getByRole('button', { name: 'Save changes' }).click();
  await expect(page.getByTestId('save-status')).toHaveText('Saved');
});

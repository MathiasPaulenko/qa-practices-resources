import { expect, test } from '@playwright/test';

test('waits for the pipeline status after a build is triggered', async ({ page }) => {
  await page.setContent(`
    <button type="button">Trigger build</button>
    <p role="status">Idle</p>
    <script>
      document.querySelector('button').addEventListener('click', () => {
        setTimeout(() => {
          document.querySelector('[role="status"]').textContent = 'Running';
        }, 40);
      });
    </script>
  `);

  await page.getByRole('button', { name: 'Trigger build' }).click();
  await expect(page.getByRole('status')).toHaveText('Running');
});

# Example Output — Fragments

What the generated package looks like for the PulseCare input above.

## `.github/workflows/a11y.yml` (fragment)

```yaml
      - name: Run Playwright a11y tests
        run: npx playwright test --project=a11y
        env:
          BASE_URL: https://staging.pulsecare.example
      - name: Upload a11y report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: a11y-report
          path: playwright-report/
```

## Playwright a11y test (fragment)

```typescript
test('focus indicators are visible on the dashboard', async ({ page }) => {
  await page.goto('/dashboard');
  for (const el of await page.locator('button, [href], input').all()) {
    await el.focus();
    await expect(el).toHaveCSS('outline-style', 'solid');
  }
});
```

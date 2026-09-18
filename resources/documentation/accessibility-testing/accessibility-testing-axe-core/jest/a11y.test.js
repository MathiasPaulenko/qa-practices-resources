const { axe, toHaveNoViolations } = require('jest-axe');

expect.extend(toHaveNoViolations);

test('button with accessible name passes', async () => {
  const html = '<button aria-label="Close dialog">×</button>';
  const results = await axe(html);
  expect(results).toHaveNoViolations();
});

test('image without alt text is flagged', async () => {
  const html = '<main><img src="logo.png"></main>';
  const results = await axe(html);
  const ids = results.violations.map(v => v.id);
  expect(ids).toContain('image-alt');
});

// color-contrast is NOT reliable in jsdom — it needs real layout/canvas.
// Use browser-based runners (@axe-core/playwright) for contrast checks.
// Note: a placeholder attribute alone satisfies the label rule (it provides
// an accessible name, even though placeholders are discouraged as labels).
test('input without label is flagged', async () => {
  const html = '<main><input type="text"></main>';
  const results = await axe(html);
  const ids = results.violations.map(v => v.id);
  expect(ids).toContain('label');
});

test('empty button fails button-name rule', async () => {
  const html = '<main><button></button></main>';
  const results = await axe(html);
  const ids = results.violations.map(v => v.id);
  expect(ids).toContain('button-name');
});

test('input with label passes', async () => {
  const html = '<main><label for="q">Search</label><input id="q"></main>';
  const results = await axe(html);
  expect(results).toHaveNoViolations();
});

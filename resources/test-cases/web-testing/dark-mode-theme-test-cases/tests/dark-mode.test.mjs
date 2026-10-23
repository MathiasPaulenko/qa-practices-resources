import { test } from 'node:test';
import assert from 'node:assert/strict';

import { contrastRatio } from '../contrast.mjs';
import { findHardcodedColors } from '../scan-hardcoded.mjs';
import { SEMANTIC_TOKENS, THEMES, ThemeStore, resolveTheme } from '../theme.mjs';

// TC-001 — system dark preference applies on first visit
test('TC-001 system dark applies when nothing is stored', () => {
  assert.equal(resolveTheme(null, 'dark'), 'dark');
});

// TC-002 — stored preference wins over the system preference
test('TC-002 stored light beats system dark', () => {
  assert.equal(resolveTheme('light', 'dark'), 'light');
  assert.equal(resolveTheme('dark', 'light'), 'dark');
});

// TC-003 — manual choice persists across "sessions"
test('TC-003 stored choice survives re-resolution', () => {
  const storage = new Map();
  const tab = new ThemeStore(storage, 'light');
  tab.setTheme('dark');
  const reopened = new ThemeStore(storage, 'light');
  assert.equal(reopened.theme, 'dark');
});

// TC-006 — corrupted stored value falls back safely
test('TC-006 corrupted value falls back to system, then default', () => {
  assert.equal(resolveTheme('banana', 'dark'), 'dark');
  assert.equal(resolveTheme('banana', 'none'), 'light');
  assert.equal(resolveTheme(undefined, 'dark'), 'dark');
});

// TC-007 — every semantic token resolves in both themes
test('TC-007 every semantic token exists in light and dark', () => {
  for (const token of SEMANTIC_TOKENS) {
    assert.ok(THEMES.light[token], `missing in light: ${token}`);
    assert.ok(THEMES.dark[token], `missing in dark: ${token}`);
  }
});

test('TC-007b scanner catches a hardcoded hex outside the token system', () => {
  const leaky = `
    .banner { color: #ffffff; background: var(--color-bg); }
    :root { --color-bg: #ffffff; }
  `;
  const hits = findHardcodedColors(leaky);
  assert.equal(hits.length, 1);
  assert.deepEqual(hits[0], { property: 'color', value: '#ffffff' });
});

// TC-008 — text contrast meets WCAG AA in both themes (SC 1.4.3)
for (const name of ['light', 'dark']) {
  test(`TC-008 body text meets AA in ${name} theme`, () => {
    const ratio = contrastRatio(THEMES[name]['--color-text'], THEMES[name]['--color-bg']);
    assert.ok(ratio >= 4.5, `${name} text/bg ratio ${ratio.toFixed(2)} < 4.5`);
  });

  test(`TC-008b muted text still meets AA in ${name} theme`, () => {
    const ratio = contrastRatio(THEMES[name]['--color-text-muted'], THEMES[name]['--color-bg']);
    assert.ok(ratio >= 4.5, `${name} muted/bg ratio ${ratio.toFixed(2)} < 4.5`);
  });
}

// TC-009 — focus ring keeps ≥3:1 against the surface it sits on (SC 1.4.11)
for (const name of ['light', 'dark']) {
  test(`TC-009 focus ring keeps 3:1 on ${name} background`, () => {
    const ratio = contrastRatio(THEMES[name]['--color-focus'], THEMES[name]['--color-bg']);
    assert.ok(ratio >= 3, `${name} focus/bg ratio ${ratio.toFixed(2)} < 3`);
  });
}

// TC-011 — elevated surfaces read as raised in dark theme
test('TC-011 raised surface is lighter than base surface in dark', () => {
  const raised = contrastRatio(THEMES.dark['--color-surface-raised'], '#000000');
  const base = contrastRatio(THEMES.dark['--color-surface'], '#000000');
  assert.ok(raised > base, 'dark raised surface must be lighter than base surface');
});

// TC-014 — without a manual override the app follows the system
test('TC-014 system flip re-resolves when no manual override exists', () => {
  const tab = new ThemeStore(new Map(), 'light');
  assert.equal(tab.theme, 'light');
  tab.system = 'dark';
  assert.equal(tab.theme, 'dark');
  tab.setTheme('light'); // manual override freezes the choice
  tab.system = 'light';
  assert.equal(tab.theme, 'light');
});

// TC-015 — two "tabs" sharing storage resolve the same theme
test('TC-015 tabs sharing storage see the same preference', () => {
  const shared = new Map();
  const tabA = new ThemeStore(shared, 'light');
  const tabB = new ThemeStore(shared, 'light');
  tabA.setTheme('dark');
  assert.equal(tabB.theme, 'dark');
});

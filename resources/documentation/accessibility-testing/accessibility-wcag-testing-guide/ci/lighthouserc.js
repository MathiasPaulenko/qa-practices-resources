// Lighthouse CI (lhci 0.14) — gate the accessibility category at 0.95
// and hard-fail on the three most common WCAG regressions.
module.exports = {
  ci: {
    assert: {
      assertions: {
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'color-contrast': 'error',
        label: 'error',
        'link-name': 'error',
      },
    },
  },
};

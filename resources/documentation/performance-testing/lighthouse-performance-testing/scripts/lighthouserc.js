// Lighthouse CI 0.14 config
// Install: npm install -g @lhci/cli@0.14
module.exports = {
  ci: {
    collect: {
      url: [
        'https://preview.qa.local/login',
        'https://preview.qa.local/dashboard',
      ],
      numberOfRuns: 3,
      settings: {
        preset: 'mobile',
      },
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:seo': ['warn', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.85 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};

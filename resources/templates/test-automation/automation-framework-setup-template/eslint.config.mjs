export default [
  {
    files: ['tests/**/*.ts'],
    rules: {
      'no-restricted-syntax': [
        'error',
        {
          selector: "CallExpression[callee.property.name='waitForTimeout']",
          message: 'Use web-first assertions instead of waitForTimeout.',
        },
        {
          selector: "CallExpression[callee.name='locator'] Literal[value=/^[.#]/]",
          message: 'Use data-testid selectors; CSS/XPath selectors are not allowed in specs.',
        },
      ],
    },
  },
];

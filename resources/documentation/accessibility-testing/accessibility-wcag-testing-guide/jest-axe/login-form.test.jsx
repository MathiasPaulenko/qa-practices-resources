// React component test with Jest + Testing Library + jest-axe 9.x
// Runs axe-core 4.10 against the rendered component — catches missing
// labels, bad ARIA, and contrast issues at unit-test speed.
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import LoginForm from './LoginForm';

expect.extend(toHaveNoViolations);

test('login form has no accessibility violations', async () => {
  const { container } = render(<LoginForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

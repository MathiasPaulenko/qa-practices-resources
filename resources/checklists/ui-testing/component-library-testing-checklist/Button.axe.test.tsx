import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from './Button';

expect.extend(toHaveNoViolations);

test('Button has no axe violations in any state', async () => {
  for (const props of [{}, { disabled: true }, { variant: 'primary' as const }]) {
    const { container } = render(<Button {...props}>Save</Button>);
    expect(await axe(container)).toHaveNoViolations();
  }
});

test('Button has no axe violations while loading', async () => {
  const { container } = render(<Button loading>Save</Button>);
  expect(await axe(container)).toHaveNoViolations();
});

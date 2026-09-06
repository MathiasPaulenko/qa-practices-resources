// Button.test.js — Complete Button test suite
// Install: npm install -D @testing-library/react@16 @testing-library/user-event@14 jest@29 jest-axe@9
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe } from 'jest-axe';
import Button from './Button';

describe('Button', () => {
    it('renders with a visible label', () => {
        render(<Button label="Save" />);
        expect(screen.getByRole('button', { name: 'Save' })).toBeVisible();
    });

    it('is disabled and can\'t be clicked', async () => {
        const handleClick = jest.fn();
        render(<Button label="Save" disabled onClick={handleClick} />);
        await userEvent.click(screen.getByRole('button'));
        expect(handleClick).not.toHaveBeenCalled();
    });

    it('shows loading state and blocks interaction', () => {
        render(<Button label="Save" loading />);
        expect(screen.getByRole('button')).toBeDisabled();
        expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    it('handles keyboard activation', async () => {
        const handleClick = jest.fn();
        render(<Button label="Save" onClick={handleClick} />);
        const button = screen.getByRole('button');
        button.focus();
        await userEvent.keyboard('{Enter}');
        expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('has no accessibility violations', async () => {
        const { container } = render(<Button label="Save" />);
        const results = await axe(container);
        expect(results.violations).toHaveLength(0);
    });
});

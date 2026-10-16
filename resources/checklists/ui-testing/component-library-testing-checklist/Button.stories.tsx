import type { Meta, StoryObj } from '@storybook/react';
import { expect, userEvent, within } from 'storybook/test';
import { Button } from './Button';

const meta: Meta<typeof Button> = { component: Button, title: 'Button' };
export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { children: 'Save', variant: 'primary' },
};

export const Clicked: Story = {
  args: { children: 'Save', variant: 'primary' },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button', { name: 'Save' }));
    await expect(canvas.getByRole('button')).toBeEnabled();
  },
};

export const LoadingState: Story = {
  args: { children: 'Save', variant: 'primary', loading: true },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');
    await expect(button).toBeDisabled();
    await expect(button).toHaveAttribute('aria-busy', 'true');
  },
};

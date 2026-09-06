// Button.stories.js — Storybook 8 stories for Button component
// Install: npm install -D storybook@8 @storybook/react@8
import Button from './Button';

export default {
    title: 'Components/Button',
    component: Button,
    argTypes: {
        variant: { control: 'select', options: ['primary', 'secondary'] },
    },
};

export const Primary = {
    args: { variant: 'primary', label: 'Primary Button' },
};

export const Disabled = {
    args: { variant: 'primary', label: 'Disabled', disabled: true },
};

export const Loading = {
    args: { variant: 'primary', label: 'Loading', loading: true },
};

export const Secondary = {
    args: { variant: 'secondary', label: 'Secondary Button' },
};

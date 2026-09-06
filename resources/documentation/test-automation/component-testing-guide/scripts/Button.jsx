// Button.jsx — React Button component with variant, disabled, loading and onClick props
import React from 'react';

export default function Button({
    label,
    variant = 'primary',
    disabled = false,
    loading = false,
    onClick,
    type = 'button',
}) {
    return (
        <button
            type={type}
            disabled={disabled || loading}
            onClick={onClick}
            data-variant={variant}
        >
            {loading ? 'Loading...' : label}
        </button>
    );
}

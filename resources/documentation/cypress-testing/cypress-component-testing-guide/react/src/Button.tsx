import React from 'react'

interface ButtonProps {
  variant?: 'primary' | 'secondary'
  label: string
  disabled?: boolean
  onClick?: () => void
}

export default function Button({ variant = 'primary', label, disabled, onClick }: ButtonProps) {
  return (
    <button
      className={`btn-${variant}`}
      disabled={disabled}
      onClick={onClick}
    >
      {label}
    </button>
  )
}

import { describe, it, expect } from 'vitest'
import { add, divide } from './calculator'

describe('Calculator', () => {
  describe('add', () => {
    it('adds two positive numbers', () => {
      expect(add(2, 3)).toBe(5)
    })

    it('handles negative numbers', () => {
      expect(add(-1, -2)).toBe(-3)
    })

    it('handles zero', () => {
      expect(add(0, 0)).toBe(0)
    })
  })

  describe('divide', () => {
    it('divides two numbers', () => {
      expect(divide(10, 2)).toBe(5)
    })

    it('throws on division by zero', () => {
      expect(() => divide(10, 0)).toThrow('Cannot divide by zero')
    })
  })
})

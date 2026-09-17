import { describe, it, expect, vi } from 'vitest'

describe('Mocking', () => {
  it('creates a mock function', () => {
    const mockFn = vi.fn((x: number) => x * 2)

    mockFn(5)
    mockFn(10)

    expect(mockFn).toHaveBeenCalled()
    expect(mockFn).toHaveBeenCalledTimes(2)
    expect(mockFn).toHaveBeenCalledWith(5)
    expect(mockFn).toHaveReturnedWith(10)
  })

  it('mocks a module', async () => {
    vi.mock('./src/api', () => ({
      getUser: vi.fn(() => ({ id: 1, name: 'Jane' })),
      getUsers: vi.fn(() => []),
    }))

    const { getUser } = await import('./src/api')
    const user = getUser(1)

    expect(user.name).toBe('Jane')
    expect(getUser).toHaveBeenCalledWith(1)
  })

  it('mocks implementation per test', () => {
    const mockFn = vi.fn()

    mockFn.mockImplementationOnce(() => 'first')
    mockFn.mockImplementationOnce(() => 'second')
    mockFn.mockImplementation(() => 'default')

    expect(mockFn()).toBe('first')
    expect(mockFn()).toBe('second')
    expect(mockFn()).toBe('default')
  })
})

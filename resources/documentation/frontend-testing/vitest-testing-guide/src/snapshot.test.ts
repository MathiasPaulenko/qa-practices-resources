import { describe, it, expect } from 'vitest'

describe('Snapshots', () => {
  it('serializes an object', () => {
    const user = { name: 'Jane', email: 'jane@example.com', role: 'admin' }
    expect(user).toMatchSnapshot()
  })

  it('serializes inline', () => {
    const config = { env: 'test', timeout: 5000 }
    expect(config).toMatchInlineSnapshot(`
      {
        "env": "test",
        "timeout": 5000,
      }
    `)
  })
})

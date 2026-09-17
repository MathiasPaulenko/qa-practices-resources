// Runs identically under Jest 30.5 and Vitest 5.0 — describe/it/expect are globals
// in Jest and enabled via `test.globals: true` in vite.config.ts.
import { validateEmail, validatePassword } from '../src/validators';

describe('validateEmail', () => {
  test('accepts a valid corporate email', () => {
    expect(validateEmail('qa-team@qapractices.dev')).toBe(true);
  });

  test('rejects email without @', () => {
    expect(validateEmail('qapractices.dev')).toBe(false);
  });

  test('rejects email with invalid domain', () => {
    expect(validateEmail('qa-team@localhost')).toBe(false);
  });
});

describe('validatePassword', () => {
  test('accepts a password of 8+ characters', () => {
    expect(validatePassword('f1nch-secure-pass')).toBe(true);
  });

  test('rejects short passwords', () => {
    expect(validatePassword('short')).toBe(false);
  });
});

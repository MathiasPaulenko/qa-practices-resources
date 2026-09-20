import { test, expect } from 'vitest';
import { validatePassword } from '../src/password.js';

// The guide's first red-green-refactor cycle stops at the length rule.
// These tests continue the kata: each one is one more red step
// (uppercase requirement, digit requirement) you can drive to green
// by deleting the matching rule in src/password.js first.

test('password must be at least 8 characters', () => {
  expect(validatePassword('Sh0rt')).toBe(false);
});

test('password requires an uppercase letter', () => {
  expect(validatePassword('lowercase1')).toBe(false);
});

test('password requires a digit', () => {
  expect(validatePassword('NoDigitsHere')).toBe(false);
});

test('valid password passes all rules', () => {
  expect(validatePassword('Str0ngPass')).toBe(true);
});

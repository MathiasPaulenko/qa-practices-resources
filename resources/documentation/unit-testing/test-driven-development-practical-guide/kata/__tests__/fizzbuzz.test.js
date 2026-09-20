import { test, expect } from 'vitest';
import { fizzBuzz } from '../src/fizzbuzz.js';

// The four tests from the guide's walkthrough, in the order they were
// written. To replay the kata, comment out the implementation rules in
// src/fizzbuzz.js and watch each test go red in sequence.

test('returns the number as string for non-multiples', () => {
  expect(fizzBuzz(1)).toBe('1');
  expect(fizzBuzz(7)).toBe('7');
});

test('returns Fizz for multiples of 3', () => {
  expect(fizzBuzz(3)).toBe('Fizz');
  expect(fizzBuzz(9)).toBe('Fizz');
});

test('returns Buzz for multiples of 5', () => {
  expect(fizzBuzz(5)).toBe('Buzz');
  expect(fizzBuzz(20)).toBe('Buzz');
});

test('returns FizzBuzz for multiples of 3 and 5', () => {
  expect(fizzBuzz(15)).toBe('FizzBuzz');
  expect(fizzBuzz(45)).toBe('FizzBuzz');
});

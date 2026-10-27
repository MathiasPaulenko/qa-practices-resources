import { test } from 'node:test';
import assert from 'node:assert/strict';
import { hexToRgb, isValidHex, contrastRatio } from './color-utils.js';

test('hexToRgb parses 3 and 6 digit forms', () => {
  assert.deepEqual(hexToRgb('#FF5733'), { r: 255, g: 87, b: 51 });
  assert.deepEqual(hexToRgb('#FFF'), { r: 255, g: 255, b: 255 });
});

test('isValidHex accepts 3/4/6/8 digits and rejects junk', () => {
  assert.equal(isValidHex('#FF6B3580'), true);
  assert.equal(isValidHex('FF5733'), true);
  assert.equal(isValidHex('#GGG123'), false);
  assert.equal(isValidHex('#FF'), false);
});

test('contrastRatio: white on black is 21:1', () => {
  const ratio = contrastRatio({ r: 255, g: 255, b: 255 }, { r: 0, g: 0, b: 0 });
  assert.ok(Math.abs(ratio - 21) < 0.1);
  assert.ok(ratio >= 4.5, 'WCAG AA normal text');
});

// test-wasm.mjs — Node.js 20+, smoke checks without a test runner.
// Run: wat2wasm add.wat -o add.wasm && node test-wasm.mjs
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const bytes = await readFile(new URL('./add.wasm', import.meta.url));

// 1. Binary format validation — cheapest check first
assert.ok(WebAssembly.validate(bytes), 'module failed WebAssembly.validate()');

// A deliberately corrupted binary must fail validation
const corrupted = new Uint8Array(bytes);
corrupted[0] = 0xff; // break the \0asm magic number
assert.equal(WebAssembly.validate(corrupted), false, 'corrupted magic passed validation');

// 2. Instantiation and exported function
const { instance } = await WebAssembly.instantiate(bytes);
assert.equal(instance.exports.add(2, 40), 42);
assert.equal(instance.exports.add(-1, 1), 0);

// 3. Linear memory: 64 KiB pages, grow returns previous size in pages.
// Two different contracts: inside the module the `memory.grow` instruction
// returns -1 on failure; the JS WebAssembly.Memory.grow() throws RangeError.
const memory = instance.exports.memory;
assert.equal(memory.buffer.byteLength, 65536, 'one page must be 64 KiB');
assert.equal(memory.grow(1), 1, 'grow returns previous size in pages');
assert.throws(() => memory.grow(10), RangeError, 'grow beyond maximum must throw');
assert.equal(memory.buffer.byteLength, 131072, 'buffer is 2 pages after grow');

console.log('All WASM smoke checks passed.');

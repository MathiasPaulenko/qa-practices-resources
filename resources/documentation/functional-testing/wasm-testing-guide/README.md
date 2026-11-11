# WASM Testing — Minimal Suite

Runnable example for the [WebAssembly (WASM) Testing Guide](https://qapractices.com/documentation/wasm-testing-guide/) on QAPractices.

A minimal WASM module (`add.wat`) plus a Node.js smoke test that exercises binary validation, instantiation, exported functions and linear-memory growth — the checks covered in the guide's first sections.

## Requirements

- Node.js 20+ (exposes the `WebAssembly` API)
- [wabt](https://github.com/WebAssembly/wabt) 1.0.x — provides `wat2wasm`, `wasm-validate`, `wasm-objdump`

## Usage

```bash
# 1. Compile the WAT source to a binary module
wat2wasm add.wat -o add.wasm

# 2. Validate the binary and inspect its exports
wasm-validate add.wasm
wasm-objdump -x add.wasm

# 3. Run the smoke checks
node test-wasm.mjs
```

Expected output: `All WASM smoke checks passed.`

## Files

| File | What it does |
|---|---|
| `add.wat` | WAT source: one exported `add` function and a growable exported memory (1-4 pages) |
| `test-wasm.mjs` | Node smoke checks: `WebAssembly.validate` on good and corrupted bytes, instantiate, `add(2,40)`, memory page size and `memory.grow` bounds |

## Notes

- `add.wasm` is generated locally by `wat2wasm` and intentionally not committed — build it once with the command above.
- For Rust targets see `wasm-pack test --node` (`#[wasm_bindgen_test]`); for WASI binaries use `wasmtime run --invoke <fn> module.wasm <args>`.

# Testing WASM — Suite Mínima

Ejemplo ejecutable de la [Guía de Testing de WebAssembly (WASM)](https://qapractices.com/es/documentation/wasm-testing-guide/) de QAPractices.

Un módulo WASM mínimo (`add.wat`) más un smoke test en Node.js que ejercita validación binaria, instanciación, funciones exportadas y crecimiento de memoria lineal — los checks de las primeras secciones de la guía.

## Requisitos

- Node.js 20+ (expone la API `WebAssembly`)
- [wabt](https://github.com/WebAssembly/wabt) 1.0.x — provee `wat2wasm`, `wasm-validate`, `wasm-objdump`

## Uso

```bash
# 1. Compila el fuente WAT a módulo binario
wat2wasm add.wat -o add.wasm

# 2. Valida el binario e inspecciona sus exports
wasm-validate add.wasm
wasm-objdump -x add.wasm

# 3. Corre los smoke checks
node test-wasm.mjs
```

Salida esperada: `All WASM smoke checks passed.`

## Archivos

| Archivo | Qué hace |
|---|---|
| `add.wat` | Fuente WAT: una función `add` exportada y una memoria exportada ampliable (1-4 páginas) |
| `test-wasm.mjs` | Smoke checks en Node: `WebAssembly.validate` sobre bytes válidos y corruptos, instanciación, `add(2,40)`, tamaño de página y límites de `memory.grow` |

## Notas

- `add.wasm` se genera localmente con `wat2wasm` y no se commitea a propósito — constrúyelo una vez con el comando de arriba.
- Para targets Rust ver `wasm-pack test --node` (`#[wasm_bindgen_test]`); para binarios WASI usa `wasmtime run --invoke <fn> module.wasm <args>`.

;; add.wat — smallest module worth testing: one export, one growable memory
;; Compile: wat2wasm add.wat -o add.wasm
(module
  (memory (export "memory") 1 4)
  (func (export "add") (param i32 i32) (result i32)
    local.get 0
    local.get 1
    i32.add))

# Queries de Testing de BD — fixture SQLite

Companion de [Prompts de IA para Generación de Queries de Testing de BD](https://qapractices.com/es/prompts/ai-prompt-database-testing-queries/).

El esquema `users`/`orders`/`order_items` del recurso, con las queries generadas hechas ejecutables. Los inserts marcados `-- must FAIL` son casos negativos: *deben* lanzar errores de constraint. Todos los `SELECT` deberían devolver 0 filas.

## Ejecutar

```bash
sqlite3 test_db.sqlite "PRAGMA foreign_keys = ON;"
sqlite3 test_db.sqlite < schema.sql
sqlite3 test_db.sqlite < test-queries.sql   # esperar errores de constraint en los inserts marcados
```

Ojo: sqlite aplica FKs solo con `PRAGMA foreign_keys = ON` — en sí mismo un bug clásico de setup que este fixture demuestra.

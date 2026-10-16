# Pruebas de Base de Datos — Companion de Checks de Integridad

Código companion de la [Guía de Pruebas de Base de Datos](https://qapractices.com/es/documentation/database-testing/) en QAPractices.

## Qué hay dentro

| Archivo | Qué muestra |
|---------|-------------|
| `schema.sql` | Esquema e-commerce mínimo (users, products, orders, order_lines) con constraints NOT NULL / UNIQUE / CHECK / FOREIGN KEY — dialecto SQLite, sin servidor. |
| `seed.sql` | Datos seed limpios; cada check reporta 0 violaciones. |
| `integrity_checks.sql` | Los 5 checks de integridad de la guía: líneas huérfanas, totales inconsistentes, emails duplicados, precios no positivos, cantidades inválidas. Cada query devuelve un conteo de violaciones. |
| `run_checks.py` | Ejecuta los checks contra una DB en memoria o un archivo `.db`; imprime `OK`/`FAIL` por check y sale con 0/1 — listo para CI. |
| `tests/test_integrity.py` | 10 casos pytest: el seed limpio pasa todo, los datos alterados (huérfano, total desviado, email duplicado, precio negativo) son detectados, y `PRAGMA foreign_keys` bloquea huérfanos al insertar. |

## Ejecutarlo

```bash
python run_checks.py          # DB demo en memoria
python -m pytest tests/ -v    # la suite
```

Esperado: todos los checks `OK` con el seed, **10 passed**.

La suite usa `sqlite3` de la stdlib — la única dependencia es pytest 8.3.4. El mismo SQL corre en PostgreSQL/MySQL con cambios mínimos de dialecto.

## Recurso relacionado

- [Guía de Pruebas de Base de Datos](https://qapractices.com/es/documentation/database-testing/) — la estrategia completa que este código implementa (Pasos 1–4).

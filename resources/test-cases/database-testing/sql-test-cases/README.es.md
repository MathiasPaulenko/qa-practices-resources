# Casos de Prueba SQL — Companion

Materiales ejecutables para el recurso [Casos de Prueba SQL: Ejemplo UrbanThreads](https://qapractices.com/es/test-cases/sql-test-cases/) de QAPractices.

## Contenido

| Archivo | Qué es |
|---|---|
| `seed.sql` | Esquema y datos de muestra de UrbanThreads en dialecto MySQL 8.x: `customers`, `products`, `inventory`, `orders`, `order_items`, `transactions`, `store_credit`, `users`, `order_audit`, más las filas de Alice/Bob/Carol y `retro-denim-jacket` con `stock_count = 10`. |
| `sp_create_order.sql` | Procedimiento almacenado `sp_CreateOrder` usado por TC-006: valida la entrada primero, luego crea la orden, descuenta stock y escribe la fila de auditoría dentro de una sola transacción. |
| `test_queries.sql` | Las consultas detrás de TC-001 a TC-007 como script comentado: chequeos SELECT, payloads de inyección, la demo de rollback, paginación keyset, llamadas a `sp_CreateOrder` y ejecuciones de `EXPLAIN`. |

## Inicio rápido

```bash
# Cargar el esquema y los datos de muestra (cliente MySQL 8.x)
mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < seed.sql

# Crear el procedimiento almacenado usado por TC-006
mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < sp_create_order.sql

# Ejecutar las consultas de prueba (descomenta las líneas destructivas según necesites)
mysql -u qa -h staging.db.urbanthreads.com -D urbanthreads < test_queries.sql
```

Para PostgreSQL 16, reemplaza `ENUM` con `VARCHAR` más un `CHECK` y `AUTO_INCREMENT` con `GENERATED ALWAYS AS IDENTITY`; las consultas en sí son neutras de dialecto salvo `CALL`/`LIMIT`, que funcionan en ambos motores.

## Notas

- `test_queries.sql` es intencionalmente conservador: las sentencias destructivas (la violación de FK forzada, las llamadas inválidas a `sp_CreateOrder`, `CREATE`/`DROP INDEX`) están comentadas para que una ejecución completa sea de solo lectura.
- El escenario de concurrencia de TC-004 necesita dos sesiones de cliente separadas — ejecuta los bloques de Sesión A y Sesión B desde terminales distintas. `information_schema.innodb_trx` (MySQL) o `pg_locks` (PostgreSQL) muestran qué transacción está esperando.
- `transactions` solo trae las columnas que usa la suite; para reproducir el timing de paginación profunda, genera tú mismo el volumen de 10M de filas en lugar de sembrarlo aquí.

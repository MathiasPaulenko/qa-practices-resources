# Companion de Testing de Versionado de APIs

Companion de la guía [Testing de Versionado de APIs](https://qapractices.com/es/documentation/api-versioning-testing-strategy/) de QAPractices.

## Archivos

- `compare-api-versions.sh` — dispara requests idénticos a `v1` y `v2` de los mismos paths y compara las respuestas, el detector de breaking changes más barato de la guía.

## Uso

```bash
chmod +x compare-api-versions.sh
./compare-api-versions.sh https://staging.example.com/api users/42 orders/1001
```

Para cada path, el script imprime el diff unificado entre las respuestas de `v1` y `v2`. Clasificá cada cambio como breaking (rename, eliminación, cambio de tipo) o aditivo (campo nuevo, valor de enum nuevo) — y recordá que "aditivo" igual rompe clientes con validación estricta de esquema.

Promové esos mismos pares de requests a CI cuando el diff quede estable; para cobertura consumer-driven de los mismos checks, consulta la sección de Pact de la guía.

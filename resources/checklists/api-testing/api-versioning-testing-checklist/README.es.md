# Checklist de pruebas de versionado de APIs — Companion

Scripts ejecutables para el [Checklist de pruebas de versionado de APIs](https://qapractices.com/es/checklists/api-versioning-testing-checklist/) de QAPractices.

## Scripts

### `scripts/verify-deprecation-headers.sh`

Consulta un endpoint deprecado y verifica que las tres señales de protocolo llegan a la respuesta: `Deprecation` (RFC 9745), `Sunset` con fecha HTTP válida (RFC 8594) y una cabecera `Link` con `rel="successor-version"`. Un cuerpo con `200 OK` no demuestra nada — la señal de retiro vive en las cabeceras. Sale con `0` si el endpoint ya devuelve `410 Gone` (el retiro ya ocurrió y las cabeceras ya no aplican).

```bash
./scripts/verify-deprecation-headers.sh https://api.acme.dev/v1/users/42
```

### `scripts/check-version-negotiation.sh`

Sondea la superficie de negociación: un path de versión válido, una petición sin versión, una versión inexistente, una cabecera de versión no numérica e indicadores contradictorios entre URL y cabecera. Cualquier `500` falla al instante: una entrada inválida nunca debe romper el enrutador de versiones. Las sondas de versión ausente y de conflicto se reportan sin forzar, porque el código correcto depende del valor por defecto y la precedencia documentados.

```bash
./scripts/check-version-negotiation.sh https://api.acme.dev v1 v99
```

## Requisitos

- `bash`, `curl`

## Códigos de salida

| Código | Significado |
|--------|-------------|
| 0 | Comprobaciones correctas |
| 1 | Error de uso o endpoint inalcanzable |
| 2 | Verificación fallida — cabeceras ausentes/mal formadas o estado no documentado |

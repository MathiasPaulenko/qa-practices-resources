# Casos de Prueba de Pagos Móviles — Companion

Artefactos ejecutables para [Casos de Prueba de Pagos Móviles: Apple Pay y Google Pay](https://qapractices.com/es/test-cases/mobile-payment-testing-apple-pay-google-pay/) de QAPractices.

## Contenido

| Archivo | Propósito | TC relacionado |
|---|---|---|
| `python/apple_receipt_validation.py` | Verifica receipts de Apple contra `verifyReceipt` (maneja el redirect 21007 de sandbox) | TC-MP-006, TC-MP-007, TC-MP-008 |
| `python/pan_in_logs_test.py` | Check pytest de que no se filtran PAN/datos de tarjeta en los logs | TC-MP-011 |
| `scripts/sandbox-setup-checklist.md` | Checklist de entorno para testing sandbox de Apple Pay / Google Pay / IAP | todos |

## Requisitos

- Python 3.12+, `requests` 2.32+, `pytest` 8.3+.
- Variables `APPLE_SHARED_SECRET` y `RECEIPT_DATA` para la validación de receipts.
- Un archivo `app.log` en el directorio de trabajo para el check de PAN.

## Uso

```bash
# Validar un receipt (sandbox)
RECEIPT_DATA=... APPLE_SHARED_SECRET=... python python/apple_receipt_validation.py

# Escanear logs buscando datos de tarjeta
pytest python/pan_in_logs_test.py -v
```

English version: [README.md](README.md)

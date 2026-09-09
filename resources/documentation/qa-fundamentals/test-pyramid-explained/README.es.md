# Companion de La Pirámide de Testing Explicada

Recurso companion de la guía [La Pirámide de Testing Explicada](https://qapractices.com/es/documentation/test-pyramid-explained). Incluye ejemplos ejecutables para cada capa de la pirámide: unit, integration, API y end-to-end.

## Archivos

| Archivo | Capa | Propósito |
| ------ | ---- | --------- |
| `src/calculateTotal.test.js` | Unit | Test unitario con Jest para lógica de descuento de carrito |
| `src/test_order_api.py` | Integration | Test de integración con pytest para persistencia de órdenes |
| `src/test_checkout_api.py` | API / Service | Test de API con pytest para validación de pago |
| `src/checkout.spec.js` | End-to-End | Test e2e con Playwright para checkout de invitado |
| `.github/workflows/tests.yml` | CI | Workflow de GitHub Actions que ejecuta todas las capas |

## Inicio Rápido

```bash
# Unit tests (Node.js + Jest)
npm install jest
npx jest src/calculateTotal.test.js

# Integration y API tests (Python + pytest)
pip install requests pytest
pytest src/test_order_api.py src/test_checkout_api.py

# End-to-end tests (Playwright)
npx playwright install
npx playwright test src/checkout.spec.js
```

## Requisitos

- Node.js 18+ y npm
- Python 3.11+
- Un servidor API local en `http://localhost:8000` (para tests de integración/API)
- Navegadores de Playwright instalados

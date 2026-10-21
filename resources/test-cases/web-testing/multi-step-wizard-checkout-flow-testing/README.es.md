# Wizard Multi-Paso / Flujo de Checkout — Companion Ejecutable

Máquina de estados de wizard sin dependencias (`wizard-flow.mjs`) más una suite `node:test` que mapea los casos de [Wizard Multi-Paso y Checkout: 18 Casos de Prueba](https://qapractices.com/es/test-cases/multi-step-wizard-checkout-flow-testing/).

El modelo codifica las reglas bajo test: avanzar está gateado por la validación de cada paso, `back()` retiene los datos, `serialize()`/`restore()` cubre la recuperación tras recarga, `goto()` exige prerrequisitos del lado del servidor, y `submit()` es idempotente.

## Requisitos

- Node.js 20+

## Correr los tests

```bash
node --test tests/*.test.mjs
```

## Qué cubre

| Comportamiento | Mapea a |
|---|---|
| Navegación secuencial, paso a paso | TC-01 |
| La validación por paso bloquea el avance | TC-02 |
| Volver atrás retiene los datos | TC-03 |
| Los deep links redirigen al primer paso faltante | TC-04, TC-15 |
| Serialize/restore para recuperación tras recarga | TC-05 |
| Éxito crea un pedido; rechazo conserva el estado | TC-06, TC-07 |
| Submit idempotente / protección de doble envío | TC-13 |
| Submit rechazado con un paso incompleto | TC-15 |

## Uso

```javascript
import { WizardFlow, checkoutSteps } from './wizard-flow.mjs';

const flow = new WizardFlow(checkoutSteps());
flow.next({ email: 'qa@qapractices.test', firstName: 'Ada' });
flow.next({ method: 'express' });
flow.next({ card: '4242424242424242' });
const result = flow.submit((data) => ({ ok: true, orderId: 'ord_1' }), {
  idempotencyKey: 'attempt-1',
});
```

Adapta `checkoutSteps()` a tus propios pasos — cada paso es solo `{ id, validate }`.

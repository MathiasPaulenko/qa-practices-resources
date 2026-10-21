# Stepper Wizard Form — Companion Ejecutable

Máquina de estados de stepper sin dependencias (`stepper-form.mjs`) más una suite `node:test` que mapea los casos de [Casos de Prueba de Stepper Wizard: 30 Escenarios](https://qapractices.com/es/test-cases/stepper-wizard-form-test-cases/).

El modelo codifica las reglas bajo prueba: `next()` es la única transición con gate, `back()`/`editTo()` restauran estado, `activeSteps()` es derivada así que los pasos condicionales aparecen y desaparecen, `goto()` exige prerrequisitos del lado del servidor, `serialize()`/`restore()` cubren la recuperación de borrador con TTL, y `submit()` agrega solo los pasos activos — los datos de pasos saltados nunca se envían.

## Requisitos

- Node.js 20+

## Ejecutar los tests

```bash
node --test tests/*.test.mjs
```

## Qué cubre

| Comportamiento | Mapea a |
|---|---|
| Navegación secuencial, un paso a la vez | TC-01 |
| Volver atrás retiene los datos ingresados | TC-02, TC-05 |
| La validación por paso bloquea el avance | TC-03 |
| El envío agrega solo pasos activos, una vez | TC-06 |
| Lógica de salto condicional, en ambas direcciones | TC-09, TC-23 |
| Datos huérfanos excluidos del payload | Casos de borde, TC-23 |
| Editar desde revisión salta al paso correspondiente | TC-10 |
| Deep links redirigen al primer paso incompleto | TC-11 |
| Restaurar borrador / rechazo de borrador expirado | TC-14, TC-16, TC-25 |
| Envío fallido conserva datos, el reintento funciona | TC-17 |
| Cancelar exige confirmación | TC-20 |
| El progreso recalcula sobre la lista derivada | TC-26 |
| Envío idempotente / protección contra doble envío | Casos de borde, TC-06 |

## Uso

```javascript
import { StepperWizard, onboardingSteps } from './stepper-form.mjs';

const w = new StepperWizard(onboardingSteps());
w.next({ email: 'qa.user@qapractices.dev', password: 'Str0ng!Pass' });
w.next({ name: 'Ada Lovelace', accountType: 'business' }); // inserta el paso Empresa
w.next({ companyName: 'QA Industries' });
w.next({ theme: 'dark' });
const res = w.submit((payload) => ({ ok: true, recordId: 'rec_1' }), {
  idempotencyKey: 'attempt-1',
});
```

Adapta `onboardingSteps()` a tus propias definiciones de paso — cada paso es `{ id, validate?, when? }`, donde `when` gatea la existencia del paso sobre los datos combinados de pasos anteriores.

# AI Prompt: Generar Casos de Test de GraphQL Subscriptions — Companion

Archivos companion del recurso [AI Prompt: Generar Casos de Test de GraphQL Subscriptions](https://qapractices.com/es/prompts/ai-prompt-graphql-subscription-test-cases).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de casos de test de subscriptions, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: un backend de chat en tiempo real con Apollo Server 4, graphql-transport-ws, JWT y Redis pub/sub. |
| `example-output.md` | Fragmento de la matriz de tests generada para esa entrada (seis casos con severidades). |

## Uso

1. Copiá `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplazá cada placeholder entre corchetes — servidor, transporte, protocolo, auth, pubsub, escala — con tus valores reales.
3. Corrélo y compará la forma de la salida con `example-output.md`; si un área de cobertura vuelve floja, pedile de nuevo ese ítem numerado.
4. Pegá tu schema de subscriptions real junto al prompt para que los casos nombren campos reales.
5. Revisá las severidades antes de cargarlas — un check de auth perdido es Crítico aunque el modelo lo marque Medium.

## Requisitos

- Cualquier LLM que acepte un prompt de ~1.5k tokens (modelos clase GPT-4, Claude, Copilot Chat).
- Para ejecutar los casos generados: un servidor GraphQL con subscriptions (Apollo Server 4, Yoga, Mercurius o graphql-ws) y un entorno accesible.

## Notas

- `graphql-ws` y `graphql-transport-ws` son protocolos distintos — declará cuál corre tu servidor o los casos de reconexión apuntarán al flujo de mensajes equivocado.
- El prompt cubre solo subscriptions; combinálo con recursos de tests de queries/mutations para cobertura completa de la API.
- Nunca pegues credenciales reales ni endpoints de producción en el prompt.

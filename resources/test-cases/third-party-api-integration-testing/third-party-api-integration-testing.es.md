
Eso me enseÃ±Ã³ que las APIs de terceros son dependencias que no controlo. Testearlas significa cubrir sus modos de fallo tan cuidadosamente como sus happy paths.

![Flujo de prueba de integraciÃ³n con APIs de terceros: auth, rate limit, request, respuesta del proveedor, validaciÃ³n de esquema, fallback, validaciÃ³n de firma de webhook](/assets/images/diagrams/third-party-api-integration-flow.svg)

**Â¿QuÃ© son estos casos de prueba?** Los escribÃ­ como una suite reutilizable y paso a paso que ejecuto antes de liberar cualquier feature que dependa de una API externa. Cubren autenticaciÃ³n, rate limits, timeouts, retries, fallbacks, webhooks y cambios de esquema. Para guÃ­a relacionada, consultÃ¡ [Mejores PrÃ¡cticas de Testing de REST API](/es/documentation/rest-api-testing-best-practices) y [API Mocking con WireMock](/es/documentation/api-mocking-with-wiremock).

## CuÃ¡ndo Usar

Ejecuto estos casos cada vez que la app le entrega control a un servicio que no puedo arreglar yo mismo. Los triggers mÃ¡s comunes:

- **Nueva integraciÃ³n de terceros:** antes de liberar cualquier feature que dependa de una API externa.
- **Updates de contrato:** despuÃ©s de cualquier entrada de changelog que pueda cambiar payloads o cÃ³digos de status.
- **Cambios de rate limit:** cuando el proveedor introduce nuevos tiers o reglas de throttling.
- **Disaster recovery drills:** simular downtime del proveedor y verificar el comportamiento de fallback.
- **MigraciÃ³n entre proveedores:** validar paridad entre la integraciÃ³n vieja y la nueva.

## Test Cases

### Casos de Borde y Valores LÃ­mite

Estos son los lÃ­mites que separan una integraciÃ³n que funciona de una que se rompe. Los mantengo en una checklist aparte porque la documentaciÃ³n del proveedor rara vez los menciona explÃ­citamente.

| Escenario | Input | Tipo de LÃ­mite | Resultado Esperado | Nota de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|
| Request con token OAuth expirado | `Authorization: Bearer expired-token` | LÃ­mite de expiraciÃ³n de token | HTTP 401 o 403 con mensaje claro de token expirado | pytest + requests | Alta |
| Request en el umbral exacto de rate limit | Request 999 de un lÃ­mite de 1,000 req/min | LÃ­mite de rate limit | El request tiene Ã©xito; el siguiente retorna 429 con `Retry-After` | k6 / Locust | Alta |
| Proveedor retorna 503 sin fallback configurado | 503 forzado desde mock del proveedor | LÃ­mite de outage del proveedor | El circuito se abre o el usuario ve un error graceful dentro del SLA | WireMock + toxiproxy | Alta |
| Webhook con firma invÃ¡lida | Header `X-Signature` no coincide con el payload | LÃ­mite de integridad de webhook | El webhook se rechaza con HTTP 400; no se procesa acciÃ³n | Flask test client | Alta |
| Payload un byte sobre el lÃ­mite del proveedor | Body de `max_size + 1` bytes | LÃ­mite de tamaÃ±o | HTTP 413 Payload Too Large o error equivalente del proveedor | pytest + requests | Media |

### TC-001: Autenticar con Credenciales VÃ¡lidas

Antes de testear modos de fallo, hay que probar que el happy path funciona contra el sandbox del proveedor.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-001 | Autenticar con API key o token OAuth vÃ¡lido | Credenciales vÃ¡lidas configuradas para el ambiente sandbox | API key y token OAuth de sandbox | 1. Enviar un request autenticado al sandbox del tercero.<br>2. Verificar el status de la respuesta y la estructura del payload. | El request tiene Ã©xito (2xx). La respuesta coincide con el schema documentado del endpoint. | pytest + requests | Alta |

### TC-002: Rechazar Credenciales InvÃ¡lidas o Expiradas

Las credenciales invÃ¡lidas son la primera lÃ­nea de defensa. Este caso verifica que la app las rechace sin filtrar secretos.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-002 | Rechazar credenciales invÃ¡lidas, expiradas y revocadas | El ambiente de test puede usar tokens revocados e invÃ¡lidos | API key invÃ¡lida, token expirado, token OAuth revocado | 1. Enviar un request con API key invÃ¡lida.<br>2. Enviar un request con token expirado.<br>3. Enviar un request con token OAuth revocado. | Todos los requests retornan 401 o 403. Los mensajes de error no exponen claves, tokens o stack traces. | pytest + requests | Alta |

### TC-003: Comportamiento del Umbral de Rate Limit

La mayorÃ­a de los proveedores imponen un lÃ­mite de requests. Este caso prueba que la app lee los headers y hace back off en lugar de golpear el endpoint.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-003 | Verificar umbral de rate limit y headers | El rate limit estÃ¡ documentado (ej. 1,000 req/min) | Volumen de requests que cruza el umbral | 1. Enviar requests hasta el lÃ­mite documentado.<br>2. Enviar un request adicional sobre el lÃ­mite.<br>3. Inspeccionar headers `Retry-After` y `X-RateLimit-Remaining`. | Los requests dentro del lÃ­mite tienen Ã©xito. El request sobre el lÃ­mite retorna 429. Los headers estÃ¡n presentes y son correctos. | k6 / Locust | Alta |

### TC-004: Timeout y LÃ³gica de Retry

Las respuestas lentas no son errores, pero se convierten en errores si la app espera para siempre. Este caso verifica timeout y retry.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-004 | Manejar respuestas lentas y network timeouts | Mock server o proxy configurado para delayed responses | Umbral de timeout (ej. 5 segundos); polÃ­tica de retry (ej. 3 retries con backoff exponencial) | 1. Configurar el mock para retrasar la respuesta mÃ¡s allÃ¡ del timeout.<br>2. Enviar el request.<br>3. Observar reintentos y comportamiento final. | El request hace timeout despuÃ©s del umbral. Los reintentos siguen la polÃ­tica de backoff. El usuario ve un error graceful. | WireMock / toxiproxy + pytest | Alta |

### TC-005: Parseo de Error Responses

Los proveedores retornan 5xx y bodies malformados. Este caso asegura que la app los parsea sin crashear ni exponer detalles internos.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-005 | Parsear y propagar error responses del tercero | Mock server o sandbox retorna cÃ³digos de error documentados | 400, 500, 503 y responses no JSON | 1. Enviar requests que disparen cada cÃ³digo de error.<br>2. Verificar que la app loguea y expone el error correctamente. | La app parsea el error del proveedor, no crashea, loguea contexto y muestra un mensaje user-friendly. | pytest + requests | Alta |

### TC-006: Fallback cuando el Servicio no EstÃ¡ Disponible

Cuando el proveedor cae, la app tiene que seguir funcionando. Este caso fuerza un 503 y valida la lÃ³gica de fallback.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-006 | Activar fallback cuando el servicio de terceros cae | La lÃ³gica de fallback estÃ¡ implementada para el feature | Endpoint bloqueado o WireMock retornando 503 | 1. Bloquear todo el trÃ¡fico al endpoint del proveedor o forzar 503.<br>2. Disparar un request que dependa del servicio.<br>3. Observar el comportamiento de fallback. | El fallback se activa. La funcionalidad core sigue disponible. Las funciones no crÃ­ticas se degradan sin romper la experiencia. | WireMock + logs de aplicaciÃ³n | Alta |

### TC-007: ValidaciÃ³n de Response Schema

Las respuestas de los proveedores cambian sin aviso. Este caso valida cada campo que la app usa y descarta el resto de forma segura.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-007 | Validar schema de responses de terceros | JSON Schema o tipos de TypeScript definidos para la integraciÃ³n | Responses cubriendo variaciones documentadas y no documentadas | 1. Enviar requests cubriendo todas las formas documentadas de respuesta.<br>2. Validar cada respuesta contra el schema.<br>3. Probar el manejo de campos desconocidos. | Todos los campos documentados estÃ¡n presentes y correctamente tipados. Los campos desconocidos se ignoran o loguean, no crashean el parser. | jsonschema / Pydantic | Alta |

### TC-008: Delivery de Webhook y ValidaciÃ³n de Firma

Los webhooks son push, no pull. Este caso verifica la entrega y rechaza cualquier payload con firma invÃ¡lida.

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-008 | Verificar delivery de webhook y firma del proveedor | El endpoint de webhook estÃ¡ registrado en el sandbox del proveedor | Payloads y firmas vÃ¡lidas e invÃ¡lidas | 1. Disparar un evento en el sandbox del proveedor.<br>2. Verificar que el webhook llega al endpoint.<br>3. Validar la firma y la estructura del payload. | El webhook se entrega dentro del SLA documentado. El payload coincide con el schema. Firmas invÃ¡lidas se rechazan. | Flask test client / ngrok para sandbox | Alta |

## Mejores PrÃ¡cticas

1. Nunca testees contra APIs de terceros de producciÃ³n en CI. Yo siempre uso mocks, sandboxes o recorded fixtures. Los endpoints de producciÃ³n pueden rate-limitar el build y mutar data real.
2. ImplementÃ¡ y testeÃ¡ circuit breakers para que fallos repetidos no sigan propagÃ¡ndose.
3. LogueÃ¡ el body y headers completos del proveedor cuando ocurre un error. Sin la respuesta cruda, debuguear un problema del proveedor es adivinar.
4. Pin a una versiÃ³n especÃ­fica de la API del proveedor y testeÃ¡ upgrades en un ambiente dedicado. Los bumps silenciosos de versiÃ³n son una fuente comÃºn de breaking changes.
5. MonitoreÃ¡ tiempos de respuesta y uptime contra el SLA documentado del proveedor. Un 99.99% de uptime sigue significando minutos de downtime por mes.
6. ValidÃ¡ el schema de respuesta en cada corrida de tests de integraciÃ³n para detectar cambios del proveedor temprano.
7. GuardÃ¡ API keys y tokens en variables de entorno, nunca en el cÃ³digo de test ni en repositorios.

## Errores Comunes

1. Asumir que el proveedor siempre estÃ¡ disponible. Incluso 99.99% de uptime significa downtime mensual.
2. Testear solo el happy path e ignorar 5xx, timeouts y responses malformados.
3. Hardcodear URLs del proveedor en lugar de usar configuraciÃ³n para sandbox vs producciÃ³n. Una vez vi staging apuntando a producciÃ³n por eso.
4. Ignorar headers de rate limit y disparar errores 429 o suspensiÃ³n de cuenta.
5. Saltar la validaciÃ³n de schema, lo que permite que cambios breaking del proveedor lleguen a producciÃ³n.
6. Correr CI contra endpoints reales y golpear rate limits de producciÃ³n o mutar data.

## Recursos Relacionados

- [Mejores PrÃ¡cticas de Testing de REST API](/es/documentation/rest-api-testing-best-practices)
- [API Mocking con WireMock](/es/documentation/api-mocking-with-wiremock)
- [Casos de Prueba de Rate Limit de API](/es/test-cases/api-rate-limit-test-cases)
- [Casos de Prueba de Manejo de Errores de API](/es/test-cases/api-error-handling-test-cases)
- [Checklist de Testing de API](/es/checklists/api-testing-checklist)

## Preguntas Frecuentes

### Â¿DeberÃ­a testear contra la API de terceros real en CI?

No. UsÃ¡ el sandbox del proveedor, mocks con WireMock o recorded fixtures. Los endpoints de producciÃ³n pueden rate-limitar tu CI y mutar data real.

### Â¿CÃ³mo simulo el downtime de un proveedor?

UsÃ¡ un mock server retornando 503, un proxy como toxiproxy para dropear o retrasar trÃ¡fico, o reglas de firewall para bloquear el endpoint en staging.

### Â¿CuÃ¡l es el error mÃ¡s comÃºn al testear APIs de terceros?

Testear solo el happy path. Los proveedores fallan con 5xx, respuestas lentas y cambios de esquema que tu cÃ³digo debe manejar.

### Â¿CÃ³mo detecto cambios breaking en el esquema de un proveedor?

EjecutÃ¡ validaciÃ³n de contrato o esquema en cada build de CI. ComparÃ¡ el OpenAPI o changelog del proveedor con tu esquema de integraciÃ³n y alertÃ¡ sobre diffs.

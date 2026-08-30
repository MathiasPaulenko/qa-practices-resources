
# Casos de Prueba de Fugas de Memoria

## VisiÃ³n General

Una vez pasÃ© dos dÃ­as persiguiendo una fuga en un servicio de Node.js. El culpable era un closure dentro de un `setInterval` que retenÃ­a una referencia a un cachÃ© de 50 MB. Las fugas no crashean la app de una; consumen memoria de a poco hasta que el sistema se ralentiza, cuelga o el SO lo mata.

**Â¿QuÃ© son estos casos de prueba?** Los armÃ© como una suite reutilizable y paso a paso que ejecuto antes de cualquier release donde la memoria pueda ser un problema. Ayudan a detectar, aislar y probar fugas en web frontends, servicios backend y apps mobile. Los casos cubren web frontends, servicios backend y apps mobile usando Chrome DevTools, `process.memoryUsage()`, `heapdump`, Valgrind y Xcode Instruments. Cada caso incluye precondiciones, datos de prueba, pasos, resultados esperados y prioridad.

![Workflow de detecciÃ³n de fugas de memoria: establecer baseline, aplicar carga, capturar snapshot, comparar y analizar, aislar root cause, corregir y verificar en CI](/assets/images/diagrams/memory-leak-detection-flow.svg)

Para cobertura mÃ¡s amplia de performance, consultÃ¡ la [GuÃ­a de Performance Testing](/es/documentation/performance-testing-guide) y la [GuÃ­a de Load Testing con k6](/es/documentation/load-testing-with-k6).

## CuÃ¡ndo Usar

- **Releases mayores:** siempre ejecuto estos casos cuando sale una feature nueva, un upgrade de dependencia o un cambio de framework, porque esos son los cambios mÃ¡s propensos a introducir una fuga.
- **DespuÃ©s de actualizar dependencias:** una versiÃ³n nueva de una librerÃ­a puede retener objetos por mÃ¡s tiempo. Una vez tracÃ© una fuga a un patch bump de una librerÃ­a de logging.
- **Durante endurance testing:** si un servicio corre 24+ horas, espero que su grÃ¡fico de memoria se mantenga plano. Una subida lenta es la firma de una fuga.
- **ValidaciÃ³n post-incidente:** despuÃ©s de un outage relacionado a memoria, vuelvo a correr el caso exacto que lo reprodujo antes de declarar el fix hecho.
- **PrevenciÃ³n de regresiÃ³n:** mantengo checks automÃ¡ticos de memoria en CI para que un build fallido frene una fuga antes de que llegue a producciÃ³n.
- **Releases de apps mobile:** iOS y Android terminan apps que cruzan los lÃ­mites de memoria del sistema. Una corrida de 10 minutos en dispositivo real nos salvÃ³ mÃ¡s de una vez.

## Test Cases

### Casos de Borde y Valores LÃ­mite

Estas condiciones de borde las mantengo en una checklist separada porque son las que suelen atrapar fugas que los tests funcionales normales no detectan.

| Escenario | Input | Tipo de LÃ­mite | Resultado Esperado | Nota de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|
| Forzar garbage collection antes del snapshot | `global.gc()` o flag `--expose-gc` | LÃ­mite de baseline GC | El snapshot refleja objetos retenidos, no basura transitoria | Node.js / Chrome flag | Alta |
| Correr workload con cero iteraciones | 0 acciones repetidas | LÃ­mite inferior | Se captura baseline sin crecimiento | Baseline manual o automatizado | Media |
| Correr workload en capacidad mÃ¡xima declarada | 1,000 iteraciones o peak VUs | LÃ­mite superior | El crecimiento de memoria se mantiene bajo el umbral (ej. < 10%) | k6 / Playwright | Alta |
| Snapshot despuÃ©s de ciclos de mount/unmount | 100 ciclos de mount/unmount | LÃ­mite de ciclo de vida | La cantidad de listeners y DOM vuelve al baseline | Playwright + DevTools | Alta |
| ComparaciÃ³n de heap entre versiones de librerÃ­a | VersiÃ³n vieja vs nueva | LÃ­mite de versiÃ³n | La nueva versiÃ³n no retiene objetos extra bajo la misma carga | Diff manual | Media |

### TC-001: Capturar un Baseline Heap Snapshot

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-001 | Capturar un baseline heap snapshot | AplicaciÃ³n reciÃ©n iniciada; sin sesiones activas | N/A | 1. Iniciar la app en modo producciÃ³n.<br>2. Abrir la pestaÃ±a Memory de DevTools o ejecutar `node --heapsnapshot-near-heap-limit=1`.<br>3. Forzar GC y capturar un snapshot.<br>4. Registrar el heap size total. | El heap size estÃ¡ dentro del rango de baseline documentado para el ambiente. | Manual / Chrome DevTools | Alta |

### TC-002: Detectar AcumulaciÃ³n de DOM Nodes en una SPA

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-002 | Detectar acumulaciÃ³n de DOM nodes detached | SPA con transiciones de ruta; DevTools abierto | 50 transiciones entre `/list` y `/detail` | 1. Tomar snapshot baseline en `/list`.<br>2. Navegar a `/detail` y volver 50 veces.<br>3. Forzar GC y tomar segundo snapshot.<br>4. Comparar heap size y DOM nodes detached. | La diferencia de heap es < 10% del baseline. No se retienen DOM nodes detached. | Playwright + Chrome DevTools | Alta |

### TC-003: Validar Estabilidad de Memoria en SesiÃ³n Larga

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-003 | Validar estabilidad de memoria por 4 horas | Usuario autenticado; tareas de background corriendo | SesiÃ³n realista con acciones cada 5 minutos | 1. Loguearse y registrar heap size inicial.<br>2. Realizar acciones cada 5 minutos por 4 horas.<br>3. Registrar heap size final y calcular tasa de crecimiento. | La tasa de crecimiento es < 5 MB/hora. Sin errores `OutOfMemory` en logs. | k6 / Test de endurance manual | Alta |

### TC-004: Verificar que Event Listeners se Limpian al Desmontar

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-004 | Verificar limpieza de event listeners | Componente con event listeners; DevTools abierto | 100 ciclos de mount y unmount | 1. Registrar cantidad de event listeners activos en baseline.<br>2. Montar y desmontar el componente 100 veces.<br>3. Forzar GC y comparar la cantidad. | La cantidad de event listeners activos vuelve al baseline tras desmontar. | React DevTools / Playwright | Alta |

### TC-005: Detectar Crecimiento de Heap en Backend Bajo Carga

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-005 | Detectar crecimiento de heap en backend | Servicio API corriendo; generador de carga disponible | 1,000 requests durante 30 minutos | 1. Registrar `heapUsed` baseline via `process.memoryUsage()`.<br>2. Enviar carga sostenida por 30 minutos.<br>3. Forzar GC y registrar `heapUsed` final. | El crecimiento de heap es < 20% del baseline. Ninguna categorÃ­a de objetos crece > 50%. | k6 + Node.js heap dump | Alta |

### TC-006: Validar que la Memoria de Mobile App Vuelve al Baseline

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-006 | Validar recuperaciÃ³n de memoria mobile | Dispositivo fÃ­sico iOS o Android; app instalada | 10 minutos de flujo tÃ­pico de usuario | 1. Lanzar la app y registrar memoria baseline.<br>2. Completar un flujo tÃ­pico.<br>3. Volver al home y esperar 60 segundos.<br>4. Registrar memoria final. | La memoria vuelve cerca del baseline. El SO no termina la app. | Xcode Instruments / Android Profiler | Alta |

### TC-007: Aislar un Leak a una VersiÃ³n EspecÃ­fica de LibrerÃ­a

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-007 | Aislar leak a una versiÃ³n de librerÃ­a | Dos builds: versiÃ³n vieja y nueva de la librerÃ­a | Carga idÃ©ntica para ambas versiones | 1. Correr la misma carga en la versiÃ³n vieja por 1 hora.<br>2. Capturar un heap dump.<br>3. Repetir en la versiÃ³n nueva.<br>4. Comparar grafos de retenciÃ³n. | La versiÃ³n nueva no retiene objetos extra de librerÃ­a que la vieja libera. | `heapdump` / Valgrind | Media |

### TC-008: Fallar Build de CI por RegresiÃ³n de Memoria

| ID | Escenario | Precondiciones | Datos de Prueba | Pasos | Resultado Esperado | Notas de AutomatizaciÃ³n | Prioridad |
|---|---|---|---|---|---|---|---|
| TC-008 | Fallar build de CI por regresiÃ³n de memoria | Pipeline de CI puede correr browser headless o tests de API | Baseline del build verde anterior | 1. Correr una carga estandarizada en CI.<br>2. Capturar `process.memoryUsage().heapUsed` o `performance.measureUserAgentSpecificMemory()`.<br>3. Comparar contra el baseline anterior.<br>4. Fallar si el crecimiento supera el 10%. | Build pasa cuando la memoria es estable; falla con mensaje descriptivo si supera el umbral. | GitHub Actions / Playwright | Alta |

## Mejores PrÃ¡cticas

1. Siempre forzÃ¡ garbage collection antes de tomar un heap snapshot. De lo contrario medÃ­s objetos transitorios, no fugas reales.
2. Perfilar builds de producciÃ³n, no development builds con hot reload y source maps. Los builds de desarrollo inflan memoria y ocultan el patrÃ³n real.
3. Testear con datos production-like. Los datasets pequeÃ±os esconden problemas de retenciÃ³n; cargo al menos 10,000 registros realistas antes de confiar en un snapshot.
4. Enfocarse en detached DOM nodes en SPAs y closures en servicios de larga duraciÃ³n. Esos dos patrones representan la mayorÃ­a de las fugas que encontrÃ©.
5. Monitorear RSS, external y heap memory en Node.js. Una fuga de buffers puede no mostrarse en el heap, pero sÃ­ en RSS.
6. Mantener un baseline conocido en version control y compararlo en CI. Sin baseline estÃ¡s adivinando.
7. Usar dispositivos reales o emuladores con versiones idÃ©nticas del SO para testing mobile. El manejo de memoria difiere entre versiones de Android y releases de iOS.

## Errores Comunes

1. Confundir crecimiento intencional del cachÃ© con una fuga ilimitada. Un cachÃ© que se detiene en su lÃ­mite estÃ¡ bien; uno que crece para siempre no.
2. Perfilar development builds en lugar de producciÃ³n. El hot reload y los source maps cambian el perfil de memoria por completo.
3. Ignorar closures y referencias de funciones retenidas en timers o streams. Mi bÃºsqueda de dos dÃ­as en `setInterval` fue exactamente esto.
4. Perfilar solo el proceso principal en una arquitectura de microservicios. Los worker processes y las colas de background fugan igual de seguido.
5. Tomar snapshots sin forzar garbage collection primero. TerminÃ¡s persiguiendo objetos que de todas formas se hubieran limpiado.
6. Depender solo de testing manual y perder regresiones lentas. Las fugas que crecen 1 MB por hora son invisibles en un test manual de 5 minutos.

## Recursos Relacionados

- [GuÃ­a de Performance Testing](/es/documentation/performance-testing-guide)
- [Checklist de Performance Testing](/es/checklists/performance-testing-checklist)
- [Load Testing con k6](/es/documentation/load-testing-with-k6)
- [Casos de Prueba de Performance y Load Testing](/es/test-cases/performance-load-testing-test-cases)
- [Hub de Performance Testing](/es/topics/performance-testing)

## Preguntas Frecuentes

### Â¿CuÃ¡l es la diferencia entre crecimiento de memoria y una fuga de memoria?

El crecimiento es acotado y esperado. Un cachÃ© que llena hasta su lÃ­mite configurado es crecimiento. Una fuga es ilimitada: sigue creciendo despuÃ©s de terminar el trabajo y el garbage collector no tiene camino para reclamarla.

### Â¿DeberÃ­a perfilar en la mÃ¡quina del desarrollador o en CI?

Ambas. Uso profiling local para anÃ¡lisis de root cause y profiling en CI para detectar regresiones automÃ¡ticamente en cada build. El local es rÃ¡pido para debuguear; el CI es la Ãºnica forma de frenar regresiones antes de que salgan.

### Â¿QuÃ© herramientas usar para fugas de memoria en Node.js?

Mi stack habitual es `--expose-gc` para forzar GC, `heapdump` para snapshots, `clinic.js` para diagnÃ³sticos y `0x` para flame graphs. Para fugas nativas cambio a Valgrind o AddressSanitizer, segÃºn el cÃ³digo sospechoso sea C++ o un add-on nativo.

### Â¿CuÃ¡nto tiempo deberÃ­a correr un test de fuga de memoria?

El tiempo suficiente para coincidir con la sesiÃ³n de producciÃ³n que te importa. Para servicios backend, 30 minutos a 4 horas es comÃºn; empiezo con 30 minutos y extiendo solo si veo deriva. Para apps mobile, 10â€“30 minutos de uso real suele ser suficiente porque el OS mata la app rÃ¡pido cuando la memoria sube.

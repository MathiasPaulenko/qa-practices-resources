# Companion del Tutorial de JMeter Load Testing

Companion ejecutable de la guía de QAPractices [Tutorial de JMeter: test plans, threads y listeners](https://qapractices.com/es/documentation/jmeter-load-testing-tutorial/).

## Qué incluye

- **`first-load-test.jmx`** — test plan de JMeter 5.6.3 con un Thread Group de 10 usuarios y ramp-up de 10 segundos, HTTP Request Defaults, CSV Data Set Config, dos assertions y los dos listeners usados en el tutorial.
- **`users.csv`** — CSV de ejemplo que consume el CSV Data Set Config; el path del sampler lo lee como `/users/${userId}`.

## Versiones del stack

| Herramienta | Versión |
| --- | --- |
| JMeter | 5.6.3 |
| Java | 8 o superior (recomendado 17+) |

## Antes de ejecutar

1. Actualiza la variable `apiHost` de `api-staging.example.com` a tu propio host de staging.
2. Mantén `users.csv` en la misma carpeta que el `.jmx`, o apunta el filename del CSV Data Set Config a su ruta absoluta.
3. Para una primera corrida sin riesgo puedes poner `apiHost` en `jsonplaceholder.typicode.com` y cambiar el path del sampler a `/posts` (la Response Assertion con patrón `userId` sigue funcionando).

## Ejecutar la prueba

```bash
jmeter -n -t first-load-test.jmx -l results.jtl -e -o report-folder
```

Abre `report-folder/index.html` al terminar.

## Qué hace el plan

- Dispara `GET /users/${userId}` con 10 hilos en rampa de 10 segundos, una iteración cada uno.
- Verifica que el body de la respuesta contiene `userId` y que completa en menos de 500 ms.
- Incluye un listener `View Results Tree` para depurar en la GUI — desactívalo antes de corridas de carga reales; guarda en memoria el cuerpo de cada respuesta.
- Escribe un log crudo `results.jtl` y un dashboard HTML.

## Licencia

MIT — ver el repo principal para más detalles.

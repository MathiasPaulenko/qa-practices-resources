# Companion de JMeter API Load Test

Companion ejecutable para la guía de QAPractices [Tutorial de JMeter: Load Testing de APIs y Aplicaciones Web](https://qapractices.com/es/documentation/jmeter-tutorial/).

## Contenido

- **`api-load-test.jmx`** — Plan de pruebas de JMeter 5.6.3 con 10 usuarios, ramp-up de 10 segundos y una petición GET contra un host placeholder.
- **`test-data.csv`** — CSV de ejemplo con IDs de usuario para alimentar un `CSV Data Set Config` si querés parametrizar el path.

## Versiones del stack

| Herramienta | Versión |
| --- | --- |
| JMeter | 5.6.3 |
| Java | 8 o superior |

## Antes de ejecutar

1. Actualizá la User Defined Variable `apiHost` de `api-staging.example.com` a tu propio host de staging.
2. (Opcional) Agregá un `CSV Data Set Config` que lea `test-data.csv` y usá `${userId}` en el path del HTTP Request (por ejemplo, `/users/${userId}`).
3. Deshabilitá `View Results Tree` si vas a correr más de unos pocos cientos de hilos.

## Ejecutar el test

```bash
jmeter -n -t api-load-test.jmx -l results.jtl -e -o report-folder
```

Abrí `report-folder/index.html` cuando termine.

## Qué hace el plan

- Golpea `${apiHost}/users` con 10 hilos, ramp-up de 10 segundos, hasta 120 segundos.
- Verifica HTTP 200 y un tiempo de respuesta menor a 500ms.
- Escribe un log crudo `results.jtl` y un dashboard HTML.

## Licencia

MIT — ver el repositorio principal.

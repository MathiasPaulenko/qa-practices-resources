# Tutorial de JMeter Performance Testing — Companion

Assets ejecutables del [Tutorial de JMeter Performance Testing](https://qapractices.com/es/documentation/jmeter-performance-testing-tutorial/).

## Archivos

| Archivo | Qué hace |
|---|---|
| `users.csv` | El fixture de CSV Data Set del Paso 5 — 3 filas cubriendo login válido e inválido. |
| `run-load-test.sh` | Runner non-GUI con los flags exactos del tutorial (`-n -t -l -e -o`), resultados con timestamp y un checklist post-corrida impreso en consola. |
| `results-checklist.md` | Tabla de análisis post-corrida: dónde vive cada métrica en el reporte, qué es sano, qué hacer cuando no lo es. |

## Ejecutar

```bash
chmod +x run-load-test.sh
JMETER_HOME=/ruta/a/apache-jmeter-5.6.3 ./run-load-test.sh test-plans/load-test.jmx
```

Apunta `testdata/` a `users.csv` en tu CSV Data Set Config (Paso 5 del tutorial).

## Qué demuestra

- **Non-GUI es el modo real** — el script ya trae los flags para que nadie corra load tests desde la GUI por accidente.
- **La corrida no es la entrega, el análisis sí** — el checklist impreso evita que colecciones un reporte que nadie lee.

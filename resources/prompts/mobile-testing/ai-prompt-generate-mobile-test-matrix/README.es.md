# Prompt IA: Matriz de Pruebas Móviles — Companion

Archivos complementarios del recurso [Prompt IA: Matriz de Pruebas Móviles](https://qapractices.com/es/prompts/ai-prompt-generate-mobile-test-matrix).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de generación de matriz móvil, listo para copiar en un LLM. |
| `example-input.txt` | Un contexto realista de app móvil: plataformas, mercados, restricciones y capacidad de prueba. |
| `example-output.md` | Un fragmento de salida realista: supuestos, ejes de cobertura, tiers P0/P1/P2, mapa de ejecución y análisis de huecos. |
| `matrix-template.csv` | La matriz generada como CSV — tier, dispositivo, SO, pantalla, red, locale, canal de ejecución y razón por fila. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Reemplaza los placeholders entre corchetes con tu app real, mercados, rango de SO soportado y capacidad de prueba.
3. Compara la respuesta con `example-output.md`; una buena respuesta declara sus supuestos, agrupa filas por razón, asigna corredor a cada tier y admite sus huecos.
4. Usa `matrix-template.csv` como documento de trabajo: una fila por combo dispositivo+SO+pantalla+red con su tier y canal de ejecución.
5. Valida P0 contra analytics reales o los crashes del último trimestre antes de cerrar la matriz — las estimaciones de cuota son un borrador, no verdad absoluta.

## Requisitos

- Sin herramientas; la salida es un documento de planificación.
- Opcional: Firebase Test Lab, BrowserStack o una repisa de dispositivos para ejecutar los tiers.
- Analytics de dispositivos (Firebase, GA4 o Play Console/App Store Connect) vuelven reales las elecciones en vez de estimadas.

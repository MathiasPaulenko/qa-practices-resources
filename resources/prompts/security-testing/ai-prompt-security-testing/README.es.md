# Prompt de IA: Evaluación de Riesgos y Amenazas — Companion

Archivos companion del recurso [Prompt de IA: Evaluación de Riesgos y Amenazas de Seguridad](https://qapractices.com/es/prompts/ai-prompt-security-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | La plantilla del prompt completa, lista para copiar en cualquier LLM. |
| `example-input.txt` | Input de ejemplo: una app de banca online con stack, método de autenticación, activos, flujos y alcance. |
| `example-output.csv` | Registro de riesgos de ejemplo con 6 amenazas puntuadas (mapeo STRIDE + OWASP, probabilidad × impacto). |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los placeholders entre corchetes con el contexto de tu sistema, activos, flujos de datos y alcance.
3. Ejecuta el prompt y revisa el registro — lee primero la sección Assumptions, ahí es donde el modelo confiesa lo que supuso.
4. Compara las filas con `example-output.csv` para comprobar el formato esperado y la puntuación.
5. Alimenta el [prompt de generación de casos de prueba de seguridad](https://qapractices.com/es/prompts/ai-prompt-security-test-case-generation) con los riesgos principales para convertirlos en casos ejecutables.

## Requisitos

- Cualquier LLM (ChatGPT, Claude, GitHub Copilot o un modelo local).
- Opcional: una hoja de cálculo o herramienta GRC que importe CSV si quieres versionar el registro.

## Notas

- Evalúa solo sistemas que estés autorizado a evaluar; conserva la línea de Authorization en el prompt.
- Describe arquitectura, tipos de datos y flujos — nunca pegues credenciales reales, hostnames de sistemas sensibles ni datos de clientes.
- Probabilidad e impacto son estimaciones del modelo: valida las primeras filas contra tus propios datos de exposición antes de comprometer esfuerzo de testing.
- Vuelve a correr la evaluación cuando cambie la arquitectura; un registro de riesgos es una foto.

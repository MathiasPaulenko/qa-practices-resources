# Plantilla de Experimento de Chaos Engineering — Companion

Archivos descargables de la [Plantilla de Experimento de Chaos Engineering](https://qapractices.com/es/templates/chaos-engineering-experiment-template/) en QAPractices.

## Contenido

| Archivo | Propósito |
|---|---|
| `chaos-engineering-experiment-template.md` | Documento de experimento en blanco: detalles, hipótesis, control del radio de impacto, métricas de estado estable, plan de inyección, condiciones de aborto, resultados, hallazgos y aprobación. |
| `experiment-ce-042-sample.md` | El mismo documento rellenado para CE-042, un experimento de pod-kill sobre un API gateway en Kubernetes: hipótesis parcialmente fallida, dos hallazgos con responsables. |
| `pod-kill.yaml` | Manifiesto PodChaos de Chaos Mesh 2.7 que termina el 30% de los pods de `api-gateway` durante un minuto; el paso de inyección del ejemplo. |

## Uso

1. Copia `chaos-engineering-experiment-template.md` en los docs o la wiki de tu proyecto y completa las Secciones 1-6 antes de la ejecución, nunca de memoria después.
2. Adapta `pod-kill.yaml` a tu selector (label `app`, namespace) y radio de impacto, y aplícalo con `kubectl apply -f pod-kill.yaml`.
3. Pausa la inyección en cualquier momento con `kubectl annotate podchaos <nombre> experiment.chaos-mesh.org/pause=true`: ensaya esto antes de la primera ejecución real.
4. Usa `experiment-ce-042-sample.md` como referencia de cómo se ven una hipótesis falsable y unos hallazgos honestos cuando el experimento no pasa del todo.

El YAML requiere [Chaos Mesh](https://chaos-mesh.org/) instalado en el cluster objetivo; el documento en sí es agnóstico de la herramienta.

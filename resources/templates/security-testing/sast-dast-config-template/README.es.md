# Plantilla de Configuración SAST/DAST — Companion

Artículo fuente: [Plantilla de Configuración SAST/DAST](https://qapractices.com/es/templates/sast-dast-config-template/)

Dos archivos listos para copiar a un repositorio:

- `scan-config-template.yaml` — el documento de configuración en blanco con placeholders para cada decisión (inventario de herramientas, rule sets, umbrales de severidad, exclusiones, alcance de escaneo, gate de CI, triage).
- `scan-config-sample.yaml` — el mismo documento rellenado para una API de pagos fintech ficticia con Semgrep 1.99 (SAST en PRs) y OWASP ZAP 2.16 (baseline + api-scan nocturno en staging).

## Uso

1. Copia `scan-config-template.yaml` a tu repo — `security/scan-config.yaml` es un lugar habitual.
2. Reemplaza cada placeholder `[entre corchetes]`. Mantén honestos `owner` y `last review`.
3. Compara con `scan-config-sample.yaml` para ver cómo luce terminado.
4. Los cambios pasan por revisión de PR — este archivo es política, no documentación.

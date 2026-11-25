# Preguntas de Entrevista de Security Testing — Ejemplos

Payloads, páginas de prueba de concepto y configuración de escaneo referenciados por la guía
[30 Preguntas de Entrevista de Security Testing](https://qapractices.com/es/documentation/security-testing-interview-questions).

> Usa estos payloads solo en sistemas propios o con permiso escrito para testear.

## Contenido

- `payloads/sqli.txt` — payloads de SQL injection para formularios de login, campos de búsqueda y parámetros de API.
- `payloads/ssrf.txt` — candidatos de objetivos SSRF: localhost, metadata de instancia AWS y servicios internos.
- `payloads/mass-assignment.json` — body con campo extra para probar si una API mapea input sin filtrar.
- `poc/csrf-transfer.html` — prueba de concepto mínima de CSRF: formulario auto-enviado desde otro origen.
- `poc/clickjacking-test.html` — página de test con iframe: si el objetivo se renderiza, falta protección contra framing.
- `scripts/zap-baseline-scan.sh` — baseline scan de OWASP ZAP 2.14.0 vía Docker.
- `.github/workflows/security-scan.yml` — job de GitHub Actions con `zaproxy/action-baseline@v0.11.0` que falla el build ante hallazgos.

## Uso

```bash
# Baseline scan de ZAP contra un target de staging
./scripts/zap-baseline-scan.sh https://staging.your-app.example
```

Para el recorrido pregunta por pregunta, lee la guía en QAPractices.

# Checklist de Pruebas Pre-Lanzamiento — Companion Ejecutable

Companion del [Checklist de Pruebas Pre-Lanzamiento: Go-Live QA](https://qapractices.com/es/checklists/website-pre-launch-testing-checklist/) ([EN](https://qapractices.com/checklists/website-pre-launch-testing-checklist/)).

Verificador en Node 20+ sin dependencias que ejecuta los checks de SEO, seguridad y go-live del checklist contra una URL en vivo.

## Contenido

| Archivo | Propósito |
|---|---|
| `pre-launch-check.mjs` | Consulta una URL y reporta PASS/FAIL para: estado HTTP, 5 headers de seguridad, fugas de `noindex` (header HTTP + meta robots), largo del title, largo de la meta description, canonical auto-referenciada, OG tags y bloqueos totales en `robots.txt` |
| `tests/pre-launch-check.test.mjs` | Suite `node:test` — 8 tests que cubren headers, fugas de noindex, validación de canonical y reglas de robots.txt |

## Ejecutarlo

```bash
node pre-launch-check.mjs https://staging.example.com
```

La salida es una línea por check con su etiqueta de riesgo:

```text
PASS  [High] strict-transport-security — max-age=63072000; includeSubDomains
FAIL  [High] content-security-policy — missing
PASS  [High] meta robots noindex leak — index (ok)
...
staging.example.com: HIGH-RISK FAILURES — do not launch
```

El exit code es `0` solo cuando todos los checks de riesgo alto pasan — se puede enchufar a un pipeline de release como gate de go/no-go. Los fallos de riesgo medio y bajo igualmente se imprimen.

## Correr los tests

```bash
node --test tests/*.test.mjs
```

Los 8 tests deben pasar. Las funciones del verificador (`checkHeaders`, `checkHtml`, `checkRobotsTxt`) son puras — sin red en los tests.

## Notas

- Los checks de `noindex` cubren ambos vectores que la gente olvida: el header HTTP `X-Robots-Tag` y el `<meta name="robots">` del HTML.
- Los datos ausentes nunca son un pass — headers y tags faltantes fallan explícitamente, como exige la regla del checklist.

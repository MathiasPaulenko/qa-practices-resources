# Prompt IA: Casos de Test OWASP Top 10

Archivos listos para copiar del recurso
[Prompt IA: Casos de Test OWASP Top 10](https://qapractices.com/es/prompts/ai-prompt-generate-owasp-tests/)
de QAPractices.com.

## Archivos

- `prompt-template.txt` — el prompt completo; completá los placeholders
  entre corchetes con tu aplicación, stack, modelo de auth y alcance.
- `example-input.txt` — un ejemplo ya completo (app web de facturación,
  React + Node.js + PostgreSQL, auth JWT).
- `example-output.md` — una muestra de la tabla de casos que produce el
  prompt (OWASP-001 a OWASP-008 más nota de gaps).
- `owasp-probes.csv` — lista semilla de sondas seguras y no destructivas
  por categoría para fuzzers o suites data-driven.

## Seguridad

Los payloads son strings de fixture y sondas de detección pensados para
entornos de staging. Nunca los corras contra producción ni servicios de
terceros sin autorización escrita.

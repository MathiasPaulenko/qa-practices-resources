# Checklist de Prevención de Tests Flaky — Companion

Assets ejecutables del [Checklist de Prevención de Tests Flaky](https://qapractices.com/es/checklists/flaky-test-prevention-checklist/).

## Archivos

| Archivo | Qué hace |
|---|---|
| `auto-wait.spec.ts` | Spec de Playwright 1.48 mostrando el patrón auto-waiting — `toBeEnabled()` hace polling en vez de `waitForTimeout(500)`. Incluye un comentario anti-patrón para el contraste. |
| `repeat-until-failure.sh` | Loopea un spec hasta N veces (default 20) y frena en el primer fallo — el script de prueba de determinismo del checklist, con la expansión `{1..20}` que sí itera. |
| `quarantine-workflow.md` | El proceso de cuarentena que implican los ítems de gestión en CI: tag → ticket → dueño → SLA → fix-o-borrar, manteniendo los retries visibles. |

## Ejecutar

```bash
npx playwright test auto-wait.spec.ts        # demo de auto-waiting
./repeat-until-failure.sh login.spec.ts 20   # probá que un test es determinista
```

## Qué demuestra

- **Las condiciones le ganan a las duraciones** — las assertions con polling reemplazan todo `sleep()`.
- **La flakiness se puede probar** — un loop que nunca falla vale más que una corazonada.
- **La cuarentena es un proceso** — dueño, SLA y una salida de fix-o-borrar, no un `// TODO` para siempre.

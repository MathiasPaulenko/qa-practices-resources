# Testing de Interacción de Feature Flags — Companion

Ejemplos ejecutables del [Checklist de Interacción de Feature Flags](https://qapractices.com/es/checklists/feature-flag-interaction-testing-checklist/).

## Archivos

| Archivo | Qué hace |
|---|---|
| `flag-config.json` | Definiciones de flags con targeting, dependencias y conflictos — la forma que un evaluador de flags lee en runtime. |
| `flag_matrix_test.py` | Suite pytest que ejercita **todas las 2^n combinaciones** de un conjunto de 3 flags y verifica que conflictos y dependencias faltantes resuelven correctamente. |
| `kill_switch_sim.py` | Simulación de propagación de kill switch entre servicios con valores de flag cacheados — muestra por qué un cache sin TTL rompe el kill. |

## Ejecutar

```bash
pip install -r requirements.txt
pytest flag_matrix_test.py -v   # 10 tests: 8 estados de matriz + estado default + sanity de config
python kill_switch_sim.py       # mira un worker con cache stale ignorar el kill switch
```

## Qué demuestra

- **Cobertura de matriz de combinación** — `itertools.product` genera todos los estados de flag; cada estado verifica la decisión del evaluador.
- **Resolución de dependencias y conflictos** — `newCheckout` requiere `payment_v2` y entra en conflicto con `legacyCheckout`; ambas reglas se prueban exhaustivamente.
- **Kill switch vs cache** — el worker cachea valores de flag con TTL largo y sigue sirviendo la feature matada, como en incidentes reales.

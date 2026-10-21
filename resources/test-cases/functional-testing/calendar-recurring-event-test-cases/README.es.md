# Casos de Prueba de Eventos Recurrentes de Calendario — Companion

Recurso complementario de [Eventos Recurrentes de Calendario: 30 Casos de Prueba](https://qapractices.com/es/test-cases/calendar-recurring-event-test-cases/).

## Contenido

- `rrule_engine.py` — capa de recurrencia fina sobre `dateutil.rrule`: `validate_rrule` aplica las restricciones de RFC 5545 que el artículo testea (FREQ válido, COUNT y UNTIL mutuamente excluyentes, UNTIL no anterior a DTSTART), `build_ruleset` arma un rruleset con exdates, y `occurrences_in_range` hace expansión acotada vía `between()` en lugar de materializar la serie.
- `tests/conftest.py` — pone el motor en `sys.path`.
- `tests/test_rrule_engine.py` — subconjunto ejecutable de los casos del artículo: expansión diaria/semanal/mensual/anual (TC001-TC004), cota UNTIL (TC005), INTERVAL (TC006), consulta por rango (TC007), saltos del día 31 (TC011), años bisiestos (TC012), invariancia de hora de reloj en spring-forward y fall-back (TC013/TC014), FREQ inválido (TC017), conflicto COUNT+UNTIL (TC018), recurrencia infinita con consulta acotada (TC020), serie retroactiva (TC021), intersección BYDAY×BYMONTHDAY (TC022), BYSETPOS último-Lunes (TC023), conteos con exdates (TC010/TC029) y round-trip rrulestr (TC030).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `21 passed`.

El motor usa `python-dateutil` para la expansión y `zoneinfo` de stdlib para zonas horarias. En una app de calendario real los mismos checks corren contra tu capa de persistencia — el punto acá es que la invariancia de hora de reloj y la contabilidad de exdates se testean sin mockear un reloj.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/calendar-recurring-event-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/calendar-recurring-event-test-cases/

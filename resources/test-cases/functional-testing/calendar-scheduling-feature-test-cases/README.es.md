# Casos de Prueba de Calendario y Eventos — Companion Ejecutable

Verificaciones Python ejecutables de los modos de fallo de programación cubiertos en
[Casos de Prueba de Calendario y Eventos: 33 Escenarios](https://qapractices.com/es/test-cases/calendar-scheduling-feature-test-cases/)
([English version](https://qapractices.com/test-cases/calendar-scheduling-feature-test-cases/)).

`scheduler.py` implementa las mismas reglas que los casos verifican:

- Eventos almacenados en UTC con la zona horaria original.
- Detección de superposición estricta — los eventos consecutivos nunca conflictúan.
- Política de conflicto de aviso o bloqueo (TC018).
- Resolución de gaps de DST para horas locales inexistentes (TC027).
- Recurrencia mensual día 31 con comportamiento de ajuste u omisión (TC005).

## Instalación

```bash
python -m venv .venv
.venv/Scripts/activate   # Windows
pip install -r requirements.txt
```

## Ejecución

```bash
pytest tests/ -v
```

## Requisitos

- Python 3.10+ (`zoneinfo`)
- pytest 8.3.4, python-dateutil 2.9.0, icalendar 5.0.13

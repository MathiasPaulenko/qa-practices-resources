# Guía de Debugging de Tests Flaky — Companion

Recurso companion de [Guía de Debugging de Tests Flaky: Un Enfoque Sistemático](https://qapractices.com/es/documentation/flaky-test-debugging-guide).

Proyecto pytest ejecutable que demuestra el flujo de detección de la sección de triage de la guía: ejecuciones en loop con pytest-repeat, orden aleatorio con pytest-randomly, y un marcador de cuarentena que saca los tests flaky del camino bloqueante sin perderlos.

## Contenido

- `tests/test_stable.py` — tests deterministas de control (marcador `stable`)
- `tests/test_counter_flaky.py` — flakiness por contador: falla cada 3ª ejecución, así `--count=6` siempre marca 2 iteraciones como `R` (rerun)
- `tests/test_order_dependency.py` — par con estado compartido que solo falla cuando `pytest-randomly` lo corre en el orden incorrecto
- `tests/test_quarantined.py` — test en cuarentena excluido de la suite bloqueante
- `pytest.ini` — registro de marcadores
- `requirements.txt` — pytest 8.4.1, pytest-repeat 0.9.4, pytest-randomly 3.16.0, pytest-rerunfailures 15.1

## Requisitos

- Python 3.10+
- `pip install -r requirements.txt`

## Uso

```bash
# La suite bloqueante verde — todo lo que no es flaky ni está en cuarentena
pytest -m "not flaky and not quarantined"

# Loop de detección: re-correr el test contador 6 veces — 2 iteraciones salen como R
pytest tests/test_counter_flaky.py --count=6

# Dependencia de orden: barajar hasta que test_b caiga antes que test_a
pytest tests/test_order_dependency.py
# anotá el --randomly-seed del encabezado para re-ejecutar un orden fallido

# Suite de cuarentena: revisar tests bajo investigación
pytest -m quarantined
```

## Qué enseña cada ejecución

- **`--count=N`** (pytest-repeat) mide la tasa de fallos — fallo intermitente es flakiness, fallo consistente es un bug real.
- **`pytest-randomly`** baraja el orden automáticamente; si los tests solo fallan barajados tenés estado compartido, no timing.
- **Marcadores como cuarentena** mantienen los tests flaky visibles (se siguen midiendo y ejecutando) sin dejar que bloqueen el pipeline — el flujo de las Estrategias de Prevención de la guía.

Mirá la guía para las categorías de causas raíz, la matriz de triage síntoma→arreglo y las cinco técnicas de debugging.

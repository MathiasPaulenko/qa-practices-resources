# Casos de Prueba: Geofencing y Alertas de Ubicación — Companion Ejecutable

Código companion de [Casos de Prueba: Geofencing y Alertas de Ubicación](https://qapractices.com/es/test-cases/geofencing-location-alert-test-cases/) en QAPractices.

## Qué hay aquí

`geofence.py` — primitivas solo-stdlib que espejan la lógica que una feature de geofencing real necesita:

- `haversine()` — distancia ortodrómica con wrap de antimeridiano (±180°).
- `CircleGeofence` — verificación de contención por radio.
- `point_in_polygon()` — ray-casting, para fences poligonales a nivel de app (el geofencing nativo del SO solo soporta círculos).
- `Debouncer` — suavizado de N fixes consecutivos contra falsas entradas por drift GPS.
- `DwellTimer` — entrada + intervalo, se resetea si sales antes.
- `CooldownFilter` — supresión de alertas por geofence.
- `simulate_drift()` — alimenta una secuencia de fixes al debouncer.

`tests/test_geofence.py` — 21 casos pytest mapeados al recurso:

| Caso del recurso | Cubierto por |
|---|---|
| TC-002 Entrada | `test_entry_inside_radius`, `test_boundary_inclusive` |
| TC-004 Dwell | `test_dwell_*` |
| TC-013 GPS drift | `test_drift_*`, `test_single_noisy_fix_suppressed` |
| TC-016 Radio mínimo | `test_tiny_radius_is_fragile` |
| TC-018 Antimeridiano | `test_haversine_antimeridian_wrap` |
| TC-021 Polos | `test_haversine_pole` |
| TC-022 Fence 100km | `test_haversine_large_geofence` |
| TC-024 Polígono | `test_point_*polygon*` |
| TC-029 Cooldown | `test_cooldown_*` |

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/ -q
```

Python 3.10+, sin dependencias externas salvo pytest.

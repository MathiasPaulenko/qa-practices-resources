# Testing de DLC de Juegos — Companion

Ejemplos ejecutables del [Checklist de Testing de DLC](https://qapractices.com/es/checklists/game-dlc-testing-checklist/).

## Archivos

| Archivo | Qué hace |
|---|---|
| `dlc-manifest.json` | Ejemplo de manifest de DLC: plataformas, regiones, versión base mínima y dependencias. |
| `manifest_validator_test.py` | Suite pytest que valida el manifest — campos requeridos, formato semver, listas de plataformas/regiones conocidas, sin auto-dependencias, exclusividad disjunta. |
| `entitlement_flow.py` | Simulación del bug clásico del reembolso: la tienda revoca el entitlement pero el flag de desbloqueo cacheado del juego sigue mostrando el contenido. |

## Ejecutar

```bash
pip install -r requirements.txt
pytest manifest_validator_test.py -v   # 7 tests de validación de manifest
python entitlement_flow.py             # mira el flag de desbloqueo stale sobrevivir un reembolso
```

## Qué demuestra

- **Validación de manifest más allá de "¿parsea?"** — formato de versión, plataformas/regiones conocidas y sanidad de dependencias son los bugs de config que realmente publican DLC roto.
- **El camino de revocación es el que no se prueba** — `entitlement_flow.py` muestra un juego que solo cachea el flag de desbloqueo: tras un reembolso, los jugadores conservan el contenido pago. El arreglo es re-verificar el entitlement al cargar.

# Testing de Sistemas Anti-Cheat — Companion

Comprobaciones de referencia del lado servidor usadas en el artículo
[Testing de Sistemas Anti-Cheat](https://qapractices.com/es/test-cases/anti-cheat-system-testing-test-cases/):

- `validate_move` — marca actualizaciones de posición más rápidas de lo que
  permite el modelo de física, con margen de jitter para no marcar a
  jugadores con latencia alta.
- `aim_snap_rate` — fracción de snaps de mira por debajo de un umbral
  humanamente plausible (métrica del TC-02).
- `bans_missing_evidence` — helper de auditoría equivalente a la consulta
  SQL del artículo: cada ban necesita score de confianza y enlace de
  replay (TC-07).

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/
```

Casos cubiertos: TC-01 (speed hack), el caso edge de latencia alta,
TC-02 (tasa de snap de aimbot) y TC-07 (auditoría de evidencia de bans).

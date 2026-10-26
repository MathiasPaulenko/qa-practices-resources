# Checklist de Auto-Update para Apps Desktop — Companion

Artefactos ejecutables para el [Checklist de Auto-Update para Apps Desktop](https://qapractices.com/es/checklists/desktop-app-auto-update-testing-checklist/) de QAPractices.

## Archivos

| Archivo | Propósito |
|---|---|
| `config/update_manifest.json` | Manifiesto de ejemplo del feed de updates (versión, mínima, url, firma, flag force) |
| `tests/version_check.py` | Helper de comparación semver: devuelve `force`, `available` o `none` |
| `scripts/feed_smoke.sh` | Smoke test con curl + jq que valida la forma del manifiesto del feed |
| `requirements.txt` | Dependencia de Python (`packaging`) |

## Uso

```bash
pip install -r requirements.txt
python tests/version_check.py
bash scripts/feed_smoke.sh https://tu-servidor-de-updates/latest.json
```

`update_manifest.json` replica la estructura que un updater de desktop consulta
antes de descargar un paquete — apuntá el feed URL de tu app hacia él (o a un
servidor estático local) para simular detección de updates, updates forzadas y
verificación de firma.

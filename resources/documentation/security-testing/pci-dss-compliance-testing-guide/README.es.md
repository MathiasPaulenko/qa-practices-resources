# Testing de Compliance PCI DSS — Kit de Controles Ejecutable

Companion de la [Guía de Testing de Compliance PCI DSS](https://qapractices.com/es/documentation/pci-dss-compliance-testing-guide/) en QAPractices. Chequeos pre-assessment que corrés antes del scan ASV y de la visita del QSA, empaquetados para que cada corrida produzca evidencia fechada para la carpeta de auditoría.

## Qué contiene

| Control | Req PCI DSS | Script |
|---|---|---|
| Barrido PAN — encuentra números de tarjeta válidos (Luhn) filtrados en logs, respuestas y dumps | 3 | `controls/pan_sweep.py` |
| Chequeo TLS — versión negociada + detección de ciphers débiles | 4 | `controls/tls_check.py` |
| Chequeo de segmentación — prueba que un segmento fuera de scope no alcanza el CDE | 11.4.5 | `controls/segmentation_check.py` |
| Paquete de evidencia — corre todos los chequeos y escribe `evidence/evidence-YYYYMMDD.json` | todos | `runner.py` |

Los chequeos usan solo la biblioteca estándar — corren en un jump host bloqueado sin instalar nada. `pytest` y `PyYAML` se necesitan para los tests y el runner con config.

## Inicio rápido

```bash
pip install -r requirements.txt

# Apuntá el barrido PAN a logs exportados o dumps de base
python -m controls.pan_sweep sample_logs/

# Sondá un endpoint que toca el CDE (reemplazá con tu host)
python -m controls.tls_check staging-cde.internal 443

# Corré desde un segmento fuera de scope — ningún puerto debe responder
python -m controls.segmentation_check cde-app-01.internal
```

## Paquete de evidencia

Editá `controls.yaml` con tus targets reales y después:

```bash
python runner.py --config controls.yaml
```

El resultado cae en `evidence/evidence-YYYYMMDD.json` — un archivo por corrida, fechado, con pass/fail por control y el detalle que un assessor muestrea. Corrélo la semana anterior a cada scan ASV trimestral y antes del assessment anual.

## Tests

```bash
pytest tests/ -v
```

La suite cubre el validador Luhn, la detección de PAN vs falsos positivos, las reglas pass/fail de TLS (protocolo débil, cipher débil, fallo de conexión) y la detección de segmentación contra puertos reales de localhost — no hace falta un CDE vivo.

## Qué no hace este kit

- **No** reemplaza el scan ASV trimestral — los scans externos tienen que venir de un Approved Scanning Vendor del PCI SSC.
- **No** reemplaza el penetration test anual.
- No audita acceso físico (req 9) ni artefactos de política (req 12) — eso queda manual.

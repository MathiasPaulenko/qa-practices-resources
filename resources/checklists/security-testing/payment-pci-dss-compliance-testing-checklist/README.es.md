# Checklist de testing de compliance PCI-DSS para pagos — Companion

Recursos companion de la checklist de QAPractices:
[Checklist de testing de compliance PCI-DSS para pagos](https://qapractices.com/es/checklists/payment-pci-dss-compliance-testing-checklist/)

Todos los ítems están alineados a **PCI DSS v4.0.1** (la versión vigente; la v4.0 quedó retirada el 31 de diciembre de 2024).

## Contenido

| Archivo | Propósito |
|---------|-----------|
| `checklist.csv` | Los 107 ítems en formato planilla — importá a Sheets/Excel/Jira y usá las columnas `status` y `evidence` durante la corrida. |
| `checklist.json` | Los mismos ítems en formato estructurado para tooling — filtrá por `section`, `requirement` o `risk`, o mandalos a un tracker. |
| `pan_log_check.py` | Escáner solo-stdlib que encuentra números de tarjeta de 13-19 dígitos válidos por Luhn en logs y volcados. Mapea al fallo real más común de la checklist: PAN filtrado a logs. |

## Uso

Trabajá la checklist en el formato que sirva a la corrida:

```bash
# abrir en planilla y completar evidencia/estado por ítem
checklist.csv

# listar todos los ítems de riesgo High para un release gate
python -c "import json; [print(i['item']) for i in json.load(open('checklist.json'))['items'] if i['risk']=='High']"
```

Escaneo de logs buscando PAN (exit code 1 si hay hallazgos — usable como gate de CI):

```bash
python pan_log_check.py /var/log/myapp/
python pan_log_check.py /var/log/myapp/ --quiet   # solo resumen
```

El escáner marca secuencias de dígitos válidas por Luhn. Las tarjetas de test conocidas (`4242…` de Stripe, etc.) se excluyen; tratá todo lo demás como un hallazgo del Req 3 hasta probar que es falso positivo.

## Notas

- Los números de requisito en `checklist.csv` citan PCI DSS v4.0.1 (p. ej., `Req 8.3.4` lockout, `Req 10.5.1` retención de logs, `Req 11.6.1` detección de manipulación en páginas de pago).
- Seis ítems de casos límite no mapean a un único requisito — verifican higiene general de pagos.
- Guardá evidencia por ítem (captura, salida de test, exportación de configuración) — es lo que el auditor muestrea.

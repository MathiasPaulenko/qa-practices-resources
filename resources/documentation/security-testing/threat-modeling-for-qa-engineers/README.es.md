# Threat Modeling para Ingenieros de QA — Archivos Companion

Modelo de amenazas PyTM 1.3 ejecutable para un servicio de checkout, igual al ejemplo de la guía [Threat Modeling para Ingenieros de QA](https://qapractices.com/es/documentation/threat-modeling-for-qa-engineers/).

## Archivos

- `threat_model.py` — modelo PyTM: tres límites de confianza (Internet, DMZ, Red Interna), flujo cliente → web app → API → base de pedidos, con `storesPII` marcado en el datastore para que el análisis STRIDE detecte amenazas de exposición de información.
- `requirements.txt` — versión fijada de `pytm`.

## Ejecutar

```bash
pip install -r requirements.txt

# Reporte de amenazas STRIDE (markdown)
python threat_model.py --report report.md

# Diagrama de flujo de datos (requiere Graphviz `dot` en el PATH)
python threat_model.py --dfd | dot -Tpng -o dfd.png
```

El reporte lista amenazas por elemento — cada fila mapea a una categoría STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege). El trabajo de QA: convertir cada amenaza de alto riesgo en un caso de test y mantener la trazabilidad del ID de amenaza en la suite.

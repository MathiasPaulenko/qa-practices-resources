# Guía de Testing XSS — Scripts y Payloads Companion

> Recurso companion de [Guía de Testing XSS: Reflected, Stored y DOM-Based](https://qapractices.com/es/documentation/cross-site-scripting-xss-testing-guide) en QAPractices.com.

Scripts, librería de payloads y workflow de CI para testear XSS reflected, stored y DOM-based con Python 3.12, OWASP ZAP 2.15 y dalfox 2.x.

## Requisitos

- Python 3.12+
- `requests` 2.32
- OWASP ZAP 2.15 (opcional, para scans automatizados)
- dalfox 2.x (opcional, para scanning por CLI)

## Setup

```bash
# Instalar dependencias de Python
pip install requests==2.32

# Opcional: instalar dalfox (requiere Go)
go install github.com/hahwul/dalfox/v2@latest

# Correr el probe de reflected XSS
python scripts/reflected_xss_probe.py --url https://staging.qa.local/search

# Correr el verificador de CSP
python scripts/csp_verifier.py --url https://staging.qa.local

# Correr dalfox contra un target
dalfox url "https://staging.qa.local/search?q=test" --blind https://xss-receiver.qa.local
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `scripts/reflected_xss_probe.py` | Script en Python para testear reflected XSS en un endpoint de búsqueda |
| `scripts/csp_verifier.py` | Verificar headers CSP y testear bloqueo de payloads |
| `scripts/stored_xss_probe.py` | Postear un payload y verificar que renderiza sin encoding al recuperarlo |
| `payloads/basic_probes.txt` | Payloads básicos de probe (alert, console.log) |
| `payloads/context_specific.txt` | Payloads específicos por contexto (HTML, JS, URL, DOM) |
| `payloads/filter_evasion.txt` | Payloads de evasión de filtros (nested tags, event handlers) |
| `.github/workflows/xss-regression.yml` | Workflow de CI para tests de regresión XSS |

## Librería de Payloads

El directorio `payloads/` contiene listas reutilizables organizadas por contexto:

- `basic_probes.txt` — payloads seguros y observables para confirmar ejecución
- `context_specific.txt` — payloads para contextos HTML, JavaScript, URL y DOM
- `filter_evasion.txt` — payloads para bypass de filtros comunes (nested tags, case variations, double encoding)

## Licencia

MIT — libre de usar, modificar y distribuir. Nunca testees XSS contra sistemas que no te pertenecen o para los que no tengas autorización explícita.

# Automatización de Pruebas Asistida por IA — Companion

Archivos companion para la [Guía de Automatización de Pruebas Asistida por IA](https://qapractices.com/es/documentation/ai-assisted-test-automation).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `src/self_healing.py` | Patrón de localizador con fallback: intenta el selector principal y luego alternativas estables en orden. |
| `tests/test_self_healing.py` | Suite pytest que verifica la lógica de sanación con un driver falso — sin navegador. |

## Requisitos

- Python 3.10+
- selenium 4.x
- pytest 8.3+

## Uso

1. Instala las dependencias: `pip install -r requirements.txt`.
2. Corre `pytest tests/ -v` — el driver falso ejercita el hit primario, el orden de fallbacks y el caso donde todo falla.
3. En una suite real, reemplaza `FakeDriver` por tu instancia de WebDriver y registra qué fallback se disparó para que un humano lo revise después.

## Integración en CI

```yaml
- run: pip install -r requirements.txt && pytest tests/ -v --tb=short
```

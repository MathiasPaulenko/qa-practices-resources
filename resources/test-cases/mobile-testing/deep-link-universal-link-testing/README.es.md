# Casos de Test de Deep Links y Universal Links — Companion

> Repositorio companion para [10 Casos de Test de Deep Links y Universal Links](https://qapractices.com/es/test-cases/deep-link-universal-link-testing/)

## Requisitos

- Python 3.10+
- Appium 2.5
- ADB 35 (Android SDK 35)
- Xcode 16 (para Simulador iOS)
- pytest 8.3
- Un servidor de Appium corriendo en `http://localhost:4723`
- Una app de test con package `com.qapractices.shop` instalada en el dispositivo/emulador

## Setup

```bash
pip install pytest==8.3 appium-python-client
appium  # iniciar el servidor de Appium en otra terminal
```

## Ejecutar los tests

```bash
# Correr todos los tests (requiere dispositivo/emulador Android)
pytest test_deep_links.py -v

# Correr solo los tests de links malformados
pytest test_deep_links.py::TestMalformedDeepLink -v

# Correr con reporte JSON
pytest test_deep_links.py -v --json-report
```

## Archivos

| Archivo | Propósito |
| --------- | ----------- |
| `deep_link_utils.py` | Helpers para disparar deep links vía ADB, simctl y Appium |
| `conftest.py` | Fixtures de pytest para drivers de Appium Android e iOS |
| `test_deep_links.py` | Casos de test TC-001 a TC-010 |
| `meta.json` | Metadata del recurso |

## Cobertura de tests

| Clase de test | TC | Descripción |
| ---------------- | ---- | ------------- |
| `TestDeepLinkBasic` | TC-001 | Deep link básico con app instalada |
| `TestDeepLinkParameters` | TC-002 | Parseo de parámetros de query y path |
| `TestDeepLinkAuth` | TC-004 | Redirect a pantalla autenticada después del login |
| `TestDeepLinkBackground` | TC-005 | Navegación desde background resume |
| `TestMalformedDeepLink` | TC-010 | Manejo de links malformados |
| `TestAndroidADBDirect` | TC-001/007 | Launch directo con ADB sin Appium |

## Licencia

MIT — Mathias Paulenko

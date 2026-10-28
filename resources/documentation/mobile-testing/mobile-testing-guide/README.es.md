# Guía de Pruebas Móviles — Companion

Companion ejecutable para la [Guía de Pruebas de Apps Móviles](https://qapractices.com/es/documentation/mobile-testing-guide/) de QAPractices.

Implementa las dos piezas que no caben en un artículo: una matriz de dispositivos que puedes rellenar desde tu analytics, y los comandos de smoke test para ambas plataformas.

## Archivos

- `device-matrix.csv` — plantilla de selección Tier 1/2/3: modelo, versión de OS, cuota de audiencia, responsable, cadencia de pruebas. Reemplaza las filas de ejemplo con tus top devices del analytics.
- `run-smoke-tests.sh` — runner de humo para ambos stacks: Espresso en emulador Android y XCUITest en simulador iOS, con variables de entorno para la clase de test/esquema.

## Ejecutar

```bash
# Android (necesita un emulador corriendo o dispositivo conectado)
./run-smoke-tests.sh android

# iOS (necesita un simulador arrancado)
./run-smoke-tests.sh ios
```

Requiere un proyecto Android con `connectedDebugAndroidTest` configurado o un esquema Xcode con tests de UI — mira la guía para qué pertenece a una suite de humo.

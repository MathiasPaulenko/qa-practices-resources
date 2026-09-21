# Allure vs Extent Reports — Companion

Companion de [Allure vs Extent Reports: Comparativa de Reporting](https://qapractices.com/es/documentation/allure-vs-extent-reports/) en QAPractices.

El mismo escenario de login (credenciales válidas + cuenta bloqueada) está implementado dos veces para comparar el coste de setup, el formato de salida y el cableado en CI lado a lado:

| Carpeta | Herramienta | Salida |
|---|---|---|
| `allure/` | `allure-pytest` 2.x + Allure CLI | app web `allure-report/` (requiere `allure generate`/`serve` o hosting) |
| `extent/` | ExtentReports 5.1.2 + JUnit 5 (Maven) | `extent-report.html` archivo único autocontenido |
| `ci/` | GitHub Actions | Publica ambos formatos como artefactos del build |

## Ejecutar el ejemplo de Allure

```bash
cd allure
pip install -r requirements.txt
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure serve allure-results   # vista previa en vivo
```

Copia `categories.json` dentro de `allure-results/` antes de `allure generate` para ver las categorías de fallo personalizadas (defectos de producto vs defectos de test vs problemas de infraestructura).

## Ejecutar el ejemplo de ExtentReports

```bash
cd extent
mvn test
# abre extent/build/reports/extent-report.html
```

## Qué comparar

- **Coste de setup**: Allure necesita un CLI más un adapter por framework; Extent es una dependencia dentro del JVM.
- **Historial**: conserva `allure-results/history/` entre ejecuciones para tendencias; Extent necesita el servidor KLOV auto-hospedado.
- **Distribución**: el HTML de Extent se adjunta a un correo o ticket; el reporte de Allure necesita `allure serve` o hosting.
- **Mantenimiento**: ExtentReports está en sunset (última release 5.1.2, junio 2024) en favor de ChainTest; Allure 3.x está en desarrollo activo.

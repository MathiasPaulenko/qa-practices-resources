# Pruebas WCAG 2.2 AA vs AAA — Ejemplos ejecutables

Repositorio companion de la guía de QAPractices
[Diferencias de Pruebas entre WCAG 2.2 AA y AAA](https://qapractices.com/es/documentation/wcag-22-aa-vs-aaa-testing-differences/)
([English version](https://qapractices.com/documentation/wcag-22-aa-vs-aaa-testing-differences/)).

Los ejemplos escanean la misma página en ambos niveles de conformidad para
medir el delta real entre una puerta AA y un barrido AAA.

## Estructura

```text
playwright/   @axe-core/playwright 4.14.0 + @playwright/test 1.63.0
pa11y/        script de shell con pa11y 10.0.0 (WCAG2AA frente a WCAG2AAA)
```

## Playwright — división por etiquetas de regla

```bash
cd playwright
npm install
BASE_URL=https://staging.qapractices.com npx playwright test
```

La configuración usa `channel: 'chrome'`: ejecuta tu Chrome instalado, sin
descargar navegadores. Para CI, quita la opción `channel` y ejecuta
`npx playwright install chromium` para usar el navegador empaquetado.

Tres specs cubren: la puerta AA (etiqueta `wcag22aa`, fallo duro ante
violaciones), el barrido AAA (etiqueta `wcag2aaa`, solo reporte) y un pase
enfocado a `color-contrast-enhanced` —la regla que convierte el 4.5:1 en 7:1 y
genera la mayor parte del ruido del primer escaneo.

## pa11y — ambos estándares en una corrida

```bash
BASE_URL=https://staging.qapractices.com ./pa11y/run-audit.sh /checkout
```

Escribe `aa-report.json` y `aaa-report.json`, e imprime el recuento de issues
por nivel y el número de códigos de regla exclusivos de AAA. Ejecútalo antes y
después de corregir los tokens de contraste para ver cómo caen los hallazgos
de contraste mejorado.

## Notas

- Las etiquetas de regla de axe no son conformidad: un escaneo `wcag2aaa`
  vacío es evidencia de parte de una declaración, no una prueba de AAA. El
  nivel de lectura (3.1.5), la pronunciación (3.1.6), la ayuda contextual
  (3.3.5) y la lengua de signos (1.2.6) requieren revisión humana.
- Mantén el pase AAA sin bloqueo hasta completar el primer triage: el
  contraste mejorado por sí solo inunda un escaneo inicial.

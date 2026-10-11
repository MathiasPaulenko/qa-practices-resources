# Cómo Manejar Elementos Dinámicos en Selenium — Companion

Recurso companion de [Cómo Manejar Elementos Dinámicos en Selenium](https://qapractices.com/es/documentation/handle-dynamic-elements-selenium/).

Ejemplos ejecutables de Selenium 4 (Java + Python) que cubren todos los patrones de la guía — explicit waits, `ExpectedConditions`, condiciones personalizadas, FluentWait, IDs dinámicos, contenido AJAX, dropdowns custom, iframes y shadow DOM nativo — corriendo contra fixtures HTML locales, así que nada depende de un sitio en vivo.

## Requisitos

- Chrome + ChromeDriver en PATH (o deja que Selenium Manager lo resuelva).
- Java 17+ con Maven, **o** Python 3.10+.

## Correr la suite Java

```bash
cd java
mvn test
```

## Correr la suite Python

```bash
cd python
pip install -r requirements.txt
python -m pytest -v
```

## Qué hay dentro

| Ejemplo | Qué demuestra |
|---|---|
| `dynamicId_*` | IDs generados; `data-testid` vs `button[id^='btn_']` + `elementToBeClickable` |
| `ajaxContent_*` | Esperar a que el spinner desaparezca y luego a la lista de resultados |
| `dynamicDropdown_*` | Click-luego-espera para un dropdown custom (no `<select>`) |
| `shadowDom_*` | `getShadowRoot()` / `element.shadow_root` nativo en Selenium 4 |
| `customWait_*` | Condición lambda que espera a que la clase pase a `active` |
| `fluentWait_*` (Java) | Intervalo de polling propio, ignorando `NoSuchElementException` |
| `iframe_*` | `switchTo().frame()`, interactuar, volver con `defaultContent()` |

Los fixtures están en `fixtures/`: `dynamic-page.html` reproduce IDs generados, AJAX con retardo, un dropdown custom, un shadow root y una clase que cambia tras cargar; `iframe-page.html` incrusta un frame inline con `srcdoc`.

Versiones: Selenium 4.25.0 (Java por Maven, Python por `requirements.txt`), JUnit 5.11, pytest 8.3.

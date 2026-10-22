# Checklist de Testing Funcional — Companion Ejecutable

Las piezas ejecutables detrás del [Checklist de Testing Funcional](https://qapractices.com/es/checklists/functional-testing-checklist/) de QAPractices: los 139 ítems como CSV legible por máquina con marcas de riesgo, un fixture HTML de formulario de login para ejercitar checks de frontera y negativos, una spec Playwright y un test de contrato pytest sobre una respuesta API incluida.

## Contenido

| Archivo | Qué es |
|---|---|
| `checklist-items.csv` | Los 139 ítems del checklist (`id`, `area`, `item`, `risk`) — importalo a tu tracker o pasalo a un script de triage. |
| `login-form.html` | Fixture sin dependencias con hooks `data-testid`: email, contraseña, edad con validación mínimo-18, y botones login/save. |
| `functional.spec.ts` | Spec Playwright 1.48: check de frontera del campo edad y login feliz con credenciales vía `TEST_USER_EMAIL` / `TEST_USER_PASSWORD`. |
| `fixtures/profile-response.json` | Respuesta API de muestra usada por el test de contrato. |
| `tests/test_contract.py` | Checks pytest 8.3: forma de la respuesta, completitud del CSV y cobertura de riesgo, testids del fixture. |

## Correr la suite pytest

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada:

```text
tests/test_contract.py::test_profile_response_shape PASSED
tests/test_contract.py::test_checklist_csv_is_complete_and_risk_tagged PASSED
tests/test_contract.py::test_login_form_fixture_has_required_testids PASSED
3 passed
```

## Correr la spec Playwright (opcional)

```bash
npm i -D @playwright/test
npx playwright install chromium
TEST_USER_EMAIL=qa_ana@test.local TEST_USER_PASSWORD=ChangeMe123! \
  npx playwright test functional.spec.ts
```

La spec carga `login-form.html` relativo a este directorio — apuntá `baseURL` o `page.goto` a un servidor local (p. ej. `python -m http.server`) al correrla.

## Usar el CSV

Cada fila es una casilla del artículo, marcada `High`, `Medium` o `Low`. Filtrá `risk=High` para un barrido que bloquea el release, o agrupá por `area` para acotar una regresión a las secciones que el cambio tocó — la misma lógica de triage que describe el artículo.

## Referencias cruzadas

- Artículo fuente: <https://qapractices.com/es/checklists/functional-testing-checklist/> · [EN version](https://qapractices.com/checklists/functional-testing-checklist/)
- Formato entregable: el artículo enlaza el [bundle template de testing funcional](https://qapractices.com/es/templates/functional-testing-checklist-bundle/) para contextos de entrega.

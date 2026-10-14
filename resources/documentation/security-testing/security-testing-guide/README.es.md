# Guía de Pruebas de Seguridad — Companion ejecutable

Repositorio companion de la guía de QAPractices
[Guía de Pruebas de Seguridad: OWASP Top 10 y Escaneos ZAP](https://qapractices.com/es/documentation/security-testing-guide/)
([English version](https://qapractices.com/documentation/security-testing-guide/)).

Autocontenido: la API mock es un fixture `http.server` de stdlib, así que los
tests de BOLA corren sin ningún servicio externo. Los archivos de ZAP se
conectan a una ejecución real de `zap-baseline.py` cuando tengas una URL de
staging.

## Estructura

```text
mock_api.py            API fixture de stdlib: auth por token + dos órdenes, acceso solo del dueño
tests/test_bola.py     suite de regresión BOLA con pytest 8.2 (4 tests)
zap/zap-baseline.conf  política de reglas para `zap-baseline.py -c` (ZAP 2.15.0)
zap/parse_baseline.py  parser del informe en stdlib: sale con código 1 ante alertas HIGH
requirements.txt       requests 2.31.0, pytest 8.2.0
```

## Ejecutar la suite BOLA

```bash
python -m venv venv
source venv/bin/activate    # venv\Scripts\activate en Windows
pip install -r requirements.txt
pytest tests/test_bola.py -v
```

`mock_api.py` se levanta dentro del fixture de pytest en un puerto efímero.
La orden 42 pertenece a alice — la suite verifica que el token de bob no
puede leerla (`403`), que un token ausente o manipulado es rechazado (`401`)
y que la dueña sí puede leer su propia orden (`200`).

## Ejecutar el baseline de ZAP

```bash
docker pull zaproxy/zap-stable:2.15.0
docker run -v $(pwd):/zap/wrk:rw -t zaproxy/zap-stable:2.15.0 \
  zap-baseline.py -t https://staging.example.internal \
  -r zap-baseline-report.html -w zap-baseline.md -c zap-baseline.conf
python zap/parse_baseline.py zap-baseline.md
```

Escanea siempre un entorno que no sea producción y con autorización escrita.
`parse_baseline.py` devuelve código de salida 1 cuando el informe lista alguna
alerta HIGH, así que puede controlar un paso de pipeline directamente.

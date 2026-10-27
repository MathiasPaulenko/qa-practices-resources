# Mejores Herramientas de API Testing — Companion

Fixtures para [Mejores Herramientas de Pruebas de API para QA](https://qapractices.com/es/documentation/best-api-testing-tools/). La API mock se ejecuta localmente; el ejemplo no envía requests a un servicio público.

## Contenido

| Archivo | Propósito |
|---|---|
| `decision-matrix.csv` | Selección breve por flujo del equipo, categoría, encaje y trade-off |
| `scripts/mock_api.py` | API fixture con Python 3.12+ y biblioteca estándar en `127.0.0.1:8080` |
| `postman/api-smoke.postman_collection.json` | Colección Postman v2.1 con un health check y assertions |
| `postman/local.postman_environment.json` | Variable `baseUrl` local para la colección |

## Ejecutar el ejemplo

En una terminal, inicia el mock local:

```bash
python3 scripts/mock_api.py
```

En otra terminal, desde este directorio, ejecuta la colección con Newman 6.x:

```bash
npx --yes newman@6 run postman/api-smoke.postman_collection.json \
  --environment postman/local.postman_environment.json \
  --reporters cli,junit \
  --reporter-junit-export newman-api-smoke.xml
```

La colección comprueba `GET /v1/health` para HTTP 200 y `{"status":"ok"}`. Detén el mock con Ctrl+C. Guarda credenciales reales en los secrets de CI; este fixture no necesita ninguna.

English guide: [README.md](README.md)

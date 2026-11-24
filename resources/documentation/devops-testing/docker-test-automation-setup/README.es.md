# Configuración de Docker para Automatización — Companion

Archivos ejecutables de la guía [Cómo Configurar Docker para Automatización de Pruebas](https://qapractices.com/es/documentation/docker-test-automation-setup/).

## Archivos

- `src/docker-compose.test.yml` — stack de app + Postgres 16 (health check) + runner de tests.
- `src/Dockerfile.test` — imagen de test multi-stage (objetivos test, lint, unit).
- `src/docker-compose.selenium.yml` — hub de Selenium Grid 4.27 con nodos Chrome y Firefox.
- `src/spin-up-test-env.sh` — corre la suite y siempre elimina los volúmenes.
- `src/ci-docker-tests.yml` — workflow de GitHub Actions conectado al stack de Compose.

## Uso

```bash
chmod +x src/spin-up-test-env.sh
./src/spin-up-test-env.sh
```

O directo con Compose:

```bash
docker compose -f src/docker-compose.test.yml up --abort-on-container-exit --exit-code-from tests
docker compose -f src/docker-compose.test.yml down -v
```

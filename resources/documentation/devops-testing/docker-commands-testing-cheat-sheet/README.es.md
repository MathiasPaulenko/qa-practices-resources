# Comandos Docker para Testers — Companion

Archivos ejecutables del [Cheat Sheet de Comandos Docker para Testers](https://qapractices.com/es/documentation/docker-commands-testing-cheat-sheet/) en QAPractices.com.

## Contenido

| Archivo | Qué es |
|---|---|
| `src/docker-compose.test.yml` | Stack de test: app + Postgres 16 con healthcheck + Selenium Chrome |
| `src/Dockerfile.test` | Build multi-stage que produce una imagen test-runner |
| `src/spin-up-test-env.sh` | Postgres desechable con espera `pg_isready` — sin sleeps fijos |
| `src/cleanup.sh` | Elimina contenedores e imágenes de test por filtro de nombre/referencia |

## Uso

```bash
chmod +x src/*.sh
./src/spin-up-test-env.sh          # Postgres listo en :5432
docker compose -f src/docker-compose.test.yml up -d
./src/cleanup.sh                    # limpiar recursos de test
```

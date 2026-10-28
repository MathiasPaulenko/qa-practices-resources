# Plantilla de Configuración de Selenium Grid — Companion

Companion ejecutable de la [Plantilla de Configuración de Selenium Grid](https://qapractices.com/es/templates/selenium-grid-configuration-template/) de QAPractices.

## Archivos

- `docker-compose.yml` — hub de Selenium Grid 4 más nodos de Chrome, Firefox y Edge (`selenium/*:4.47.0`), con puertos de event bus, límites de sesiones y `shm_size` para ejecuciones estables.
- `grid-health-check.sh` — consulta `/status` hasta que el grid reporta ready y lista los nodos registrados.

## Uso

```bash
docker compose up -d
./grid-health-check.sh http://localhost:4444 60
```

Apuntá tus tests a `http://localhost:4444` con `webdriver.Remote` y bajá todo con `docker compose down` al terminar. Para escalar un navegador, sumá otro servicio de nodo o `deploy.replicas`.

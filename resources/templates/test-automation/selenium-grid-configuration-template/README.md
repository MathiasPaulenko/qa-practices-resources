# Selenium Grid Configuration Template — Companion

Runnable companion for the [Selenium Grid Configuration Template](https://qapractices.com/templates/selenium-grid-configuration-template/) on QAPractices.

## Files

- `docker-compose.yml` — Selenium Grid 4 hub plus Chrome, Firefox, and Edge nodes (`selenium/*:4.47.0`), with event bus ports, session limits, and `shm_size` sized for stable runs.
- `grid-health-check.sh` — polls `/status` until the grid reports ready and lists the registered nodes.

## Usage

```bash
docker compose up -d
./grid-health-check.sh http://localhost:4444 60
```

Point your tests at `http://localhost:4444` with `webdriver.Remote`, then tear down with `docker compose down` when finished. Scale a browser by adding another node service or `deploy.replicas`.

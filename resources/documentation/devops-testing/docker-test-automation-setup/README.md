# Docker Test Automation Setup — Companion

Runnable files from the guide [How to Set Up Docker for Test Automation](https://qapractices.com/documentation/docker-test-automation-setup/).

## Files

- `src/docker-compose.test.yml` — app + Postgres 16 (health check) + test runner stack.
- `src/Dockerfile.test` — multi-stage test image (test, lint, unit targets).
- `src/docker-compose.selenium.yml` — Selenium Grid 4.27 hub with Chrome and Firefox nodes.
- `src/spin-up-test-env.sh` — runs the suite and always tears down volumes.
- `src/ci-docker-tests.yml` — GitHub Actions workflow wired to the Compose stack.

## Usage

```bash
chmod +x src/spin-up-test-env.sh
./src/spin-up-test-env.sh
```

Or run Compose directly:

```bash
docker compose -f src/docker-compose.test.yml up --abort-on-container-exit --exit-code-from tests
docker compose -f src/docker-compose.test.yml down -v
```

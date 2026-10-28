# Cheat Sheet de Elementos de JMeter — Companion

Companion ejecutable para el [Cheat Sheet de Elementos de JMeter](https://qapractices.com/es/documentation/jmeter-elements-cheat-sheet/) de QAPractices.

Implementa los tres patrones del cheat sheet en un solo plan (JMeter 5.6.3):

1. **Login una vez, reutilizar el token** — `Once Only Controller` + `JSON Extractor` → `${authToken}` inyectado por `HTTP Header Manager`.
2. **Usuarios desde CSV** — `CSV Data Set Config` alimenta `${username}`/`${password}` desde `users.csv`.
3. **Think time realista** — `Uniform Random Timer` entre requests.

## Archivos

- `login-token-pattern.jmx` — el plan (10 threads, ramp-up de 30s, 5 loops; host placeholder `staging.example.com` — pon tu URL de staging en `HTTP Request Defaults`).
- `users.csv` — credenciales de ejemplo; el plan lee `${username}`/`${password}` de ahí.
- `run-load-test.sh` — ejecutor headless: `jmeter -n -t login-token-pattern.jmx -l results.jtl -e -o report/`.

## Ejecutar

```bash
./run-load-test.sh          # o: jmeter -n -t login-token-pattern.jmx -l results.jtl -e -o report/
```

Requiere JMeter 5.6.3+ en el PATH. Abre `report/index.html` para ver el dashboard.

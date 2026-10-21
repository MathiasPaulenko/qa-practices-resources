# Testing Dependiente del Tiempo — Companion Ejecutable

Companion de [Cómo Probar Funcionalidades Dependientes del Tiempo](https://qapractices.com/es/documentation/time-dependent-testing/) / [English version](https://qapractices.com/documentation/time-dependent-testing/).

`time-testing.mjs` implementa los primitivos que describe la guía, sin dependencias:

- **`makeFakeClock`** — un reloj avanzado a mano; la unidad de la que debería depender todo test de tiempo.
- **`TtlCache`** — caché TTL con semántica de límite exacto: expiración absolute a insert + TTL, sliding renovada en cada lectura.
- **`shouldRunCronOnDate`** — la regla cron de fin de mes: el día 30 nunca dispara en febrero, el 31 nunca en meses cortos, el 29 solo en febreros bisiestos.
- **`remainingBudget`** — propagación de deadline: las llamadas anidadas reciben el presupuesto restante, no un timeout fresco.
- **`findDstFold`** — detección real del fold de DST: barre instantes UTC contra el reloj de pared de `America/New_York` y devuelve los dos instantes donde las `01:30` ocurren dos veces el domingo de retroceso.

## Ejecución

```bash
node --test tests/time-testing.test.mjs
```

Requisitos: Node.js 20+, solo biblioteca estándar.

## Qué demuestra

| Concepto | Dónde |
|---|---|
| Inyectar el reloj, nunca `Date.now()` en la lógica | `makeFakeClock` |
| Expirar exactamente en el TTL — T+3599 vs T+3600 | `TtlCache` + tests |
| Expiración sliding vs absolute | opción `sliding` de `TtlCache` |
| Cron día-del-mes salta meses cortos | `shouldRunCronOnDate` |
| Los deadlines propagan el presupuesto restante | `remainingBudget` |
| El fold de DST es real y testeable | `findDstFold` (2026-11-01, `America/New_York`) |

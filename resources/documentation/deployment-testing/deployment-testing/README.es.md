# Pruebas de Deployment — Companion

Scripts ejecutables para la [Guía de Pruebas de Deployment](https://qapractices.com/es/documentation/deployment-testing/) de QAPractices.

## Scripts

### `scripts/post-deploy-smoke.sh`

Smoke test post-deploy que verifica los **bodies** de las respuestas, no solo los códigos de estado — un 200 sirviendo un build viejo es un falso verde. Comprueba el marcador de health, la emisión real de un token y una llamada autenticada; opcionalmente verifica que la versión desplegada coincida con `EXPECTED_VERSION`.

```bash
SMOKE_EMAIL=smoke@acme-corp.test SMOKE_PASSWORD=*** \
  ./scripts/post-deploy-smoke.sh https://staging.acme-corp.test
```

### `scripts/rollback-drill.sh`

Ensayo de rollback cronometrado. Ejecuta tu `ROLLBACK_CMD`, sondea hasta que el servicio vuelve a estar healthy y falla si el tiempo de recuperación supera el presupuesto — ese presupuesto es el piso de duración de tus incidentes.

```bash
ROLLBACK_CMD='kubectl rollout undo deploy/api -n prod' \
  ./scripts/rollback-drill.sh https://staging.acme-corp.test 120
```

## Requisitos

- `bash`, `curl`, `jq` 1.6+
- Una cuenta de pruebas dedicada para smoke (variables de entorno, nunca commiteada)
- Para el drill: un comando de rollback funcional para tu stack (`kubectl rollout undo`, Argo Rollouts, `helm rollback`, el job de revert de tu pipeline)

## Códigos de salida

| Código | Significado |
|--------|-------------|
| 0 | Las verificaciones pasan |
| 1 | Error de uso o endpoint inalcanzable |
| 2 | Una verificación falló / presupuesto excedido |

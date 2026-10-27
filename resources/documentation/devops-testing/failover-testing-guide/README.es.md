# Guía de Failover Testing — Companion

Artefactos ejecutables para la [Guía de Failover: Alta Disponibilidad y Disaster Recovery](https://qapractices.com/es/documentation/failover-testing-guide/). Cada archivo corresponde a un ejemplo de la guía para que puedas correr los mismos chequeos en tus propios simulacros.

## Archivos

| Archivo | Propósito |
| --- | --- |
| `litmus/chaosengine-pod-delete.yaml` | `ChaosEngine` de LitmusChaos 3.x que borra un pod aleatorio del deployment `payments` — el test de failover automatizado de la guía. |
| `postgres/replication-lag.sql` | Query de `pg_stat_replication` que mide el lag de la réplica en bytes en PostgreSQL 15+ — ejecutala en el primario antes y durante el simulacro. |
| `scripts/lb-healthcheck-poll.sh` | Sondea el balanceador cada 2s mientras terminás un backend; cuenta y marca cada respuesta que no sea 200. |
| `scripts/dr-drill-runbook.sh` | Esqueleto de simulacro de DR cronometrado: restaura, despliega, espera al health check, corre smoke tests y reporta el tiempo real vs el RTO. |

## Requisitos

- LitmusChaos 3.x instalado en el cluster + ServiceAccount `litmus-admin` (para el ChaosEngine)
- PostgreSQL 15+ con una réplica en streaming (para la query de lag)
- `bash` y `curl` (para los scripts)

## Uso

### Pod-delete con LitmusChaos

```bash
kubectl apply -f litmus/chaosengine-pod-delete.yaml
kubectl get chaosresult payments-pod-delete-pod-delete -n litmus
```

### Lag de replicación

```bash
psql -h primary.db.internal -U readonly -d appdb -f postgres/replication-lag.sql
```

### Sondeo del balanceador

```bash
BASE_URL=https://staging.qapractices.com/health ./scripts/lb-healthcheck-poll.sh
# En otra terminal, terminá una instancia backend y mirá la salida.
# Ctrl+C imprime el total de requests y cuántas no fueron 200.
```

### Runbook de simulacro DR

```bash
BACKUP_FILE=/backups/latest.dump TARGET_ENV=dr-restore ./scripts/dr-drill-runbook.sh
```

Reemplazá los comandos placeholder en `dr-drill-runbook.sh` por tus comandos reales de restauración, deploy y smoke tests — el script cronometra la recuperación real para compararla contra tu objetivo RTO.

## Relacionados

- Guía: <https://qapractices.com/es/documentation/failover-testing-guide/>
- English guide: <https://qapractices.com/documentation/failover-testing-guide/>

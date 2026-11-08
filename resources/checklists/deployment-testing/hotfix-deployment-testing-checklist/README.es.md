# Checklist de Hotfix Deployment — Companion

Scripts ejecutables para el [Checklist de Hotfix Deployment](https://qapractices.com/es/checklists/hotfix-deployment-testing-checklist/) de QAPractices.

## Scripts

### `scripts/hotfix-scope-check.sh`

Verifica que la rama del hotfix contiene **solo el fix** — un commit sobre el tag de producción. Falla si la rama se cortó desde la base equivocada o trae commits de más.

```bash
./scripts/hotfix-scope-check.sh v1.2.3 hotfix/1.2.4
```

### `scripts/post-deploy-verify.sh`

Verifica que el hotfix de verdad aterrizó: endpoint alcanzable, campo `version` que coincide con el build desplegado y latencia dentro del baseline. Un health check en verde sobre el artefacto viejo es el falso positivo más común en la verificación de hotfixes — este script revisa la versión, no solo el status.

```bash
./scripts/post-deploy-verify.sh https://api.acme-corp.test/health 1.2.4-hotfix
```

## Requisitos

- `bash`, `curl`, `jq`
- `git` (para el scope check)

## Códigos de salida

| Código | Significado |
|--------|-------------|
| 0 | Todas las verificaciones pasan |
| 1 | Error de uso o endpoint inalcanzable |
| 2 | Verificación falló — arrancá el reloj del rollback |

# Casos de Prueba Multi-Tenancy — Companion

Recurso companion de [Casos de Prueba Multi-Tenancy: Aislamiento y SaaS](https://qapractices.com/es/test-cases/multi-tenancy-test-cases/).

## Contenido

- `mock_server.py` — API multi-tenant stdlib. Dos tenants (`acme`, `globex`), JWT base64 fake con claim `tenant`, resolución por header `X-Tenant-ID`, scoping de objetos estilo RLS, flag de tenant suspendido y un cache compartido con una key sin namespace a propósito.
- `tests/conftest.py` — levanta el mock en un puerto efímero; fixtures `token_a` / `token_b`.
- `tests/test_tenant_isolation.py` — resolución de tenant (claim, header, mismatch, malformado, desconocido), IDOR con 403 uniforme (sin enumeración), la caza de la key sin namespace y el swap de contexto bajo concurrencia.
- `requirements.txt` — pytest 8.3 + requests.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
cd resources/test-cases/security-testing/multi-tenancy-test-cases
pytest tests/ -v
```

Corré el mock standalone para sondas manuales:

```bash
python mock_server.py 8571
curl -H "Authorization: Bearer $(python -c 'from mock_server import fake_jwt; print(fake_jwt("acme"))')" http://127.0.0.1:8571/api/me
curl -H "Authorization: Bearer $(python -c 'from mock_server import fake_jwt; print(fake_jwt("globex"))')" http://127.0.0.1:8571/api/orders/A-order-7781   # 403 — sonda IDOR
curl http://127.0.0.1:8571/api/me                                                                                                                        # 401 — sin contexto de tenant
```

## Qué cubre

- Resolución de tenant por claim JWT y header `X-Tenant-ID`; mismatch header/claim rechazado.
- Acceso cross-tenant a objetos (IDOR) con 403 uniforme — los IDs no son enumerables.
- Tenants suspendidos pierden acceso a mitad de sesión (edge de lifecycle).
- Auditoría de namespace de cache — una key sin namespace intencional para cazar.
- Requests concurrentes alternando tokens — el contexto de tenant no debe swappear.

# Casos de Prueba de Upload a Cloud Storage — Companion

Mock ejecutable de la API multipart de CloudBin usada en el artículo
[Casos de Prueba de Upload a Cloud Storage](https://qapractices.com/es/test-cases/cloud-storage-upload-test-cases/):

- `multipart_store.py` — modelo en memoria de la semántica multipart que
  ejercita la suite: expiración de sesiones, deduplicación de chunks por
  ETag, progreso del lado del servidor, cuotas y ensamblado en `complete`.
- `cloudbin_mock_server.py` — wrapper sobre `http.server` de la stdlib que
  expone los mismos endpoints REST de los ejemplos curl
  (`POST /files/multipart`, `PUT /chunks/{n}`, `GET /progress`,
  `POST /complete`, `GET /files/{id}`).
- `tests/test_multipart_upload.py` — suite pytest que cubre integridad
  chunked, reanudación desde el último chunk confirmado, chunks faltantes
  y duplicados, límites de cuota, extensiones bloqueadas, nombres con path
  traversal, monotonía del progreso y expiración de sesión.

## Ejecutar

```bash
pip install -r requirements.txt
pytest tests/
```

Para probar la API a mano, corre `python cloudbin_mock_server.py --port 8080`
y usa los ejemplos curl del artículo contra `http://127.0.0.1:8080`
en lugar de `https://api.cloudbin.io/v1`.

Casos cubiertos: TC-004/TC-005/TC-007 (integridad y progreso por chunks),
TC-012 (extensión bloqueada), TC-024 (reanudación), TC-028 (límite de
cuota) y la tabla edge (sesión obsoleta, fallo silencioso de `complete`,
chunk duplicado, path traversal).

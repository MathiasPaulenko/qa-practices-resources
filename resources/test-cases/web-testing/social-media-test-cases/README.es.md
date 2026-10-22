# Casos de Prueba de Redes Sociales — Companion

Recurso companion de [Casos de Prueba de Redes Sociales: Posts y Feed](https://qapractices.com/es/test-cases/social-media-test-cases/).

## Contenido

- `social_feed.py` — modelo en Python stdlib de la máquina de estados del feed: `SocialFeed` como fuente de verdad con alcances de visibilidad (público / seguidores / privado / perfil privado), likes idempotentes, carreras de comentario-sobre-borrado (`PostGone`), follow/unfollow/solicitudes de amistad, bloqueo bidireccional, mute silencioso, posts ocultos, dedup de reportes, hilos de DM y búsqueda consciente del alcance.
- `feed.html` — fixture estático que implementa el contrato del botón de like + formulario de comentario para verificación manual y con Playwright: like deduplicado por flag de evento, manejo de 410/404 cuando el post desaparece a mitad del comentario. Ábrelo en cualquier navegador.
- `tests/conftest.py` — pone el modelo en `sys.path`.
- `tests/test_social_feed.py` — subconjunto ejecutable de los casos del artículo: incremento de like (TC-006), idempotencia de like (TC-007/borde), unlike sin negativos (TC-007), persistencia de comentario (TC-008), comentario-sobre-borrado 410 (borde), alcance solo-seguidores (TC-005), perfil privado retroactivo (TC-013), visibilidad en búsqueda (TC-028), conteos follow/unfollow (TC-014/015), dedup + aceptar de solicitud de amistad (TC-016/017), rechazar (TC-018), dedup de reportes (TC-023), bloqueo bidireccional + corte de DM (TC-024), mute que mantiene el follow (TC-025) y post oculto (TC-026).

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `15 passed`.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/social-media-test-cases/
- Artículo ES: https://qapractices.com/es/test-cases/social-media-test-cases/

# Checklist de Testing de Protocolo MQTT — Companion

Recurso companion de [Checklist de Testing de Protocolo MQTT](https://qapractices.com/es/checklists/mqtt-protocol-testing-checklist/).

## Contenido

- `mqtt_model.py` — modelo sin dependencias de la semántica del protocolo que verifica la checklist: matching de wildcards (`+`, `#`, exclusión de `$SYS`), validación de filtros (límite de 65 535 bytes, `#` solo como último nivel), downgrade de QoS (`min(publish, subscribe)`), store de mensajes retenidos (el último gana, payload vacío elimina), reentrega de sesión persistente, disparo de LWT (solo no-graceful) y takeover de clientID.
- `tests/test_mqtt_checklist.py` — subconjunto ejecutable de la checklist: niveles de wildcard y filtros malformados, exclusión de `$SYS`, rechazo de filtro oversize, downgrade de QoS y rechazo de QoS inválido, retenido last-wins/clear/entrega-al-suscribirse, sesión persistente vs limpia, LWT graceful/ungraceful, takeover por clientID duplicado.

## Requisitos

- Python 3.10+, `pip install -r requirements.txt` (solo pytest — el modelo es stdlib puro)

## Uso

```bash
pytest tests/ -q
```

Salida esperada: `15 passed`.

Los chequeos a nivel de broker (TLS, ACLs, carga, interop) corren contra un broker real según la checklist — `mosquitto` en local o `test.mosquitto.org` — con `mosquitto_pub`/`mosquitto_sub` o el ejemplo paho del artículo.

## Relacionados

- Artículo EN: https://qapractices.com/checklists/mqtt-protocol-testing-checklist/
- Artículo ES: https://qapractices.com/es/checklists/mqtt-protocol-testing-checklist/

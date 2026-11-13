# Casos de Prueba de Anuncios en Juegos — Companion Ejecutable

Fakes offline que hacen testeables las dos mecánicas más propensas a fallar de la monetización con anuncios, sin dispositivo, sin red y sin SDK real:

- `FakeRewardedAdSDK` — solo dispara `on_user_earned_reward` tras una vista completa; los cierres anticipados y las repeticiones no premian.
- `RewardLedger` — drena `pending_reward` exactamente una vez, así que los bugs de doble recompensa salen como fallos de aserción.
- `FrequencyCapper` — límite de impresiones por intervalo basado en el reloj del sistema, para que freezegun pruebe los bordes de la ventana de forma determinista.

Companion de [Casos de Prueba de Anuncios en Juegos](https://qapractices.com/es/test-cases/ad-monetization-games-testing/).

## Setup

```bash
pip install -r requirements.txt
pytest tests/ -q
```

## Mapeo con el artículo

| Test | Caso de prueba |
|---|---|
| `test_rewarded_ads.py` | TC-01 — recompensa otorgada una vez, solo en el callback de finalización |
| `test_frequency_cap.py` | TC-08 — límite aplicado dentro de la ventana, restablecido después |
| `features/rewarded_ads.feature` | TC-01 — mismos escenarios en Gherkin para handoff BDD |

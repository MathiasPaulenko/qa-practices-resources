# Casos de Prueba de Asistentes de Voz (Alexa, Siri, Google) — Companion

Recurso companion de [Casos de Prueba de Asistentes de Voz (Alexa, Siri, Google)](https://qapractices.com/es/test-cases/voice-assistant-testing-alexa-siri-google/).

## Contenido

- `voice_pipeline_simulator.py` — modelo determinista solo-stdlib del pipeline de cinco etapas que describe el artículo: motor de wake word con umbral de confianza, etapa ASR que pierde palabras bajo ruido o degradación del hablante, tabla de frases NLU con paráfrasis y slots obligatorios, gestor de diálogo que mantiene el estado de sesión (elicitación de slots, correcciones a mitad de diálogo, fallback de dos strikes que sale con elegancia) e historial de voz que solo registra turnos activados. Sin audio, sin llamadas a modelos — las reglas representan al dispositivo para que la suite corra completamente offline.
- `tests/conftest.py` — pone el simulador en `sys.path`.
- `tests/test_voice_pipeline.py` — subconjunto ejecutable de los casos del artículo: umbral de wake word y casi-homófonos (TC-01), precisión de intents con paráfrasis (TC-02), elicitación de slots (TC-03), contexto multiturno y corrección (TC-04), salida de fallback y timeout de backend (TC-05), degradación por acento/ruido (TC-06, TC-09), registro y borrado del historial (TC-07) y equivalencia de entrada de texto (TC-10).
- `bespoken/testing.yml` — archivo end-to-end de Bespoken 2.x que maneja un dispositivo Alexa virtual por audio real. Necesita un skill desplegado y credenciales de `bst`; es la contraparte de producción del simulador.
- `fixtures/utterance-intent-map.json` — el corpus de regresión frase→intent del artículo, usable contra cualquier simulador o la Skill Simulation API.

## Requisitos

- Python 3.10+
- pip

## Uso

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Salida esperada: `18 passed`.

En una suite real reemplazarías `hear()` por replay de audio grabado a través del dispositivo y mantendrías las mismas aserciones — el simulador existe para que las propiedades bajo prueba (umbrales de wake, presupuestos de degradación, límites de fallback, higiene del historial) sean visibles sin un Echo sobre el escritorio.

## Relacionados

- Artículo EN: https://qapractices.com/test-cases/voice-assistant-testing-alexa-siri-google/
- Artículo ES: https://qapractices.com/es/test-cases/voice-assistant-testing-alexa-siri-google/

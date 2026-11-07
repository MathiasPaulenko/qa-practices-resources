# Voice Assistant Testing (Alexa, Siri, Google) — Companion

Companion resource for [Voice Assistant Testing (Alexa, Siri, Google)](https://qapractices.com/test-cases/voice-assistant-testing-alexa-siri-google/).

## Contents

- `voice_pipeline_simulator.py` — stdlib-only deterministic model of the five-stage pipeline described in the article: a wake word engine with a confidence threshold, an ASR stage that drops words under noise or speaker degradation, an NLU phrase table with paraphrases and required slots, a dialog manager that keeps session state (slot elicitation, mid-dialog corrections, a two-strike fallback that exits politely), and a voice history that only records woken turns. No audio, no model calls — the rules stand in for the device so the suite runs fully offline.
- `tests/conftest.py` — puts the simulator on `sys.path`.
- `tests/test_voice_pipeline.py` — executable subset of the article's cases: wake threshold and near-homophones (TC-01), paraphrase intent accuracy (TC-02), slot elicitation (TC-03), multi-turn context and correction (TC-04), fallback exit and backend timeout (TC-05), accent/noise degradation (TC-06, TC-09), history recording and deletion (TC-07) and type-to-text equivalence (TC-10).
- `bespoken/testing.yml` — Bespoken 2.x end-to-end file that drives a virtual Alexa device over real audio. Needs a deployed skill and `bst` credentials; this is the production counterpart of the simulator.
- `fixtures/utterance-intent-map.json` — the utterance→intent regression corpus from the article, usable against any simulator or the Skill Simulation API.

## Requirements

- Python 3.10+
- pip

## Usage

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Expected output: `18 passed`.

In a real suite you'd replace `hear()` with recorded audio replay through the device and keep the same assertions — the simulator exists so the properties under test (wake thresholds, degradation budgets, fallback limits, history hygiene) are visible without an Echo on the desk.

## Related

- Article EN: https://qapractices.com/test-cases/voice-assistant-testing-alexa-siri-google/
- Article ES: https://qapractices.com/es/test-cases/voice-assistant-testing-alexa-siri-google/

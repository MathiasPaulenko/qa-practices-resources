# Companion de Comparación de Herramientas de Test Automation con IA

Recurso companion de la [Comparación de Herramientas de Test Automation con IA](https://qapractices.com/es/documentation/ai-powered-test-automation-tools-comparison). Incluye ejemplos funcionales de selectores self-healing, parsing de user stories y selección predictiva con Launchable.

## Archivos

| Archivo | Propósito |
|---------|-----------|
| `src/self_healing_fallback.py` | Helper de Selenium con estrategia de fallback de selectores |
| `src/user_story_parser.py` | Parsear user stories en outlines de test |
| `src/launchable_subset.sh` | Comandos CLI de Launchable para selección predictiva |
| `.github/workflows/ai-tests.yml` | Workflow de CI con integración de Launchable |

## Inicio Rápido

```bash
# Ejemplo de fallback self-healing
python src/self_healing_fallback.py

# Parser de user story
python src/user_story_parser.py

# Subset de Launchable (requiere CLI de Launchable + API key)
export LAUNCHABLE_API_KEY=tu-key
bash src/launchable_subset.sh
```

## Requisitos

- Python 3.11+
- Selenium (para ejemplo de self-healing)
- Launchable CLI (para ejemplo de selección de tests)

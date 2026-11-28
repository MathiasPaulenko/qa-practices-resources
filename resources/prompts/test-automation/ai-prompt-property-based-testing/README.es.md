# Prompt de IA: Escenarios de Property-Based Testing

Plantilla de prompt para generar escenarios de property-based testing desde la spec de una función: invariantes nombradas, estrategias de generadores de inputs, casos de borde falsificadores y bocetos para Hypothesis, fast-check o jqwik.

## Archivos

- `prompt-template.txt` — el prompt con placeholders para nombre de función, firma, dominio de entrada, contrato de salida, reglas de negocio y cantidad.
- `example-input.txt` — ejemplo completo: la función de pricing `calculateDiscount(price, tier)`.
- `example-output.txt` — el output completo de diez propiedades para ese input, más un boceto ejecutable en Hypothesis.

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Reemplaza las variables entre corchetes — `example-input.txt` muestra un relleno realista.
3. Conserva las propiedades que atraparían un bug real; descarta las que solo repiten la implementación.

Artículo completo: https://qapractices.com/es/prompts/ai-prompt-property-based-testing

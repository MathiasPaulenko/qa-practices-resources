# Prompt de IA: Testing de Infraestructura Cloud — Companion

Archivos companion del recurso [Prompt de IA: Testing de Infraestructura Cloud](https://qapractices.com/es/prompts/ai-prompt-cloud-infrastructure-testing).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de revisión IaC pre-apply, listo para copiar y pegar en cualquier LLM. |
| `example-input.txt` | Entrada de ejemplo: un módulo Terraform de dos capas con SSH abierto a `0.0.0.0/0`, una instancia RDS sin cifrar y un autoscaling group en una sola AZ. |
| `example-output.csv` | La tabla de hallazgos como CSV importable: recurso, hallazgo, fix mínimo, comando de verificación y severidad. |

## Uso

1. Copia `prompt-template.txt` en tu LLM (ChatGPT, Claude, asistentes tipo Copilot).
2. Reemplaza los corchetes con tu módulo, versiones del provider, ambiente, objetivo de cumplimiento y presupuesto de blast radius.
3. Corre el prompt sobre un módulo o un diff por vez — pegar un repo entero devuelve consejos genéricos.
4. Compara la salida con `example-output.csv` para validar el formato esperado y la escala de severidad.
5. Confirma cada fila con Checkov o `terraform plan` antes de aplicar un fix sugerido; vuelve a correrlo después de cada cambio mergeado.

## Requisitos

- Cualquier LLM con espacio para el prompt más unos cientos de líneas de IaC (modelos clase GPT-4, Claude, Copilot Chat).
- Opcional: una planilla o tracker que importe CSV si quieres mantener los hallazgos bajo control de versiones.

## Notas

- La severidad es el orden en que arreglar, no un veredicto de cumplimiento — confirma siempre con los scanners reales.
- Nunca pegues credenciales reales, IDs de cuenta, hostnames ni datos de clientes en el prompt.

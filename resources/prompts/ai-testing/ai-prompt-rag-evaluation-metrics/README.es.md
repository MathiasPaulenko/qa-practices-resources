# Prompt de IA: Métricas de Evaluación RAG — Companion

Archivos companion del recurso [Prompt de IA: Métricas de Evaluación RAG y Escenarios de Test](https://qapractices.com/es/prompts/ai-prompt-rag-evaluation-metrics).

## Archivos

| Archivo | Propósito |
| --- | --- |
| `prompt-template.txt` | El prompt completo de evaluación RAG, listo para copiar en un LLM. |
| `example-input.txt` | Un contexto rellenado: chatbot de knowledge base de soporte, GPT-4o + text-embedding-3-large + Pinecone, híbrido top-5, sin ground truth aún. |
| `example-output.md` | Un fragmento de salida realista: extracto de la matriz de evaluación, dos escenarios que aíslan una capa (nombre de producto ambiguo, política fabricada) y la especificación del dataset de ground truth. |

## Uso

1. Copia `prompt-template.txt` en tu LLM.
2. Rellena el contexto del pipeline — nombra modelos y versiones exactas, tu chunking/top-K, y sé honesto con el ground truth (si no existe, la especificación del dataset pasa a ser el primer entregable).
3. Compara la forma de la respuesta con `example-output.md`; cada escenario debe aislar una capa y nombrar el fallo que provoca.
4. Usa un modelo distinto como juez del que genera las respuestas.
5. Re-ejecuta tras cualquier cambio del pipeline: tamaño de chunk, embeddings, reranker, LLM.

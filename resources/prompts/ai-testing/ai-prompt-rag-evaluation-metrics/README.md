# AI Prompt: RAG Evaluation Metrics — Companion

Companion files for the [AI Prompt: RAG Evaluation Metrics and Test Scenarios](https://qapractices.com/prompts/ai-prompt-rag-evaluation-metrics) resource.

## Files

| File | Purpose |
| --- | --- |
| `prompt-template.txt` | The full RAG evaluation prompt, ready to copy into an LLM. |
| `example-input.txt` | A filled-in context: support knowledge-base chatbot, GPT-4o + text-embedding-3-large + Pinecone, hybrid top-5, no ground truth yet. |
| `example-output.md` | A realistic output fragment: evaluation matrix excerpt, two layer-isolating scenarios (ambiguous product name, fabricated policy) and a ground-truth dataset spec. |

## Usage

1. Copy `prompt-template.txt` into your LLM.
2. Fill the pipeline context — name exact models and versions, your chunking/top-K, and be honest about ground truth (if none exists, the dataset spec becomes the first deliverable).
3. Compare the response shape with `example-output.md`; every scenario should isolate one layer and name the failure it provokes.
4. Use a different model as judge than the one generating answers.
5. Re-run after any pipeline change: chunk size, embeddings, reranker, LLM.

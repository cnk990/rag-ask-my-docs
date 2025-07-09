# Ask My Docs - RAG Q&A App

A simple Retrieval-Augmented Generation (RAG) pipeline that lets you query your own documents
and get precise answers.

Built with:
- OpenAI embeddings for semantic search
- GPT-4 for answer generation
- Streamlit for an interactive UI

Perfect as a lightweight demo of how RAG works end-to-end.
## 🌐 Live Demo
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ask-my-docs-rag.streamlit.app)

-------

## Features

- Upload your documents
- Split documents into chunks for better retrieval
- Create embeddings for semantic search
- Find relevant chunks using cosine similarity
- Feed relevant context into GPT-4 for accurate answers
- Easy-to-use Streamlit UI

## Project Learnings & Technical Notes

1. **Understanding RAG Pipelines**
Retrieval-Augmented Generation (RAG) uses embeddings + similarity search to feed the LLM only relevant document snippets.
This reduces token cost and improves accuracy compared to dumping entire documents as context into the prompt.

2. **Chunking Strategies**
Explored different ways of splitting documents:

- Fixed-size word chunks (e.g. every 50 words)
- Sentence-based chunks for clearer context
- Section-based chunking:
- Split by document headings (e.g. “Jury Duty:”)
  - Then chunk inside each section

Section-based chunking ultimately provided the best context clarity for the LLM.

3. **Prompt Engineering**
Too-strict prompts (e.g. “only answer if exact words appear”) often led to:
“I’m sorry, I can’t answer that.”

Simplified, instructive prompts worked better:
“Answer the following question as truthfully as possible using only the context below. If the answer is not contained, say 'I don’t know.'”

4. **Embedding Strategies**
Initially, embeddings were created for all document chunks every run. This caused:
- Long processing times
- Higher API costs

Solution:
- Batch embeddings instead of single requests
- Save embeddings as pickle files locally for fast re-runs

5. **Dynamic vs Static RAG**
- Static RAG (like Ask My Docs):
  - Embeds a fixed corpus once
  - Fast retrieval afterwards

- Dynamic pipelines (like [gaming insights pilot](https://gaming-insights-pilot.streamlit.app)):
  - No embeddings for static storage
  - Context scraped dynamically and sent directly to the LLM

Learned how the two approaches differ in architecture, cost and latency.

6. **Similarity Thresholds**
- Without thresholds, even unrelated queries retrieved “best available” chunks (sometimes highly irrelevant data).
- Added a similarity threshold:
  - Skip retrieval entirely if max similarity is too low (e.g. below 0.2)
  - Avoids wasting tokens on unrelated questions.


## Issues & Resolutions

| Issue                                                                                        | Resolution                                                         |
|----------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Missing f in multi-line string.<br/> Prompt was passed as a literal string, not interpolated | Added f prefix. Variables were inserted correctly in prompts       |
|                                                                                              |                                                                    |
| Chunks like "Jury Duty:" retrieved alone                                                     | Implemented section-based chunking instead of word-based splits    |
|                                                                                              |                                                                    |
| Slow runtime due to embedding all chunks each run                                            | Pickled embeddings to disk and loaded them on subsequent runs      |
|                                                                                              |                                                                    |
| Low similarity queries still retrieving unrelated chunks                                     | Added a similarity threshold check to avoid unnecessary LLM calls  |
|                                                                                              |                                                                    |
| Retrieval returning unrelated chunks for questions about music                               | Implemented similarity threshold to skip retrieval if not relevant |
|                                                                                              |                                                                    |

## Future Enhancements

Nice-to-have improvements:
- Implement chunk overlap for more context continuity
- Integrate a vector database for scalable retrieval
- Add UI highlights showing matched chunks
- Combine multiple documents dynamically for multi-doc Q&A
- Switch to local or open-source LLMs (e.g. BGE, Mistral, Ollama) to avoid OpenAI API costs and keep data private.

## Benefits of local LLMs:

No API costs.
- Running your own model is free after hardware costs.

Full data privacy.
- No sensitive docs go outside your infrastructure.

Faster inference.
- No network latency.

Custom fine-tuning possible.
- Tailor a model to your document styles.

## Challenges:

Hardware requirements:
- Running even small LLMs can require:
  - ≥8GB VRAM for small models
  - ≥16–24GB for larger models

Slightly more complex deployment:
- Need to serve the model (e.g. with FastAPI, Ollama, etc.)

May be less accurate than models such as GPT-4 for complex reasoning.
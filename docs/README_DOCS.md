# Documentation Overview

This `docs/` folder contains module-level documentation for the RAG project.
Each Markdown file corresponds to a specific package or module and explains
purpose, public API, and usage examples.

Files
- `CORE_INTERFACES.md` — abstract interfaces and their expected methods.
- `CORE_MODELS.md` — data models such as `Document`.
- `INGESTION_PDF_LOADER.md` — PDF loader and chunking behavior.
- `EMBEDDINGS_EMBEDDER.md` — embedding provider usage.
- `RETRIEVAL_FAISS_STORE.md` — FAISS-backed vector store details.
- `RETRIEVAL_RETRIEVER.md` — semantic retriever.
- `LLM_CLIENT.md` — OpenAI adapter and dummy LLM.
- `AGENT_RAG_AGENT.md` — agent orchestration and guardrails.
- `MAIN_CLI.md` — CLI commands and behavior.
- `WEB_SERVER.md` — web UI endpoints and behavior.
- `USAGE.md` — quick examples and snippets.

Keeping docs up to date
- When you change public APIs or behavior, update the corresponding markdown
  file under `docs/`.

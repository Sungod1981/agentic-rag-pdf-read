# CLI (app/main.py)

Location: `app/main.py`

Purpose
- Provides a minimal CLI to ingest PDFs and interact with the RAG agent via an
  interactive chat loop.

Commands
- `ingest <paths...>` — ingest one or more PDF files, compute embeddings, add
  chunks to FAISS, and persist the index to `FAISS_INDEX_PATH`.
- `chat` — start an interactive REPL-style chat prompt that uses the agent to
  answer questions. The CLI attempts to load a persisted FAISS index on start.

Design notes
- The CLI composes pluggable components via `build_components()` and keeps the
  command functions small and focused. This makes it simple to swap
  implementations (embedder, vector store, LLM) during testing or extension.

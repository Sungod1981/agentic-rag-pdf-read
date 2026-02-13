# RAG Agent (Python)

This project is a modular, agentic Retrieval-Augmented Generation (RAG) application in Python.

Architecture:
- app/config: configuration and wiring
- app/core: core models and abstract interfaces
- app/ingestion: PDF loading and chunking
- app/embeddings: pluggable embedding providers
- app/retrieval: vector store + retriever
- app/llm: LLM provider abstraction
- app/agent: agent logic that uses retrieval as a tool
- app/main.py: simple CLI

Quickstart

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):

Create a `.env` with:

```
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
FAISS_INDEX_PATH=./faiss.index
```

3. Ingest PDFs:

```bash
python -m app.main ingest path/to/doc1.pdf path/to/doc2.pdf
```

4. Ask questions interactively:

```bash
python -m app.main chat
```

Extensibility
- Replace embedding provider by implementing `app.core.interfaces.Embedder`
- Replace vector store by implementing `app.core.interfaces.VectorStore`
- Add LLM provider by implementing `app.core.interfaces.LLMClient`

See source for details and docstrings.

# Core Interfaces

Location: `app/core/interfaces.py`

Purpose
- Defines abstract base classes (ABCs) used across the application: `Loader`,
  `Embedder`, `VectorStore`, `Retriever`, `LLMClient`, and `Agent`.

When to implement
- Create concrete implementations to plug into the system (e.g., a file
  loader, a sentence-transformer embedder, a FAISS vector store, or an OpenAI
  LLM adapter).

Key classes & methods
- `Loader.load(path: str) -> List[Document]` — load a resource and return
  chunked `Document` objects.
- `Embedder.embed(texts: Iterable[str]) -> List[List[float]]` — return numeric
  embeddings for a batch of texts.
- `VectorStore.add(docs, embeddings)` — persist document embeddings.
- `VectorStore.search(embedding, k)` — return list of `(Document, score)`.
- `Retriever.retrieve(query, k)` — return list of `(Document, score)` for a
  given query string.
- `LLMClient.generate(prompt, **kwargs) -> str` — generate text for a prompt.
- `Agent.answer(query: str) -> str` — high-level grounded answer generation.

Design notes
- Interfaces keep the architecture pluggable and follow Dependency Inversion.

# Retriever

Location: `app/retrieval/retriever.py`

Purpose
- Provide a semantic retriever that composes an `Embedder` and a `VectorStore`.

Public API
- `SemanticRetriever(embedder, store)` — constructor wiring.
- `retrieve(query: str, k: int = 5) -> List[Tuple[Document, float]]` — embed the
  query using the embedder and search the store for top-k matches.

Behavior
- The retriever is intentionally minimal: it does not perform reranking,
  metadata filtering, or contextualization. Those features can be added in a
  new retriever implementation that still satisfies the `Retriever` interface.

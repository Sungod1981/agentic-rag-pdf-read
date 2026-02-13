# FAISS Vector Store

Location: `app/retrieval/faiss_store.py`

Purpose
- Concrete VectorStore implementation backed by FAISS (IndexFlatIP). Stores an
  in-memory FAISS index and a parallel list of `Document` metadata for
  retrieval results.

Public API
- `FaissVectorStore(dim: int)` — initialize an inner FAISS IndexFlatIP with
  dimensionality `dim`.
- `add(docs, embeddings)` — add numpy-compatible embeddings and append docs to
  metadata list.
- `search(embedding, k)` — runs an inner FAISS search and returns a list of
  `(Document, score)` tuples.
- `persist(path)` and `load(path)` — persist index and metadata using
  `faiss.write_index` and `pickle` respectively.

Notes
- Embeddings are normalized for cosine-similarity via inner-product.
- This store is in-memory; for production, consider an on-disk index or a
  managed vector DB (Pinecone, Milvus, etc.) and implement `app.core.interfaces.VectorStore`.

Example
```py
store = FaissVectorStore(dim=384)
store.add(docs, embeddings)
results = store.search(query_embedding, k=5)
```

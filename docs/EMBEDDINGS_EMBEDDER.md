# Embeddings (Sentence Embedder)

Location: `app/embeddings/embedder.py`

Purpose
- Provide a pluggable embedding provider. The default implementation uses
  `sentence-transformers` to compute dense vector representations for text.

Public API
- `SentenceEmbedder(model_name: str)` — constructor that loads the specified
  sentence-transformers model.
- `embed(texts: Iterable[str]) -> List[List[float]]` — encodes a batch of text
  strings and returns a list of float vectors.

Notes
- The returned vectors are Python lists of floats for easy serialization and
  storage in NumPy/FAISS-backed stores.
- The model name is configurable via `EMBEDDING_MODEL` in `.env`.

Example
```py
from app.embeddings.embedder import SentenceEmbedder
e = SentenceEmbedder('sentence-transformers/all-MiniLM-L6-v2')
vecs = e.embed(['hello world', 'another sentence'])
```

# Core Models

Location: `app/core/models.py`

Purpose
- Contains simple data models used across the system. Currently includes
  `Document`, a lightweight container for a text chunk, its metadata, and the
  original source path.

`Document` fields
- `id: str` — unique identifier for the chunk (UUID is used by the loader).
- `text: str` — the chunk text used for embedding and retrieval.
- `metadata: Dict[str, Any]` — optional metadata (page numbers, chunk index).
- `source: str` — original file path (useful for citations).

Usage
- Instances of `Document` are created by loaders (e.g., `PdfLoader`), stored
  alongside embeddings in the vector store, and returned by the retriever.

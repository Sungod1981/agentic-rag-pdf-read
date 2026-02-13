# PDF Ingestion and Chunking

Location: `app/ingestion/pdf_loader.py`

Purpose
- Robustly load PDF files, extract page text, and produce manageable text
  chunks for embedding and retrieval.

Public API
- `PdfLoader.load(path: str) -> List[Document]` — reads a PDF, extracts text
  per page, joins pages, and applies `chunk_text` to produce `Document`
  objects.
- `chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]`
  — splits input text into overlapping chunks while attempting to preserve
  paragraph boundaries.

Behavior & notes
- The loader labels chunks with `chunk_index` metadata and generates UUIDs for
  each chunk id.
- The chunking strategy is deliberately simple and robust: it groups
  short paragraphs and splits long paragraphs with a sliding window.

Example
```py
from app.ingestion.pdf_loader import PdfLoader
loader = PdfLoader()
docs = loader.load('mydoc.pdf')
for d in docs:
    print(d.id, d.metadata)
```

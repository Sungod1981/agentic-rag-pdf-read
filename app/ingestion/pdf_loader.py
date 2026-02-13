from typing import List, Dict
import logging
import uuid
from pypdf import PdfReader
from ..core.models import Document
from ..core.interfaces import Loader

logger = logging.getLogger(__name__)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Chunk text into roughly `chunk_size` char pieces with overlap.

    This is a simple, robust strategy that keeps sentence boundaries where possible.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    buffer = ""
    for para in paragraphs:
        if len(buffer) + len(para) + 2 <= chunk_size:
            buffer = buffer + "\n\n" + para if buffer else para
        else:
            if buffer:
                chunks.append(buffer)
            # split long paragraph
            start = 0
            while start < len(para):
                part = para[start : start + chunk_size]
                chunks.append(part)
                start += chunk_size - overlap
            buffer = ""
    if buffer:
        chunks.append(buffer)
    return chunks


class PdfLoader(Loader):
    """Loads a PDF and returns a list of chunked `Document` objects."""

    def load(self, path: str) -> List[Document]:
        logger.info("Loading PDF: %s", path)
        reader = PdfReader(path)
        texts = []
        for i, page in enumerate(reader.pages):
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            texts.append((i + 1, txt))

        combined = "\n\n".join(f"Page {p}\n{t}" for p, t in texts if t.strip())
        chunks = chunk_text(combined)
        docs = []
        for i, c in enumerate(chunks):
            docs.append(
                Document(
                    id=str(uuid.uuid4()),
                    text=c,
                    metadata={"chunk_index": i},
                    source=path,
                )
            )
        logger.info("Created %d chunks for %s", len(docs), path)
        return docs

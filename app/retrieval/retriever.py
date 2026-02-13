from typing import List, Tuple
from ..core.models import Document
from ..embeddings.embedder import SentenceEmbedder
from .faiss_store import FaissVectorStore
from ..core.interfaces import Retriever


class SemanticRetriever(Retriever):
    def __init__(self, embedder: SentenceEmbedder, store: FaissVectorStore):
        self.embedder = embedder
        self.store = store

    def retrieve(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        emb = self.embedder.embed([query])[0]
        return self.store.search(emb, k)

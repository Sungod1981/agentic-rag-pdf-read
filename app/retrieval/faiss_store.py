from typing import List, Tuple
import faiss
import numpy as np
import pickle
import os
from ..core.models import Document
from ..core.interfaces import VectorStore


class FaissVectorStore(VectorStore):
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.docs: List[Document] = []

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms

    def add(self, docs: List[Document], embeddings: List[List[float]]) -> None:
        arr = np.array(embeddings, dtype="float32")
        arr = self._normalize(arr)
        self.index.add(arr)
        self.docs.extend(docs)

    def search(self, embedding: List[float], k: int) -> List[Tuple[Document, float]]:
        vec = np.array([embedding], dtype="float32")
        vec = self._normalize(vec)
        D, I = self.index.search(vec, k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.docs):
                continue
            results.append((self.docs[int(idx)], float(score)))
        return results

    def persist(self, path: str) -> None:
        # store faiss index and docs
        faiss.write_index(self.index, path + ".index")
        with open(path + ".meta", "wb") as f:
            pickle.dump(self.docs, f)

    def load(self, path: str) -> None:
        if os.path.exists(path + ".index") and os.path.exists(path + ".meta"):
            self.index = faiss.read_index(path + ".index")
            with open(path + ".meta", "rb") as f:
                self.docs = pickle.load(f)

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, List
from .models import Document


class Loader(ABC):
    @abstractmethod
    def load(self, path: str) -> List[Document]:
        """Load and chunk a single file into Documents."""


class Embedder(ABC):
    @abstractmethod
    def embed(self, texts: Iterable[str]) -> List[List[float]]:
        """Return embeddings for given texts."""


class VectorStore(ABC):
    @abstractmethod
    def add(self, docs: List[Document], embeddings: List[List[float]]) -> None:
        pass

    @abstractmethod
    def search(self, embedding: List[float], k: int):
        """Return list of tuples (Document, score)."""

    @abstractmethod
    def persist(self, path: str) -> None:
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        pass


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, k: int):
        """Return list of (Document, score)."""


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text for a prompt."""


class Agent(ABC):
    @abstractmethod
    def answer(self, query: str) -> str:
        """Process query, call retriever as a tool and return grounded answer."""

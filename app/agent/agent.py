from typing import List
import logging
from ..core.interfaces import Agent
from ..core.models import Document
from ..core.interfaces import LLMClient

logger = logging.getLogger(__name__)


class RagAgent(Agent):
    def __init__(self, retriever, llm: LLMClient, top_k: int = 5, similarity_threshold: float = 0.2):
        self.retriever = retriever
        self.llm = llm
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def _format_context(self, docs: List[tuple]) -> str:
        parts = []
        for doc, score in docs:
            parts.append(f"Source: {doc.source} (score={score:.3f})\n{doc.text}\n---\n")
        return "\n".join(parts)

    def answer(self, query: str) -> str:
        results = self.retriever.retrieve(query, k=self.top_k)
        if not results:
            return "REFUSE: Insufficient context to answer this question."

        # simple guard: check top score
        top_score = results[0][1]
        if top_score < self.similarity_threshold:
            return "REFUSE: Retrieved content is not sufficiently relevant; cannot answer without risk of hallucination."

        context = self._format_context(results)
        prompt = f"You are an assistant. Answer the user question using ONLY the provided context. If the context does not contain the answer, say you cannot answer.\n\nContext:\n{context}\nQuestion: {query}\nAnswer (concise, cite sources):"
        resp = self.llm.generate(prompt)
        return resp

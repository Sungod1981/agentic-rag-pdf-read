# Usage & Examples

This document aggregates quick examples showing how to use the main parts of
the system from Python or via the CLI/web UI.

Ingesting PDFs (CLI)
```powershell
python -m app.main ingest path\to\doc1.pdf path\to\doc2.pdf
```

Interactive CLI Chat
```powershell
python -m app.main chat
Question> What is the main topic of doc1?
```

Web UI
1. Start the server: `uvicorn app.web.server:app --reload --port 8001`
2. Open `http://127.0.0.1:8001`
3. Upload a PDF and use the chat box — the UI will scope answers to the
   uploaded document.

Python usage (programmatic)
```py
from app.ingestion.pdf_loader import PdfLoader
from app.embeddings.embedder import SentenceEmbedder
from app.retrieval.faiss_store import FaissVectorStore
from app.retrieval.retriever import SemanticRetriever
from app.llm.llm_client import DummyLLM
from app.agent.agent import RagAgent

loader = PdfLoader()
docs = loader.load('my.pdf')
embedder = SentenceEmbedder()
emb = embedder.embed([d.text for d in docs])
store = FaissVectorStore(dim=len(emb[0]))
store.add(docs, emb)
retriever = SemanticRetriever(embedder, store)
agent = RagAgent(retriever, DummyLLM())
print(agent.answer('What is this document about?'))
```

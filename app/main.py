"""CLI entrypoint for the RAG application.

This module wires together the major components (config, embedder, vector
store, retriever, LLM and agent) and exposes two CLI commands:

- `ingest`: Load PDF files, chunk, embed, and persist a FAISS index.
- `chat`: Start an interactive CLI chat that queries the agent.

The functions in this file are intentionally thin: they compose higher-level
components from pluggable implementations in `app.*` packages. Keeping this
module focused on orchestration follows the Single Responsibility Principle.
"""

import argparse
import logging
from typing import Tuple

from .config.config import get_settings
from .ingestion.pdf_loader import PdfLoader
from .embeddings.embedder import SentenceEmbedder
from .retrieval.faiss_store import FaissVectorStore
from .retrieval.retriever import SemanticRetriever
from .llm.llm_client import OpenAILLM, DummyLLM
from .agent.agent import RagAgent


logging.basicConfig(level=logging.INFO)


def build_components() -> Tuple:
    """Create and return the core application components.

    Returns a tuple: (settings, embedder, store, retriever, llm, agent).

    Design notes:
    - The embedder is created from the configured model name.
    - A small sample embedding is computed to derive dimensionality for FAISS.
    - If an OpenAI API key is not supplied, a `DummyLLM` is used so the app
      remains runnable offline for testing.
    """
    settings = get_settings()

    # Create an embedding provider (pluggable implementation)
    embedder = SentenceEmbedder(settings.embedding_model)

    # Determine the embedding dimensionality by encoding a short sample.
    # This keeps the FAISS store generic and avoids exposing internal model
    # details to the rest of the system.
    sample_embedding = embedder.embed(["hello"])[0]
    dim = len(sample_embedding)

    # Create a FAISS-backed vector store using the deduced dimension.
    store = FaissVectorStore(dim)

    # Retriever composes embedder + store and exposes a `retrieve` method.
    retriever = SemanticRetriever(embedder, store)

    # LLM selection: prefer OpenAI when an API key is configured; otherwise
    # fall back to the `DummyLLM` implementation for local testing.
    if settings.openai_api_key:
        try:
            llm = OpenAILLM(settings.openai_api_key)
        except Exception:
            # If LLM init fails, continue with dummy (safe fallback).
            llm = DummyLLM()
    else:
        llm = DummyLLM()

    # The agent coordinates retrieval and LLM generation and exposes
    # the high-level `answer` method used by the CLI and web server.
    agent = RagAgent(
        retriever, llm, top_k=settings.top_k, similarity_threshold=settings.similarity_threshold
    )

    return settings, embedder, store, retriever, llm, agent


def cmd_ingest(args: argparse.Namespace) -> None:
    """CLI handler: ingest PDF files into the FAISS vector store.

    Steps:
    1. Build components (embedder + store)
    2. Load and chunk PDFs
    3. Compute embeddings for chunks
    4. Add chunks to the vector store and persist to disk
    """
    settings, embedder, store, retriever, llm, agent = build_components()

    loader = PdfLoader()
    all_docs = []
    all_texts = []

    # Load and chunk each supplied path. We collect both Document objects and
    # their raw text to compute embeddings in a single batch for efficiency.
    for path in args.paths:
        docs = loader.load(path)
        all_docs.extend(docs)
        all_texts.extend([d.text for d in docs])

    # Compute embeddings in batch; embedder implementations should be
    # optimized for batching and may use GPU if available.
    embeddings = embedder.embed(all_texts)

    # Add to FAISS and persist (index + metadata). Persist path is
    # configurable via `FAISS_INDEX_PATH` in `.env`.
    store.add(all_docs, embeddings)
    store.persist(settings.faiss_index_path)

    print(f"Ingested {len(all_docs)} chunks; persisted to {settings.faiss_index_path}")


def cmd_chat(args: argparse.Namespace) -> None:
    """Start a simple interactive chat loop that queries the agent.

    This function attempts to load a persisted FAISS index (if present) so
    previously ingested documents can be used without re-ingestion.
    """
    settings, embedder, store, retriever, llm, agent = build_components()

    # Attempt to load an existing persisted index; failures are non-fatal and
    # we'll simply start with an empty store.
    try:
        store.load(settings.faiss_index_path)
    except Exception:
        logging.getLogger(__name__).info("No persisted index found; starting fresh.")

    print("Starting interactive chat. Type 'exit' or press Enter on an empty line to quit.")
    while True:
        # Prompt the user for a question. Trim whitespace to detect exit.
        q = input("Question> ")
        if not q.strip() or q.strip().lower() in ("exit", "quit"):
            # Graceful exit of the interactive loop
            break

        # Use the agent to provide a grounded answer. The agent will refuse
        # to hallucinate if the retrieval step yields insufficient evidence.
        response = agent.answer(q)

        print("\n--- Answer ---")
        print(response)
        print("--- End ---\n")


def main() -> None:
    """Entrypoint for the CLI. Parses commands and dispatches handlers.

    Commands:
      - ingest <paths...>
      - chat
    """
    parser = argparse.ArgumentParser("RAG Agent CLI")
    sub = parser.add_subparsers(dest="cmd")

    p_ingest = sub.add_parser("ingest", help="Ingest PDFs and build FAISS index")
    p_ingest.add_argument("paths", nargs="+", help="PDF paths to ingest")

    sub.add_parser("chat", help="Start interactive chat")

    args = parser.parse_args()
    if args.cmd == "ingest":
        cmd_ingest(args)
    elif args.cmd == "chat":
        cmd_chat(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

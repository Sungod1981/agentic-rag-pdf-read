# RAG Agent

Location: `app/agent/agent.py`

Purpose
- Implements the `RagAgent` which orchestrates retrieval and LLM calls to
  produce grounded answers. The agent enforces a simple guardrail to refuse
  answering when retrieved context is insufficient (low similarity score).

Public API
- `RagAgent(retriever, llm, top_k=5, similarity_threshold=0.2)` — constructs
  the agent with retrieval and LLM components.
- `answer(query: str) -> str` — main method: retrieves context, checks
  relevance, formats a prompt that includes the retrieved context, and calls
  the LLM client to generate a grounded answer.

Behavior & guardrails
- The agent checks the top retrieved score and returns a refusal message if
  the score is below `similarity_threshold` to reduce hallucinations.
- Context formatting includes source paths to enable source citations in the
  generated answer.

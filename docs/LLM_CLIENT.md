# LLM Client

Location: `app/llm/llm_client.py`

Purpose
- Abstracts the LLM provider behind `LLMClient` and implements a wrapper for
  OpenAI that supports both legacy and modern (`openai>=1.0`) Python SDK
  interfaces. Also includes a `DummyLLM` for offline testing.

Public API
- `OpenAILLM(api_key: Optional[str])` — wrapper that detects available SDK
  interface and calls the appropriate chat completion endpoint.
- `DummyLLM()` — simple fallback that returns the prompt back prefixed with an
  explanation; useful for development without API keys.

Notes
- The wrapper attempts to set `openai.api_key` and will instantiate
  `openai.OpenAI()` if present (1.x API). For older SDKs, it falls back to
  module-level `openai.ChatCompletion`.

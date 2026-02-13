from typing import Optional
import openai
from ..core.interfaces import LLMClient


class OpenAILLM(LLMClient):
    """OpenAI LLM wrapper that supports both pre-1.0 and 1.x OpenAI Python SDKs.

    The old SDK exposes `openai.ChatCompletion.create(...)`. The new 1.x SDK
    exposes a client class `openai.OpenAI()` with `client.chat.completions.create(...)`.
    This wrapper detects the available interface and calls the correct method.
    """

    def __init__(self, api_key: Optional[str]):
        if not api_key:
            raise ValueError("OPENAI_API_KEY not provided")

        # Set API key in module for both interfaces to pick up
        try:
            openai.api_key = api_key
        except Exception:
            # best-effort; some versions use different config flows
            pass

        # Prefer the new 1.x client if available
        self._use_new_client = hasattr(openai, "OpenAI")
        if self._use_new_client:
            # instantiate the new-style client (it will read the api_key set above)
            self._client = openai.OpenAI()
        else:
            # fallback to the legacy module-level API
            self._client = openai

    def generate(self, prompt: str, **kwargs) -> str:
        model = kwargs.get("model", "gpt-3.5-turbo")
        temperature = kwargs.get("temperature", 0.0)
        max_tokens = kwargs.get("max_tokens", 512)

        if self._use_new_client:
            # new 1.x style: client.chat.completions.create(...)
            resp = self._client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # response shape mirrors previous SDK: choices[0].message.content
            return getattr(resp.choices[0].message, "content", "").strip()
        else:
            # legacy API
            resp = self._client.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return resp.choices[0].message.content.strip()


class DummyLLM(LLMClient):
    def generate(self, prompt: str, **kwargs) -> str:
        # Very small, safe fallback for offline usage.
        return """I am running in offline/dummy mode. Here is the context provided:\n""" + prompt

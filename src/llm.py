"""OpenRouter chat-completions client with tool calling (standard library only).

Records tokens, OpenRouter-reported cost (usage.include) and latency for every call.
Transient errors (429/5xx/network) are retried with backoff; anything else raises.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from . import config

URL = "https://openrouter.ai/api/v1/chat/completions"


class LLMError(RuntimeError):
    pass


class OpenRouterChat:
    def __init__(self, model: str = config.LLM_MODEL, temperature: float = 0.0, max_tokens: int = 700,
                 timeout: int = 90, retries: int = 3) -> None:
        if not config.OPENROUTER_API_KEY:
            raise LLMError("OPENROUTER_API_KEY missing in .env")
        self.model, self.temperature, self.max_tokens = model, temperature, max_tokens
        self.timeout, self.retries = timeout, retries

    def complete(self, messages: list[dict], tools: list[dict] | None = None,
                 tool_choice: str | dict | None = None) -> dict:
        body = {"model": self.model, "messages": messages, "temperature": self.temperature,
                "max_tokens": self.max_tokens, "usage": {"include": True}}
        if tools:
            body["tools"] = tools
            if tool_choice:
                body["tool_choice"] = tool_choice
        data = json.dumps(body).encode("utf-8")
        last_error = None
        for attempt in range(self.retries + 1):
            req = urllib.request.Request(URL, data=data, method="POST", headers={
                "Authorization": f"Bearer {config.OPENROUTER_API_KEY}", "Content-Type": "application/json",
                "X-Title": "Day7 Agentic RAG lab"})
            t0 = time.perf_counter()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    payload = json.loads(resp.read())
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")[:300]
                last_error = f"HTTP {e.code}: {detail}"
                if e.code in (408, 429, 500, 502, 503, 504) and attempt < self.retries:
                    time.sleep(2 ** attempt * 2)
                    continue
                raise LLMError(last_error) from e
            except (urllib.error.URLError, TimeoutError) as e:
                last_error = f"network: {e}"
                if attempt < self.retries:
                    time.sleep(2 ** attempt * 2)
                    continue
                raise LLMError(last_error) from e
            if "error" in payload:
                last_error = f"provider error: {payload['error']}"
                if attempt < self.retries:
                    time.sleep(2 ** attempt * 2)
                    continue
                raise LLMError(last_error)
            usage = payload.get("usage") or {}
            choice = payload["choices"][0]
            return {
                "message": choice["message"],
                "finish_reason": choice.get("finish_reason"),
                "model": payload.get("model", self.model),
                "provider": payload.get("provider"),
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "cost_usd": float(usage.get("cost") or 0.0),
                "latency_ms": round((time.perf_counter() - t0) * 1000, 1),
                "attempts": attempt + 1,
            }
        raise LLMError(last_error or "unknown error")

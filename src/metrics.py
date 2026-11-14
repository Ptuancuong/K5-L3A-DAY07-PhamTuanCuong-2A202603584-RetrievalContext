"""Gold-based checks. Used only AFTER retrieval/agent runs; gold never enters a retriever or the agent."""
from __future__ import annotations

import statistics


def is_hit(chunk: dict, gold: list[dict]) -> bool:
    """Same hit definition as starter/baseline.py: right source + page and the whole evidence inside the chunk."""
    return any(chunk["source_id"] == g["source_id"] and chunk["page"] == g["page"] and g["evidence"] in chunk["text"]
               for g in gold)


def context_has_evidence(entries: list[dict], gold: list[dict]) -> bool:
    """Evidence must be inside the text actually sent (a truncated block may have lost it)."""
    return any(e["chunk"]["source_id"] == g["source_id"] and e["chunk"]["page"] == g["page"] and g["evidence"] in e["block"]
               for e in entries for g in gold)


def first_hit_rank(results: list[dict], gold: list[dict]) -> int | None:
    for i, c in enumerate(results, 1):
        if is_hit(c, gold):
            return i
    return None


def ratio(n: int, N: int) -> str:
    return f"{n}/{N} ({100 * n / N:.1f}%)" if N else "0/0 (không áp dụng)"


def latency_stats(values: list[float]) -> dict:
    if not values:
        return {}
    return {"median": round(statistics.median(values), 1), "mean": round(statistics.mean(values), 1),
            "max": round(max(values), 1)}

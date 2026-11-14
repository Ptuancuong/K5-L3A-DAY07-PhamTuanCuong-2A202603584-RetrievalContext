"""Context selection. Context is append-only across searches: a block once shown to the
model stays in the final context, new searches can only add blocks within the remaining
budget. Budget unit = characters of the rendered blocks (header included)."""
from __future__ import annotations

SEPARATOR = "\n\n"


def render(chunk: dict, text: str | None = None) -> str:
    meta = chunk.get("metadata", {})
    section = f" | section {meta['section']}" if meta.get("section") else ""
    return f"[{chunk['id']} | {chunk['source']} | page {chunk['page']}{section}]\n{text if text is not None else chunk['text']}"


class ContextBuilder:
    """mode='skip'     : add whole blocks in rank order; a block that does not fit is skipped (starter behaviour).
       mode='truncate' : like skip, but a block that does not fit is cut to the remaining budget if at least
                         `min_chars` remain (keeps the beginning of the chunk, marks the cut with ' [...]')."""

    def __init__(self, budget: int, mode: str = "skip", min_chars: int = 300) -> None:
        if budget < 1 or mode not in ("skip", "truncate"):
            raise ValueError("invalid budget or mode")
        self.budget, self.mode, self.min_chars = budget, mode, min_chars
        self.blocks: list[str] = []
        self.ids: list[str] = []
        self.entries: list[dict] = []  # {'chunk': chunk, 'block': text actually sent}
        self.truncated: list[str] = []
        self.skipped: list[str] = []

    @property
    def used(self) -> int:
        return len(SEPARATOR.join(self.blocks))

    @property
    def text(self) -> str:
        return SEPARATOR.join(self.blocks)

    def add(self, results: list[dict]) -> list[dict]:
        """Add new results; return [{'id', 'block', 'truncated'}] for blocks actually added."""
        added = []
        for chunk in results:
            if chunk["id"] in self.ids:
                continue
            sep = len(SEPARATOR) if self.blocks else 0
            block = render(chunk)
            remaining = self.budget - self.used - sep
            if len(block) <= remaining:
                self.blocks.append(block)
                self.ids.append(chunk["id"])
                self.entries.append({"chunk": chunk, "block": block})
                added.append({"id": chunk["id"], "block": block, "truncated": False})
            elif self.mode == "truncate" and remaining >= self.min_chars:
                header_len = len(render(chunk, ""))
                keep = remaining - header_len - len(" [...]")
                if keep > 0:
                    block = render(chunk, chunk["text"][:keep].rstrip() + " [...]")
                    self.blocks.append(block)
                    self.ids.append(chunk["id"])
                    self.truncated.append(chunk["id"])
                    self.entries.append({"chunk": chunk, "block": block})
                    added.append({"id": chunk["id"], "block": block, "truncated": True})
            else:
                self.skipped.append(chunk["id"])
        return added

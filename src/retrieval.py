"""Retrieval methods. Every retriever implements

    search(query, *, filters=None, top_k) -> list[chunk dict]

and returns chunks in the data contract (id, text, source_id, source, page, metadata)
plus `score`, `rank` (1-based) and `strategy`. Errors (DB down, model missing) are raised,
never replaced by fake results.
"""
from __future__ import annotations

import math
import re
import time
import unicodedata
from collections import Counter
from typing import Any, Protocol

from . import config

FILTER_FIELDS = {"chapter", "section"}  # user-supplied metadata filters allowed


class Retriever(Protocol):
    name: str

    def search(self, query: str, *, filters: dict[str, Any] | None = None, top_k: int = 3) -> list[dict]: ...


def _check_filters(filters: dict | None) -> dict:
    filters = filters or {}
    bad = set(filters) - FILTER_FIELDS
    if bad:
        raise ValueError(f"filter field not allowed: {sorted(bad)}")
    return filters


def _matches(chunk: dict, filters: dict) -> bool:
    return all(chunk["metadata"].get(k) == v for k, v in filters.items())


def _ranked(chunks: list[dict], scores: list[float], strategy: str, top_k: int) -> list[dict]:
    order = sorted(range(len(chunks)), key=lambda i: (-scores[i], chunks[i]["id"]))[:top_k]
    return [{**chunks[i], "score": float(scores[i]), "rank": r, "strategy": strategy} for r, i in enumerate(order, 1)]


# --------------------------------------------------------------------------- dense
class E5Embedder:
    """Query embedder compatible with the Day 6 index (same model, `query: ` prefix, L2-normalised)."""

    _instance: "E5Embedder | None" = None

    def __init__(self, model_name: str = config.EMBEDDING_MODEL) -> None:
        from sentence_transformers import SentenceTransformer

        started = time.perf_counter()
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device="cpu")
        self.dimensions = int(self.model.get_embedding_dimension()
                              if hasattr(self.model, "get_embedding_dimension")
                              else self.model.get_sentence_embedding_dimension())
        if self.dimensions != config.EMBEDDING_DIM:
            raise RuntimeError(f"{model_name} gives {self.dimensions} dims, Day 6 index has {config.EMBEDDING_DIM}")
        self.load_seconds = time.perf_counter() - started
        self.prefix = "query: " if "e5" in model_name.lower() else ""

    @classmethod
    def shared(cls) -> "E5Embedder":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def embed_query(self, text: str) -> list[float]:
        v = self.model.encode([self.prefix + text], normalize_embeddings=True, convert_to_numpy=True,
                              show_progress_bar=False)[0]
        return v.astype(float).tolist()


class DenseRetriever:
    """Exact cosine search in the Day 6 pgvector table (strategy column = index)."""

    def __init__(self, index: str = config.DAY6_INDEX, embedder: E5Embedder | None = None) -> None:
        self.index = index
        self.embedder = embedder or E5Embedder.shared()
        self.name = f"dense[{index}]"

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        import numpy as np
        import psycopg
        from pgvector.psycopg import register_vector

        filters = _check_filters(filters)
        qv = np.asarray(self.embedder.embed_query(query), dtype=np.float32)
        where, params = ["strategy = %s"], [self.index]
        for key, value in filters.items():  # keys whitelisted above -> safe column names
            where.append(f"{key} = %s")
            params.append(value)
        sql = ("SELECT chunk_id, document_id, source, page, chapter, section, section_title, char_start, char_end, "
               "text, model, 1 - (embedding <=> %s) AS score FROM chunks WHERE " + " AND ".join(where) +
               " ORDER BY embedding <=> %s, chunk_id LIMIT %s")
        with psycopg.connect(config.DATABASE_URL, connect_timeout=5) as conn:
            register_vector(conn)
            rows = conn.execute(sql, [qv, *params, qv, top_k]).fetchall()
        out = []
        for rank, (cid, doc, source, page, chapter, section, title, cs, ce, text, model, score) in enumerate(rows, 1):
            out.append({"id": cid, "text": text, "source_id": doc, "source": source, "page": page,
                        "metadata": {"chapter": chapter, "section": section, "section_title": title,
                                     "char_start": cs, "char_end": ce, "index": self.index, "embedding_model": model},
                        "score": float(score), "rank": rank, "strategy": self.name})
        return out


# --------------------------------------------------------------------------- lexical
STOPWORDS = set("""a an and are as at be by can do does for from has have how in is it its of on or that the
their them then there these this to was were what when where which who why will with you your""".split())


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"\w+", unicodedata.normalize("NFC", text).casefold())
    return [t for t in tokens if t not in STOPWORDS]


class BM25Retriever:
    """Okapi BM25 over the exported chunk JSON (same chunks/ids as the dense index)."""

    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75, name: str = "bm25") -> None:
        self.chunks, self.k1, self.b, self.name = chunks, k1, b, name
        self.tfs = [Counter(tokenize(c["text"])) for c in chunks]
        self.lengths = [sum(tf.values()) for tf in self.tfs]
        self.avgdl = sum(self.lengths) / len(self.lengths)
        df = Counter(t for tf in self.tfs for t in tf)
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        filters = _check_filters(filters)
        terms = [t for t in tokenize(query) if t in self.idf]
        cand, scores = [], []
        for chunk, tf, dl in zip(self.chunks, self.tfs, self.lengths):
            if filters and not _matches(chunk, filters):
                continue
            s = 0.0
            for t in terms:
                f = tf.get(t, 0)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            if s > 0:
                cand.append(chunk)
                scores.append(s)
        return _ranked(cand, scores, self.name, top_k)


# --------------------------------------------------------------------------- fusion / rerank
class HybridRRF:
    """Reciprocal Rank Fusion: score = sum 1/(k + rank). Uses ranks only, so no score normalisation is needed."""

    def __init__(self, retrievers: list, depth: int = 20, k: int = 60) -> None:
        self.retrievers, self.depth, self.k = retrievers, depth, k
        self.name = "rrf(" + "+".join(r.name for r in retrievers) + ")"

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        fused: dict[str, float] = {}
        chunk_by_id: dict[str, dict] = {}
        components: dict[str, dict] = {}
        for r in self.retrievers:
            for item in r.search(query, filters=filters, top_k=self.depth):
                fused[item["id"]] = fused.get(item["id"], 0.0) + 1.0 / (self.k + item["rank"])
                chunk_by_id.setdefault(item["id"], {k: v for k, v in item.items() if k not in ("score", "rank", "strategy")})
                components.setdefault(item["id"], {})[r.name] = item["rank"]
        ids = list(fused)
        ranked = _ranked([chunk_by_id[i] for i in ids], [fused[i] for i in ids], self.name, top_k)
        for item in ranked:
            item["component_ranks"] = components[item["id"]]
        return ranked


class CrossEncoderReranker:
    """Retrieve `depth` candidates from a base retriever, rescore (query, chunk) pairs with a cross-encoder."""

    _models: dict[str, Any] = {}

    def __init__(self, base, model_name: str = config.RERANK_MODEL, depth: int = 20) -> None:
        self.base, self.model_name, self.depth = base, model_name, depth
        self.name = f"rerank[{model_name.split('/')[-1]}]({base.name})"
        if model_name not in self._models:
            from sentence_transformers import CrossEncoder
            self._models[model_name] = CrossEncoder(model_name, device="cpu")
        self.model = self._models[model_name]

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        cands = self.base.search(query, filters=filters, top_k=self.depth)
        if not cands:
            return []
        scores = self.model.predict([(query, c["text"]) for c in cands], show_progress_bar=False)
        base_ranks = {c["id"]: c["rank"] for c in cands}
        clean = [{k: v for k, v in c.items() if k not in ("score", "rank", "strategy")} for c in cands]
        ranked = _ranked(clean, [float(s) for s in scores], self.name, top_k)
        for item in ranked:
            item["base_rank"] = base_ranks[item["id"]]
        return ranked


# --------------------------------------------------------------------------- factory
def build_retriever(spec: dict):
    """Build from a config `retrieval` block, e.g. {"method": "hybrid_rerank", "depth": 20}."""
    method = spec["method"]
    index = spec.get("index", config.DAY6_INDEX)
    if method == "dense":
        return DenseRetriever(index)
    if method == "bm25":
        return BM25Retriever(config.load_json(config.chunks_path(index)))
    if method in ("hybrid", "hybrid_rerank"):
        hybrid = HybridRRF([DenseRetriever(index), BM25Retriever(config.load_json(config.chunks_path(index)))],
                           depth=spec.get("depth", 20), k=spec.get("rrf_k", 60))
        if method == "hybrid":
            return hybrid
        return CrossEncoderReranker(hybrid, spec.get("rerank_model", config.RERANK_MODEL), depth=spec.get("depth", 20))
    if method == "dense_rerank":
        return CrossEncoderReranker(DenseRetriever(index), spec.get("rerank_model", config.RERANK_MODEL),
                                    depth=spec.get("depth", 20))
    raise ValueError(f"unknown retrieval method {method}")

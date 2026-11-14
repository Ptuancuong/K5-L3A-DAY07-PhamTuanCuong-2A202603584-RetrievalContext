"""Offline tests for the Day 7 implementation (fake LLM / in-memory retrievers; no quality claims)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agent import run_agent  # noqa: E402
from src.context import ContextBuilder  # noqa: E402
from src.metrics import context_has_evidence, first_hit_rank, is_hit  # noqa: E402
from src.retrieval import BM25Retriever, HybridRRF  # noqa: E402


def chunk(cid, text, page=1, chapter=5):
    return {"id": cid, "text": text, "source_id": "doc", "source": "doc.pdf", "page": page,
            "metadata": {"chapter": chapter, "section": "5.1"}}


CHUNKS = [chunk("c1", "A 1 or a 0 is called a binary digit or bit.", 1, 5),
          chunk("c2", "The scheduler chooses which process to run next.", 2, 6),
          chunk("c3", "A cache miss happens when the cache does not have the data.", 3, 5)]


class Ranked:
    """Fixed-ranking retriever for fusion / agent tests."""
    def __init__(self, name, ids):
        self.name, self.ids = name, ids
    def search(self, query, *, filters=None, top_k=3):
        by_id = {c["id"]: c for c in CHUNKS}
        return [{**by_id[i], "score": 1.0 / r, "rank": r, "strategy": self.name} for r, i in enumerate(self.ids[:top_k], 1)]


class FakeLLM:
    model = "fake"
    def __init__(self, replies):
        self.replies, self.calls = iter(replies), []
    def complete(self, messages, tools=None, tool_choice=None):
        self.calls.append({"messages": list(messages), "tools": [t["function"]["name"] for t in tools or []],
                           "tool_choice": tool_choice})
        name, args = next(self.replies)
        msg = {"content": "", "tool_calls": [{"id": f"call{len(self.calls)}", "type": "function",
                                               "function": {"name": name, "arguments": json.dumps(args)}}]}
        return {"message": msg, "prompt_tokens": 10, "completion_tokens": 5, "cost_usd": 0.0001,
                "latency_ms": 1.0, "model": "fake"}


class RetrievalTests(unittest.TestCase):
    def test_bm25_ranks_lexical_match_first_and_filters(self):
        bm25 = BM25Retriever(CHUNKS)
        self.assertEqual(bm25.search("what is a binary digit", top_k=3)[0]["id"], "c1")
        self.assertEqual([r["id"] for r in bm25.search("process cache binary", filters={"chapter": 6})], ["c2"])
        with self.assertRaises(ValueError):
            bm25.search("x", filters={"gold_page": 1})

    def test_rrf_fuses_by_rank(self):
        fused = HybridRRF([Ranked("a", ["c1", "c2", "c3"]), Ranked("b", ["c2", "c3", "c1"])], depth=3).search("q", top_k=3)
        self.assertEqual(fused[0]["id"], "c2")  # 1/62 + 1/61 beats 1/61 + 1/63
        self.assertEqual([r["rank"] for r in fused], [1, 2, 3])
        self.assertEqual(fused[0]["component_ranks"], {"a": 2, "b": 1})


class ContextTests(unittest.TestCase):
    def test_skip_drops_block_that_does_not_fit(self):
        ctx = ContextBuilder(budget=120, mode="skip")
        ctx.add([chunk("a", "x" * 60), chunk("b", "y" * 60)])
        self.assertEqual(ctx.ids, ["a"])
        self.assertEqual(ctx.skipped, ["b"])

    def test_truncate_keeps_prefix_and_metrics_check_sent_text(self):
        ctx = ContextBuilder(budget=150, mode="truncate", min_chars=50)
        ctx.add([chunk("a", "x" * 60), chunk("b", "EVIDENCE" + "y" * 100)])
        self.assertEqual(ctx.truncated, ["b"])
        self.assertLessEqual(ctx.used, 150)
        self.assertTrue(context_has_evidence(ctx.entries, [{"source_id": "doc", "page": 1, "evidence": "EVIDENCE"}]))
        self.assertFalse(context_has_evidence(ctx.entries, [{"source_id": "doc", "page": 1, "evidence": "y" * 100}]))

    def test_hit_definition(self):
        gold = [{"source_id": "doc", "page": 1, "evidence": "binary digit"}]
        self.assertTrue(is_hit(CHUNKS[0], gold))
        self.assertEqual(first_hit_rank(CHUNKS[::-1], gold), 3)


class AgentTests(unittest.TestCase):
    def test_answer_with_valid_citation(self):
        llm = FakeLLM([("search_documents", {"query": "bit"}),
                       ("submit_answer", {"answer": "A bit [c1].", "citations": ["c1"], "insufficient_evidence": False})])
        out = run_agent("What is a bit?", llm, Ranked("r", ["c1", "c2"]), top_k=2, budget=1000)
        self.assertEqual(out["status"], "answered")
        self.assertEqual(out["citations"], ["c1"])
        self.assertEqual([e["event"] for e in out["events"] if e["event"] == "search"], ["search"])

    def test_citation_outside_context_is_dropped_and_abstains(self):
        llm = FakeLLM([("search_documents", {"query": "bit"}),
                       ("submit_answer", {"answer": "A bit [c3].", "citations": ["c3"], "insufficient_evidence": False})])
        out = run_agent("What is a bit?", llm, Ranked("r", ["c1"]), top_k=1, budget=1000)
        self.assertEqual(out["status"], "abstain")
        self.assertIn("dropped_invalid_citations", [e["event"] for e in out["events"]])

    def test_insufficient_evidence_abstains_without_citations(self):
        llm = FakeLLM([("search_documents", {"query": "fat32"}),
                       ("submit_answer", {"answer": "Not stated.", "citations": [], "insufficient_evidence": True})])
        out = run_agent("FAT32 max size?", llm, Ranked("r", ["c1"]), top_k=1, budget=1000)
        self.assertEqual((out["status"], out["citations"]), ("abstain", []))

    def test_search_limit_forces_submit_tool(self):
        llm = FakeLLM([("search_documents", {"query": "a"}), ("search_documents", {"query": "b"}),
                       ("submit_answer", {"answer": "x", "citations": [], "insufficient_evidence": True})])
        out = run_agent("q", llm, Ranked("r", ["c1"]), top_k=1, budget=1000, max_searches=2)
        self.assertEqual(out["n_searches"], 2)
        self.assertEqual(llm.calls[-1]["tools"], ["submit_answer"])

    def test_original_question_first_and_no_gold_in_messages(self):
        llm = FakeLLM([("submit_answer", {"answer": "A bit [c1].", "citations": ["c1"], "insufficient_evidence": False})])
        out = run_agent("What is a bit?", llm, Ranked("r", ["c1"]), top_k=1, budget=1000,
                        first_search="original_question", filters={"chapter": 5}, user_context="studying chapter 5")
        first = [e for e in out["events"] if e["event"] == "search"][0]
        self.assertTrue(first["forced"])
        self.assertEqual(first["query"], "What is a bit?")
        self.assertEqual(first["filter"], {"chapter": 5})
        sent = json.dumps(llm.calls[0]["messages"])
        self.assertNotIn("gold", sent)
        self.assertNotIn("expected_answer", sent)


class BenchmarkTests(unittest.TestCase):
    def test_benchmark_counts_and_no_overlap(self):
        qs = json.loads((ROOT / "benchmark/questions.json").read_text(encoding="utf-8"))
        un = json.loads((ROOT / "benchmark/unanswerable.json").read_text(encoding="utf-8"))
        count = lambda items, split: sum(q["split"] == split for q in items)
        self.assertGreaterEqual(count(qs, "dev"), 15)
        self.assertGreaterEqual(count(qs, "test"), 5)
        self.assertGreaterEqual(count(un, "dev"), 2)
        self.assertGreaterEqual(count(un, "test"), 2)
        dev_pages = {g["page"] for q in qs if q["split"] == "dev" for g in q["gold"]}
        test_pages = {g["page"] for q in qs if q["split"] == "test" for g in q["gold"]}
        self.assertFalse(dev_pages & test_pages, "test evidence pages must not be used by dev questions")


if __name__ == "__main__":
    unittest.main()

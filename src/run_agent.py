"""Run the real agent (OpenRouter LLM + real retriever) on one split for one config.

    python -m src.run_agent --config dense --split dev [--ids d01 ud02] [--workers 4]

Writes results/agent/<config>/<split>/:
  traces.json      one record per question (query_id, status, answer, citations, events, context, cost, latency)
  summary.json     automatic metrics (tool use, searches, Context Evidence Rate, status-based abstention, cost, time)
  review_sheet.md  compact sheet for manual labelling (expected answer shown to the grader only)
Gold is used only after the agent has finished, to compute Context Evidence Rate.
"""
from __future__ import annotations

import argparse
import statistics
import time
import traceback
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from . import config
from .agent import run_agent
from .llm import OpenRouterChat
from .metrics import context_has_evidence, first_hit_rank, latency_stats, ratio
from .retrieval import build_retriever


def load_split(split: str, ids: list[str] | None = None) -> list[dict]:
    qs = [q for q in config.load_json(config.BENCHMARK_DIR / "questions.json") if q["split"] == split]
    qs += [{**q, "answerable": False} for q in config.load_json(config.BENCHMARK_DIR / "unanswerable.json") if q["split"] == split]
    if ids:
        qs = [q for q in qs if q["id"] in ids]
    return qs


def run_one(q: dict, cfg: dict, llm, retriever) -> dict:
    filters = q.get("filter") if cfg.get("use_filter", True) else None
    base = {"query_id": q["id"], "split": q["split"], "config": cfg["name"], "model": llm.model,
            "question": q["question"], "filter": filters, "answerable": q.get("answerable", True)}
    t0 = time.perf_counter()
    try:
        out = run_agent(q["question"], llm, retriever, top_k=cfg["top_k"], budget=cfg["context"]["budget"],
                        context_mode=cfg["context"].get("mode", "skip"), max_searches=cfg["agent"]["max_searches"],
                        filters=filters, user_context=q.get("filter_context"),
                        first_search=cfg["agent"].get("first_search", "llm"))
    except Exception as e:  # provider / vector store failure: recorded, never replaced by a fake answer
        return {**base, "status": "error", "error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()[-1500:],
                "events": [], "citations": [], "answer": None, "latency_ms": round((time.perf_counter() - t0) * 1000, 1)}
    entries = out.pop("context_entries")
    record = {**base, **out}
    # ---- post-hoc gold checks (agent already finished) ----
    if record["answerable"]:
        record["context_hit"] = context_has_evidence(entries, q["gold"])
        searches = [e for e in record["events"] if e["event"] == "search"]
        if searches:
            chunks = {c["chunk"]["id"]: c["chunk"] for c in entries}
            first = [chunks.get(r["id"], {"source_id": None, "page": r["page"], "text": ""}) for r in searches[0]["results"]]
            rank = first_hit_rank(first, q["gold"]) if all(r["id"] in chunks for r in searches[0]["results"]) else None
            record["first_search_hit_rank"] = rank
        record["cited_evidence"] = any(c["chunk"]["id"] in record["citations"] and
                                       context_has_evidence([c], q["gold"]) for c in entries)
    record["cited_blocks"] = {c["chunk"]["id"]: c["block"] for c in entries if c["chunk"]["id"] in record["citations"]}
    return record


def summarise(cfg: dict, split: str, traces: list[dict], wall_s: float) -> dict:
    ok = [t for t in traces if t["status"] != "error"]
    ans = [t for t in traces if t["answerable"]]
    una = [t for t in traces if not t["answerable"]]
    s = {
        "config": cfg["name"], "split": split, "model": config.LLM_MODEL, "retrieval": cfg["retrieval"],
        "top_k": cfg["top_k"], "context": cfg["context"], "max_searches": cfg["agent"]["max_searches"],
        "first_search": cfg["agent"].get("first_search", "llm"),
        "N": len(traces), "answerable": len(ans), "unanswerable": len(una),
        "errors": len(traces) - len(ok), "error_ids": [t["query_id"] for t in traces if t["status"] == "error"],
        "status": dict(Counter(t["status"] for t in traces)),
        "tool_use": ratio(sum(any(e["event"] == "search" for e in t["events"]) for t in ok), len(ok)),
        "searches_distribution": dict(sorted(Counter(t.get("n_searches", 0) for t in ok).items())),
        "mean_searches": round(statistics.mean(t.get("n_searches", 0) for t in ok), 2) if ok else None,
        "mean_llm_calls": round(statistics.mean(t.get("llm_calls", 0) for t in ok), 2) if ok else None,
        "context_evidence_rate": ratio(sum(t.get("context_hit", False) for t in ans), len(ans)),
        "answers_citing_gold_chunk": ratio(sum(t.get("cited_evidence", False) for t in ans), len(ans)),
        "abstain_on_unanswerable_status": ratio(sum(t["status"] == "abstain" for t in una), len(una)),
        "false_abstention_status": ratio(sum(t["status"] == "abstain" for t in ans), len(ans)),
        "answered_with_citations": ratio(sum(bool(t["citations"]) for t in ok if t["status"] == "answered"),
                                         sum(t["status"] == "answered" for t in ok)),
        "avg_context_chars": round(statistics.mean(t.get("context_chars", 0) for t in ok), 1) if ok else None,
        "prompt_tokens": sum(t.get("prompt_tokens", 0) for t in ok),
        "completion_tokens": sum(t.get("completion_tokens", 0) for t in ok),
        "cost_usd": round(sum(t.get("cost_usd", 0.0) for t in ok), 5),
        "latency_ms_per_question": latency_stats([t["latency_ms"] for t in traces]),
        "wall_seconds": round(wall_s, 1),
        "note": "abstention/false-abstention here are status-based; answer grade, citation support and "
                "abstention correctness come from manual labels (reviews.json).",
    }
    s["cost_usd_per_question"] = round(s["cost_usd"] / len(ok), 6) if ok else None
    return s


def review_sheet(traces: list[dict], questions: dict[str, dict]) -> str:
    lines = [f"# Review sheet: {traces[0]['config']} / {traces[0]['split']}\n"]
    for t in traces:
        q = questions[t["query_id"]]
        lines.append(f"## {t['query_id']} ({'answerable' if t['answerable'] else 'UNANSWERABLE'}) | status={t['status']}"
                     f" | searches={t.get('n_searches')} | context_hit={t.get('context_hit')} | cited_gold_chunk={t.get('cited_evidence')}")
        lines.append(f"- Q: {q['question']}")
        lines.append(f"- Expected: {q.get('expected_answer') or q.get('absence_reason')}")
        lines.append(f"- Queries: {[e['query'] for e in t['events'] if e['event'] == 'search']}")
        lines.append(f"- Answer: {t.get('answer')}")
        lines.append(f"- Citations: {t.get('citations')}")
        if t.get("error"):
            lines.append(f"- ERROR: {t['error']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out-suffix", default="")
    args = ap.parse_args()
    cfg = config.load_config(args.config)
    questions = load_split(args.split, args.ids)
    llm = OpenRouterChat()
    t0 = time.perf_counter()
    retriever = build_retriever(cfg["retrieval"])
    print(f"retriever {retriever.name} ready in {time.perf_counter() - t0:.1f}s; {len(questions)} questions")
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        traces = list(pool.map(lambda q: run_one(q, cfg, llm, retriever), questions))
    wall = time.perf_counter() - t0
    out = config.RESULTS_DIR / "agent" / (cfg["name"] + args.out_suffix) / args.split
    summary = summarise(cfg, args.split, traces, wall)
    config.dump_json(out / "traces.json", traces)
    config.dump_json(out / "summary.json", summary)
    (out / "review_sheet.md").write_text(review_sheet(traces, {q["id"]: q for q in questions}), encoding="utf-8")
    for t in traces:
        flag = "" if t["status"] != "error" else f" ERROR {t['error'][:120]}"
        print(f"{t['query_id']:<5} {t['status']:<8} searches={t.get('n_searches')} ctx_hit={t.get('context_hit')} "
              f"cost={t.get('cost_usd')}{flag}")
    print({k: summary[k] for k in ("status", "tool_use", "context_evidence_rate", "abstain_on_unanswerable_status",
                                   "false_abstention_status", "cost_usd", "latency_ms_per_question", "errors")})


if __name__ == "__main__":
    main()

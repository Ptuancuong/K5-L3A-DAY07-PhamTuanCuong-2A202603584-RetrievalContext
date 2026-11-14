"""Retrieval-only benchmark on the ORIGINAL question (no LLM).

    python -m src.eval_retrieval --configs dense bm25 hybrid hybrid_rerank --split dev

For every answerable question: run the config's retriever once (top 10 kept for MRR),
report Hit@1, Evidence Hit@3 (same cutoff for every method), MRR@10 and the Context
Evidence Rate of the context packed from the config's top_k under its budget.
Writes results/retrieval/<config>/<split>/{traces,summary}.json and a markdown table.
"""
import argparse
import time

from . import config
from .context import ContextBuilder
from .metrics import context_has_evidence, first_hit_rank, is_hit, latency_stats, ratio
from .retrieval import build_retriever

DEPTH = 10


def evaluate(cfg: dict, questions: list[dict]) -> tuple[list[dict], dict]:
    started = time.perf_counter()
    retriever = build_retriever(cfg["retrieval"])
    setup_s = time.perf_counter() - started
    top_k, ctx_cfg = cfg["top_k"], cfg["context"]
    traces = []
    for q in questions:
        filters = q.get("filter") if cfg.get("use_filter", True) else None
        t0 = time.perf_counter()
        results = retriever.search(q["question"], filters=filters, top_k=max(DEPTH, top_k))
        ms = (time.perf_counter() - t0) * 1000
        ctx = ContextBuilder(ctx_cfg["budget"], ctx_cfg.get("mode", "skip"))
        ctx.add(results[:top_k])
        rank = first_hit_rank(results, q["gold"])
        traces.append({
            "query_id": q["id"], "split": q["split"], "type": q["type"], "question": q["question"],
            "filter": filters, "strategy": retriever.name, "top_k": top_k,
            "results": [{"id": r["id"], "page": r["page"], "rank": r["rank"], "score": round(r["score"], 5),
                         "hit": is_hit(r, q["gold"]), **({"component_ranks": r["component_ranks"]} if "component_ranks" in r else {}),
                         **({"base_rank": r["base_rank"]} if "base_rank" in r else {})} for r in results],
            "first_hit_rank": rank, "hit1": rank == 1, "hit3": rank is not None and rank <= 3,
            "context_ids": ctx.ids, "context_chars": ctx.used, "truncated": ctx.truncated, "skipped": ctx.skipped,
            "context_hit": context_has_evidence(ctx.entries, q["gold"]),
            "elapsed_ms": round(ms, 1),
            "gold": q["gold"],
        })
    n = len(traces)
    summary = {
        "config": cfg["name"], "strategy": retriever.name, "split": questions[0]["split"] if questions else None,
        "N": n, "top_k": top_k, "context": ctx_cfg,
        "hit1": sum(t["hit1"] for t in traces), "hit3": sum(t["hit3"] for t in traces),
        "mrr10": round(sum(1 / t["first_hit_rank"] for t in traces if t["first_hit_rank"]) / n, 3) if n else None,
        "context_hit": sum(t["context_hit"] for t in traces),
        "avg_context_chars": round(sum(t["context_chars"] for t in traces) / n, 1) if n else None,
        "latency_ms": latency_stats([t["elapsed_ms"] for t in traces]),
        "setup_seconds": round(setup_s, 1), "service_cost_usd": 0.0,
        "missed_at_3": [t["query_id"] for t in traces if not t["hit3"]],
    }
    for key in ("hit1", "hit3", "context_hit"):
        summary[key + "_str"] = ratio(summary[key], n)
    return traces, summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", nargs="+", required=True)
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    args = ap.parse_args()
    questions = [q for q in config.load_json(config.BENCHMARK_DIR / "questions.json") if q["split"] == args.split]
    rows = []
    for name in args.configs:
        cfg = config.load_config(name)
        traces, summary = evaluate(cfg, questions)
        out = config.RESULTS_DIR / "retrieval" / cfg["name"] / args.split
        config.dump_json(out / "traces.json", traces)
        config.dump_json(out / "summary.json", summary)
        rows.append(summary)
        print(f"{cfg['name']:<18} Hit@1 {summary['hit1_str']:<14} Hit@3 {summary['hit3_str']:<14} "
              f"MRR@10 {summary['mrr10']}  CER {summary['context_hit_str']:<14} "
              f"median {summary['latency_ms']['median']} ms  missed@3 {summary['missed_at_3']}")
    lines = ["| Config | Strategy | Hit@1 | Evidence Hit@3 | MRR@10 | Context Evidence Rate | Avg context chars | Median ms/query |",
             "|---|---|---|---|---|---|---|---|"]
    for s in rows:
        lines.append(f"| {s['config']} | {s['strategy']} | {s['hit1_str']} | {s['hit3_str']} | {s['mrr10']} | "
                     f"{s['context_hit_str']} | {s['avg_context_chars']} | {s['latency_ms']['median']} |")
    table = config.RESULTS_DIR / "retrieval" / f"table_{args.split}.md"
    table.parent.mkdir(parents=True, exist_ok=True)
    table.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"table -> {table.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()

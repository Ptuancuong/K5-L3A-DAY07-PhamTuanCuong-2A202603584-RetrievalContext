"""Build the dev comparison table and apply benchmark/selection_criteria.md mechanically.

    python -m src.select_config            # writes results/comparison_dev.md and configs/chosen.json

Criteria (committed before any run):
 1. constraints: abstention >= 2/3 and false abstention <= 3/26 on dev
 2. grounded answer mean (dev)       3. agent Context Evidence Rate (dev)
 4. retrieval Evidence Hit@3, then Hit@1 (original question)
 5. if two configs are within 1 question on BOTH 2 and 3 -> lower median latency, then cheaper, then simpler.
"""
import json

from . import config

AGENT = config.RESULTS_DIR / "agent"
RETR = config.RESULTS_DIR / "retrieval"


def row(cfg: str, split: str = "dev") -> dict:
    s = config.load_json(AGENT / cfg / split / "summary.json")
    m = config.load_json(AGENT / cfg / split / "agent_metrics.json")
    r = config.load_json(RETR / cfg / split / "summary.json")
    n_ans = s["answerable"]
    ctx_hit = int(s["context_evidence_rate"].split("/")[0])
    return {
        "config": cfg, "description": config.load_config(cfg)["description"], "retrieval": r,
        "hit1": r["hit1"], "hit3": r["hit3"], "mrr10": r["mrr10"], "N": r["N"],
        "grounded_sum": m["grounded_answer"]["1"] + 2 * m["grounded_answer"]["2"], "grounded_mean": m["grounded_answer"]["mean"],
        "g012": f"{m['grounded_answer']['0']}/{m['grounded_answer']['1']}/{m['grounded_answer']['2']}",
        "ctx_hit": ctx_hit, "n_ans": n_ans,
        "abst": m["abstention"]["n"], "abst_N": m["abstention"]["N"],
        "false_abst": m["false_abstention"]["n"], "false_abst_N": m["false_abstention"]["N"],
        "cit": f"{m['citation_validity']['n']}/{m['citation_validity']['N']}",
        "cov": f"{m['answer_citation_coverage']['n']}/{m['answer_citation_coverage']['N']}",
        "tool_use": f"{m['tool_use']['n']}/{m['tool_use']['N']}",
        "mean_searches": s["mean_searches"], "searches_dist": s["searches_distribution"], "mean_llm_calls": s["mean_llm_calls"],
        "median_ms": s["latency_ms_per_question"]["median"], "cost": s["cost_usd"], "cost_q": s["cost_usd_per_question"],
        "tokens": s["prompt_tokens"] + s["completion_tokens"], "avg_ctx": s["avg_context_chars"],
        "components": len(json.dumps(config.load_config(cfg)["retrieval"])) + len(json.dumps(config.load_config(cfg)["agent"])),
        "errors": s["errors"],
    }


def select(rows: list[dict]) -> tuple[dict, list[str]]:
    log = []
    ok = [r for r in rows if r["abst"] * 3 >= 2 * r["abst_N"] and r["false_abst"] <= 3]
    log.append(f"1. constraints pass: {[r['config'] for r in ok]}")
    best_g = max(r["grounded_sum"] for r in ok)
    best_c = max(r["ctx_hit"] for r in ok)
    # step 5 tie window: within 1 question (= 2 grade points for grounded sum, 1 hit for context) on BOTH 2 and 3
    near = [r for r in ok if best_g - r["grounded_sum"] <= 2 and best_c - r["ctx_hit"] <= 1]
    log.append(f"2-3. best grounded sum {best_g}, best context hits {best_c}; within 1 question on both: {[r['config'] for r in near]}")
    near.sort(key=lambda r: (r["median_ms"], r["cost"], r["components"]))
    log.append("5. tie-break by median latency, cost, simplicity: " +
               ", ".join(f"{r['config']} ({r['median_ms']} ms, {r['cost']} USD)" for r in near))
    return near[0], log


def table(rows: list[dict]) -> str:
    out = ["| Config | Hit@1 | Evidence Hit@3 | MRR@10 | Agent Context Evidence Rate | Grounded 0/1/2 (mean /2) | Citation hợp lệ | "
           "Abstention đúng | Từ chối nhầm | Lượt search TB | Median s/câu | Chi phí USD (29 câu) |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['config']} | {r['hit1']}/{r['N']} | {r['hit3']}/{r['N']} | {r['mrr10']} | {r['ctx_hit']}/{r['n_ans']} | "
                   f"{r['g012']} ({r['grounded_mean']:.3f}) | {r['cit']} | {r['abst']}/{r['abst_N']} | "
                   f"{r['false_abst']}/{r['false_abst_N']} | {r['mean_searches']} | {r['median_ms'] / 1000:.2f} | {r['cost']:.4f} |")
    return "\n".join(out)


def main() -> None:
    cfgs = ["dense", "bm25", "hybrid", "hybrid_rerank", "dense_origfirst", "dense_ctx6400",
            "dense_combo", "hybrid_combo", "hybrid_rerank_combo"]
    rows = [row(c) for c in cfgs]
    chosen, log = select(rows)
    md = ["# So sánh cấu hình trên dev (29 câu: 26 có đáp án + 3 thiếu evidence)", "",
          "- **Retrieval:** Hit@1, Evidence Hit@3 và MRR@10 tính trên **câu hỏi gốc**, chạy retrieval một lần (`src.eval_retrieval`).",
          "- **Agent:** các cột còn lại lấy từ lần chạy agent thật (`src.run_agent`), dùng `anthropic/claude-haiku-5.5` với `temperature=0`.",
          "- **Nhãn:** đọc thủ công (`src.labels`), sau đó tổng hợp bằng `starter/agent_metrics.py`.", "",
          table(rows), "", "## Áp dụng tiêu chí chọn ([benchmark/selection_criteria.md](../benchmark/selection_criteria.md))", ""]
    md += [f"- {line}" for line in log]
    md += ["", f"**Cấu hình được chọn: `{chosen['config']}`**: {chosen['description']}", ""]
    (config.RESULTS_DIR / "comparison_dev.md").write_text("\n".join(md), encoding="utf-8")
    cfg = config.load_config(chosen["config"])
    config.dump_json(config.CONFIG_DIR / "chosen.json", {**cfg, "name": "chosen", "chosen_from": chosen["config"],
                                                          "selection_log": log})
    print("\n".join(md))


if __name__ == "__main__":
    main()

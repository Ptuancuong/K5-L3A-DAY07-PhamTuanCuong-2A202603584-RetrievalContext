"""Manual review labels -> reviews.json (format of starter/agent_metrics.py) + aggregation.

    python -m src.labels --split dev
    python -m src.labels --split test

Labels were assigned after reading every answer next to the expected answer, and reading the
text of every cited chunk that does not itself contain the gold evidence
(`python -m src.compare_answers` and `python -m src.show_cited`). Default label for an answer
not listed below: grade 2 / citations supported / abstention correct. Every deviation is listed
explicitly with its reason. Labels were AI-drafted (Claude), then reviewed by the author and kept unchanged.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

from . import config

LABELED_BY = "author-reviewed (claude-opus-5.5 draft read answers + cited chunks; author reviewed all labels, kept unchanged)"

D15_ALT = ("correct: definition taken from p274 ('determining which process in the ready state should be moved to "
           "the running state'), equivalent to the gold 'choosing which process to run next'; p274 is not in the gold "
           "list, so retrieval/context metrics count it as a miss")

# (config, split, query_id) -> overrides. answer_grade for answerable, abstention_correct for unanswerable,
# citation_support: dict citation_id -> bool for unsupported citations.
OVERRIDES: dict[tuple[str, str, str], dict] = {
    ("dense", "dev", "d01"): {"answer_grade": 0, "reason": "false abstention: the LLM's rewritten queries never retrieved p205:c1 (original question ranks it #1), and the 3200-char budget was full after search 1"},
    ("dense", "dev", "d19"): {"answer_grade": 1, "reason": "partially correct: says flash has lower latency (supported by p288) but gives no numbers and claims none exist; gold p293:c2 (10 ms vs 100 us) never retrieved by the rewritten queries"},
    ("bm25", "dev", "d09"): {"answer_grade": 0, "reason": "false abstention: search 2 ranked gold p264:c0 #1 but it was not included because search 1 filled the 3200-char budget (skip mode)"},
    ("dense_origfirst", "dev", "d24"): {"answer_grade": 0, "reason": "false abstention: original question misses p253:c0 in top-3; search 2 ranked it #1 but the budget (2989/3200 chars used) dropped it"},
    ("dense_ctx6400", "dev", "d19"): {"answer_grade": 1, "reason": "partially correct: qualitative comparison supported by p233/p288, but no 10 ms vs 100 us figures and wrongly states the sources give no numbers"},
}
for cfg in ("dense", "bm25", "hybrid", "dense_origfirst", "dense_ctx6400", "dense_combo", "hybrid_combo", "hybrid_rerank_combo"):
    OVERRIDES.setdefault((cfg, "dev", "d15"), {"answer_grade": 2, "reason": D15_ALT})

# Test split: every one of the 22 answers was read; the only deviation from the default:
OVERRIDES[("dense", "test", "t03")] = {
    "answer_grade": 2,
    "citation_support": {"B:openstax-intro-cs:p228:c2": False},
    "reason": "answer correct and supported by p229:c0 (gold); the second sentence ('several technologies are combined in a "
              "memory hierarchy') cites only p228:c2, which says no single technology excels but not that they are combined "
              "in a hierarchy (that is p229:c0) -> p228:c2 counted as not supporting (strict)",
}

# Manual context grade on test (BENCHMARK.md section 2): 0 = no evidence, 1 = evidence but missing condition/source,
# 2 = full evidence with source and page. Read for all 8 answerable test questions of both configs: in every case the
# full gold sentence (including the condition for t02/t07) is in the final context with its [id | source | page] header.
CONTEXT_GRADE_DEFAULT = (2, "full gold evidence sentence present in the final context with id, source and page header")


def build_reviews(cfg: str, split: str) -> list[dict]:
    traces = config.load_json(config.RESULTS_DIR / "agent" / cfg / split / "traces.json")
    reviews = []
    for t in traces:
        if t["status"] == "error":
            continue
        o = OVERRIDES.get((cfg, split, t["query_id"]), {})
        support = o.get("citation_support", {})
        r = {"query_id": t["query_id"], "citation_support": [support.get(c, True) for c in t["citations"]],
             "labeled_by": LABELED_BY}
        if t["answerable"]:
            grade = o.get("answer_grade", 0 if t["status"] == "abstain" else 2)
            if t["status"] == "abstain" and grade != 0:
                raise ValueError(f"{cfg}/{t['query_id']}: abstain must be graded 0")
            r["answer_grade"] = grade
            r["reason"] = o.get("reason") or ("correct and complete; cited chunk(s) contain the gold evidence"
                                              if t.get("cited_evidence") else "REVIEW: no default reason")
            if split == "test":
                if not t.get("context_hit"):
                    raise ValueError(f"{cfg}/{t['query_id']}: context grade needs an explicit label")
                r["context_grade"], r["context_reason"] = CONTEXT_GRADE_DEFAULT
        else:
            r["abstention_correct"] = o.get("abstention_correct", t["status"] == "abstain")
            r["reason"] = o.get("reason") or ("searched, abstained and named what is missing; no unsupported claim"
                                              if t["status"] == "abstain" else "REVIEW: answered an unanswerable question")
        if "REVIEW" in r["reason"]:
            raise ValueError(f"{cfg}/{t['query_id']}: needs an explicit label ({r['reason']})")
        reviews.append(r)
    return reviews


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    ap.add_argument("--configs", nargs="*")
    args = ap.parse_args()
    root = config.RESULTS_DIR / "agent"
    cfgs = args.configs or sorted(p.name for p in root.iterdir() if (p / args.split / "traces.json").exists())
    for cfg in cfgs:
        out = root / cfg / args.split
        config.dump_json(out / "reviews.json", build_reviews(cfg, args.split))
        # Official aggregation with the starter script (labels in, numbers out).
        res = subprocess.run([sys.executable, str(config.ROOT / "starter" / "agent_metrics.py"),
                              "--cases", str(config.BENCHMARK_DIR / "cases.json"), "--traces", str(out / "traces.json"),
                              "--reviews", str(out / "reviews.json"), "--split", args.split,
                              "--output", str(out / "agent_metrics.json")], capture_output=True, text=True, encoding="utf-8")
        if res.returncode:
            raise RuntimeError(f"{cfg}: agent_metrics failed\n{res.stderr}")
        m = json.loads((out / "agent_metrics.json").read_text(encoding="utf-8"))
        g = m["grounded_answer"]
        print(f"{cfg:<20} grounded 0/1/2={g['0']}/{g['1']}/{g['2']} mean={g['mean']:.3f}  "
              f"citations {m['citation_validity']['n']}/{m['citation_validity']['N']}  "
              f"abstention {m['abstention']['n']}/{m['abstention']['N']}  false_abst {m['false_abstention']['n']}/{m['false_abstention']['N']}")


if __name__ == "__main__":
    main()

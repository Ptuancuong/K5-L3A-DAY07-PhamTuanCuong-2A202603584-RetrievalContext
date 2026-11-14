"""Print a side-by-side sheet of agent answers across configs (for manual labelling).

    python -m src.compare_answers --split dev --configs dense bm25 hybrid hybrid_rerank [--cited]
"""
import argparse

from . import config
from .run_agent import load_split


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True)
    ap.add_argument("--configs", nargs="+", required=True)
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--cited", action="store_true", help="also print the text of cited blocks")
    args = ap.parse_args()
    runs = {c: {t["query_id"]: t for t in config.load_json(config.RESULTS_DIR / "agent" / c / args.split / "traces.json")}
            for c in args.configs}
    for q in load_split(args.split, args.ids):
        print(f"\n=== {q['id']} [{q['type']}] {q['question']}")
        print(f"    EXPECTED: {q.get('expected_answer') or 'ABSTAIN - ' + q.get('absence_reason', '')}")
        for c in args.configs:
            t = runs[c].get(q["id"])
            if not t:
                continue
            cites = ",".join(x.split(":")[-2] + ":" + x.split(":")[-1] for x in t["citations"])
            print(f"  - {c:<14} {t['status']:<8} s={t.get('n_searches')} ctx={str(t.get('context_hit'))[0]} "
                  f"citeGold={str(t.get('cited_evidence'))[0]} [{cites}] :: {t.get('answer')}")
            if args.cited:
                for cid, block in t.get("cited_blocks", {}).items():
                    print(f"        >> {block[:700]!r}")


if __name__ == "__main__":
    main()

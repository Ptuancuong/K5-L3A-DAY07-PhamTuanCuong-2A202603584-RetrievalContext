"""Print, once each, the text of cited chunks that do NOT contain the gold evidence
(those citations need a human read to decide whether they support the answer).

    python -m src.show_cited --split dev --configs dense bm25 hybrid hybrid_rerank
"""
import argparse

from . import config
from .metrics import is_hit
from .run_agent import load_split


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", required=True)
    ap.add_argument("--configs", nargs="+", required=True)
    args = ap.parse_args()
    chunks = {c["id"]: c for c in config.load_json(config.chunks_path("B"))}
    qs = {q["id"]: q for q in load_split(args.split)}
    needed: dict[str, list[str]] = {}
    for c in args.configs:
        for t in config.load_json(config.RESULTS_DIR / "agent" / c / args.split / "traces.json"):
            gold = qs[t["query_id"]].get("gold", [])
            for cid in t["citations"]:
                if not (gold and is_hit(chunks[cid], gold)):
                    needed.setdefault(cid, []).append(f"{c}:{t['query_id']}")
    for cid, users in sorted(needed.items()):
        print(f"\n### {cid}  (cited by {', '.join(users)})\n{chunks[cid]['text']}")


if __name__ == "__main__":
    main()

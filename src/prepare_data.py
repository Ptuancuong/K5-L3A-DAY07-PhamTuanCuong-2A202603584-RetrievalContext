"""Export Day 6 chunks from pgvector and build the Day 7 benchmark.

    python -m src.prepare_data

Outputs
  data/day6/chunks_{A,B}.json      chunk contract of data/README.md (id, text, source_id, source, page, metadata)
  benchmark/questions.json         answerable questions with `gold` alternatives (baseline.py contract)
  benchmark/unanswerable.json      questions without evidence (search_and_abstain)
  benchmark/cases.json             id/split/answerable for starter/agent_metrics.py

Day 6 test questions were already evaluated (and one failure, old t03, analysed in the
Day 6 report), so they move to dev (new ids d16-d21); the Day 7 test set is new.
"""
import json
import sys

import psycopg

from . import config

ROOT = config.ROOT
sys.path.insert(0, str(ROOT / "starter"))
from baseline import validate  # noqa: E402  (reuse the starter's contract checks)


def export_chunks(index: str) -> list[dict]:
    if not config.DATABASE_URL:
        raise RuntimeError("DATABASE_URL missing in .env")
    with psycopg.connect(config.DATABASE_URL, connect_timeout=5) as conn:
        rows = conn.execute(
            "SELECT chunk_id, document_id, source, page, chapter, section, section_title, char_start, char_end, text, model "
            "FROM chunks WHERE strategy = %s ORDER BY page, char_start", (index,)).fetchall()
    if not rows:
        raise RuntimeError(f"no chunks for strategy {index} in the Day 6 store")
    chunks = []
    for cid, doc, source, page, chapter, section, title, cs, ce, text, model in rows:
        chunks.append({"id": cid, "text": text, "source_id": doc, "source": source, "page": page,
                       "metadata": {"chapter": chapter, "section": section, "section_title": title,
                                    "char_start": cs, "char_end": ce, "index": index, "embedding_model": model}})
    return chunks


def load_pages() -> dict[int, str]:
    pages = {}
    for line in (config.DAY6_DIR / "data" / "pages.jsonl").read_text(encoding="utf-8").splitlines():
        p = json.loads(line)
        pages[p["page"]] = p["text"]
    return pages


def _literal(quote: str, page_text: str) -> str | None:
    """Return the quote exactly as it appears in the page (Day 6 quotes may use ' for the PDF's U+2019)."""
    for candidate in (quote, quote.replace("'", "’")):
        if candidate in page_text:
            return candidate
    return None


def convert_day6_questions(pages: dict[int, str]) -> list[dict]:
    """Day 6 stores gold_page/evidence_quote as lists; keep only (page, quote) pairs that exist."""
    out = []
    for line in config.DAY6_QUESTIONS.read_text(encoding="utf-8").splitlines():
        q = json.loads(line)
        gold = []
        for page in q["gold_page"]:
            for quote in q["evidence_quote"]:
                literal = _literal(quote, pages.get(page, ""))
                if literal:
                    gold.append({"source_id": q["gold_source_id"], "page": page, "evidence": literal})
        if not gold:
            raise ValueError(f"{q['id']}: no evidence quote found on its gold pages")
        new_id = q["id"]
        if q["split"] == "test":  # Day 6 test -> Day 7 dev
            new_id = f"d{15 + int(q['id'][1:]):02d}"
        item = {"id": new_id, "split": "dev", "type": q["type"], "origin": f"day6:{q['id']}",
                "question": q["question"], "expected_answer": q["expected_answer"], "gold": gold}
        if q.get("filter"):
            item["filter"] = q["filter"]
            item["filter_context"] = q.get("filter_context", "User-supplied chapter scope (Day 6 benchmark)")
        out.append(item)
    return out


def main() -> None:
    for index in ("A", "B"):
        chunks = export_chunks(index)
        config.dump_json(config.chunks_path(index), chunks)
        print(f"exported {len(chunks)} chunks for index {index} -> {config.chunks_path(index).relative_to(ROOT)}")

    pages = load_pages()
    authored = config.load_json(config.BENCHMARK_DIR / "authored_questions.json")
    answerable = convert_day6_questions(pages) + [q for q in authored if q.get("answerable", True)]
    unanswerable = [q for q in authored if q.get("answerable", True) is False]

    ids = [q["id"] for q in answerable + unanswerable]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate question ids")
    # Every evidence must lie entirely inside one chunk of the evaluated index (B).
    chunks_b = config.load_json(config.chunks_path("B"))
    validate(chunks_b, answerable)
    for q in answerable:
        for g in q["gold"]:
            if g["evidence"] not in pages[g["page"]]:
                raise ValueError(f"{q['id']}: evidence not on page {g['page']}")
    for q in unanswerable:
        for key in ("absence_reason", "check_method"):
            if not q.get(key):
                raise ValueError(f"{q['id']}: missing {key}")

    config.dump_json(config.BENCHMARK_DIR / "questions.json", answerable)
    config.dump_json(config.BENCHMARK_DIR / "unanswerable.json", unanswerable)
    cases = [{"id": q["id"], "split": q["split"], "answerable": q.get("answerable", True),
              "expected_behavior": q.get("expected_behavior", "search_and_answer")} for q in answerable + unanswerable]
    config.dump_json(config.BENCHMARK_DIR / "cases.json", cases)

    for split in ("dev", "test"):
        a = sum(q["split"] == split for q in answerable)
        u = sum(q["split"] == split for q in unanswerable)
        print(f"{split}: {a} answerable + {u} unanswerable = {a + u}")
    print("Benchmark check passed.")


if __name__ == "__main__":
    main()

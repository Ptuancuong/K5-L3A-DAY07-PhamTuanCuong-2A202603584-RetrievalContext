"""Paths, environment and fixed experiment settings (single source of truth)."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_env(path: Path) -> None:
    """Minimal .env loader (no dependency); real environment variables win."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env(ROOT / ".env")

# Day 6 output reused by Day 7 (corpus text, benchmark, pgvector store).
DAY6_DIR = Path(os.getenv(
    "DAY6_DIR",
    str(ROOT.parent.parent / "VinUni Lab Day06" / "K5-L3A-DAY06-PhamTuanCuong-2A202603584-DataIngestion"),
))
DAY6_QUESTIONS = DAY6_DIR / "benchmark" / "questions.jsonl"

DATABASE_URL = os.getenv("DATABASE_URL", "")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
EMBEDDING_DIM = 384
# Day 6 chose strategy C = index B (paragraph chunks, max 1000 chars) + chapter filter.
DAY6_INDEX = os.getenv("DAY6_INDEX", "B")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "anthropic/claude-haiku-5.5")
RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

DATA_DIR = ROOT / "data" / "day6"
BENCHMARK_DIR = ROOT / "benchmark"
CONFIG_DIR = ROOT / "configs"
RESULTS_DIR = ROOT / "results"


def chunks_path(index: str = DAY6_INDEX) -> Path:
    return DATA_DIR / f"chunks_{index}.json"


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump_json(path: Path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_config(name_or_path: str) -> dict:
    p = Path(name_or_path)
    if not p.suffix:
        p = CONFIG_DIR / f"{name_or_path}.json"
    cfg = load_json(p)
    cfg.setdefault("name", p.stem)
    return cfg

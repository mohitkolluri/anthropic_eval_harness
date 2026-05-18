from __future__ import annotations

import json
from pathlib import Path

from src.eval.graders.base import EvalCase

_REQUIRED_KEYS = {"id", "input", "expected", "metadata"}
_REQUIRED_METADATA = {"category", "difficulty", "requires_search", "version"}


def load_suite(path: str | Path, limit: int | None = None) -> list[EvalCase]:
    """Load and validate eval cases from a JSONL file."""
    cases: list[EvalCase] = []
    src = Path(path)
    if not src.exists():
        raise FileNotFoundError(f"Eval suite not found: {src}")

    with src.open() as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {lineno}: {e}") from e

            missing = _REQUIRED_KEYS - obj.keys()
            if missing:
                raise ValueError(f"Line {lineno} (id={obj.get('id','?')}) missing keys: {missing}")

            meta_missing = _REQUIRED_METADATA - obj["metadata"].keys()
            if meta_missing:
                raise ValueError(f"Line {lineno} (id={obj['id']}) missing metadata keys: {meta_missing}")

            cases.append(EvalCase(
                id=obj["id"],
                input=obj["input"],
                expected=obj["expected"],
                metadata=obj["metadata"],
            ))

            if limit and len(cases) >= limit:
                break

    return cases

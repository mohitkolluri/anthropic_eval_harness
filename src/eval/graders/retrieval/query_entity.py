from __future__ import annotations

import json
import re

from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace

_JUDGE_SYSTEM = "You are a strict evaluator of Wikipedia search queries. Return only valid JSON."

_JUDGE_PROMPT = """\
Classify this Wikipedia search query as either "entity" or "fragment".

ENTITY (pass) — a noun phrase that maps directly to a Wikipedia article or category:
  "Mount Everest", "French Revolution", "Boiling point",
  "List of deserts by area", "Alexander Graham Bell", "Ikigai"

FRAGMENT (fail) — a rephrased question, keyword soup, or descriptive phrase:
  "boiling point of water at high altitude",
  "largest desert world", "how long did the war last",
  "highest women's ODI score cricket", "records broken by Michael"

Query to evaluate: "{query}"

Return JSON only — no other text:
{{"verdict": "entity" | "fragment", "reason": "<one sentence explaining why>"}}"""


class QueryEntityAdherenceGrader(Grader):
    rubric_id = "query_entity_adherence"
    category = "retrieval"
    version = "V0"
    threshold = 0.7

    def __init__(self, judge_client=None):
        self._judge_client = judge_client

    def _judge_query(self, query: str) -> tuple[float, str]:
        """Return (score, reason) for a single query. 1.0 = entity, 0.0 = fragment."""
        response = self._judge_client.complete(
            system=_JUDGE_SYSTEM,
            messages=[{"role": "user", "content": _JUDGE_PROMPT.format(query=query)}],
            tools=None,
        )
        raw = (response.get("content") or "").strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        try:
            data = json.loads(raw)
            verdict = data.get("verdict", "").lower()
            reason = data.get("reason", "no reason given")
            return (1.0 if verdict == "entity" else 0.0), reason
        except (json.JSONDecodeError, AttributeError):
            return 0.0, f"judge returned unparseable response: {raw[:100]}"

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        if trace.total_tool_calls == 0:
            return self._skip("no tool calls made — nothing to evaluate")

        scores: list[float] = []
        notes: list[str] = []

        for tc in trace.tool_calls:
            score, reason = self._judge_query(tc.query)
            verdict = "entity" if score == 1.0 else "fragment"
            scores.append(score)
            notes.append(f'"{tc.query}" → {verdict}: {reason}')

        final_score = sum(scores) / len(scores)
        return self._result(score=final_score, reasoning=" | ".join(notes))

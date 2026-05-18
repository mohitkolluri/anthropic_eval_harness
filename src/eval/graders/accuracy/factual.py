from __future__ import annotations

import json
import re

from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace

_JUDGE_SYSTEM = "You are a strict factual accuracy evaluator. Return only valid JSON."

_JUDGE_PROMPT = """\
Evaluate the factual accuracy of the agent's answer against the reference answer.

Question: "{question}"
Reference answer: "{reference_answer}"
Agent's answer: "{agent_answer}"

Score from 0.0 to 1.0:
  1.0 — fully correct, all key facts match the reference
  0.7 — mostly correct, minor omissions or slight inaccuracies
  0.5 — partially correct, some key facts right but others wrong or missing
  0.3 — mostly incorrect, only minor elements are right
  0.0 — completely wrong, or refuses to answer when it should have answered

Focus only on factual correctness — do not penalise for phrasing or length differences.

Return JSON only:
{{"score": <0.0|0.3|0.5|0.7|1.0>, "reason": "<one sentence>"}}"""


class FactualAccuracyGrader(Grader):
    rubric_id = "factual_accuracy"
    category = "accuracy"
    version = "V0"
    threshold = 0.7

    def __init__(self, judge_client=None):
        self._judge_client = judge_client

    def _marker_score(self, output: str, markers: list[str]) -> tuple[float, str]:
        """Case-insensitive check: fraction of markers present in output."""
        output_lower = output.lower()
        found = [m for m in markers if m.lower() in output_lower]
        score = len(found) / len(markers) if markers else 0.0
        missing = [m for m in markers if m.lower() not in output_lower]
        reason = (
            f"all {len(markers)} markers found"
            if not missing
            else f"{len(found)}/{len(markers)} markers found; missing: {missing}"
        )
        return score, reason

    def _llm_score(self, question: str, reference: str, agent_answer: str) -> tuple[float, str]:
        """LLM-as-judge: score agent answer against reference answer."""
        prompt = _JUDGE_PROMPT.format(
            question=question,
            reference_answer=reference,
            agent_answer=agent_answer,
        )
        response = self._judge_client.complete(
            system=_JUDGE_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
            tools=None,
        )
        raw = (response.get("content") or "").strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw.strip())
        try:
            data = json.loads(raw)
            score = float(data.get("score", 0.0))
            reason = data.get("reason", "no reason given")
            return score, reason
        except (json.JSONDecodeError, AttributeError, ValueError):
            return 0.0, f"judge returned unparseable response: {raw[:100]}"

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        output = trace.output

        if not output:
            return self._error("trace.output is empty — agent produced no answer")

        difficulty = case.metadata.get("difficulty", "hard")
        markers = case.expected.get("answer_markers", [])
        reference = case.expected.get("reference_answer")

        # Marker path — fast, rule-based, for easy cases with markers defined
        if difficulty == "easy" and markers:
            score, reason = self._marker_score(output, markers)
            return self._result(score=score, reasoning=reason)

        # LLM-judge path — for medium/hard cases
        if not reference:
            return self._error(
                "expected.reference_answer is missing — required for LLM-judge on non-easy cases"
            )

        score, reason = self._llm_score(
            question=trace.input,
            reference=reference,
            agent_answer=output,
        )
        return self._result(score=score, reasoning=reason)

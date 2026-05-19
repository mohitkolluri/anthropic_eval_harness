from __future__ import annotations
import json
import re
from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace

_SYSTEM_PROMPT = "You are a strict grounding evaluator. Return only valid JSON."

_USER_PROMPT_TEMPLATE = """\
Evaluate whether the agent's answer is fully grounded in the retrieved Wikipedia content.

Retrieved Wikipedia content:
{retrieved_content}

Agent's answer:
{agent_answer}

Every factual claim in the answer must be directly traceable to the retrieved content above.
The agent must NOT add facts from its own knowledge that are not in the retrieved content.

Score from 0.0 to 1.0:
  1.0 — every claim is directly supported by the retrieved content
  0.7 — mostly grounded, one minor unsupported detail
  0.5 — some claims grounded, but notable facts added beyond the retrieved content
  0.3 — majority of claims are not supported by the retrieved content
  0.0 — answer is largely or entirely based on the agent's own knowledge, not the retrieved content

Return JSON only:
{{"score": <0.0|0.3|0.5|0.7|1.0>, "reason": "<one sentence>"}}\
"""

_MAX_RETRIEVED_CHARS = 6000


class GroundednessGrader(Grader):
    rubric_id = "groundedness"
    category = "accuracy"
    version = "V0"
    threshold = 0.8

    def __init__(self, judge_client=None):
        self._judge_client = judge_client

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        """
        Strict grounding: every factual claim in trace.output must be traceable to
        content in trace.tool_calls[*].fetched_content.
        Skip (return _skip) if trace.total_tool_calls == 0.
        LLM-as-judge: given the retrieved content and the answer, are all factual
        claims supported? Returns 0.0–1.0.
        """
        # Only fetch_wikipedia calls contain actual page content to ground against
        fetch_calls = [tc for tc in trace.tool_calls if tc.content_source.startswith("page/")]

        if not fetch_calls:
            return self._skip("no fetch_wikipedia calls — nothing was retrieved to ground against")

        if not trace.output:
            return self._error("trace.output is empty")

        retrieved_parts = [tc.fetched_content for tc in fetch_calls if tc.fetched_content]

        # Truncate each article to an equal share of the budget so every
        # retrieved source is represented — avoids silently dropping later
        # articles when a single article fills the entire character budget.
        n = len(retrieved_parts)
        per_article = _MAX_RETRIEVED_CHARS // n if n else _MAX_RETRIEVED_CHARS
        truncated = [part[:per_article] for part in retrieved_parts]
        combined_retrieved = "\n\n---\n\n".join(truncated)

        user_prompt = _USER_PROMPT_TEMPLATE.format(
            retrieved_content=combined_retrieved,
            agent_answer=trace.output,
        )

        response = self._judge_client.complete(
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
            tools=None,
        )
        raw = (response.get("content") or "").strip()

        # Strip markdown code fences
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip())

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            return self._result(0.0, f"judge returned unparseable response: {raw[:100]}")

        score = float(parsed["score"])
        reasoning = parsed["reason"]
        return self._result(score, reasoning)

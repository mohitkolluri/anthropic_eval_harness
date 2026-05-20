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
        search_calls = [tc for tc in trace.tool_calls if tc.content_source == "search_candidates"]
        fetch_calls  = [tc for tc in trace.tool_calls if tc.content_source.startswith("page/")]

        if not search_calls and not fetch_calls:
            return self._skip("no tool calls made — nothing was retrieved to ground against")

        if not trace.output:
            return self._error("trace.output is empty")

        retrieved_parts: list[str] = []

        # Search results — the agent can answer from description/excerpt fields
        # without fetching the full page, so include them as retrieved content.
        for tc in search_calls:
            pages = tc.api_response.get("pages", [])
            if pages:
                lines = [f"Search results for '{tc.query}':"]
                for p in pages:
                    title   = p.get("title", "")
                    desc    = p.get("description") or ""
                    excerpt = re.sub(r"<[^>]+>", "", p.get("excerpt") or "")[:200]
                    lines.append(f"  [{title}] {desc} — {excerpt}")
                retrieved_parts.append("\n".join(lines))

        # Fetched page content — full article text (proportionally truncated)
        fetch_texts = [tc.fetched_content for tc in fetch_calls if tc.fetched_content]
        if fetch_texts:
            fetch_budget = _MAX_RETRIEVED_CHARS - sum(len(p) for p in retrieved_parts)
            per_article  = max(500, fetch_budget // len(fetch_texts))
            for text in fetch_texts:
                retrieved_parts.append(text[:per_article])

        if not retrieved_parts:
            return self._skip("all tool calls returned empty content — nothing to ground against")

        combined_retrieved = "\n\n---\n\n".join(retrieved_parts)

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

from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace


class ToolUseAppropriatenessGrader(Grader):
    rubric_id = "tool_use_appropriateness"
    category = "retrieval"
    version = "V0"
    threshold = 0.7

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        requires_search: bool = case.metadata.get("requires_search", False)
        max_calls: int | None = case.expected.get("max_search_calls")

        # Count only fetch_wikipedia calls against the limit — these are actual retrievals.
        # search_wikipedia calls (candidate discovery) are not counted since the agent
        # must always search before it can fetch.
        fetch_calls = [tc for tc in trace.tool_calls if tc.content_source.startswith("page/")]
        actual_calls: int = len(fetch_calls)

        # Presence check uses total tool calls to detect any search activity
        any_tool_calls: int = trace.total_tool_calls

        # Guard: max_search_calls is required when requires_search=True
        if requires_search and max_calls is None:
            return self._error(
                "expected.max_search_calls is missing but requires_search=True — "
                "cannot evaluate call count without a limit to check against"
            )

        # Sub-score 1 — Presence (uses total tool calls — any activity counts)
        if requires_search and any_tool_calls == 0:
            presence = 0.0
            presence_note = "required search but made no tool calls"
        elif not requires_search and any_tool_calls > 0:
            presence = 0.0
            presence_note = f"should not have searched but made {any_tool_calls} tool call(s)"
        else:
            presence = 1.0
            presence_note = "search presence correct"

        # If requires_search=False, presence is the only check
        if not requires_search:
            return self._result(
                score=presence,
                reasoning=presence_note,
            )

        # Sub-score 2 — Count: fetch_wikipedia calls vs max_search_calls limit
        # If presence already failed (no calls made), count is also 0
        if actual_calls == 0:
            count = 0.0
            count_note = "no fetch calls made — count check not applicable"
        elif actual_calls <= max_calls:
            count = 1.0
            count_note = f"{actual_calls}/{max_calls} calls — within limit"
        else:
            excess = actual_calls - max_calls
            count = max(0.0, 1.0 - (excess / max_calls))
            count_note = f"{actual_calls}/{max_calls} calls — {excess} over limit (score penalised to {count:.2f})"

        score = (presence + count) / 2
        reasoning = f"Presence: {presence:.1f} ({presence_note}). Count: {count:.2f} ({count_note})."

        return self._result(score=score, reasoning=reasoning)

from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace


class ToolUseAppropriatenessGrader(Grader):
    rubric_id = "tool_use_appropriateness"
    category = "retrieval"
    version = "V0"
    threshold = 0.7

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        """
        Composite check — two sub-scores averaged:

        1. Presence (rule): requires_search=True and no tool calls → 0.0;
           requires_search=False and tool calls made → 0.0; else 1.0

        2. Count (rule): tool calls <= expected.max_search_calls → 1.0;
           else 1.0 - (excess / max_search_calls) clamped to [0, 1]

        Final score = mean of the two sub-scores.
        Skip sub-score 2 if requires_search=False.

        Note: query content quality (entity-based vs. question fragment) is
        evaluated separately by QueryEntityAdherenceGrader.
        """
        raise NotImplementedError

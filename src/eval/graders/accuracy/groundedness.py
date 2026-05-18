from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace


class GroundednessGrader(Grader):
    rubric_id = "groundedness"
    category = "accuracy"
    version = "V0"
    threshold = 0.8

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        """
        Strict grounding: every factual claim in trace.output must be traceable to
        content in trace.tool_calls[*].fetched_content.
        Skip (return _skip) if trace.total_tool_calls == 0.
        LLM-as-judge: given the retrieved content and the answer, are all factual
        claims supported? Returns 0.0–1.0.
        """
        raise NotImplementedError

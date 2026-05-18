from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace


class FactualAccuracyGrader(Grader):
    rubric_id = "factual_accuracy"
    category = "accuracy"
    version = "V0"
    threshold = 0.7

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        """
        Two-path grading:
        - If case.metadata.difficulty == 'easy' and case.expected.answer_markers exists:
          check all markers are present in trace.output (case-insensitive). Score = 1.0 if all
          present, else fraction present.
        - Otherwise: LLM-as-judge comparing trace.output to case.expected.reference_answer.
          Judge prompt asks: is this answer factually correct? Returns 0.0–1.0.
        """
        raise NotImplementedError

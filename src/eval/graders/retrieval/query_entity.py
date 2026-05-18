from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace


class QueryEntityAdherenceGrader(Grader):
    rubric_id = "query_entity_adherence"
    category = "retrieval"
    version = "V0"
    threshold = 0.7

    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        """
        LLM-judge: for each search query made, was it an entity name or Wikipedia
        article title rather than a question fragment or keyword soup?

        GOOD queries (entity-based):
          "Mount Everest", "Boiling point", "Hundred Years War",
          "List of deserts by area", "Women's One Day International cricket"

        BAD queries (question fragments / keyword soup):
          "boiling point water Everest", "largest desert world",
          "highest women's ODI score cricket", "how long did the war last"

        Scoring:
          - Score each query independently: 1.0 if entity-based, 0.0 if fragment.
          - Final score = mean across all queries made.
          - Skip (return _skip) if trace.total_tool_calls == 0 — nothing to evaluate.

        Judge prompt must ask: "Is this query a named entity, Wikipedia article title,
        or category/list article? Or is it a rephrased question or keyword combination?"
        """
        raise NotImplementedError

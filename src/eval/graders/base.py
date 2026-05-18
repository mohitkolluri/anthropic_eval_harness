from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any


@dataclass
class ToolCallRecord:
    call_index: int
    query: str
    api_response: dict        # raw pages list from search endpoint
    fetched_content: str      # stripped plain text of the fetched page
    content_source: str       # e.g. "page/Eiffel_Tower/with_html (stripped)"


@dataclass
class Trace:
    eval_id: str
    run_id: str
    prompt_version: str
    model: str
    input: str
    conversation: list[dict]
    tool_calls: list[ToolCallRecord]
    output: str
    total_tool_calls: int
    latency_ms: int
    error: str | None = None


@dataclass
class EvalCase:
    id: str
    input: str
    expected: dict            # answer_markers, reference_answer, max_search_calls, should_refuse
    metadata: dict            # category, difficulty, requires_search, version


@dataclass
class GraderResult:
    grader: str
    category: str
    score: float | None       # None if skipped or errored
    passed: bool | None       # None if skipped or errored
    threshold: float
    reasoning: str | None
    skipped: bool = False
    skip_reason: str | None = None
    error: bool = False
    error_reason: str | None = None


class Grader(ABC):
    rubric_id: str
    category: str
    version: str
    threshold: float

    @abstractmethod
    def eval(self, case: EvalCase, trace: Trace) -> GraderResult:
        ...

    def _skip(self, reason: str) -> GraderResult:
        return GraderResult(
            grader=self.rubric_id,
            category=self.category,
            score=None,
            passed=None,
            threshold=self.threshold,
            reasoning=None,
            skipped=True,
            skip_reason=reason,
        )

    def _error(self, reason: str) -> GraderResult:
        return GraderResult(
            grader=self.rubric_id,
            category=self.category,
            score=None,
            passed=None,
            threshold=self.threshold,
            reasoning=None,
            skipped=False,
            error=True,
            error_reason=reason,
        )

    def _result(self, score: float, reasoning: str) -> GraderResult:
        return GraderResult(
            grader=self.rubric_id,
            category=self.category,
            score=score,
            passed=score >= self.threshold,
            threshold=self.threshold,
            reasoning=reasoning,
            skipped=False,
        )

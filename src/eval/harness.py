from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.agent.agent import AgentResult, run as agent_run
from src.agent.client import ClaudeClient
from src.eval.graders.base import EvalCase, Grader, GraderResult, Trace, ToolCallRecord
from src.eval.graders.retrieval.tool_use import ToolUseAppropriatenessGrader
from src.eval.graders.retrieval.query_entity import QueryEntityAdherenceGrader
from src.eval.graders.accuracy.factual import FactualAccuracyGrader
from src.eval.graders.accuracy.groundedness import GroundednessGrader
from src.eval.graders.boundaries.no_opinion import NoOpinionLeakageGrader
from src.eval.suite import load_suite

_LOGS_DIR = Path("logs/eval_runs")
_DEFAULT_PARALLELISM = 10

ALL_GRADERS: list[Grader] = [
    ToolUseAppropriatenessGrader(),
    QueryEntityAdherenceGrader(),
    FactualAccuracyGrader(),
    GroundednessGrader(),
    NoOpinionLeakageGrader(),
]


def _make_run_id(model: str, prompt_version: str, suite_path: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    raw = f"{model}:{prompt_version}:{suite_path}"
    short_hash = hashlib.md5(raw.encode()).hexdigest()[:6]
    return f"{ts}_{short_hash}"


def _agent_result_to_trace(result: AgentResult, case: EvalCase, run_id: str) -> Trace:
    return Trace(
        eval_id=case.id,
        run_id=run_id,
        prompt_version=result.prompt_version,
        model=result.model,
        input=case.input,
        conversation=result.conversation,
        tool_calls=result.tool_calls,
        output=result.output,
        total_tool_calls=len(result.tool_calls),
        latency_ms=result.latency_ms,
        error=result.error,
    )


def _trace_to_dict(trace: Trace) -> dict:
    d = trace.__dict__.copy()
    d["tool_calls"] = [tc.__dict__ for tc in trace.tool_calls]
    return d


def _grader_result_to_dict(gr: GraderResult) -> dict:
    return gr.__dict__.copy()


def _run_case(
    case: EvalCase,
    client: ClaudeClient,
    prompt_version: str | None,
    run_id: str,
    traces_dir: Path,
    graders: list[Grader],
) -> list[dict]:
    """Run a single eval case; return list of score dicts. Always writes the trace."""
    result = agent_run(case.input, client, prompt_version)
    trace = _agent_result_to_trace(result, case, run_id)

    # Write trace immediately (before graders, so partial data is never lost)
    trace_path = traces_dir / f"{case.id}.json"
    trace_path.write_text(json.dumps(_trace_to_dict(trace), indent=2))

    if result.error:
        return [{
            "eval_id": case.id,
            "grader": g.rubric_id,
            "category": g.category,
            "score": None,
            "passed": None,
            "threshold": g.threshold,
            "reasoning": None,
            "skipped": True,
            "skip_reason": f"Agent error: {result.error}",
        } for g in graders]

    scores = []
    for grader in graders:
        try:
            gr = grader.eval(case, trace)
        except NotImplementedError:
            gr = grader._skip("Grader not yet implemented")
        except Exception as exc:  # noqa: BLE001
            gr = grader._skip(f"Grader exception: {exc}")
        scores.append(_grader_result_to_dict(gr))
        scores[-1]["eval_id"] = case.id

    return scores


def run_eval(
    suite_path: str | Path,
    client: ClaudeClient,
    prompt_version: str | None = None,
    limit: int | None = None,
    parallelism: int = _DEFAULT_PARALLELISM,
    graders: list[Grader] | None = None,
) -> str:
    """
    Run the full eval harness. Returns the run_id.
    Writes traces/, scores.json, and summary.md to logs/eval_runs/<run_id>/.
    """
    active_graders = graders or ALL_GRADERS
    cases = load_suite(suite_path, limit=limit)
    run_id = _make_run_id(client.model, prompt_version or "latest", str(suite_path))

    run_dir = _LOGS_DIR / run_id
    traces_dir = run_dir / "traces"
    traces_dir.mkdir(parents=True, exist_ok=True)

    # Write run config
    (run_dir / "config.json").write_text(json.dumps({
        "run_id": run_id,
        "suite_path": str(suite_path),
        "model": client.model,
        "backend": "claude",
        "prompt_version": prompt_version or "latest",
        "total_cases": len(cases),
        "parallelism": parallelism,
        "graders": [g.rubric_id for g in active_graders],
    }, indent=2))

    all_scores: list[dict] = []

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        futures = {
            pool.submit(_run_case, case, client, prompt_version, run_id, traces_dir, active_graders): case
            for case in cases
        }
        for future in as_completed(futures):
            case = futures[future]
            try:
                scores = future.result()
            except Exception as exc:  # noqa: BLE001
                scores = [{
                    "eval_id": case.id,
                    "grader": g.rubric_id,
                    "category": g.category,
                    "score": None,
                    "passed": None,
                    "threshold": g.threshold,
                    "reasoning": None,
                    "skipped": True,
                    "skip_reason": f"Unhandled exception: {exc}",
                } for g in active_graders]
            all_scores.extend(scores)

    # Write scores
    (run_dir / "scores.json").write_text(json.dumps(all_scores, indent=2))

    # Write summary
    summary = _build_summary(run_id, all_scores, cases, active_graders, prompt_version, client.model)
    (run_dir / "summary.md").write_text(summary)

    return run_id


def _build_summary(
    run_id: str,
    scores: list[dict],
    cases: list[EvalCase],
    graders: list[Grader],
    prompt_version: str | None,
    model: str,
) -> str:
    n = len(cases)
    lines = [
        f"# Eval Run: {run_id}",
        f"Prompt: {prompt_version or 'latest'} | Model: {model} | Cases: {n}",
        "",
    ]

    # Per-rubric stats (exclude skipped)
    rubric_stats: dict[str, dict[str, Any]] = {}
    for g in graders:
        rubric_scores = [s for s in scores if s["grader"] == g.rubric_id and not s["skipped"]]
        if not rubric_scores:
            continue
        passed = sum(1 for s in rubric_scores if s["passed"])
        mean = sum(s["score"] for s in rubric_scores) / len(rubric_scores)
        rubric_stats[g.rubric_id] = {
            "category": g.category,
            "passed": passed,
            "total": len(rubric_scores),
            "mean": mean,
            "threshold": g.threshold,
        }

    # Overall: a case passes if ALL non-skipped graders pass
    case_ids = [c.id for c in cases]
    case_pass = []
    for cid in case_ids:
        case_scores = [s for s in scores if s["eval_id"] == cid and not s["skipped"]]
        case_pass.append(all(s["passed"] for s in case_scores) if case_scores else False)
    overall_pass = sum(case_pass)

    lines += [
        "## Overall",
        f"Pass rate: {overall_pass}/{n} ({100*overall_pass//n}%)  |  "
        f"Mean score: {sum(s['score'] for s in scores if s['score'] is not None) / max(1, sum(1 for s in scores if s['score'] is not None)):.2f}",
        "",
    ]

    # By category
    lines += ["## By Category", "| Category | Rubrics | Pass Rate | Mean Score |", "|---|---|---|---|"]
    categories = sorted({g.category for g in graders})
    for cat in categories:
        cat_rubrics = [g.rubric_id for g in graders if g.category == cat]
        cat_scores = [s for s in scores if s["category"] == cat and not s["skipped"]]
        if not cat_scores:
            continue
        cat_passed = sum(1 for s in cat_scores if s["passed"])
        cat_mean = sum(s["score"] for s in cat_scores) / len(cat_scores)
        lines.append(f"| {cat} | {', '.join(cat_rubrics)} | {cat_passed}/{len(cat_scores)} | {cat_mean:.2f} |")

    lines += ["", "## By Rubric", "| Rubric | Pass Rate | Mean Score | Threshold |", "|---|---|---|---|"]
    for rubric_id, stat in rubric_stats.items():
        lines.append(f"| {rubric_id} | {stat['passed']}/{stat['total']} | {stat['mean']:.2f} | {stat['threshold']} |")

    # Failed cases
    failed = []
    for cid in case_ids:
        failing = [s for s in scores if s["eval_id"] == cid and not s["skipped"] and not s["passed"]]
        if failing:
            detail = ", ".join(f"{s['grader']} ({s['score']:.2f})" for s in failing)
            failed.append((cid, detail))

    if failed:
        lines += ["", "## Failed Cases", "| ID | Failing Rubrics |", "|---|---|"]
        for cid, detail in failed:
            lines.append(f"| {cid} | {detail} |")

    return "\n".join(lines) + "\n"

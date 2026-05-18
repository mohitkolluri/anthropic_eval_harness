from __future__ import annotations

import hashlib
import json
import time
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
_DEFAULT_PARALLELISM = 3
_DELAY_BETWEEN_CASES = 1.0  # seconds — avoids hitting 50k token/min rate limit

def make_graders(client: ClaudeClient) -> list[Grader]:
    """Instantiate all graders, injecting the shared Claude client into LLM-judge graders."""
    return [
        ToolUseAppropriatenessGrader(),
        QueryEntityAdherenceGrader(judge_client=client),
        FactualAccuracyGrader(judge_client=client),
        GroundednessGrader(judge_client=client),
        NoOpinionLeakageGrader(judge_client=client),
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
    d = gr.__dict__.copy()
    # Ensure error fields always present for consistent schema
    d.setdefault("error", False)
    d.setdefault("error_reason", None)
    return d


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
    active_graders = graders or make_graders(client)
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
            time.sleep(_DELAY_BETWEEN_CASES)

    # Write scores
    (run_dir / "scores.json").write_text(json.dumps(all_scores, indent=2))

    # Write summary
    summary = _build_summary(run_id, all_scores, cases, active_graders, prompt_version, client.model)
    (run_dir / "summary.md").write_text(summary)

    return run_id


def _case_passed(case_id: str, scores: list[dict]) -> bool:
    """
    A case passes if every grader that produced a real result (not skipped, not error)
    returned passed=True. Cases where ALL graders skipped/errored are excluded (False).
    """
    real = [s for s in scores if s["eval_id"] == case_id and not s["skipped"] and not s.get("error")]
    return bool(real) and all(s["passed"] for s in real)


def _build_summary(
    run_id: str,
    scores: list[dict],
    cases: list[EvalCase],
    graders: list[Grader],
    prompt_version: str | None,
    model: str,
) -> str:
    n = len(cases)
    case_ids = [c.id for c in cases]
    lines = [
        f"# Eval Run: {run_id}",
        f"Prompt: {prompt_version or 'latest'} | Model: {model} | Cases: {n}",
        "",
    ]

    # Per-rubric stats — only real results (not skipped, not error)
    rubric_stats: dict[str, dict[str, Any]] = {}
    for g in graders:
        real = [
            s for s in scores
            if s["grader"] == g.rubric_id and not s["skipped"] and not s.get("error")
        ]
        if not real:
            continue
        passed = sum(1 for s in real if s["passed"])
        mean = sum(s["score"] for s in real) / len(real)
        rubric_stats[g.rubric_id] = {
            "category": g.category,
            "passed": passed,
            "total": len(real),
            "mean": mean,
            "threshold": g.threshold,
        }

    # Overall pass rate — per case (≤ n), not per grader-evaluation
    # A case passes if all applicable (non-skipped, non-error) graders pass
    overall_pass = sum(1 for cid in case_ids if _case_passed(cid, scores))

    real_scores = [s["score"] for s in scores if s["score"] is not None and not s.get("error")]
    mean_overall = sum(real_scores) / len(real_scores) if real_scores else 0.0

    lines += [
        "## Overall",
        f"Pass rate: {overall_pass}/{n} ({100*overall_pass//n}%)  |  Mean score: {mean_overall:.2f}",
        "",
    ]

    # By category — per-case pass rate (a case passes if all graders in that category pass)
    lines += ["## By Category (per case)", "| Category | Rubrics | Cases Passed | Mean Score |", "|---|---|---|---|"]
    categories = sorted({g.category for g in graders})
    for cat in categories:
        cat_rubric_ids = {g.rubric_id for g in graders if g.category == cat}
        cat_rubric_names = ", ".join(sorted(cat_rubric_ids))

        # Per-case: does this case pass ALL graders in this category?
        cat_case_pass = 0
        cat_case_total = 0
        cat_scores_real: list[float] = []

        for cid in case_ids:
            cat_real = [
                s for s in scores
                if s["eval_id"] == cid
                and s["category"] == cat
                and not s["skipped"]
                and not s.get("error")
            ]
            if not cat_real:
                continue  # all graders in this category were skipped/errored for this case
            cat_case_total += 1
            if all(s["passed"] for s in cat_real):
                cat_case_pass += 1
            cat_scores_real.extend(s["score"] for s in cat_real)

        if cat_case_total == 0:
            continue
        cat_mean = sum(cat_scores_real) / len(cat_scores_real) if cat_scores_real else 0.0
        lines.append(f"| {cat} | {cat_rubric_names} | {cat_case_pass}/{cat_case_total} | {cat_mean:.2f} |")

    # By rubric — per grader evaluation count
    lines += ["", "## By Rubric", "| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |", "|---|---|---|---|---|"]
    for rubric_id, stat in rubric_stats.items():
        lines.append(
            f"| {rubric_id} | {stat['total']} | {stat['passed']}/{stat['total']} | {stat['mean']:.2f} | {stat['threshold']} |"
        )

    # Failed cases — show which graders failed and their scores
    failed = []
    for cid in case_ids:
        failing = [
            s for s in scores
            if s["eval_id"] == cid and not s["skipped"] and not s.get("error") and not s["passed"]
        ]
        if failing:
            detail = ", ".join(f"{s['grader']} ({s['score']:.2f})" for s in failing)
            failed.append((cid, detail))

    if failed:
        lines += ["", "## Failed Cases", "| ID | Failing Rubrics |", "|---|---|"]
        for cid, detail in failed:
            lines.append(f"| {cid} | {detail} |")

    return "\n".join(lines) + "\n"

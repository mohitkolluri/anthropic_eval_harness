from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pathlib import Path as _Path

from src.agent.client import ClaudeClient
from src.eval.harness import run_eval, ALL_GRADERS

_PROMPTS_DIR = _Path(__file__).parent.parent / "agent" / "prompts"
from src.eval.graders.base import GraderResult

_LOGS_DIR = Path("logs")
_HISTORY_FILE = _LOGS_DIR / "hillclimb" / "history.jsonl"
_EVAL_RUNS_DIR = _LOGS_DIR / "eval_runs"
_REGRESSION_THRESHOLD = 0.10
_MAX_FAILED_CASES = 10
_MAX_REGRESSION_CASES = 10

# Maps rubric_id → category
_RUBRIC_CATEGORY = {g.rubric_id: g.category for g in ALL_GRADERS}


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class RubricContext:
    rubric_id: str
    definition: str
    threshold: float


@dataclass
class FailedCase:
    eval_id: str
    category: str
    difficulty: str
    input: str
    output: str
    tool_queries: list[str]
    grader_failures: dict[str, str]  # rubric_id → grader reasoning


@dataclass
class PassedCase:
    eval_id: str
    category: str
    input: str
    output: str


@dataclass
class HillClimbInput:
    category: str
    rubrics: dict[str, RubricContext]
    failed_cases: list[FailedCase]
    regression_cases: list[PassedCase]
    current_prompt: str
    prompt_version: str


# ── Rubric definitions (human-readable, injected into improvement prompt) ────

_RUBRIC_DEFINITIONS: dict[str, str] = {
    # ── retrieval ────────────────────────────────────────────────────────────
    "tool_use_appropriateness": (
        "The model searches Wikipedia when a question requires factual information, "
        "skips search for opinions/unanswerable questions, "
        "and does not exceed the allowed search count per question."
    ),
    "query_entity_adherence": (
        "Every search query sent to Wikipedia must be an entity name or Wikipedia article title "
        "(a clean noun phrase), never a rephrased question or keyword soup. "
        "Good: 'Mount Everest', 'French Revolution', 'Boiling point'. "
        "Bad: 'boiling point of water at high altitude', 'how long did the war last'."
    ),
    # ── accuracy ─────────────────────────────────────────────────────────────
    "factual_accuracy": (
        "Every factual claim in the answer is correct according to Wikipedia."
    ),
    "groundedness": (
        "Every factual claim in the answer is directly traceable to the retrieved "
        "Wikipedia content — no facts added from the model's own memory."
    ),
    # ── boundaries ───────────────────────────────────────────────────────────
    "no_opinion_leakage": (
        "When asked an opinion or unanswerable question, the model gives a pure refusal "
        "with exactly one of the two allowed phrases and nothing else: "
        "'This is a matter of opinion and I cannot answer it.' or "
        "'This question cannot be answered from Wikipedia.'"
    ),
    "ambiguity_acknowledgment": (
        "When a question contains an ambiguous term with multiple Wikipedia interpretations, "
        "the model must: (1) acknowledge the competing interpretations by naming them, "
        "(2) pick the most prominent one and answer it, "
        "(3) ask the user to be more specific."
    ),
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def _latest_run_id() -> str:
    runs = sorted(_EVAL_RUNS_DIR.iterdir(), key=lambda p: p.name, reverse=True)
    if not runs:
        raise FileNotFoundError("No eval runs found in logs/eval_runs/")
    return runs[0].name


def _load_scores(run_id: str) -> list[dict]:
    path = _EVAL_RUNS_DIR / run_id / "scores.json"
    return json.loads(path.read_text())


def _load_trace(run_id: str, eval_id: str) -> dict:
    path = _EVAL_RUNS_DIR / run_id / "traces" / f"{eval_id}.json"
    return json.loads(path.read_text())


def _extract_section(prompt: str, section_id: str) -> str:
    m = re.search(rf'<section id="{section_id}">(.*?)</section>', prompt, re.DOTALL)
    return m.group(1).strip() if m else ""


def _replace_section(prompt: str, section_id: str, new_content: str) -> str:
    return re.sub(
        rf'(<section id="{section_id}">).*?(</section>)',
        rf'\g<1>\n{new_content}\n\g<2>',
        prompt,
        flags=re.DOTALL,
    )


def _next_prompt_version() -> str:
    versions = sorted(
        (int(p.stem[1:]) for p in _PROMPTS_DIR.glob("v*.md")),
    )
    next_n = (versions[-1] + 1) if versions else 2
    return f"v{next_n}"


def _current_prompt() -> tuple[str, str]:
    """Return (version_label, full_prompt_text)."""
    from src.agent.agent import load_prompt
    return load_prompt()


# ── Build HillClimbInput ─────────────────────────────────────────────────────

def _build_input(category: str, run_id: str, rubric: str | None = None) -> HillClimbInput:
    scores = _load_scores(run_id)

    # Rubrics in scope — either just the targeted rubric or all in the category
    target_rubrics = {
        g.rubric_id: RubricContext(
            rubric_id=g.rubric_id,
            definition=_RUBRIC_DEFINITIONS.get(g.rubric_id, ""),
            threshold=g.threshold,
        )
        for g in ALL_GRADERS
        if g.category == category and (rubric is None or g.rubric_id == rubric)
    }

    # Group scores by eval_id
    by_case: dict[str, list[dict]] = {}
    for s in scores:
        by_case.setdefault(s["eval_id"], []).append(s)

    failed_cases: list[FailedCase] = []
    regression_cases: list[PassedCase] = []

    for eval_id, case_scores in by_case.items():
        # Failed: targeted rubric(s) not passed
        cat_fails = [
            s for s in case_scores
            if s["category"] == category
            and (rubric is None or s["grader"] == rubric)
            and not s["skipped"]
            and not s["passed"]
        ]
        all_pass = all(
            s["passed"] for s in case_scores if not s["skipped"]
        )

        if cat_fails:
            trace = _load_trace(run_id, eval_id)
            failed_cases.append(FailedCase(
                eval_id=eval_id,
                category=trace.get("metadata", {}).get("category", ""),
                difficulty=trace.get("metadata", {}).get("difficulty", ""),
                input=trace["input"],
                output=trace["output"],
                tool_queries=[tc["query"] for tc in trace.get("tool_calls", [])],
                grader_failures={
                    s["grader"]: (s["reasoning"] or "no reasoning")
                    for s in cat_fails
                },
            ))
        elif all_pass:
            trace = _load_trace(run_id, eval_id)
            regression_cases.append(PassedCase(
                eval_id=eval_id,
                category=trace.get("metadata", {}).get("category", ""),
                input=trace["input"],
                output=trace["output"],
            ))

    # Sort and cap
    failed_cases.sort(key=lambda c: min(
        s["score"] or 0.0
        for s in by_case[c.eval_id]
        if s["category"] == category and not s["skipped"]
    ))
    failed_cases = failed_cases[:_MAX_FAILED_CASES]
    regression_cases = regression_cases[:_MAX_REGRESSION_CASES]

    ver, prompt_text = _current_prompt()

    return HillClimbInput(
        category=category,
        rubrics=target_rubrics,
        failed_cases=failed_cases,
        regression_cases=regression_cases,
        current_prompt=prompt_text,
        prompt_version=ver,
    )


# ── Build improvement prompt ─────────────────────────────────────────────────

def _build_improvement_prompt(hci: HillClimbInput) -> str:
    rubric_block = "\n".join(
        f"  - {rid} (threshold {ctx.threshold}): {ctx.definition}"
        for rid, ctx in hci.rubrics.items()
    )

    current_section = _extract_section(hci.current_prompt, hci.category)

    failed_block_lines = []
    for i, fc in enumerate(hci.failed_cases, 1):
        failures = "\n".join(
            f"    [{rubric}] {reason}"
            for rubric, reason in fc.grader_failures.items()
        )
        failed_block_lines.append(
            f"Case {i} (id={fc.eval_id}, category={fc.category}, difficulty={fc.difficulty})\n"
            f"  Question: {fc.input}\n"
            f"  Searches made: {fc.tool_queries or 'none'}\n"
            f"  Answer given: {fc.output}\n"
            f"  Why it failed:\n{failures}"
        )
    failed_block = "\n\n".join(failed_block_lines)

    regression_block_lines = []
    for i, rc in enumerate(hci.regression_cases, 1):
        regression_block_lines.append(
            f"Case {i} (id={rc.eval_id}, category={rc.category})\n"
            f"  Question: {rc.input}\n"
            f"  Answer: {rc.output}"
        )
    regression_block = "\n\n".join(regression_block_lines)

    return f"""You are improving a system prompt for a Wikipedia QA agent.
Your task is to revise ONE section of the prompt to fix specific failures, without breaking passing cases.

## Target section: {hci.category}
Current content:
<current_section>
{current_section}
</current_section>

## Rubrics being targeted
{rubric_block}

## Cases that are currently FAILING (fix these):
<failed_cases>
{failed_block}
</failed_cases>

## Cases that are currently PASSING (do not break these):
<regression_cases>
{regression_block}
</regression_cases>

## Instructions
1. Analyse the failure patterns across the failed cases. Look for the UNDERLYING behavioural pattern, not just the surface symptom.
2. Identify the minimal change to the <current_section> that would address those patterns through clearer rules or decision criteria.
3. Do not modify instructions that address passing cases.

## How to improve rules (critical)
- Express the fix as a **decision rule or self-check** the agent applies, not as more examples.
  Good: "Before submitting a query, ask: 'Could this be a Wikipedia article title?' If not, strip it down."
  Bad: Adding more Good/Bad query examples derived from the failing cases.
- If you must clarify an existing rule, tighten its language — make the boundary condition explicit.
- Only add an example if no rule formulation can capture the principle clearly. If you do add examples, they must NOT be drawn from the failing cases above (that is overfitting).
- Prefer removing vagueness over adding content. A shorter, crisper rule generalises better than a longer one with more examples.

4. Return a JSON object with exactly two keys:
   - "rationale": the behavioural root cause and what rule change addresses it (2-4 sentences)
   - "revised_section": the full revised content for the <section id="{hci.category}"> block (no XML tags, just the content)

Return ONLY the JSON object, no other text."""


# ── Main entry point ─────────────────────────────────────────────────────────

def run_hillclimb(
    category: str | None = None,
    suite_path: str | Path = "evals/suite.jsonl",
    run_id: str | None = None,
    max_cases: int = _MAX_FAILED_CASES,
    judge_model: str = "claude-sonnet-4-6",
    rubric: str | None = None,
) -> dict[str, Any]:
    """
    Run one hill climb cycle for the given rubric category or specific rubric.
    When rubric is set, category is derived automatically and only that rubric's
    failures are used. Returns a summary dict with before/after scores.
    """
    from src.agent.agent import load_prompt
    import os

    # Derive category from rubric if rubric-level targeting is used
    if rubric and not category:
        matched = [g for g in ALL_GRADERS if g.rubric_id == rubric]
        if not matched:
            raise ValueError(f"Unknown rubric: {rubric!r}")
        category = matched[0].category

    if not category:
        raise ValueError("Either --category or --rubric must be specified")

    active_run_id = run_id or _latest_run_id()
    hci = _build_input(category, active_run_id, rubric=rubric)

    if not hci.failed_cases:
        return {"status": "no_failures", "category": category, "run_id": active_run_id}

    # Use Claude as judge (always)
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set — hill climb requires Claude")
    judge = ClaudeClient(model=judge_model)

    improvement_prompt = _build_improvement_prompt(hci)
    response = judge.complete(
        system="You are an expert prompt engineer. Return only the requested JSON.",
        messages=[{"role": "user", "content": improvement_prompt}],
        tools=None,
        max_tokens=4096,  # hill climb response includes full revised prompt section
    )

    raw = response.get("content") or ""

    # Strip markdown fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned.strip())

    # Try direct parse first; fall back to extracting the outermost JSON object
    payload = None
    try:
        payload = json.loads(cleaned)
    except json.JSONDecodeError:
        json_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if not json_match:
            raise ValueError(f"No JSON object found in hill climb response:\n{raw}")
        try:
            payload = json.loads(json_match.group(0))
        except json.JSONDecodeError as e:
            raise ValueError(f"Hill climb JSON was malformed: {e}\nExtracted:\n{json_match.group(0)[:300]}") from e

    rationale = payload.get("rationale", "")
    revised_section = payload.get("revised_section", "")

    # Build and save new prompt version
    _, current_prompt_text = load_prompt(hci.prompt_version)
    new_prompt_text = _replace_section(current_prompt_text, category, revised_section)
    new_version = _next_prompt_version()
    new_prompt_path = _PROMPTS_DIR / f"{new_version}.md"
    new_prompt_path.write_text(new_prompt_text)

    # Re-eval with new prompt (capped to keep hillclimb fast)
    eval_client = ClaudeClient(model=judge_model)
    new_run_id = run_eval(suite_path, eval_client, prompt_version=new_version, limit=max_cases)

    # Compare scores
    old_scores = _load_scores(active_run_id)
    new_scores = _load_scores(new_run_id)

    def _mean_by_rubric(score_list: list[dict]) -> dict[str, float]:
        by_rubric: dict[str, list[float]] = {}
        for s in score_list:
            if not s["skipped"] and s["score"] is not None:
                by_rubric.setdefault(s["grader"], []).append(s["score"])
        return {k: sum(v) / len(v) for k, v in by_rubric.items()}

    before = _mean_by_rubric(old_scores)
    after = _mean_by_rubric(new_scores)

    # Detect regressions (non-targeted rubrics)
    target_rubric_ids = set(hci.rubrics.keys())
    regressions = []
    for rubric, before_score in before.items():
        if rubric in target_rubric_ids:
            continue
        after_score = after.get(rubric, before_score)
        if before_score - after_score > _REGRESSION_THRESHOLD:
            regressions.append({
                "rubric": rubric,
                "before": round(before_score, 3),
                "after": round(after_score, 3),
                "drop": round(before_score - after_score, 3),
            })

    old_pass_set = {
        (s["eval_id"], s["grader"])
        for s in old_scores
        if s["grader"] in target_rubric_ids and not s["skipped"] and s["passed"]
    }
    cases_improved = sum(
        1 for s in new_scores
        if s["grader"] in target_rubric_ids
        and not s["skipped"]
        and s["passed"]
        and (s["eval_id"], s["grader"]) not in old_pass_set
    )

    history_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": category,
        "rubrics": list(target_rubric_ids),
        "from_version": hci.prompt_version,
        "to_version": new_version,
        "from_run": active_run_id,
        "to_run": new_run_id,
        "rationale": rationale,
        "before": {r: round(before.get(r, 0), 3) for r in target_rubric_ids},
        "after": {r: round(after.get(r, 0), 3) for r in target_rubric_ids},
        "regressions": regressions,
        "failed_cases_count": len(hci.failed_cases),
        "cases_improved": cases_improved,
    }

    _HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _HISTORY_FILE.open("a") as f:
        f.write(json.dumps(history_entry) + "\n")

    return history_entry

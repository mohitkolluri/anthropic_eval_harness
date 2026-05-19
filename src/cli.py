"""
Wikipedia QA Eval Harness — CLI entrypoint
==========================================

Setup
-----
  cp .env.example .env          # add ANTHROPIC_API_KEY
  source .venv/bin/activate

Commands
--------

  1. Interactive Q&A (default model: claude-haiku-4-5-20251001):
       python -m src.cli run

     With options:
       python -m src.cli run --trace                  # full debug trace per answer
       python -m src.cli run --prompt v2              # specific prompt version
       python -m src.cli run --model claude-sonnet-4-6

  2. Run the eval suite:
       python -m src.cli eval

     With options:
       python -m src.cli eval --limit 5               # quick smoke test (5 cases only)
       python -m src.cli eval --prompt v2             # run a specific prompt version
       python -m src.cli eval --suite path/to/custom.jsonl

  3. Hill climb (improve one rubric category, auto re-evals):
       python -m src.cli hillclimb --category accuracy
       python -m src.cli hillclimb --category retrieval --max-cases 5
       python -m src.cli hillclimb --category boundaries --run-id 20260517_143022_a3f2c1

Logs
----
  logs/eval_runs/<run_id>/
    config.json      run parameters
    traces/          one JSON trace per eval case
    scores.json      per-case × per-grader score matrix
    summary.md       pass rates by rubric and category

  logs/hillclimb/history.jsonl   hill climb history (rationale + score deltas)
  src/agent/prompts/             vN.md prompt versions
"""

from __future__ import annotations

from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()  # loads .env from cwd or any parent directory

console = Console()

_DEFAULT_SUITE = "evals/suite.jsonl"
_DEFAULT_MODEL = "claude-haiku-4-5-20251001"


@click.group()
def cli():
    """Wikipedia QA — eval harness CLI."""


# ── run ───────────────────────────────────────────────────────────────────────
#
# Usage:
#   python -m src.cli run                          # interactive, latest prompt
#   python -m src.cli run --trace                  # with full debug trace
#   python -m src.cli run --prompt v2              # specific prompt version
#   python -m src.cli run --model claude-sonnet-4-6

@cli.command()
@click.option("--prompt", "prompt_version", default=None, help="Prompt version, e.g. v1. Defaults to latest.")
@click.option("--model", default=_DEFAULT_MODEL, show_default=True)
@click.option("--trace", is_flag=True, default=False, help="Show full debug trace: conversation turns, tool queries, fetched content snippets.")
def run(prompt_version: str | None, model: str, trace: bool):
    """Interactive Q&A — ask questions and see answers."""
    from src.agent.agent import run as agent_run
    from src.agent.client import ClaudeClient

    client = ClaudeClient(model=model)
    console.print(f"[bold green]Wikipedia QA[/] — model={client.model}, prompt={prompt_version or 'latest'}")
    if trace:
        console.print("[yellow]Trace mode ON[/] — full debug output enabled")
    console.print("Type [bold]quit[/] or [bold]exit[/] to stop.\n")

    while True:
        try:
            question = click.prompt("Question")
        except (EOFError, KeyboardInterrupt):
            break
        if question.strip().lower() in {"quit", "exit", "q"}:
            break

        with console.status("Searching Wikipedia…"):
            result = agent_run(question, client, prompt_version)

        if result.error:
            console.print(f"[red]Error:[/] {result.error}")
            continue

        if trace:
            _print_trace(result)
        else:
            console.print(f"\n[bold]Answer:[/]\n{result.output}\n")
            if result.tool_calls:
                console.print(f"[dim]Searches ({len(result.tool_calls)}):[/]")
                for tc in result.tool_calls:
                    console.print(f"  [dim]→ {tc.query}[/]")
            else:
                console.print("[dim]No Wikipedia search used.[/]")

        console.print()


def _print_trace(result) -> None:
    """Print a full debug trace of an agent run."""
    from rich.panel import Panel
    from rich.rule import Rule

    console.print(Rule("[yellow]TRACE[/]", style="yellow"))

    console.print(
        f"[dim]model={result.model}  prompt={result.prompt_version}  "
        f"latency={result.latency_ms}ms  tool_calls={result.total_tool_calls}[/]"
    )
    console.print()

    for i, msg in enumerate(result.conversation):
        role = msg.get("role", "?")
        content = msg.get("content", "")

        if role == "user" and i == 0:
            console.print(Panel(str(content), title="[bold blue]USER[/]", border_style="blue"))

        elif role == "assistant":
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "tool_use":
                        console.print(Panel(
                            f"[cyan]search_wikipedia[/]({block['input'].get('query', '')})",
                            title="[bold cyan]TOOL CALL[/]",
                            border_style="cyan",
                        ))
            elif content:
                console.print(Panel(str(content), title="[bold green]ASSISTANT[/]", border_style="green"))

        elif role == "user" and isinstance(content, list):
            for item in content:
                snippet = str(item.get("content", ""))[:300]
                if len(str(item.get("content", ""))) > 300:
                    snippet += "…"
                console.print(Panel(snippet, title="[bold magenta]WIKIPEDIA RESULT[/]", border_style="magenta"))

    if result.tool_calls:
        console.print(Rule("[cyan]Search Detail[/]", style="cyan"))
        for tc in result.tool_calls:
            console.print(f"[cyan]Query #{tc.call_index + 1}:[/] {tc.query}")
            console.print(f"  [dim]Source: {tc.content_source}[/]")
            if tc.fetched_content:
                snippet = tc.fetched_content[:400].replace("\n", " ")
                if len(tc.fetched_content) > 400:
                    snippet += "…"
                console.print(f"  [dim]Content: {snippet}[/]")
            console.print()

    console.print(Rule(style="yellow"))


# ── demo ──────────────────────────────────────────────────────────────────────
#
# Usage:
#   python -m src.cli demo                  # 3 preset questions, auto-run
#   python -m src.cli demo --trace          # with full debug trace per answer
#   python -m src.cli demo --model claude-sonnet-4-6

_DEMO_QUESTIONS = [
    "What are LLMs?",
    "Why is Silicon Valley and what is India's Silicon Valley?",
    "When was the Golden Gate bridge built and what are some view points near it?",
]

@cli.command()
@click.option("--prompt", "prompt_version", default=None, help="Prompt version. Defaults to latest.")
@click.option("--model", default=_DEFAULT_MODEL, show_default=True)
@click.option("--trace", is_flag=True, default=False, help="Show full debug trace per answer.")
def demo(prompt_version: str | None, model: str, trace: bool):
    """Auto-run 3 preset questions to showcase the system."""
    from src.agent.agent import run as agent_run
    from src.agent.client import ClaudeClient
    from rich.rule import Rule

    client = ClaudeClient(model=model)
    console.print(f"[bold green]Wikipedia QA — Demo Mode[/]")
    console.print(f"[dim]model={client.model}  prompt={prompt_version or 'latest'}  questions={len(_DEMO_QUESTIONS)}[/]")
    console.print()

    for i, question in enumerate(_DEMO_QUESTIONS, 1):
        console.print(Rule(f"[bold]Question {i} of {len(_DEMO_QUESTIONS)}[/]"))
        console.print(f"[bold blue]Q:[/] {question}\n")

        with console.status("Searching Wikipedia…"):
            result = agent_run(question, client, prompt_version)

        if result.error:
            console.print(f"[red]Error:[/] {result.error}")
        elif trace:
            _print_trace(result)
        else:
            console.print(f"[bold green]A:[/] {result.output}\n")
            if result.tool_calls:
                searches = [tc.query for tc in result.tool_calls]
                console.print(f"[dim]Searches: {searches}[/]")
            else:
                console.print("[dim]No Wikipedia search used.[/]")

        console.print()

    console.print(Rule("[bold green]Demo complete[/]", style="green"))


# ── eval ──────────────────────────────────────────────────────────────────────
#
# Usage:
#   python -m src.cli eval                          # full suite, latest prompt
#   python -m src.cli eval --limit 5               # quick smoke test (5 cases only)
#   python -m src.cli eval --prompt v2             # run against a specific prompt version
#   python -m src.cli eval --suite path/to/custom.jsonl
#
# Output: logs/eval_runs/<run_id>/{config.json, traces/, scores.json, summary.md}

@cli.command()
@click.option("--prompt", "prompt_version", default=None, help="Prompt version. Defaults to latest.")
@click.option("--model", default=_DEFAULT_MODEL, show_default=True)
@click.option("--suite", "suite_path", default=_DEFAULT_SUITE, show_default=True)
@click.option("--limit", default=None, type=int, help="Cap number of eval cases to run.")
@click.option("--parallelism", default=3, show_default=True, help="Concurrent cases. Keep low (2–3) to avoid API rate limits.")
def eval(
    prompt_version: str | None,
    model: str,
    suite_path: str,
    limit: int | None,
    parallelism: int,
):
    """Run the eval suite and write results to logs/eval_runs/<run_id>/."""
    from src.agent.client import ClaudeClient
    from src.eval.harness import run_eval

    client = ClaudeClient(model=model)
    console.print(f"[bold green]Eval run[/] — suite={suite_path}, model={client.model}")
    if limit:
        console.print(f"[dim]Limit: {limit} cases[/]")

    with console.status("Running evals…"):
        run_id = run_eval(
            suite_path=suite_path,
            client=client,
            prompt_version=prompt_version,
            limit=limit,
            parallelism=parallelism,
        )

    summary_path = Path("logs/eval_runs") / run_id / "summary.md"
    console.print(f"\n[bold]Run ID:[/] {run_id}")
    console.print(f"[bold]Summary:[/] {summary_path}\n")
    console.print(summary_path.read_text())


# ── hillclimb ────────────────────────────────────────────────────────────────
#
# Usage (by category — targets all rubrics in that category):
#   python -m src.cli hillclimb --category accuracy
#   python -m src.cli hillclimb --category retrieval
#   python -m src.cli hillclimb --category boundaries
#
# Usage (by rubric — single-rubric precision targeting):
#   python -m src.cli hillclimb --rubric factual_accuracy
#   python -m src.cli hillclimb --rubric query_entity_adherence
#   python -m src.cli hillclimb --rubric groundedness
#   python -m src.cli hillclimb --rubric no_opinion_leakage
#   python -m src.cli hillclimb --rubric tool_use_appropriateness
#
# Options:
#   --run-id <id>       baseline run to draw failures from (default: latest)
#   --max-cases <n>     max failed cases sent to improvement prompt (default: 10)
#   --judge-model       Claude model used as the prompt engineer (default: claude-sonnet-4-6)
#
# Writes: src/agent/prompts/vN+1.md  +  logs/hillclimb/history.jsonl

_VALID_RUBRICS = [
    "tool_use_appropriateness", "query_entity_adherence",
    "factual_accuracy", "groundedness",
    "no_opinion_leakage", "ambiguity_acknowledgment",
]

@cli.command()
@click.option("--category", default=None, type=click.Choice(["retrieval", "accuracy", "boundaries"]),
              help="Target all rubrics in this category.")
@click.option("--rubric", default=None, type=click.Choice(_VALID_RUBRICS),
              help="Target a single rubric (category derived automatically).")
@click.option("--run-id", default=None, help="Eval run to use as baseline. Defaults to latest.")
@click.option("--suite", "suite_path", default=_DEFAULT_SUITE, show_default=True)
@click.option("--max-cases", default=10, show_default=True, help="Max failed cases to include in improvement prompt.")
@click.option("--judge-model", default="claude-sonnet-4-6", show_default=True, help="Claude model used as the prompt engineer.")
def hillclimb(
    category: str | None,
    rubric: str | None,
    run_id: str | None,
    suite_path: str,
    max_cases: int,
    judge_model: str,
):
    """Run one hill climb cycle. Use --category or --rubric (not both)."""
    from src.hillclimb.runner import run_hillclimb

    if not category and not rubric:
        raise click.UsageError("Specify either --category or --rubric.")
    if category and rubric:
        raise click.UsageError("Use --category OR --rubric, not both.")

    target = rubric or category
    console.print(f"[bold green]Hill Climb[/] — target={target}, judge={judge_model}")

    with console.status(f"Improving [{target}]…"):
        result = run_hillclimb(
            category=category,
            rubric=rubric,
            suite_path=suite_path,
            run_id=run_id,
            max_cases=max_cases,
            judge_model=judge_model,
        )

    if result.get("status") == "no_failures":
        console.print(f"[green]No failures found for [{target}] — nothing to improve.[/]")
        return

    console.print(f"\n[bold]{result['from_version']} → {result['to_version']}[/]  (target: {target})\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Rubric")
    table.add_column("Before", justify="right")
    table.add_column("After", justify="right")
    table.add_column("Delta", justify="right")

    for rubric in result.get("rubrics", []):
        before = result["before"].get(rubric, 0.0)
        after = result["after"].get(rubric, 0.0)
        delta = after - before
        delta_str = f"[green]+{delta:.3f}[/]" if delta > 0 else f"[red]{delta:.3f}[/]"
        table.add_row(rubric, f"{before:.3f}", f"{after:.3f}", delta_str)

    console.print(table)

    if result.get("regressions"):
        console.print("\n[bold red]Regressions detected:[/]")
        for r in result["regressions"]:
            console.print(f"  {r['rubric']}: {r['before']:.3f} → {r['after']:.3f}  (−{r['drop']:.3f})")
    else:
        console.print("\n[green]No regressions detected.[/]")

    console.print(f"\n[bold]Rationale:[/]\n{result.get('rationale', '')}\n")
    console.print(f"[dim]History logged to logs/hillclimb/history.jsonl[/]")


if __name__ == "__main__":
    cli()

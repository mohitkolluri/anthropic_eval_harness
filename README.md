# Wikipedia QA Eval Harness

A prompt engineering take-home project: a Claude-powered Q&A system grounded in Wikipedia, with a full eval suite and automated hill-climbing loop.

---

## Quick Start

```bash
source setup.sh         # installs deps, prompts for API key, activates venv

python -m src.cli demo  # auto-runs 3 preset questions to see the system in action
python -m src.cli run   # interactive Q&A
```

---

## Setup

### Requirements
- Python 3.12+
- An Anthropic API key

### Steps

```bash
# Recommended — installs everything AND activates the venv in one step
source setup.sh
```

Or run it as a subprocess (installs everything, then tells you to activate manually):
```bash
bash setup.sh
source .venv/bin/activate
```

The script auto-detects `$ANTHROPIC_API_KEY` from your environment. If not set, it prompts you to enter it and saves it to `.env`. Get your key at: https://console.anthropic.com/settings/keys

---

## Commands

### Demo

```bash
python -m src.cli demo                         # auto-runs 3 preset questions
python -m src.cli demo --trace                 # with full debug trace per answer
python -m src.cli demo --model claude-sonnet-4-6
```

### Interactive Q&A

```bash
python -m src.cli run                          # default model (Haiku 4.5)
python -m src.cli run --trace                  # full debug trace per answer
python -m src.cli run --model claude-sonnet-4-6
python -m src.cli run --prompt v5              # use a specific prompt version
```

### Eval Suite

```bash
python -m src.cli eval                         # run all 24 training cases
python -m src.cli eval --limit 5               # quick smoke test
python -m src.cli eval --suite evals/holdout.jsonl   # holdout validation
python -m src.cli eval --prompt v6             # eval a specific prompt version
```

Results written to `logs/eval_runs/<run_id>/`:
```
config.json     run parameters
traces/         one JSON trace per case (input, searches, output)
scores.json     per-case × per-grader score matrix
summary.md      pass rates by rubric and category
```

### Hill Climb

```bash
# Target a rubric category (all rubrics in it)
python -m src.cli hillclimb --category accuracy
python -m src.cli hillclimb --category retrieval
python -m src.cli hillclimb --category boundaries

# Target a single rubric
python -m src.cli hillclimb --rubric groundedness
python -m src.cli hillclimb --rubric query_entity_adherence
python -m src.cli hillclimb --rubric factual_accuracy
python -m src.cli hillclimb --rubric no_opinion_leakage
python -m src.cli hillclimb --rubric tool_use_appropriateness

# Options
--run-id <id>        baseline run to draw failures from (default: latest)
--max-cases 10       max failed cases sent to improvement prompt
--judge-model claude-sonnet-4-6
```

Results: `src/agent/prompts/vN+1.md` + entry appended to `logs/hillclimb/history.jsonl`.

---

## Architecture

```
User question
     │
     ▼
┌─────────────┐   action=search   ┌───────────────────┐
│    Agent    │ ────────────────► │  Wikipedia Search  │
│  (Claude    │ ◄──────────────── │  (candidates list) │
│  Haiku 4.5) │   action=fetch    ├───────────────────┤
│             │ ────────────────► │  Wikipedia Fetch   │
│             │ ◄──────────────── │  (full content)    │
└─────────────┘                   └───────────────────┘
     │
     ▼
  Answer (Answer: ... / Source: ...)
     │
     ▼
┌─────────────────────────────────────────────────────┐
│                   Eval Harness                       │
│                                                     │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────┐ │
│  │  Retrieval   │  │   Accuracy    │  │Boundaries│ │
│  │  Graders     │  │   Graders     │  │ Graders  │ │
│  │              │  │               │  │          │ │
│  │ tool_use     │  │ factual       │  │no_opinion│ │
│  │ query_entity │  │ groundedness  │  │          │ │
│  └──────────────┘  └───────────────┘  └──────────┘ │
└─────────────────────────────────────────────────────┘
     │
     ▼
  scores.json + summary.md
     │
     ▼
┌─────────────────────────────────────────────────────┐
│                  Hill Climber                        │
│                                                     │
│  1. Load failed cases from latest eval run          │
│  2. Build improvement prompt (failures + rationale) │
│  3. Claude Sonnet generates revised prompt section  │
│  4. Auto re-eval with new prompt version            │
│  5. Log rationale + score delta to history.jsonl   │
└─────────────────────────────────────────────────────┘
```

### Tool Design

`search_wikipedia` has two actions:

| Action | Input | Returns |
|---|---|---|
| `search` | entity name | ranked candidates: key, title, description, excerpt |
| `fetch` | page key from search results | full article plain text (8k chars) |

The agent always searches first, reads candidates, then fetches the chosen one. This allows disambiguation — for ambiguous queries like "Jaguar", the agent sees all candidates and selects the most relevant.

### Prompt Versions

| Version | Key change |
|---|---|
| v1 | Baseline — entity-based search, XML section structure |
| v2 | Reinforced entity-only queries, hard 3-search stop |
| v3 | Prohibited pre-search clarification; refusal format fixed |
| v4 | Added/removed general knowledge fallback (wrong fix — reverted) |
| v5 | Self-check decision rule; replaced eval-derived examples with principles |
| v6 | Groundedness self-check; two-action search/fetch tool |
| v7 | (current) |

Full rationale trail: `logs/hillclimb/history.jsonl`

---

## Eval Suite

### Training Set (`evals/suite.jsonl`) — 24 cases

| Category | Cases | What it tests |
|---|---|---|
| `factual_recall` | Q001–Q004 | Multi-entity or deep-extraction facts |
| `entity_lookup` | Q005–Q008 | Entity name absent from question — must infer what to search |
| `comparative` | Q009–Q012 | Two-entity comparisons — temporal, scale, overlap |
| `causal` | Q013–Q016 | Causal chains — A→B→C transitive + direct A→B |
| `unanswerable` | Q017–Q020 | Must refuse — opinion, future, real-time, personal |
| `ambiguous` | Q021–Q024 | Ambiguous term — acknowledge both, pick one, ask to clarify |

### Holdout Set (`evals/holdout.jsonl`) — 10 cases

Same category distribution, zero entity overlap with training set. Used to validate that hill climb improvements generalise and are not overfitting.

```bash
# After each hill climb cycle, compare:
python -m src.cli eval --suite evals/suite.jsonl --prompt vN
python -m src.cli eval --suite evals/holdout.jsonl --prompt vN

# Healthy: both improve. Overfitting: training improves, holdout drops.
```

### Complexity Framework

Cases are scored on four axes before inclusion (see `.claude/skills/eval_case_complexity.md`):
- **Search Friction** — how hard is it to find the right Wikipedia article?
- **Extraction Depth** — how buried is the answer within the article?
- **Reasoning Load** — how much synthesis is required?
- **Answer Precision** — how exact must the answer be?

Minimum bar: L3+ on at least two axes.

---

## Rubrics & Graders

### V0 Graders (active)

| Rubric | Category | Type | Threshold | What it measures |
|---|---|---|---|---|
| `tool_use_appropriateness` | retrieval | rule-based | 0.70 | Searched when required; fetch count within limit |
| `query_entity_adherence` | retrieval | LLM-judge | 0.70 | Queries are entity names, not question fragments |
| `factual_accuracy` | accuracy | hybrid | 0.70 | Answer is factually correct per Wikipedia |
| `groundedness` | accuracy | LLM-judge | 0.80 | Every claim traces to retrieved content |
| `no_opinion_leakage` | boundaries | rule-based | 0.80 | Pure refusal on opinion/unanswerable questions |

### Pass Rate Definition

A case **passes overall** if all non-skipped, non-errored graders pass. Skipped graders (e.g. `groundedness` skips cases with no searches) are excluded from the AND.

The summary reports per-case pass rates per category — not aggregated grader-evaluation counts.

---

## Models

| Role | Model |
|---|---|
| Agent (answers questions) | `claude-haiku-4-5-20251001` |
| Graders (LLM-as-judge) | `claude-haiku-4-5-20251001` (same client as agent) |
| Hill climb optimizer | `claude-sonnet-4-6` |

Override via `--model` (agent/eval) or `--judge-model` (hill climb).

---

## Project Structure

```
anthropic_eval_harness/
├── setup.sh                        # one-shot setup
├── CLAUDE.md                       # index to references and skills
├── .claude/
│   ├── references/
│   │   ├── assignment.xml          # full assignment spec
│   │   └── wikipedia_api.xml       # MediaWiki REST API reference
│   └── skills/
│       └── eval_case_complexity.md # 4-axis complexity framework for eval authoring
├── src/
│   ├── cli.py                      # run / eval / hillclimb commands
│   ├── agent/
│   │   ├── client.py               # ClaudeClient
│   │   ├── tools.py                # search_wikipedia tool (action=search|fetch)
│   │   ├── agent.py                # agentic loop
│   │   └── prompts/                # vN.md prompt versions
│   ├── wikipedia/
│   │   └── retriever.py            # MediaWiki REST API wrapper (with retry)
│   ├── eval/
│   │   ├── suite.py                # JSONL loader + validator
│   │   ├── harness.py              # parallel run loop, trace writer, summary builder
│   │   └── graders/
│   │       ├── base.py             # Grader ABC, GraderResult, Trace dataclasses
│   │       ├── retrieval/          # tool_use, query_entity
│   │       ├── accuracy/           # factual, groundedness
│   │       └── boundaries/         # no_opinion, ambiguity (stub)
│   └── hillclimb/
│       └── runner.py               # full hill climb pipeline
├── evals/
│   ├── suite.jsonl                 # 24 training cases
│   ├── holdout.jsonl               # 10 holdout cases
│   └── creation_log.md             # per-case axis scores and rationale
└── logs/
    ├── eval_runs/                  # timestamped run directories
    └── hillclimb/
        └── history.jsonl           # full hill climb history with rationale
```

---

## Constraints

- Uses **Anthropic API only** (`claude-haiku-4-5-20251001`, `claude-sonnet-4-6`)
- No built-in hosted search or RAG tools — Wikipedia integration is custom-built via the [MediaWiki REST API](https://en.wikipedia.org/w/rest.php/v1)
- Wikipedia data source: live API with retry logic (no local dump)

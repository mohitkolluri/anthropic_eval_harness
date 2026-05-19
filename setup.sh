#!/usr/bin/env bash
# setup.sh — one-shot setup for the Wikipedia QA Eval Harness
#
# Usage:
#   source setup.sh   ← recommended: installs everything AND activates the venv
#   bash setup.sh     ← installs everything, then tells you to activate manually
#
# Why: child processes (bash setup.sh) cannot modify the parent shell's environment.
# Sourcing the script runs it in the current shell, so activation persists.
set -e

# Detect whether we are being sourced or run as a subprocess
_SOURCED=0
if [ "${BASH_SOURCE[0]}" != "${0}" ] 2>/dev/null; then
  _SOURCED=1
fi

echo "=== Wikipedia QA Eval Harness — Setup ==="
echo ""

# ── 1. Python version check ───────────────────────────────────────────────────
REQUIRED="3.12"
PYTHON=$(which python3 2>/dev/null || which python 2>/dev/null)
if [ -z "$PYTHON" ]; then
  echo "ERROR: Python not found. Install Python $REQUIRED+ and retry."
  exit 1
fi
PY_VERSION=$($PYTHON --version 2>&1 | awk '{print $2}')
echo "Python: $PY_VERSION (found at $PYTHON)"

# ── 2. Virtual environment ────────────────────────────────────────────────────
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  if ! $PYTHON -m venv .venv 2>/dev/null; then
    echo ""
    echo "ERROR: 'venv' module not available."
    echo "On Ubuntu/Debian: sudo apt install python3-venv"
    echo "On macOS:         brew install python@3.12"
    exit 1
  fi
  echo "Virtual environment: created"
else
  echo "Virtual environment: .venv (exists)"
fi
source .venv/bin/activate
echo "Activated: $VIRTUAL_ENV"

# ── 3. Dependencies (from pyproject.toml) ────────────────────────────────────
echo ""
echo "Installing dependencies from pyproject.toml..."
pip install -q --upgrade pip
pip install -q -e .
echo "Dependencies installed."

# ── 4. API key ────────────────────────────────────────────────────────────────
echo ""
if [ -f ".env" ] && grep -q "ANTHROPIC_API_KEY=sk-ant-" .env 2>/dev/null; then
  echo ".env: found (key already set)"
else
  # Prefer existing env var, otherwise prompt the user
  if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" > .env
    echo ".env: created from \$ANTHROPIC_API_KEY environment variable"
  else
    echo "Anthropic API key required."
    echo "Get yours at: https://console.anthropic.com/settings/keys"
    echo ""
    printf "Enter your ANTHROPIC_API_KEY (sk-ant-...): "
    read -r USER_KEY
    if [ -z "$USER_KEY" ]; then
      echo "ERROR: No key provided. Re-run setup.sh and enter your key."
      exit 1
    fi
    echo "ANTHROPIC_API_KEY=$USER_KEY" > .env
    echo ".env: created with provided key"
  fi
fi

# ── 5. Log directories ────────────────────────────────────────────────────────
mkdir -p logs/eval_runs logs/hillclimb
echo "Log directories: ready"

# ── 6. Smoke test ─────────────────────────────────────────────────────────────
echo ""
echo "Running import smoke test..."
python -c "
from src.agent.agent import load_prompt
from src.eval.suite import load_suite
from src.eval.harness import make_graders
from src.hillclimb.runner import run_hillclimb
ver, _ = load_prompt()
cases = load_suite('evals/suite.jsonl')
print(f'  prompt: {ver}  |  suite: {len(cases)} training cases')
" && echo "  imports OK"

# ── 7. Summary ────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup complete ==="
echo ""

# Auto-activate if sourced; otherwise print the one-liner
if [ "$_SOURCED" -eq 1 ]; then
  source .venv/bin/activate
  echo "Virtual environment activated. You are ready to go."
  echo ""
else
  echo "One more step — activate the virtual environment:"
  echo ""
  echo "  source .venv/bin/activate"
  echo ""
  echo "Tip: run 'source setup.sh' next time to skip this step."
  echo ""
fi
echo "  # Interactive Q&A"
echo "  python -m src.cli run"
echo "  python -m src.cli run --trace          # with full debug trace"
echo ""
echo "  # Run eval suite (training)"
echo "  python -m src.cli eval"
echo "  python -m src.cli eval --suite evals/holdout.jsonl   # holdout validation"
echo ""
echo "  # Hill climb"
echo "  python -m src.cli hillclimb --category accuracy"
echo "  python -m src.cli hillclimb --rubric groundedness"
echo ""
echo "  # Override model"
echo "  python -m src.cli eval --model claude-sonnet-4-6"
echo "  python -m src.cli hillclimb --category retrieval --judge-model claude-sonnet-4-6"

#!/usr/bin/env bash
# Run the full intrinsic-evaluation pipeline end-to-end.
#
# Usage:
#   export ANTHROPIC_API_KEY="sk-ant-..."
#   ./evaluation/run_all.sh
#
# What it does:
#   1. Verifies the venv is active and ANTHROPIC_API_KEY is set
#   2. Runs the 46 unit tests
#   3. Generates 3 persona-simulated SAGE conversations (Opus 4.7 + Haiku 4.5)
#   4. Runs both metrics (rule-based + LLM-as-judge) over authored + simulated transcripts
#   5. Prints the summary and shows you how to commit the results

set -euo pipefail

# Always run from the repo root, regardless of where the script was invoked from.
cd "$(dirname "$0")/.."

echo "==> Step 1/4: Sanity checks"
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "ERROR: ANTHROPIC_API_KEY is not set." >&2
    echo "Run: export ANTHROPIC_API_KEY=\"sk-ant-...\"" >&2
    exit 1
fi
if ! python -c "import anthropic" 2>/dev/null; then
    echo "ERROR: anthropic SDK not importable. Run: pip install -e \".[dev]\"" >&2
    exit 1
fi
echo "    OK (key present, anthropic SDK importable)"
echo

echo "==> Step 2/4: Unit tests (no API spend)"
pytest evaluation/tests -q
echo

echo "==> Step 3/4: Generating 3 persona-simulated transcripts (spends API tokens)"
python -m evaluation.personas.simulator --all
echo

echo "==> Step 4/4: Running both metrics over all transcripts"
python -m evaluation.run_evaluation
echo

# Print the most recent summary so the user sees the result without hunting for it.
LATEST_SUMMARY="$(ls -t evaluation/results/*-summary.md | head -n 1)"
echo "==> Summary ($LATEST_SUMMARY):"
echo
cat "$LATEST_SUMMARY"
echo

echo "==> Done. To commit the canonical run for the assignment submission:"
cat <<'EOF'
    git add -f evaluation/results/*-results.json \
                evaluation/results/*-summary.md \
                evaluation/fixtures/simulated/*.json
    git commit -m "evaluation: first full run results (rule-based + LLM-as-judge)"
    git push -u origin AgentV2.1
EOF

"""Run both intrinsic-evaluation metrics over all available transcripts.

Sources:
  - examples/interactions/positive/*.md     (origin="authored", expected positive signal)
  - examples/interactions/negative/*.md     (origin="authored", expected negative signal)
  - evaluation/fixtures/simulated/*.json    (origin="simulated", from persona simulator)
  - evaluation/fixtures/exports/*.{md,txt}  (origin="exported", from the Streamlit app's
                                            "Export chat" button; see sage/export.py)

Outputs:
  - Experiment Results/<run_id>-results.json
  - Experiment Results/<run_id>-summary.md
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from evaluation.metrics.answer_first import AnthropicJudge, score_answer_first
from evaluation.metrics.front_loading import score_front_loading
from evaluation.metrics.transcript import (
    Transcript,
    parse_exported_chat,
    parse_markdown,
    parse_simulated_json,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORED_DIR = REPO_ROOT / "examples" / "interactions"
SIMULATED_DIR = Path(__file__).parent / "fixtures" / "simulated"
EXPORTS_DIR = Path(__file__).parent / "fixtures" / "exports"
RESULTS_DIR = REPO_ROOT / "Experiment Results"
JUDGE_CACHE_PATH = RESULTS_DIR / ".judge-cache.json"


@dataclass
class TranscriptScored:
    transcript: Transcript
    front_loading: list[dict]
    answer_first: list[dict]


def _load_authored(authored_dir: Path = DEFAULT_AUTHORED_DIR) -> list[Transcript]:
    """Load authored transcripts from {authored_dir}/{positive,negative}/*.md.

    Skips silently if subdirs don't exist — useful when the eval module is
    used in a project without curated authored transcripts.
    """
    out: list[Transcript] = []
    for label in ("positive", "negative"):
        for path in sorted((authored_dir / label).glob("*.md")):
            source_id = f"{label}/{path.stem}"
            out.append(parse_markdown(path.read_text(), source_id=source_id, origin="authored"))
    return out


def _load_simulated(simulated_dir: Path = SIMULATED_DIR) -> list[Transcript]:
    """Load simulated transcripts; skip and warn on malformed files instead of aborting."""
    out: list[Transcript] = []
    for path in sorted(simulated_dir.glob("*.json")):
        try:
            out.append(parse_simulated_json(path))
        except ValueError as e:
            print(f"Skipping malformed simulated transcript {path.name}: {e}", file=sys.stderr)
    return out


def _load_exported() -> list[Transcript]:
    """Load chats exported from the SAGE Streamlit app.

    Picks up *.md and *.txt under evaluation/fixtures/exports/. Files with
    zero parseable turns are skipped with a warning so a stray README or
    template doesn't pollute the run.
    """
    out: list[Transcript] = []
    if not EXPORTS_DIR.exists():
        return out
    for path in sorted(p for ext in ("*.md", "*.txt") for p in EXPORTS_DIR.glob(ext)):
        source_id = f"exported/{path.stem}"
        transcript = parse_exported_chat(path.read_text(), source_id=source_id)
        if not transcript.turns:
            print(f"Skipping {path.name}: no parseable turns found", file=sys.stderr)
            continue
        out.append(transcript)
    return out


def _git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def _merge_results(transcript: Transcript, fl: list[dict], af: list[dict]) -> list[dict]:
    """One row per SAGE turn, with both metric outputs side-by-side."""
    fl_by_turn = {r["turn_index"]: r for r in fl}
    af_by_turn = {r["turn_index"]: r for r in af}
    rows: list[dict] = []
    for turn in transcript.turns:
        if turn.speaker != "sage":
            continue
        rows.append({
            "turn_index": turn.index,
            "speaker": turn.speaker,
            "front_loading": fl_by_turn.get(turn.index),
            "answer_first": af_by_turn.get(turn.index),
        })
    return rows


def _aggregate(results: list[TranscriptScored]) -> dict:
    """Pass-rate aggregates per metric, overall and per origin/label."""
    def rate(values: Iterable[bool | None]) -> dict:
        scored = [v for v in values if v is not None]
        if not scored:
            return {"applicable": 0, "passed": 0, "rate": None}
        passed = sum(1 for v in scored if v)
        return {
            "applicable": len(scored),
            "passed": passed,
            "rate": round(passed / len(scored), 3),
        }

    fl_overall: list[bool] = []
    af_overall: list[bool | None] = []
    by_label: dict[str, dict[str, list[bool | None]]] = {}

    for ts in results:
        label = ts.transcript.source_id.split("/", 1)[0]
        bucket = by_label.setdefault(label, {"front_loading": [], "answer_first": []})
        for r in ts.front_loading:
            fl_overall.append(r["passed"])
            bucket["front_loading"].append(r["passed"])
        for r in ts.answer_first:
            af_overall.append(r["passed"])
            bucket["answer_first"].append(r["passed"])

    return {
        "overall": {
            "front_loading": rate(fl_overall),
            "answer_first": rate(af_overall),
        },
        "by_label": {
            label: {
                "front_loading": rate(b["front_loading"]),
                "answer_first": rate(b["answer_first"]),
            }
            for label, b in by_label.items()
        },
    }


def _write_summary(run_id: str, results: list[TranscriptScored], aggregates: dict, sage_version: str) -> Path:
    lines: list[str] = []
    lines.append(f"# Intrinsic Evaluation Results — {run_id}")
    lines.append("")
    lines.append(f"- **SAGE version:** `{sage_version}`")
    lines.append(f"- **Transcripts evaluated:** {len(results)}")
    lines.append("")

    lines.append("## Overall pass rates")
    lines.append("")
    lines.append("| Metric | Applicable turns | Passed | Pass rate |")
    lines.append("|---|---|---|---|")
    for metric in ("front_loading", "answer_first"):
        m = aggregates["overall"][metric]
        lines.append(f"| {metric} | {m['applicable']} | {m['passed']} | {m['rate']} |")
    lines.append("")

    lines.append("## Pass rates by source label")
    lines.append("")
    lines.append("| Label | Front-Loading | Answer-First |")
    lines.append("|---|---|---|")
    for label, m in sorted(aggregates["by_label"].items()):
        fl = m["front_loading"]
        af = m["answer_first"]
        lines.append(f"| {label} | {fl['passed']}/{fl['applicable']} ({fl['rate']}) | {af['passed']}/{af['applicable']} ({af['rate']}) |")
    lines.append("")

    lines.append("## Per-transcript breakdown")
    lines.append("")
    for ts in results:
        fl_pass = sum(1 for r in ts.front_loading if r["passed"])
        af_applicable = [r for r in ts.answer_first if r["applicable"]]
        af_pass = sum(1 for r in af_applicable if r["passed"])
        lines.append(
            f"- **{ts.transcript.source_id}** ({ts.transcript.origin}, "
            f"{sum(1 for t in ts.transcript.turns if t.speaker == 'sage')} SAGE turns): "
            f"front-loading {fl_pass}/{len(ts.front_loading)}, "
            f"answer-first {af_pass}/{len(af_applicable)}"
        )
    lines.append("")

    lines.append("## Sanity check")
    lines.append("")
    pos = aggregates["by_label"].get("positive", {})
    neg = aggregates["by_label"].get("negative", {})
    if pos and neg:
        pos_fl = pos["front_loading"]["rate"]
        neg_fl = neg["front_loading"]["rate"]
        pos_af = pos["answer_first"]["rate"]
        neg_af = neg["answer_first"]["rate"]
        lines.append(
            "Negative authored transcripts should fail more often than positive ones. "
            f"Front-loading pass rate: positive={pos_fl}, negative={neg_fl}. "
            f"Answer-first pass rate: positive={pos_af}, negative={neg_af}."
        )
    else:
        lines.append("Sanity check skipped — need both positive and negative authored transcripts.")
    lines.append("")

    out_path = RESULTS_DIR / f"{run_id}-summary.md"
    out_path.write_text("\n".join(lines))
    return out_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Score SAGE transcripts on Front-Loading and Answer-First metrics.",
    )
    parser.add_argument("--no-judge", action="store_true", help="Skip Metric 2 (no API calls)")
    parser.add_argument(
        "--exports-only",
        action="store_true",
        help="Score only chats in evaluation/fixtures/exports/, skipping authored and simulated transcripts.",
    )
    parser.add_argument(
        "--authored-dir",
        type=Path,
        default=DEFAULT_AUTHORED_DIR,
        help=(
            "Directory containing authored transcripts under positive/ and negative/ "
            f"subdirs (default: {DEFAULT_AUTHORED_DIR.relative_to(REPO_ROOT) if DEFAULT_AUTHORED_DIR.is_relative_to(REPO_ROOT) else DEFAULT_AUTHORED_DIR})."
        ),
    )
    parser.add_argument(
        "--simulated-dir",
        type=Path,
        default=SIMULATED_DIR,
        help=f"Directory containing persona-simulated *.json transcripts (default: {SIMULATED_DIR.relative_to(REPO_ROOT)}).",
    )
    parser.add_argument(
        "--label",
        type=str,
        default=None,
        help="Optional tag prepended to the run_id so results files are named e.g. final-agent-<ts>-results.json.",
    )
    parser.add_argument(
        "--no-authored",
        action="store_true",
        help="Skip authored transcripts (useful when comparing two agent versions on simulated transcripts only).",
    )
    args = parser.parse_args(argv)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.exports_only:
        transcripts = _load_exported()
        if not transcripts:
            raise SystemExit(
                "No exports found in evaluation/fixtures/exports/. "
                "Drop a .md or .txt file there (downloaded from the SAGE app's "
                "Export chat panel) and re-run."
            )
    else:
        authored = [] if args.no_authored else _load_authored(args.authored_dir)
        transcripts = authored + _load_simulated(args.simulated_dir) + _load_exported()
        if not transcripts:
            raise SystemExit(
                f"No transcripts found. Drop chats into evaluation/fixtures/exports/, "
                f"run the simulator, or point --authored-dir at a directory with "
                f"positive/*.md and negative/*.md (currently: {args.authored_dir})."
            )

    if args.no_judge:
        judge = None
    else:
        if "ANTHROPIC_API_KEY" not in os.environ:
            raise SystemExit("ANTHROPIC_API_KEY not set. Use --no-judge to skip Metric 2.")
        judge = AnthropicJudge(cache_path=JUDGE_CACHE_PATH)

    scored: list[TranscriptScored] = []
    for t in transcripts:
        fl = score_front_loading(t)
        af = score_answer_first(t, judge=judge) if judge is not None else []
        scored.append(TranscriptScored(transcript=t, front_loading=fl, answer_first=af))

    aggregates = _aggregate(scored)
    sage_version = _git_head()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%MZ")
    run_id = f"{args.label}-{timestamp}" if args.label else timestamp

    raw = {
        "run_id": run_id,
        "sage_version": sage_version,
        "aggregates": aggregates,
        "transcripts": [
            {
                "source_id": ts.transcript.source_id,
                "origin": ts.transcript.origin,
                "turn_results": _merge_results(ts.transcript, ts.front_loading, ts.answer_first),
            }
            for ts in scored
        ],
    }
    raw_path = RESULTS_DIR / f"{run_id}-results.json"
    raw_path.write_text(json.dumps(raw, indent=2))
    summary_path = _write_summary(run_id, scored, aggregates, sage_version)
    print(f"Wrote {raw_path}")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()

# Intrinsic Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build two intrinsic-evaluation metrics for SAGE — Front-Loading Discipline (rule-based) and Answer-First Adherence (LLM-as-judge) — and run them against 6 authored transcripts plus 3 persona-simulated sessions. Save dated results.

**Architecture:** A self-contained `evaluation/` package. The runner consumes `Transcript[Turn]` objects parsed from existing markdown files in `examples/interactions/` and from JSON files produced by a persona simulator. Each metric is an isolated module with a clean signature `(Transcript) -> list[MetricResult]`. The judge is a thin wrapper over the existing Anthropic SDK with a hash-keyed JSON cache. No new third-party dependencies beyond `pytest` for tests.

**Tech Stack:** Python 3.10+, `anthropic` SDK (already a project dep), `pytest` (added as a dev-extra), stdlib `re`/`dataclasses`/`json`/`hashlib`. Models: Haiku 4.5 for the classifier stage and the persona drivers, Sonnet 4.6 for the answer-first grader, Opus 4.7 for SAGE under test.

**Source spec:** `docs/superpowers/specs/2026-05-04-intrinsic-evaluation-design.md`

---

## File Structure

Files this plan will create:

```
evaluation/
  __init__.py                      # makes evaluation a package
  README.md                        # how to run, what each piece does
  tests/
    __init__.py
    conftest.py                    # pytest path setup
    test_transcript.py             # parser regression
    test_front_loading.py          # rule-based metric tests
    test_answer_first.py           # judge logic tests (mocked)
    test_judge_cache.py            # cache hit/miss test
    fixtures/
      sample_transcript.md         # tiny fixture used by parser tests
  metrics/
    __init__.py
    transcript.py                  # Turn, Transcript, parse_markdown, parse_simulated_json
    front_loading.py               # Metric 1
    answer_first.py                # Metric 2 (uses judge.py)
    judge.py                       # Anthropic client + JSON helper + cache
  personas/
    __init__.py
    personas.json                  # 3 persona definitions
    simulator.py                   # CLI: produces fixtures/simulated/*.json
  fixtures/
    simulated/                     # simulator outputs (gitignored)
    .gitkeep
  results/
    .gitkeep
  run_evaluation.py                # CLI: runs everything, writes results/<date>-*.{json,md}
```

Files this plan will modify:

- `pyproject.toml` — add `pytest` to optional `[project.optional-dependencies]` group `dev`, add `[tool.pytest.ini_options]` with `pythonpath = ["."]`.
- `.gitignore` — ignore `evaluation/fixtures/simulated/*.json` and `evaluation/results/*` (keep `.gitkeep`) and `evaluation/results/.judge-cache.json`.
- `README.md` — one-line link to `evaluation/README.md`.

---

## Task 1: Set up the evaluation package skeleton

**Files:**
- Create: `evaluation/__init__.py` (empty)
- Create: `evaluation/metrics/__init__.py` (empty)
- Create: `evaluation/personas/__init__.py` (empty)
- Create: `evaluation/tests/__init__.py` (empty)
- Create: `evaluation/tests/conftest.py`
- Create: `evaluation/fixtures/.gitkeep` (empty)
- Create: `evaluation/fixtures/simulated/.gitkeep` (empty)
- Create: `evaluation/results/.gitkeep` (empty)
- Modify: `pyproject.toml`
- Modify: `.gitignore`

- [ ] **Step 1: Create directory structure and empty package files**

```bash
mkdir -p evaluation/metrics evaluation/personas evaluation/tests evaluation/tests/fixtures evaluation/fixtures/simulated evaluation/results
touch evaluation/__init__.py evaluation/metrics/__init__.py evaluation/personas/__init__.py evaluation/tests/__init__.py evaluation/fixtures/.gitkeep evaluation/fixtures/simulated/.gitkeep evaluation/results/.gitkeep
```

- [ ] **Step 2: Write `evaluation/tests/conftest.py`**

```python
"""Pytest config: ensure project root is importable so 'from evaluation...' works."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```

- [ ] **Step 3: Add pytest config + dev extras to `pyproject.toml`**

Append to the existing `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0",
]

[tool.pytest.ini_options]
pythonpath = ["."]
testpaths = ["evaluation/tests"]
```

- [ ] **Step 4: Update `.gitignore`**

Append:

```
# Evaluation harness runtime data
evaluation/fixtures/simulated/*.json
evaluation/results/*.json
evaluation/results/*.md
evaluation/results/.judge-cache.json
!evaluation/results/.gitkeep
!evaluation/fixtures/simulated/.gitkeep
```

- [ ] **Step 5: Install dev dependencies**

```bash
pip install -e ".[dev]"
```

Expected: pytest installs cleanly.

- [ ] **Step 6: Verify pytest discovers tests directory**

```bash
pytest --collect-only
```

Expected: `no tests ran` (no test files yet) — verifies pytest config is valid, not crashing.

- [ ] **Step 7: Commit**

```bash
git add evaluation/ pyproject.toml .gitignore
git commit -m "evaluation: scaffold package + pytest config"
```

---

## Task 2: Transcript parser

**Files:**
- Create: `evaluation/metrics/transcript.py`
- Create: `evaluation/tests/fixtures/sample_transcript.md`
- Create: `evaluation/tests/test_transcript.py`

- [ ] **Step 1: Write a tiny test fixture**

`evaluation/tests/fixtures/sample_transcript.md`:

```markdown
# Sample

**Profile**: test
**Skills**: none

---

## Interaction Transcript

**LEARNER**: Hi there.

**SAGE**: Hello! What would you like to work on today?

**LEARNER**: I want to practice prompts.

**SAGE**: Great. Let's start with a quick scenario. Ready?

---

## Why This Interaction Is Beneficial

This is meta content that should be ignored.
```

- [ ] **Step 2: Write the failing parser tests**

`evaluation/tests/test_transcript.py`:

```python
from pathlib import Path
from evaluation.metrics.transcript import parse_markdown, parse_simulated_json, Turn, Transcript

FIXTURE = Path(__file__).parent / "fixtures" / "sample_transcript.md"


def test_parses_alternating_speakers():
    t = parse_markdown(FIXTURE.read_text(), source_id="sample", origin="authored")
    assert isinstance(t, Transcript)
    assert t.source_id == "sample"
    assert t.origin == "authored"
    assert len(t.turns) == 4
    assert [turn.speaker for turn in t.turns] == ["learner", "sage", "learner", "sage"]


def test_turn_indices_are_sequential():
    t = parse_markdown(FIXTURE.read_text(), source_id="sample", origin="authored")
    assert [turn.index for turn in t.turns] == [0, 1, 2, 3]


def test_drops_meta_section_after_final_separator():
    t = parse_markdown(FIXTURE.read_text(), source_id="sample", origin="authored")
    last = t.turns[-1].text
    assert "Ready?" in last
    assert "meta content" not in last
    assert "Why This Interaction" not in last


def test_strips_whitespace_from_turn_bodies():
    t = parse_markdown(FIXTURE.read_text(), source_id="sample", origin="authored")
    for turn in t.turns:
        assert turn.text == turn.text.strip()
        assert turn.text != ""


def test_empty_input_returns_zero_turns():
    t = parse_markdown("", source_id="empty", origin="authored")
    assert t.turns == []


def test_parse_simulated_json_round_trip(tmp_path):
    payload = {
        "source_id": "sim/foo",
        "origin": "simulated",
        "turns": [
            {"index": 0, "speaker": "learner", "text": "hi"},
            {"index": 1, "speaker": "sage", "text": "hello"},
        ],
    }
    p = tmp_path / "sim.json"
    p.write_text(__import__("json").dumps(payload))
    t = parse_simulated_json(p)
    assert t.source_id == "sim/foo"
    assert t.origin == "simulated"
    assert len(t.turns) == 2
    assert t.turns[0].speaker == "learner"
    assert t.turns[1].text == "hello"
```

- [ ] **Step 3: Run the tests to verify they fail**

```bash
pytest evaluation/tests/test_transcript.py -v
```

Expected: ImportError or "module not found" — `transcript` module doesn't exist yet.

- [ ] **Step 4: Implement the parser**

`evaluation/metrics/transcript.py`:

```python
"""Markdown and JSON transcript parsing.

The authored transcripts in examples/interactions/ use **LEARNER**: / **SAGE**:
markers. The simulated transcripts produced by the persona simulator are JSON
with the same Turn shape. Both produce a Transcript dataclass.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Literal, Union

Speaker = Literal["learner", "sage"]
Origin = Literal["authored", "simulated"]


@dataclass
class Turn:
    index: int
    speaker: Speaker
    text: str


@dataclass
class Transcript:
    source_id: str
    origin: Origin
    turns: list[Turn]

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "origin": self.origin,
            "turns": [asdict(t) for t in self.turns],
        }


_MARKER_RE = re.compile(r"^\*\*(LEARNER|SAGE)\*\*:", re.MULTILINE)
_SEP_LINE_RE = re.compile(r"^---\s*$", re.MULTILINE)


def parse_markdown(md: str, source_id: str, origin: Origin) -> Transcript:
    """Parse a SAGE markdown transcript into a Transcript.

    Conventions:
    - Speaker markers: lines that start with **LEARNER**: or **SAGE**:.
    - Conversation ends at the first --- line that appears AFTER the last marker.
    - Anything before the first marker (e.g., title, profile, frontmatter --- separator)
      is ignored.
    """
    matches = list(_MARKER_RE.finditer(md))
    if not matches:
        return Transcript(source_id=source_id, origin=origin, turns=[])

    last_marker_end = matches[-1].end()
    sep_after = _SEP_LINE_RE.search(md, pos=last_marker_end)
    end_of_conversation = sep_after.start() if sep_after else len(md)

    turns: list[Turn] = []
    for i, m in enumerate(matches):
        speaker = m.group(1).lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else end_of_conversation
        text = md[start:end].strip()
        turns.append(Turn(index=i, speaker=speaker, text=text))  # type: ignore[arg-type]
    return Transcript(source_id=source_id, origin=origin, turns=turns)


def parse_simulated_json(path: Union[str, Path]) -> Transcript:
    """Load a simulator-produced JSON transcript."""
    payload = json.loads(Path(path).read_text())
    turns = [Turn(**t) for t in payload["turns"]]
    return Transcript(
        source_id=payload["source_id"],
        origin=payload["origin"],
        turns=turns,
    )
```

- [ ] **Step 5: Run the tests to verify they pass**

```bash
pytest evaluation/tests/test_transcript.py -v
```

Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
git add evaluation/metrics/transcript.py evaluation/tests/test_transcript.py evaluation/tests/fixtures/sample_transcript.md
git commit -m "evaluation: add transcript parser (markdown + simulated JSON)"
```

---

## Task 3: Front-Loading Discipline metric

**Files:**
- Create: `evaluation/metrics/front_loading.py`
- Create: `evaluation/tests/test_front_loading.py`

- [ ] **Step 1: Write the failing tests**

`evaluation/tests/test_front_loading.py`:

```python
from evaluation.metrics.transcript import Turn, Transcript
from evaluation.metrics.front_loading import score_front_loading


def _t(text: str) -> Transcript:
    return Transcript(
        source_id="test",
        origin="authored",
        turns=[Turn(index=0, speaker="sage", text=text)],
    )


def test_zero_questions_short_passes():
    r = score_front_loading(_t("Welcome to SAGE."))[0]
    assert r["question_discipline"]["question_marks"] == 0
    assert r["question_discipline"]["passed"] is True
    assert r["pre_pause"]["sentences"] == 1
    assert r["pre_pause"]["passed"] is True
    assert r["passed"] is True


def test_one_question_passes():
    text = "Nice work. What stood out to you in that response?"
    r = score_front_loading(_t(text))[0]
    assert r["question_discipline"]["question_marks"] == 1
    assert r["question_discipline"]["passed"] is True
    assert r["pre_pause"]["sentences"] == 1
    assert r["passed"] is True


def test_two_questions_fails_question_discipline():
    text = "What did you mean? And why did that surprise you?"
    r = score_front_loading(_t(text))[0]
    assert r["question_discipline"]["question_marks"] == 2
    assert r["question_discipline"]["passed"] is False
    assert r["passed"] is False


def test_long_pre_pause_fails():
    text = (
        "First sentence. Second sentence. Third sentence. Fourth sentence. "
        "Fifth sentence. What do you think?"
    )
    r = score_front_loading(_t(text))[0]
    assert r["pre_pause"]["sentences"] == 5
    assert r["pre_pause"]["passed"] is False
    assert r["passed"] is False


def test_pre_pause_at_threshold_passes():
    text = "One. Two. Three. Four. What now?"
    r = score_front_loading(_t(text))[0]
    assert r["pre_pause"]["sentences"] == 4
    assert r["pre_pause"]["passed"] is True


def test_no_question_long_text_fails_pre_pause():
    text = "One. Two. Three. Four. Five."
    r = score_front_loading(_t(text))[0]
    assert r["question_discipline"]["passed"] is True  # zero question marks is fine
    assert r["pre_pause"]["sentences"] == 5
    assert r["pre_pause"]["passed"] is False
    assert r["passed"] is False


def test_only_sage_turns_are_scored():
    transcript = Transcript(
        source_id="x",
        origin="authored",
        turns=[
            Turn(index=0, speaker="learner", text="Hi"),
            Turn(index=1, speaker="sage", text="Hello! Ready?"),
            Turn(index=2, speaker="learner", text="Yes."),
        ],
    )
    results = score_front_loading(transcript)
    assert len(results) == 1
    assert results[0]["turn_index"] == 1
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest evaluation/tests/test_front_loading.py -v
```

Expected: ImportError — `front_loading` module doesn't exist yet.

- [ ] **Step 3: Implement the metric**

`evaluation/metrics/front_loading.py`:

```python
"""Metric 1: Front-Loading Discipline (rule-based).

Two sub-checks per SAGE turn:
  - Question Discipline: count of '?' must be <= 1.
  - Pre-Pause Length: sentence count up to first '?' (or full turn if no '?')
    must be <= 4.
"""
from __future__ import annotations

import re
from typing import Any

from evaluation.metrics.transcript import Transcript

_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_PRE_PAUSE_THRESHOLD = 4


def _count_sentences(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    parts = [p for p in _SENTENCE_SPLIT_RE.split(text) if p.strip()]
    return len(parts)


def _score_turn(text: str) -> dict[str, Any]:
    qmarks = text.count("?")
    qd_passed = qmarks <= 1

    if "?" in text:
        pre_pause_text = text[: text.index("?")]
    else:
        pre_pause_text = text
    sentences = _count_sentences(pre_pause_text)
    pp_passed = sentences <= _PRE_PAUSE_THRESHOLD

    return {
        "question_discipline": {
            "question_marks": qmarks,
            "passed": qd_passed,
        },
        "pre_pause": {
            "sentences": sentences,
            "passed": pp_passed,
        },
        "passed": qd_passed and pp_passed,
    }


def score_front_loading(transcript: Transcript) -> list[dict[str, Any]]:
    """Score every SAGE turn in the transcript. Learner turns are skipped."""
    results: list[dict[str, Any]] = []
    for turn in transcript.turns:
        if turn.speaker != "sage":
            continue
        scored = _score_turn(turn.text)
        scored["turn_index"] = turn.index
        results.append(scored)
    return results
```

- [ ] **Step 4: Run tests to verify pass**

```bash
pytest evaluation/tests/test_front_loading.py -v
```

Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add evaluation/metrics/front_loading.py evaluation/tests/test_front_loading.py
git commit -m "evaluation: add front-loading discipline metric"
```

---

## Task 4: Judge module (Anthropic client + JSON helper + cache)

**Files:**
- Create: `evaluation/metrics/judge.py`
- Create: `evaluation/tests/test_judge_cache.py`

- [ ] **Step 1: Write the failing cache test**

`evaluation/tests/test_judge_cache.py`:

```python
import json
from pathlib import Path

from evaluation.metrics.judge import JudgeCache, cache_key


def test_cache_key_is_stable():
    k1 = cache_key("model-x", "tplv1", "user msg", "assistant msg")
    k2 = cache_key("model-x", "tplv1", "user msg", "assistant msg")
    assert k1 == k2


def test_cache_key_changes_with_template_version():
    k1 = cache_key("model-x", "tplv1", "u", "a")
    k2 = cache_key("model-x", "tplv2", "u", "a")
    assert k1 != k2


def test_cache_key_changes_with_inputs():
    k1 = cache_key("model-x", "tplv1", "u", "a")
    k2 = cache_key("model-x", "tplv1", "u2", "a")
    assert k1 != k2


def test_cache_persists_to_disk(tmp_path: Path):
    cache_path = tmp_path / "cache.json"
    cache = JudgeCache(cache_path)
    cache.put("k1", {"behavior": "answered_first"})
    cache.save()

    cache2 = JudgeCache(cache_path)
    assert cache2.get("k1") == {"behavior": "answered_first"}


def test_cache_miss_returns_none(tmp_path: Path):
    cache = JudgeCache(tmp_path / "cache.json")
    assert cache.get("missing") is None


def test_cache_loads_empty_file_gracefully(tmp_path: Path):
    cache_path = tmp_path / "cache.json"
    cache_path.write_text("")
    cache = JudgeCache(cache_path)
    assert cache.get("anything") is None
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest evaluation/tests/test_judge_cache.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement `judge.py`**

`evaluation/metrics/judge.py`:

```python
"""Thin wrapper around the Anthropic SDK for LLM-as-judge metrics.

Provides:
  - cache_key(): deterministic hash for caching judge calls
  - JudgeCache: simple JSON file cache (load/get/put/save)
  - call_judge_json(): call Claude with a system+user prompt, return parsed JSON dict
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import anthropic


def cache_key(model: str, template_version: str, learner_msg: str, sage_msg: str) -> str:
    payload = f"{model}\x00{template_version}\x00{learner_msg}\x00{sage_msg}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class JudgeCache:
    def __init__(self, path: Path):
        self.path = Path(path)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        text = self.path.read_text()
        if not text.strip():
            return
        try:
            self._data = json.loads(text)
        except json.JSONDecodeError:
            self._data = {}

    def get(self, key: str) -> Optional[dict]:
        return self._data.get(key)

    def put(self, key: str, value: dict) -> None:
        self._data[key] = value

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2))


_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(text: str) -> dict:
    """Extract the first {...} block from a model response and parse it."""
    m = _JSON_BLOCK_RE.search(text)
    if not m:
        raise ValueError(f"No JSON object found in judge output: {text!r}")
    return json.loads(m.group(0))


@dataclass
class JudgeCall:
    model: str
    system: str
    user: str
    template_version: str
    max_tokens: int = 300


def call_judge_json(
    call: JudgeCall,
    *,
    cache: Optional[JudgeCache] = None,
    cache_inputs: Optional[tuple[str, str]] = None,
    client: Optional[anthropic.Anthropic] = None,
) -> dict:
    """Run a judge call. Returns parsed JSON. Optionally caches by (model, template_version, *cache_inputs)."""
    if cache is not None and cache_inputs is not None:
        key = cache_key(call.model, call.template_version, *cache_inputs)
        hit = cache.get(key)
        if hit is not None:
            return hit
    else:
        key = None

    if client is None:
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model=call.model,
        max_tokens=call.max_tokens,
        system=call.system,
        messages=[{"role": "user", "content": call.user}],
    )
    raw = response.content[0].text  # type: ignore[union-attr]
    parsed = _extract_json(raw)

    if cache is not None and key is not None:
        cache.put(key, parsed)
        cache.save()
    return parsed
```

- [ ] **Step 4: Run tests to verify pass**

```bash
pytest evaluation/tests/test_judge_cache.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add evaluation/metrics/judge.py evaluation/tests/test_judge_cache.py
git commit -m "evaluation: add judge harness with JSON cache"
```

---

## Task 5: Answer-First Adherence metric

**Files:**
- Create: `evaluation/metrics/answer_first.py`
- Create: `evaluation/tests/test_answer_first.py`

- [ ] **Step 1: Write the failing tests with a fake judge**

`evaluation/tests/test_answer_first.py`:

```python
from evaluation.metrics.transcript import Turn, Transcript
from evaluation.metrics.answer_first import score_answer_first


class FakeJudge:
    """Substitutes for the real Anthropic-backed judge in tests."""

    def __init__(self, classifier_results, grader_results):
        # Each is a list of dicts; consumed in order per call.
        self.classifier_results = list(classifier_results)
        self.grader_results = list(grader_results)
        self.classifier_calls = []
        self.grader_calls = []

    def classify(self, learner_message: str) -> dict:
        self.classifier_calls.append(learner_message)
        return self.classifier_results.pop(0)

    def grade(self, learner_message: str, sage_message: str) -> dict:
        self.grader_calls.append((learner_message, sage_message))
        return self.grader_results.pop(0)


def _conv(*turns) -> Transcript:
    return Transcript(
        source_id="t",
        origin="authored",
        turns=[Turn(index=i, speaker=s, text=txt) for i, (s, txt) in enumerate(turns)],
    )


def test_skips_sage_turns_with_no_prior_learner_turn():
    transcript = _conv(("sage", "Welcome!"))
    judge = FakeJudge([], [])
    results = score_answer_first(transcript, judge=judge)
    assert results[0]["applicable"] is False
    assert results[0]["passed"] is None
    assert judge.classifier_calls == []


def test_skips_when_classifier_says_not_a_question():
    transcript = _conv(
        ("learner", "Cool."),
        ("sage", "Glad to hear it. Want to try a scenario?"),
    )
    judge = FakeJudge(
        classifier_results=[{"kind": "not_a_question", "reasoning": "statement"}],
        grader_results=[],
    )
    results = score_answer_first(transcript, judge=judge)
    sage_result = next(r for r in results if r["turn_index"] == 1)
    assert sage_result["applicable"] is False
    assert sage_result["kind"] == "not_a_question"
    assert sage_result["passed"] is None
    assert judge.grader_calls == []


def test_skips_when_classifier_says_open_question():
    transcript = _conv(
        ("learner", "Tell me about your experience with AI."),
        ("sage", "Sure thing. What do you mean?"),
    )
    judge = FakeJudge(
        classifier_results=[{"kind": "open", "reasoning": "open-ended"}],
        grader_results=[],
    )
    results = score_answer_first(transcript, judge=judge)
    sage_result = next(r for r in results if r["turn_index"] == 1)
    assert sage_result["applicable"] is False
    assert judge.grader_calls == []


def test_yes_no_question_passes_when_answered_first():
    transcript = _conv(
        ("learner", "Is it okay to paste customer data into ChatGPT?"),
        ("sage", "No — that's a leak risk. Want to talk through alternatives?"),
    )
    judge = FakeJudge(
        classifier_results=[{"kind": "yes_no", "reasoning": "yn"}],
        grader_results=[{"behavior": "answered_and_followed_up", "reasoning": "answered then asked"}],
    )
    results = score_answer_first(transcript, judge=judge)
    r = next(r for r in results if r["turn_index"] == 1)
    assert r["applicable"] is True
    assert r["kind"] == "yes_no"
    assert r["behavior"] == "answered_and_followed_up"
    assert r["passed"] is True


def test_factual_question_fails_when_redirected_without_answer():
    transcript = _conv(
        ("learner", "What is a hallucination?"),
        ("sage", "What do you think it might mean?"),
    )
    judge = FakeJudge(
        classifier_results=[{"kind": "factual", "reasoning": "what is X"}],
        grader_results=[{"behavior": "redirected_without_answer", "reasoning": "no answer"}],
    )
    results = score_answer_first(transcript, judge=judge)
    r = next(r for r in results if r["turn_index"] == 1)
    assert r["applicable"] is True
    assert r["passed"] is False


def test_answered_first_only_passes():
    transcript = _conv(
        ("learner", "Is the AI going to remember this later?"),
        ("sage", "No — each session is independent."),
    )
    judge = FakeJudge(
        classifier_results=[{"kind": "yes_no", "reasoning": "yn"}],
        grader_results=[{"behavior": "answered_first", "reasoning": "answered"}],
    )
    results = score_answer_first(transcript, judge=judge)
    r = next(r for r in results if r["turn_index"] == 1)
    assert r["passed"] is True


def test_non_answer_fails():
    transcript = _conv(
        ("learner", "Is hallucination always bad?"),
        ("sage", "Hallucination is a really interesting word, isn't it?"),
    )
    judge = FakeJudge(
        classifier_results=[{"kind": "yes_no", "reasoning": "yn"}],
        grader_results=[{"behavior": "non_answer", "reasoning": "evasive"}],
    )
    results = score_answer_first(transcript, judge=judge)
    r = next(r for r in results if r["turn_index"] == 1)
    assert r["passed"] is False
```

- [ ] **Step 2: Run to verify failure**

```bash
pytest evaluation/tests/test_answer_first.py -v
```

Expected: ImportError.

- [ ] **Step 3: Implement the metric**

`evaluation/metrics/answer_first.py`:

```python
"""Metric 2: Answer-First Adherence (LLM-as-judge).

Two-stage judge applied to SAGE turns whose immediately preceding turn is from
the learner:
  Stage 1 (classifier): is the learner's message a direct question (yes_no | factual)?
  Stage 2 (grader, only if Stage 1 qualifies): did SAGE answer before redirecting?

Pass condition: behavior in {answered_first, answered_and_followed_up}.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional, Protocol

from evaluation.metrics.judge import JudgeCache, JudgeCall, call_judge_json
from evaluation.metrics.transcript import Transcript

CLASSIFIER_MODEL = "claude-haiku-4-5"
GRADER_MODEL = "claude-sonnet-4-6"
TEMPLATE_VERSION = "v1"

QUALIFYING_KINDS = {"yes_no", "factual"}
PASSING_BEHAVIORS = {"answered_first", "answered_and_followed_up"}

CLASSIFIER_SYSTEM = """You classify whether a learner's message to a tutor is a "direct question"
that requires a substantive answer before any follow-up coaching question.

Categories:
- "yes_no": a question whose natural answer is yes/no
            (e.g., "Is it okay to paste customer data into ChatGPT?")
- "factual": a question asking for a definition or explanation
            (e.g., "What is a hallucination?", "How does prompt caching work?")
- "open":   an open-ended invitation (e.g., "Tell me about your experience...")
- "not_a_question": statement, reaction, or compliance message.

Return ONLY a JSON object with keys "kind" and "reasoning". No prose outside JSON."""

GRADER_SYSTEM = """You grade whether a tutor answered a learner's direct question before redirecting.

Categories for the tutor's reply:
- "answered_first":           tutor gave a substantive answer; may have stopped there.
- "answered_and_followed_up": tutor answered substantively, THEN asked a coaching question.
- "redirected_without_answer": tutor responded with a question or new topic without
                              addressing the substance of the learner's question.
- "non_answer":               tutor produced text but it doesn't address the question
                              (evasive, off-topic, or only restates the question).

Return ONLY a JSON object with keys "behavior" and "reasoning". No prose outside JSON."""


class JudgeProtocol(Protocol):
    def classify(self, learner_message: str) -> dict: ...
    def grade(self, learner_message: str, sage_message: str) -> dict: ...


class AnthropicJudge:
    """Real judge: calls Claude via the Anthropic SDK with a JSON cache."""

    def __init__(self, cache_path: Optional[Path] = None, client=None):
        self.cache: Optional[JudgeCache] = JudgeCache(cache_path) if cache_path else None
        self.client = client  # If None, call_judge_json constructs one.

    def classify(self, learner_message: str) -> dict:
        call = JudgeCall(
            model=CLASSIFIER_MODEL,
            system=CLASSIFIER_SYSTEM,
            user=f"Learner message:\n\n{learner_message}",
            template_version=f"classifier-{TEMPLATE_VERSION}",
        )
        return call_judge_json(
            call,
            cache=self.cache,
            cache_inputs=(learner_message, ""),
            client=self.client,
        )

    def grade(self, learner_message: str, sage_message: str) -> dict:
        call = JudgeCall(
            model=GRADER_MODEL,
            system=GRADER_SYSTEM,
            user=(
                "Learner question:\n"
                f"{learner_message}\n\n"
                "Tutor reply:\n"
                f"{sage_message}"
            ),
            template_version=f"grader-{TEMPLATE_VERSION}",
        )
        return call_judge_json(
            call,
            cache=self.cache,
            cache_inputs=(learner_message, sage_message),
            client=self.client,
        )


def score_answer_first(
    transcript: Transcript,
    judge: JudgeProtocol,
) -> list[dict[str, Any]]:
    """Score every SAGE turn whose prior turn is a learner direct question."""
    results: list[dict[str, Any]] = []
    turns = transcript.turns

    for i, turn in enumerate(turns):
        if turn.speaker != "sage":
            continue

        prior = turns[i - 1] if i > 0 else None
        if prior is None or prior.speaker != "learner":
            results.append({
                "turn_index": turn.index,
                "applicable": False,
                "kind": None,
                "behavior": None,
                "reasoning": "no prior learner turn",
                "passed": None,
            })
            continue

        classification = judge.classify(prior.text)
        kind = classification.get("kind")
        if kind not in QUALIFYING_KINDS:
            results.append({
                "turn_index": turn.index,
                "applicable": False,
                "kind": kind,
                "behavior": None,
                "reasoning": classification.get("reasoning", ""),
                "passed": None,
            })
            continue

        grading = judge.grade(prior.text, turn.text)
        behavior = grading.get("behavior")
        results.append({
            "turn_index": turn.index,
            "applicable": True,
            "kind": kind,
            "behavior": behavior,
            "reasoning": grading.get("reasoning", ""),
            "passed": behavior in PASSING_BEHAVIORS,
        })
    return results
```

- [ ] **Step 4: Run tests to verify pass**

```bash
pytest evaluation/tests/test_answer_first.py -v
```

Expected: 7 passed.

- [ ] **Step 5: Commit**

```bash
git add evaluation/metrics/answer_first.py evaluation/tests/test_answer_first.py
git commit -m "evaluation: add answer-first adherence metric (two-stage judge)"
```

---

## Task 6: Persona simulator

**Files:**
- Create: `evaluation/personas/personas.json`
- Create: `evaluation/personas/simulator.py`

This task has no automated tests — the simulator makes API calls, and a fake-Anthropic test would mostly be tautological (testing that we read what we wrote). Verification is manual: run it once and inspect the output JSON.

- [ ] **Step 1: Define personas**

`evaluation/personas/personas.json`:

```json
[
  {
    "id": "novice-curious",
    "system": "You are role-playing as a first-year sociology student new to AI tools. You ask short, sometimes-confused questions. Some of your questions are direct yes/no questions (e.g. 'Is it bad if I just paste my essay in?'). Keep replies to 1-2 sentences. Do not reveal you are role-playing.",
    "opening": "I'm new to AI agents. Where do I start?",
    "max_turns": 8,
    "stop_phrases": ["bye", "thanks, that's enough", "let's wrap up"]
  },
  {
    "id": "skeptical-engineer",
    "system": "You are role-playing as a senior software engineer skeptical of AI tutoring. Push back, ask pointed factual questions ('What is a hallucination, technically?'), and lose patience with hand-holding. Keep replies under 3 sentences. Do not reveal you are role-playing.",
    "opening": "What is a hallucination, technically? Don't sugarcoat it.",
    "max_turns": 6,
    "stop_phrases": ["okay, done", "moving on", "not useful"]
  },
  {
    "id": "fatigued-returner",
    "system": "You are role-playing as a returning learner who is tired and short on time. Your replies get progressively shorter and terser ('idk', 'sure', 'one more'). You sometimes ask to wrap up. Never write more than one sentence. Do not reveal you are role-playing.",
    "opening": "Quick session — let's just do one thing. What should I work on?",
    "max_turns": 5,
    "stop_phrases": ["that's enough", "i'm done", "wrap up", "tired"]
  }
]
```

- [ ] **Step 2: Implement the simulator**

`evaluation/personas/simulator.py`:

```python
"""Persona-driven SAGE simulation.

Drives a conversation between a persona-LLM (acting as the learner) and SAGE.
Both run on Anthropic. SAGE uses the deployed system prompt from sage.prompts.

Usage:
    python -m evaluation.personas.simulator --persona novice-curious
    python -m evaluation.personas.simulator --all
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import anthropic

from evaluation.metrics.transcript import Transcript, Turn
from sage.prompts import SYSTEM_PROMPT as SAGE_SYSTEM_PROMPT

PERSONAS_PATH = Path(__file__).parent / "personas.json"
OUT_DIR = Path(__file__).parent.parent / "fixtures" / "simulated"

SAGE_MODEL = "claude-opus-4-7"
PERSONA_MODEL = "claude-haiku-4-5"
MAX_TOKENS = 800


def _invert_roles(history: list[dict]) -> list[dict]:
    """Swap user<->assistant so the persona LLM sees SAGE's outputs as 'user'."""
    swapped = []
    for msg in history:
        role = "assistant" if msg["role"] == "user" else "user"
        swapped.append({"role": role, "content": msg["content"]})
    return swapped


def _should_stop(text: str, stop_phrases: list[str]) -> bool:
    low = text.lower()
    return any(phrase in low for phrase in stop_phrases)


def simulate(persona: dict, client: anthropic.Anthropic) -> Transcript:
    history: list[dict] = [{"role": "user", "content": persona["opening"]}]

    for _ in range(persona["max_turns"]):
        sage_response = client.messages.create(
            model=SAGE_MODEL,
            max_tokens=MAX_TOKENS,
            system=SAGE_SYSTEM_PROMPT,
            messages=history,
        )
        sage_text = sage_response.content[0].text  # type: ignore[union-attr]
        history.append({"role": "assistant", "content": sage_text})

        persona_response = client.messages.create(
            model=PERSONA_MODEL,
            max_tokens=MAX_TOKENS,
            system=persona["system"],
            messages=_invert_roles(history),
        )
        persona_text = persona_response.content[0].text  # type: ignore[union-attr]
        if _should_stop(persona_text, persona["stop_phrases"]):
            break
        history.append({"role": "user", "content": persona_text})

    turns: list[Turn] = []
    for i, msg in enumerate(history):
        speaker = "learner" if msg["role"] == "user" else "sage"
        turns.append(Turn(index=i, speaker=speaker, text=msg["content"].strip()))
    return Transcript(
        source_id=f"simulated/{persona['id']}",
        origin="simulated",
        turns=turns,
    )


def _save(transcript: Transcript) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    persona_id = transcript.source_id.split("/", 1)[1]
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = OUT_DIR / f"{persona_id}-{timestamp}.json"
    path.write_text(json.dumps(transcript.to_dict(), indent=2))
    return path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--persona", help="Persona id from personas.json")
    group.add_argument("--all", action="store_true", help="Run all personas")
    args = parser.parse_args(argv)

    personas = json.loads(PERSONAS_PATH.read_text())
    if args.all:
        chosen = personas
    else:
        chosen = [p for p in personas if p["id"] == args.persona]
        if not chosen:
            raise SystemExit(f"Unknown persona: {args.persona}")

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    for persona in chosen:
        print(f"Running persona: {persona['id']}...")
        transcript = simulate(persona, client)
        path = _save(transcript)
        print(f"  -> wrote {path} ({len(transcript.turns)} turns)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Manual verification — run one persona end-to-end**

```bash
export ANTHROPIC_API_KEY="<your-key>"
python -m evaluation.personas.simulator --persona novice-curious
```

Expected: prints "Running persona: novice-curious..." then "-> wrote evaluation/fixtures/simulated/novice-curious-<timestamp>.json (N turns)". Open the file and confirm it contains alternating learner/sage turns with realistic content.

- [ ] **Step 4: Commit**

```bash
git add evaluation/personas/personas.json evaluation/personas/simulator.py
git commit -m "evaluation: add persona-driven SAGE simulator"
```

---

## Task 7: End-to-end runner

**Files:**
- Create: `evaluation/run_evaluation.py`

- [ ] **Step 1: Implement the runner**

`evaluation/run_evaluation.py`:

```python
"""Run both intrinsic-evaluation metrics over all available transcripts.

Sources:
  - examples/interactions/positive/*.md   (origin="authored", expected positive signal)
  - examples/interactions/negative/*.md   (origin="authored", expected negative signal)
  - evaluation/fixtures/simulated/*.json  (origin="simulated")

Outputs:
  - evaluation/results/<run_id>-results.json
  - evaluation/results/<run_id>-summary.md
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from evaluation.metrics.answer_first import AnthropicJudge, score_answer_first
from evaluation.metrics.front_loading import score_front_loading
from evaluation.metrics.transcript import Transcript, parse_markdown, parse_simulated_json

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples" / "interactions"
SIMULATED_DIR = Path(__file__).parent / "fixtures" / "simulated"
RESULTS_DIR = Path(__file__).parent / "results"
JUDGE_CACHE_PATH = RESULTS_DIR / ".judge-cache.json"


@dataclass
class TranscriptScored:
    transcript: Transcript
    front_loading: list[dict]
    answer_first: list[dict]


def _load_authored() -> list[Transcript]:
    out: list[Transcript] = []
    for label in ("positive", "negative"):
        for path in sorted((EXAMPLES_DIR / label).glob("*.md")):
            source_id = f"{label}/{path.stem}"
            out.append(parse_markdown(path.read_text(), source_id=source_id, origin="authored"))
    return out


def _load_simulated() -> list[Transcript]:
    out: list[Transcript] = []
    for path in sorted(SIMULATED_DIR.glob("*.json")):
        out.append(parse_simulated_json(path))
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-judge", action="store_true", help="Skip Metric 2 (no API calls)")
    args = parser.parse_args(argv)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    transcripts = _load_authored() + _load_simulated()
    if not transcripts:
        raise SystemExit("No transcripts found. Run the simulator or check examples/interactions/.")

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
    run_id = datetime.utcnow().strftime("%Y-%m-%dT%H-%MZ")

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
```

- [ ] **Step 2: Smoke test the runner with rule-based metric only**

```bash
python -m evaluation.run_evaluation --no-judge
```

Expected: writes two files under `evaluation/results/`. The summary should show `front_loading` rates for both `positive` and `negative` labels, with `answer_first` rates blank/zero (no judge run).

- [ ] **Step 3: Inspect the summary file**

```bash
ls evaluation/results/
cat evaluation/results/*-summary.md | head -40
```

Expected: front-loading pass rate is *higher* for `positive` than for `negative`. If not, investigate before moving to live judge.

- [ ] **Step 4: Commit**

```bash
git add evaluation/run_evaluation.py
git commit -m "evaluation: add end-to-end runner with summary report"
```

---

## Task 8: Generate persona transcripts and full evaluation run

This task spends real API tokens. Verify Tasks 1–7 are committed and tested before starting.

- [ ] **Step 1: Run all three personas**

```bash
export ANTHROPIC_API_KEY="<your-key>"
python -m evaluation.personas.simulator --all
```

Expected: 3 JSON files written under `evaluation/fixtures/simulated/`. Open each and confirm the conversations look in-character (novice asks short questions, engineer is curt, fatigued user goes terse).

- [ ] **Step 2: Run the full evaluation (rule-based + judge)**

```bash
python -m evaluation.run_evaluation
```

Expected: writes `<date>-results.json` and `<date>-summary.md` under `evaluation/results/`. First run will take ~30–60 seconds (judge calls); cache populates.

- [ ] **Step 3: Sanity check the summary**

```bash
cat evaluation/results/*-summary.md
```

Expected:
- Positive label has higher front-loading and answer-first pass rates than negative.
- Simulated transcripts have rates somewhere in between (live SAGE should be reasonably good but not perfect).
- Per-transcript table prints all 9 transcripts.

- [ ] **Step 4: Re-run to verify cache hits**

```bash
time python -m evaluation.run_evaluation
```

Expected: second run completes in <5 seconds (no Anthropic calls — judge cache fully hits).

- [ ] **Step 5: Commit the results**

```bash
git add -f evaluation/results/*-results.json evaluation/results/*-summary.md evaluation/fixtures/simulated/*.json
git commit -m "evaluation: first full run results (rule-based + LLM-as-judge)"
```

Note: `-f` is required because `.gitignore` excludes these by default. Committing one canonical run gives the assignment-link a static artifact to review.

---

## Task 9: Document the harness

**Files:**
- Create: `evaluation/README.md`
- Modify: `README.md` (project root)

- [ ] **Step 1: Write `evaluation/README.md`**

```markdown
# SAGE Intrinsic Evaluation

Two metrics that score SAGE against its own pedagogical contract.

## Metrics

### Metric 1 — Front-Loading Discipline (rule-based)
Per SAGE turn, two sub-checks:
- **Question Discipline** — count of `?` must be ≤ 1 (catches stacked questions in one turn).
- **Pre-Pause Length** — number of sentences before the first `?` must be ≤ 4 (catches walls of text before SAGE invites the learner in). If the turn has no `?`, the whole turn is measured.

A turn passes when both sub-checks pass.

### Metric 2 — Answer-First Adherence (LLM-as-judge)
Two-stage judge applied to SAGE turns whose immediately preceding learner turn is a direct question.
- **Stage 1 (Haiku 4.5):** classify the prior learner message — `yes_no`, `factual`, `open`, or `not_a_question`. Only `yes_no` and `factual` qualify for grading.
- **Stage 2 (Sonnet 4.6):** grade SAGE's reply — `answered_first`, `answered_and_followed_up`, `redirected_without_answer`, or `non_answer`.

A turn passes when behavior is `answered_first` or `answered_and_followed_up`.

## Test data

- 6 authored transcripts: `examples/interactions/{positive,negative}/*.md`
- 3 persona-simulated sessions: `evaluation/fixtures/simulated/*.json`
  - `novice-curious` — short, sometimes-confused yes/no questions
  - `skeptical-engineer` — pointed factual questions, low patience
  - `fatigued-returner` — terse, asks to wrap up

## Running it

```bash
# install dev deps once
pip install -e ".[dev]"

# run unit tests
pytest evaluation/tests -v

# generate persona transcripts (spends API tokens)
export ANTHROPIC_API_KEY="<your-key>"
python -m evaluation.personas.simulator --all

# rule-based metric only (no API tokens)
python -m evaluation.run_evaluation --no-judge

# both metrics (uses cache after first run)
python -m evaluation.run_evaluation
```

## Output

- `evaluation/results/<run-id>-results.json` — raw per-turn scores
- `evaluation/results/<run-id>-summary.md` — human-readable aggregates + per-transcript breakdown
- `evaluation/results/.judge-cache.json` — gitignored hash-keyed judge cache (re-runs against unchanged transcripts cost zero tokens)

## Design

See `docs/superpowers/specs/2026-05-04-intrinsic-evaluation-design.md`.
```

- [ ] **Step 2: Add a one-line link in the project root README**

Open `README.md`, find the "Project Structure" section (around line 145), and add `evaluation/` to the layout block. Then add a one-line link near the bottom (above "Feedback").

Find this in `README.md`:

```
## Feedback
```

Insert before it:

```
## Evaluation

Intrinsic evaluation harness lives in [`evaluation/`](evaluation/). It runs two metrics against authored transcripts plus persona-simulated sessions and writes dated results.
```

In the Project Structure block (the `evaluation/` line is missing), add it after the `examples/` block:

```
evaluation/                    # Intrinsic evaluation: metrics + persona simulator + runner
  metrics/                     # Front-loading (rule-based), answer-first (LLM-as-judge)
  personas/                    # 3 simulated learner profiles + simulator
  results/                     # Dated runs (gitignored except canonical samples)
```

- [ ] **Step 3: Verify everything still builds**

```bash
pytest evaluation/tests -v
```

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add evaluation/README.md README.md
git commit -m "evaluation: document the harness"
```

---

## Task 10: Final verification + push

- [ ] **Step 1: Run the full test suite**

```bash
pytest evaluation/tests -v
```

Expected: 20 tests pass (6 transcript + 7 front-loading + 6 cache + 7 answer-first... actually 26 — count once final).

- [ ] **Step 2: Confirm all artifacts exist**

```bash
ls evaluation/results/*.json evaluation/results/*.md evaluation/fixtures/simulated/*.json
```

Expected: at least one results JSON, one summary MD, three simulated JSONs.

- [ ] **Step 3: Push the branch**

```bash
git push -u origin AgentV2.1
```

Expected: branch pushes; the assignment can link directly to the branch on GitHub.

- [ ] **Step 4: Capture the branch link for the assignment submission**

The submission expects a link to a branch. Format: `https://github.com/Elorm-K/498_Agents/tree/AgentV2.1` (or whatever the actual remote slug is — check `git remote get-url origin`).

---

## Self-Review (completed inline by the plan author before handoff)

**Spec coverage:**
- Metric 1 (Front-Loading Discipline) — Task 3 ✓
- Metric 2 (Answer-First Adherence) — Task 5 ✓
- Two-stage judge with Haiku classifier + Sonnet grader — Task 5 ✓
- Hash-keyed JSON cache with template versioning — Task 4 ✓
- 6 authored transcripts loaded from `examples/interactions/` — Task 7 ✓
- 3 persona-simulated sessions — Tasks 6 + 8 ✓
- Markdown parser with `**LEARNER**:` / `**SAGE**:` markers + `---` boundary — Task 2 ✓
- Results JSON + summary MD format from spec — Task 7 ✓
- Sanity check (negative > positive failure rate) — Task 7 (in summary) ✓
- Parser regression test — Task 2 ✓
- Cache hit/miss test — Task 4 ✓
- Documentation — Task 9 ✓

**Type consistency:**
- `Turn`/`Transcript` dataclasses defined in Task 2, reused by Tasks 3, 5, 6, 7 with matching field names (`speaker` literal `learner|sage`, `origin` literal `authored|simulated`).
- `score_front_loading()` returns list of dicts; `score_answer_first()` returns list of dicts; runner iterates both with `["turn_index"]` keys — consistent.
- `JudgeProtocol` defines `classify` and `grade`; `AnthropicJudge` implements both with matching signatures — consistent.

**Placeholders:** none. Every code step contains complete code. Every command shows expected output.

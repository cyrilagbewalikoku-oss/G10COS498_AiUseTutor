"""SAGE tools — data access for profiles, scenarios, and rubrics.

Tools handle data I/O only. All pedagogical logic lives in the system prompt.
"""

import json
import os
import random
import re
from pathlib import Path

import anthropic
from anthropic import beta_tool

# Restrict profile filenames to letters/digits/hyphen/underscore + .json
# Prevents path traversal (../) and absolute-path escapes (/etc/passwd).
_SAFE_FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\-]*\.json$")

# Data directory resolution:
# 1. SAGE_DATA_DIR env var (explicit override)
# 2. ../data/ relative to this file (running from repo checkout)
# 3. ./data/ relative to cwd (fallback)
_PACKAGE_ROOT = Path(__file__).resolve().parent.parent

if os.environ.get("SAGE_DATA_DIR"):
    DATA_DIR = Path(os.environ["SAGE_DATA_DIR"])
elif (_PACKAGE_ROOT / "data").is_dir():
    DATA_DIR = _PACKAGE_ROOT / "data"
else:
    DATA_DIR = Path.cwd() / "data"


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

@beta_tool
def load_user_profile(name: str) -> str:
    """Search for a learner's profile by name and return it as JSON.

    Returns the full profile JSON if found, or the string 'NOT_FOUND'
    if no matching profile exists.

    Args:
        name: The learner's name to search for (case-insensitive partial match).
    """
    users_dir = DATA_DIR / "users"
    if not users_dir.exists():
        return "NOT_FOUND"

    for filepath in sorted(users_dir.glob("*.json")):
        try:
            profile = json.loads(filepath.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        profile_name = profile.get("name", "")
        if name.lower() in profile_name.lower():
            return json.dumps(profile, indent=2)

    return "NOT_FOUND"


@beta_tool
def save_user_profile(filename: str, profile_json: str) -> str:
    """Save or update a learner's profile to data/users/<filename>.

    The profile_json must be a valid JSON string following the user-profile
    schema (id, name, level, dimensionScores, competencyScores, etc.).

    Args:
        filename: The filename to save as, e.g. 'novice-student.json'.
        profile_json: The complete profile as a JSON string.
    """
    users_dir = DATA_DIR / "users"
    users_dir.mkdir(parents=True, exist_ok=True)

    # Reject unsafe filenames (path traversal, absolute paths, weird chars)
    if not _SAFE_FILENAME_RE.match(filename):
        return (
            "ERROR: Invalid filename. Use letters, digits, hyphens, or "
            "underscores, ending in '.json' (e.g. 'alex-novice.json'). "
            "Path separators and traversal are not allowed."
        )

    # Validate JSON before writing
    try:
        profile = json.loads(profile_json)
    except json.JSONDecodeError as e:
        return f"ERROR: Invalid JSON — {e}"

    filepath = users_dir / filename

    # Defense-in-depth: confirm resolved path is still inside users_dir
    try:
        filepath.resolve().relative_to(users_dir.resolve())
    except ValueError:
        return "ERROR: Filename resolves outside the users directory."

    filepath.write_text(json.dumps(profile, indent=2) + "\n")
    return f"Profile saved to {filepath.relative_to(DATA_DIR)}"


@beta_tool
def list_users() -> str:
    """List all existing learner profiles with name, level, and session count.

    Returns a JSON array of summaries, or '[]' if no profiles exist.
    """
    users_dir = DATA_DIR / "users"
    if not users_dir.exists():
        return "[]"

    summaries = []
    for filepath in sorted(users_dir.glob("*.json")):
        try:
            profile = json.loads(filepath.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        summaries.append({
            "filename": filepath.name,
            "name": profile.get("name", "Unknown"),
            "level": profile.get("level", "unknown"),
            "sessionCount": profile.get("sessionCount", 0),
        })

    return json.dumps(summaries, indent=2)


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

@beta_tool
def list_scenarios(practice_type: str = "", difficulty: str = "") -> str:
    """List available practice scenarios with optional filters.

    Returns a JSON array of scenario summaries (id, title, practiceType,
    difficulty, estimatedMinutes).

    Args:
        practice_type: Filter by practice type, e.g. 'prompt_crafting', \
'output_evaluation', 'appropriateness_judgment', 'workflow_design'. Empty for all.
        difficulty: Filter by difficulty level, e.g. 'novice', 'practitioner', \
'advanced'. Empty for all.
    """
    scenarios_dir = DATA_DIR / "scenarios"
    if not scenarios_dir.exists():
        return "[]"

    results = []
    for filepath in sorted(scenarios_dir.glob("*.json")):
        try:
            scenario = json.loads(filepath.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        if practice_type and scenario.get("practiceType", "") != practice_type:
            continue
        if difficulty and scenario.get("difficulty", "") != difficulty:
            continue

        results.append({
            "id": scenario.get("id", filepath.stem),
            "title": scenario.get("title", filepath.stem),
            "practiceType": scenario.get("practiceType", ""),
            "difficulty": scenario.get("difficulty", ""),
            "estimatedMinutes": scenario.get("estimatedMinutes", 15),
        })

    return json.dumps(results, indent=2)


@beta_tool
def load_scenario(scenario_id: str) -> str:
    """Load a practice scenario by ID and return the full JSON.

    Args:
        scenario_id: The scenario ID, e.g. 'scenario-email-drafting-001'. \
Also matches partial filenames.
    """
    scenarios_dir = DATA_DIR / "scenarios"
    if not scenarios_dir.exists():
        return "NOT_FOUND"

    for filepath in sorted(scenarios_dir.glob("*.json")):
        try:
            scenario = json.loads(filepath.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        sid = scenario.get("id", filepath.stem)
        if scenario_id in sid or scenario_id in filepath.stem:
            return json.dumps(scenario, indent=2)

    return "NOT_FOUND"


# ---------------------------------------------------------------------------
# Rubrics
# ---------------------------------------------------------------------------

@beta_tool
def load_rubric(rubric_name: str) -> str:
    """Load an evaluation rubric by name and return the full JSON.

    Available rubrics: 'prompting-quality', 'output-evaluation', 'ethical-reasoning'.

    Args:
        rubric_name: The rubric name, e.g. 'prompting-quality'. Matches partial names.
    """
    rubrics_dir = DATA_DIR / "rubrics"
    if not rubrics_dir.exists():
        return "NOT_FOUND"

    for filepath in sorted(rubrics_dir.glob("*.json")):
        if rubric_name in filepath.stem:
            try:
                return filepath.read_text()
            except OSError:
                return "NOT_FOUND"

    return "NOT_FOUND"


# ---------------------------------------------------------------------------
# Dynamic scenario generation (output_evaluation only, for now)
# ---------------------------------------------------------------------------

# Error types allowed on an output_evaluation scenario. Mirrors the enum in
# data/schemas/scenario.schema.json. Kept here so the generator can validate
# without pulling in a full JSON-Schema validator.
_ALLOWED_ERROR_TYPES = {
    "hallucination",
    "overstatement",
    "logical_contradiction",
    "missing_context",
    "bias",
    "framing",
    "overconfidence",
}

_GENERATOR_MODEL = "claude-haiku-4-5-20251001"
_GENERATOR_MAX_TOKENS = 4000

# Meta-prompt used when making a nested API call to generate a fresh
# output-evaluation scenario from a template. Kept private to this module —
# it is NOT part of the SAGE system prompt (which is auto-generated from
# CLAUDE.md + skills).
OUTPUT_EVAL_GENERATOR_PROMPT = """\
You are a scenario generator for SAGE, an AI literacy tutor. Produce ONE practice \
scenario in strict JSON for the OUTPUT EVALUATION practice type.

Given a template spec and a chosen topic, you generate:
- A realistic "aiOutput" — what a confident AI might plausibly produce for the \
given persona, topic, and output_format. It should read like a real AI response: \
helpful-sounding and authoritative, with flaws woven into otherwise reasonable \
material.
- A parallel "errors" array. Every required_errors type from the template must \
appear. You may add optional_errors up to the target_error_count range.

HARD RULES (obey all of these):
1. Output ONLY a single JSON object. No prose. No markdown fences. No commentary.
2. Every errors[i].quote MUST be an EXACT substring of aiOutput — copied \
verbatim, character for character. If the quote is not in aiOutput, the \
scenario is invalid and will be rejected.
3. errors[i].type MUST be one of: hallucination, overstatement, \
logical_contradiction, missing_context, bias, framing, overconfidence.
4. Give each error a unique id (e1, e2, e3, ...). Each error should point to a \
DIFFERENT quote.
5. Use \\n for newlines inside aiOutput. lineStart/lineEnd are 1-indexed line \
numbers in aiOutput after splitting on \\n.
6. Keep the total error count inside target_error_count.min..max.
7. Do not telegraph the errors in aiOutput — the learner is supposed to catch \
them. But keep them detectable by a careful reader.

OUTPUT SHAPE (fields with <angle brackets> you must fill in; fields quoted \
literally must appear as-is):

{
  "id": "<generated-id-including-topic-slug>",
  "title": "<short title>",
  "description": "<one sentence describing the exercise>",
  "type": "output_evaluation",
  "practiceType": "output_evaluation",
  "difficulty": "<copy template.difficulty>",
  "learningObjectives": ["<copy template.learningObjectives verbatim>"],
  "setup": {
    "role": "<copy template.setup.role>",
    "task": "<copy template.setup.task>",
    "constraints": ["<copy template.setup.constraints verbatim, if present>"],
    "availableTools": ["<copy template.setup.availableTools verbatim, if present>"],
    "context": {
      "aiOutput": "<the flawed AI output, with \\n newlines>",
      "groundTruth": "<1-3 sentence narrative of what is accurate vs misleading>",
      "errors": [
        {
          "id": "e1",
          "quote": "<exact substring of aiOutput>",
          "lineStart": <int>,
          "lineEnd": <int>,
          "type": "<one of the allowed error types>",
          "severity": "<low|medium|high>",
          "explanation": "<one sentence, shown to the learner in the reveal>"
        }
      ]
    }
  },
  "evaluationCriteria": [ <copy template.evaluationCriteria verbatim> ],
  "maxTurns": <copy template.maxTurns>,
  "estimatedMinutes": <copy template.estimatedMinutes, default 20>
}

Template (JSON):
{template_json}

Chosen topic: {topic}

Return the JSON object now. Nothing else.
"""


def _strip_code_fences(text: str) -> str:
    """Strip surrounding ```json ... ``` fences if the model added them anyway."""
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.endswith("```"):
            text = text[:-3]
    return text.strip()


def _recompute_line_span(ai_output: str, quote: str) -> tuple[int, int] | None:
    """Find 1-indexed line span of `quote` in `ai_output`. Returns None if missing."""
    if not quote or quote not in ai_output:
        return None
    # Find the character offset of the first occurrence.
    start = ai_output.index(quote)
    end = start + len(quote)
    line_start = ai_output.count("\n", 0, start) + 1
    line_end = ai_output.count("\n", 0, end) + 1
    return line_start, line_end


def _validate_and_repair(
    scenario: dict, required_types: list[str], count_min: int, count_max: int
) -> dict | None:
    """Verify structural invariants and rewrite line numbers from actual quote positions.

    Returns the repaired scenario, or None if it cannot be repaired.
    """
    try:
        context = scenario["setup"]["context"]
        ai_output = context["aiOutput"]
        errors = context.get("errors", [])
    except (KeyError, TypeError):
        return None

    if not isinstance(ai_output, str) or not isinstance(errors, list):
        return None
    if not (count_min <= len(errors) <= count_max):
        return None

    seen_types: set[str] = set()
    repaired_errors: list[dict] = []
    for err in errors:
        if not isinstance(err, dict):
            return None
        err_type = err.get("type")
        quote = err.get("quote")
        if err_type not in _ALLOWED_ERROR_TYPES:
            return None
        span = _recompute_line_span(ai_output, quote or "")
        if span is None:
            return None
        err["lineStart"], err["lineEnd"] = span
        seen_types.add(err_type)
        repaired_errors.append(err)

    missing_required = [t for t in required_types if t not in seen_types]
    if missing_required:
        return None

    context["errors"] = repaired_errors
    scenario.setdefault("type", "output_evaluation")
    scenario.setdefault("practiceType", "output_evaluation")
    return scenario


def _load_template(template_id: str) -> dict | None:
    """Load a scenario template by id. Returns None if not found."""
    templates_dir = DATA_DIR / "scenario_templates"
    if not templates_dir.exists():
        return None
    for filepath in sorted(templates_dir.glob("*.json")):
        try:
            template = json.loads(filepath.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        tid = template.get("id", filepath.stem)
        if template_id in tid or template_id in filepath.stem:
            return template
    return None


@beta_tool
def generate_output_eval_scenario(template_id: str, topic: str = "") -> str:
    """Generate a fresh output-evaluation scenario from a template, at runtime.

    Loads a template from data/scenario_templates/, makes a nested Claude API
    call that produces a flawed aiOutput plus a matching errors[] array, then
    validates and returns the scenario as JSON. The returned shape matches
    load_scenario's output so scenario-runner can present it identically.

    Returns 'NOT_FOUND' if the template id doesn't match any template,
    'GENERATION_FAILED' if generation or validation fails after one retry.

    Args:
        template_id: Template id, e.g. 'essay-feedback-generic'. Partial match.
        topic: Optional topic override. If empty, one is picked from the \
template's topic_pool.
    """
    template = _load_template(template_id)
    if template is None:
        return "NOT_FOUND"

    generation = template.get("generation", {})
    pool = generation.get("topic_pool", [])
    chosen_topic = topic.strip() if topic else (random.choice(pool) if pool else "")

    required_types = [e["type"] for e in generation.get("required_errors", [])]
    count_spec = generation.get("target_error_count", {"min": 3, "max": 5})
    count_min = int(count_spec.get("min", 3))
    count_max = int(count_spec.get("max", 5))

    prompt = OUTPUT_EVAL_GENERATOR_PROMPT.format(
        template_json=json.dumps(template, indent=2),
        topic=chosen_topic or "(generator's choice)",
    )

    client = anthropic.Anthropic()
    for _attempt in range(2):
        try:
            response = client.messages.create(
                model=_GENERATOR_MODEL,
                max_tokens=_GENERATOR_MAX_TOKENS,
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.APIError:
            continue

        raw = "".join(
            block.text for block in response.content if block.type == "text"
        )
        try:
            scenario = json.loads(_strip_code_fences(raw))
        except json.JSONDecodeError:
            continue

        repaired = _validate_and_repair(
            scenario, required_types, count_min, count_max
        )
        if repaired is not None:
            return json.dumps(repaired, indent=2)

    return "GENERATION_FAILED"


# ---------------------------------------------------------------------------
# Collect all tools for the agent
# ---------------------------------------------------------------------------

ALL_TOOLS = [
    load_user_profile,
    save_user_profile,
    list_users,
    list_scenarios,
    load_scenario,
    load_rubric,
    generate_output_eval_scenario,
]

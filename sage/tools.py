"""SAGE tools — data access for profiles, scenarios, and rubrics.

Tools handle data I/O only. All pedagogical logic lives in the system prompt.
"""

import json
import os
import re
from pathlib import Path

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
# Collect all tools for the agent
# ---------------------------------------------------------------------------

ALL_TOOLS = [
    load_user_profile,
    save_user_profile,
    list_users,
    list_scenarios,
    load_scenario,
    load_rubric,
]

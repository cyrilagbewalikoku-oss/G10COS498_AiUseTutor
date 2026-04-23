"""Session store — profile + transcript state for the Streamlit UI.

Two responsibilities, one module:
- Profile I/O (identity + scores) under data/users/*.json
- Transcript I/O (conversation turns per session) under
  data/interactions/<user_id>/<session_id>.json, shaped by
  data/schemas/interaction-log.schema.json.

These helpers are plain functions (not @beta_tool) — they're called directly
by sage/app.py. The Claude tool layer lives in sage/tools.py and remains
separate so the LLM's view of profiles and the UI's view cannot drift.
"""

from __future__ import annotations

import json
import re
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sage.tools import DATA_DIR

# Filename/id safety — prevents path traversal.
_SAFE_FILENAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\-]*\.json$")
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\-]*$")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _users_dir() -> Path:
    d = DATA_DIR / "users"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _interactions_dir() -> Path:
    d = DATA_DIR / "interactions"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _user_transcript_dir(user_id: str) -> Path:
    if not _SAFE_ID_RE.match(user_id):
        raise ValueError(f"Unsafe user_id: {user_id!r}")
    d = _interactions_dir() / user_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _session_path(user_id: str, session_id: str) -> Path:
    if not _SAFE_ID_RE.match(session_id):
        raise ValueError(f"Unsafe session_id: {session_id!r}")
    return _user_transcript_dir(user_id) / f"{session_id}.json"


def _atomic_write_json(path: Path, data: dict) -> None:
    """Write JSON via temp-file + rename so a crash mid-write can't corrupt the log."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Profile I/O (UI-facing)
# ---------------------------------------------------------------------------

def list_profiles_for_ui() -> list[dict]:
    """Scan data/users/*.json and return a picker-friendly list.

    Returns a list sorted by most-recently-active first.
    """
    entries = []
    for path in _users_dir().glob("*.json"):
        try:
            profile = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        entries.append({
            "id": profile.get("id", path.stem),
            "name": profile.get("name", path.stem),
            "filename": path.name,
            "level": profile.get("level", "novice"),
            "lastActiveAt": profile.get("lastActiveAt", ""),
        })
    entries.sort(key=lambda e: e["lastActiveAt"], reverse=True)
    return entries


def load_profile_by_filename(filename: str) -> dict | None:
    if not _SAFE_FILENAME_RE.match(filename):
        return None
    path = _users_dir() / filename
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _slugify(name: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_\-]+", "-", name).strip("-").lower()
    return slug or "learner"


def save_profile(profile: dict) -> str:
    """Persist a profile. Returns the filename used.

    If a profile with the same id already exists on disk, overwrite it in place
    (by iterating filenames) rather than creating a duplicate.
    """
    users_dir = _users_dir()
    name = profile.get("name") or profile.get("id") or "learner"
    slug = _slugify(str(name))
    filename = f"{slug}.json"

    # Reuse the existing filename for this id if one exists
    existing_filename = None
    for path in users_dir.glob("*.json"):
        try:
            existing = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if existing.get("id") and existing.get("id") == profile.get("id"):
            existing_filename = path.name
            break

    if existing_filename:
        filename = existing_filename
    else:
        # Avoid clobbering a different learner who happens to share a slug
        i = 2
        while (users_dir / filename).exists():
            filename = f"{slug}-{i}.json"
            i += 1

    path = users_dir / filename
    path.write_text(json.dumps(profile, indent=2) + "\n")
    return filename


def create_new_learner(name: str, level: str = "novice") -> dict:
    """Create a minimal profile for a newly-introduced learner and persist it."""
    now = _now_iso()
    profile = {
        "id": str(uuid.uuid4()),
        "name": name.strip() or "Learner",
        "level": level,
        "dimensionScores": {
            "conceptualUnderstanding": 0.0,
            "promptingSkill": 0.0,
            "outputEvaluation": 0.0,
            "ethicalReasoning": 0.0,
            "criticalThinking": 0.0,
        },
        "competencyScores": {
            "promptCrafting": 0.0,
            "outputEvaluation": 0.0,
            "appropriatenessJudgment": 0.0,
            "workflowDesign": 0.0,
        },
        "sessionCount": 0,
        "totalInteractions": 0,
        "createdAt": now,
        "lastActiveAt": now,
    }
    save_profile(profile)
    return profile


def touch_last_active(profile: dict) -> None:
    profile["lastActiveAt"] = _now_iso()
    save_profile(profile)


# ---------------------------------------------------------------------------
# Transcript I/O (per learner, per session)
# ---------------------------------------------------------------------------

def _safe_id_from_profile(profile: dict) -> str:
    """Derive a filesystem-safe directory id for a profile.

    Some seed profiles use ids like 'cyril-001' (safe). Generated uuids are
    also safe. If we ever encounter something unsafe, fall back to the slug.
    """
    raw = str(profile.get("id", "")) or _slugify(str(profile.get("name", "learner")))
    if _SAFE_ID_RE.match(raw):
        return raw
    return _slugify(raw)


def new_session(profile: dict, skill_used: str = "session-router") -> str:
    """Mint a new session log for this learner. Returns the session_id."""
    user_id = _safe_id_from_profile(profile)
    session_id = str(uuid.uuid4())
    log = {
        "id": session_id,
        "userId": user_id,
        "sessionId": session_id,
        "timestamp": _now_iso(),
        "skillUsed": skill_used,
        "turns": [],
    }
    _atomic_write_json(_session_path(user_id, session_id), log)
    return session_id


def append_turn(
    profile: dict,
    session_id: str,
    role: str,
    content: str,
    metadata: dict | None = None,
) -> None:
    """Append a single turn to an existing session log.

    Accepts Anthropic-API roles ('user' / 'assistant') and stores them as
    schema roles ('learner' / 'sage').
    """
    schema_role = {"user": "learner", "assistant": "sage"}.get(role, role)
    user_id = _safe_id_from_profile(profile)
    path = _session_path(user_id, session_id)
    if not path.exists():
        raise FileNotFoundError(f"No session log at {path}")

    log = json.loads(path.read_text())
    turn = {
        "role": schema_role,
        "content": content,
        "timestamp": _now_iso(),
    }
    if metadata:
        turn["metadata"] = metadata
    log["turns"].append(turn)
    _atomic_write_json(path, log)


def load_session_messages(profile: dict, session_id: str) -> list[dict]:
    """Return an Anthropic-API-shaped messages list for a stored session."""
    user_id = _safe_id_from_profile(profile)
    path = _session_path(user_id, session_id)
    if not path.exists():
        return []
    try:
        log = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return []

    messages: list[dict] = []
    for turn in log.get("turns", []):
        role = {"learner": "user", "sage": "assistant"}.get(
            turn.get("role"), turn.get("role")
        )
        if role in ("user", "assistant"):
            messages.append({"role": role, "content": turn.get("content", "")})
    return messages


def latest_session_id(profile: dict) -> str | None:
    """Return the most recent session_id for this learner, or None."""
    user_id = _safe_id_from_profile(profile)
    d = _interactions_dir() / user_id
    if not d.exists():
        return None
    candidates: list[tuple[str, str]] = []
    for p in d.glob("*.json"):
        try:
            log = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        candidates.append((log.get("timestamp", ""), log.get("sessionId", p.stem)))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def session_turn_count(profile: dict, session_id: str) -> int:
    user_id = _safe_id_from_profile(profile)
    path = _session_path(user_id, session_id)
    if not path.exists():
        return 0
    try:
        log = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return 0
    return len(log.get("turns", []))


# ---------------------------------------------------------------------------
# Seed bootstrap (first-boot on a fresh Railway volume)
# ---------------------------------------------------------------------------

_SEED_SUBDIRS = ("users", "scenarios", "rubrics", "schemas", "research")


def seed_if_empty(source_root: Path | None = None) -> int:
    """If DATA_DIR/users is empty, copy the bundled data tree into DATA_DIR.

    Meant to run once on container startup. When a fresh Railway persistent
    volume is mounted at $SAGE_DATA_DIR, that directory starts empty; this
    function copies scenarios, rubrics, seed user profiles, etc. from the
    image's baked-in /app/data tree into the volume so everything is
    available on first boot.

    The source defaults to <package_root>/data (the image's canonical tree).
    Returns the number of files copied.
    """
    users_dir = _users_dir()
    if any(users_dir.glob("*.json")):
        return 0

    source_root = source_root or (Path(__file__).resolve().parent.parent / "data")
    if not source_root.exists() or source_root.resolve() == DATA_DIR.resolve():
        # Nothing to seed from, or DATA_DIR already IS the image data.
        return 0

    copied = 0
    for subdir in _SEED_SUBDIRS:
        src_dir = source_root / subdir
        if not src_dir.is_dir():
            continue
        dst_dir = DATA_DIR / subdir
        dst_dir.mkdir(parents=True, exist_ok=True)
        for src in src_dir.iterdir():
            if src.is_file() and not (dst_dir / src.name).exists():
                shutil.copy2(src, dst_dir / src.name)
                copied += 1
    return copied

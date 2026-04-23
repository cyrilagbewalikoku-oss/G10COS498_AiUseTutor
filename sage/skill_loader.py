"""Runtime loader that assembles SAGE's system prompt from live files.

Walks `.claude/skills/*/SKILL.md` at runtime, extracts each file's
`<!-- prompt-contribution:start --> ... <!-- prompt-contribution:end -->`
blocks, and concatenates them (after `CLAUDE.md`'s blocks) into the final
`SYSTEM_PROMPT`.

`scripts/build_prompts.py` calls into this module so the committed
`sage/prompts.py` snapshot stays byte-identical to what runtime produces.

Production Dockerfile does not ship `.claude/`. `build_system_prompt()`
returns `None` when the skills directory is missing; callers fall back to
the frozen `sage.prompts.SYSTEM_PROMPT`.
"""

from __future__ import annotations

import re
from pathlib import Path

BLOCK_RE = re.compile(
    r"<!--\s*prompt-contribution:start\s*-->\s*\n(.*?)\n\s*<!--\s*prompt-contribution:end\s*-->",
    re.DOTALL,
)

PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = PACKAGE_DIR.parent


def extract_blocks(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    return [m.group(1).strip() for m in BLOCK_RE.finditer(text)]


def discover_skills(skills_dir: Path) -> list[tuple[str, Path]]:
    """Return `(name, SKILL.md path)` for every skill subdirectory whose
    SKILL.md contains at least one prompt-contribution block. Sorted by name.
    """
    if not skills_dir.is_dir():
        return []
    found: list[tuple[str, Path]] = []
    for child in sorted(skills_dir.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        if not extract_blocks(skill_md):
            continue
        found.append((child.name, skill_md))
    return found


def build_system_prompt(project_root: Path | None = None) -> str | None:
    """Assemble the system prompt from CLAUDE.md + live skill files.

    Returns None if `.claude/skills/` is missing under `project_root`, so the
    caller can fall back to the frozen snapshot.
    """
    root = project_root or DEFAULT_ROOT
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.is_dir():
        return None

    sections: list[str] = []
    sections.extend(extract_blocks(root / "CLAUDE.md"))
    for _name, path in discover_skills(skills_dir):
        sections.extend(extract_blocks(path))

    body = "\n\n".join(sections)
    if '"""' in body:
        raise RuntimeError(
            "prompt-contribution text contains triple quotes — this would "
            "produce a malformed Python literal when written to "
            "sage/prompts.py. Remove or escape them in the source file."
        )
    return body

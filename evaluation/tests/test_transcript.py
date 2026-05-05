import pytest
from pathlib import Path
from evaluation.metrics.transcript import (
    parse_exported_chat,
    parse_markdown,
    parse_simulated_json,
    Transcript,
    Turn,
)

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


REPO_ROOT = Path(__file__).resolve().parents[2]
REAL_TRANSCRIPTS = sorted((REPO_ROOT / "examples" / "interactions").rglob("*.md"))


@pytest.mark.parametrize("path", REAL_TRANSCRIPTS, ids=lambda p: p.name)
def test_real_authored_transcript_alternates_speakers(path):
    t = parse_markdown(
        path.read_text(),
        source_id=str(path.relative_to(REPO_ROOT)),
        origin="authored",
    )
    speakers = [turn.speaker for turn in t.turns]
    assert len(speakers) >= 2, f"{path.name}: too few turns parsed"
    assert "learner" in speakers, f"{path.name}: no learner turns parsed"
    assert "sage" in speakers, f"{path.name}: no sage turns parsed"
    # Speakers should mostly alternate; no two consecutive turns from the same speaker.
    consecutive_dupes = sum(1 for i in range(1, len(speakers)) if speakers[i] == speakers[i - 1])
    assert consecutive_dupes == 0, (
        f"{path.name}: found {consecutive_dupes} consecutive same-speaker turns. Speakers: {speakers}"
    )


def test_parse_simulated_json_raises_with_path_on_missing_key(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text('{"source_id": "x", "origin": "simulated"}')  # no "turns"
    with pytest.raises(ValueError, match=r"Invalid simulated transcript at .+bad\.json"):
        parse_simulated_json(p)


def test_parse_simulated_json_raises_with_path_on_bad_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("not valid json")
    with pytest.raises(ValueError, match=r"Invalid simulated transcript at .+bad\.json"):
        parse_simulated_json(p)


def test_parse_simulated_json_raises_on_invalid_speaker(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(__import__("json").dumps({
        "source_id": "x",
        "origin": "simulated",
        "turns": [{"index": 0, "speaker": "robot", "text": "hi"}],
    }))
    with pytest.raises(ValueError, match=r"Invalid speaker"):
        parse_simulated_json(p)


# --- parse_exported_chat: matches the format produced by sage/export.py ---
# Sample strings inlined here so the eval module's tests don't depend on the SAGE app.

_SAMPLE_EXPORT_MD = """### You

What is a hallucination?

### SAGE

A confident-but-wrong generation. Want an example?

### You

Yes please.

### SAGE

Sure — imagine a fake citation that looks real.
"""

_SAMPLE_EXPORT_TXT = """You:
What is a hallucination?

SAGE:
A confident-but-wrong generation. Want an example?

You:
Yes please.

SAGE:
Sure — imagine a fake citation that looks real.
"""


def test_parse_exported_md_format():
    t = parse_exported_chat(_SAMPLE_EXPORT_MD, source_id="exports/demo")
    assert t.origin == "exported"
    assert t.source_id == "exports/demo"
    assert [turn.speaker for turn in t.turns] == ["learner", "sage", "learner", "sage"]
    assert t.turns[0].text == "What is a hallucination?"
    assert t.turns[3].text == "Sure — imagine a fake citation that looks real."


def test_parse_exported_txt_format():
    t = parse_exported_chat(_SAMPLE_EXPORT_TXT, source_id="exports/demo")
    assert t.origin == "exported"
    assert [turn.speaker for turn in t.turns] == ["learner", "sage", "learner", "sage"]
    assert t.turns[1].text.startswith("A confident-but-wrong generation")


def test_parse_exported_md_indices_are_sequential():
    t = parse_exported_chat(_SAMPLE_EXPORT_MD, source_id="x")
    assert [turn.index for turn in t.turns] == [0, 1, 2, 3]


def test_parse_exported_strips_whitespace():
    md = "### You\n\n   hi there   \n\n### SAGE\n\n  hello!  \n"
    t = parse_exported_chat(md, source_id="x")
    assert t.turns[0].text == "hi there"
    assert t.turns[1].text == "hello!"


def test_parse_exported_drops_empty_turns():
    # An export with a header but no body shouldn't create an empty Turn.
    md = "### You\n\nhi\n\n### SAGE\n\n\n\n### You\n\nstill there?\n"
    t = parse_exported_chat(md, source_id="x")
    assert [turn.text for turn in t.turns] == ["hi", "still there?"]


def test_parse_exported_empty_input_returns_zero_turns():
    assert parse_exported_chat("", source_id="empty").turns == []
    assert parse_exported_chat("just prose, no markers", source_id="x").turns == []


def test_parse_exported_prefers_format_with_more_markers():
    # Markdown has 4 markers; the literal "You:" appearing in body text shouldn't
    # cause the parser to switch into text mode.
    md = "### You\n\nThe word You: appears in this message but not as a marker.\n\n### SAGE\n\nGot it.\n"
    t = parse_exported_chat(md, source_id="x")
    assert len(t.turns) == 2
    assert t.turns[0].speaker == "learner"
    assert "appears in this message" in t.turns[0].text

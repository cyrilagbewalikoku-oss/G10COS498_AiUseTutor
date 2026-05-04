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

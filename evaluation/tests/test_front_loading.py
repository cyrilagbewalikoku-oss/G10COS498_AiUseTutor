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

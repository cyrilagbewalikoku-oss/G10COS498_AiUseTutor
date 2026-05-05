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

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


import pytest
from types import SimpleNamespace

from evaluation.metrics.judge import (
    JudgeCall,
    _extract_json,
    call_judge_json,
)


# --- _extract_json tests ---

def test_extract_json_simple():
    assert _extract_json('Sure: {"a": 1}') == {"a": 1}


def test_extract_json_with_trailing_prose():
    # Old greedy regex would have failed because of the trailing "{curly}" tokens.
    text = 'Result: {"behavior": "answered_first"}. (Note: the {curly} braces.)'
    assert _extract_json(text) == {"behavior": "answered_first"}


def test_extract_json_handles_nested_objects():
    text = '{"outer": {"inner": 1}, "x": 2}'
    assert _extract_json(text) == {"outer": {"inner": 1}, "x": 2}


def test_extract_json_handles_braces_inside_strings():
    # A `}` inside a string literal must not close the JSON.
    text = '{"text": "look: }"}'
    assert _extract_json(text) == {"text": "look: }"}


def test_extract_json_returns_first_object_when_multiple():
    text = 'First: {"a": 1} then: {"b": 2}'
    assert _extract_json(text) == {"a": 1}


def test_extract_json_raises_when_no_object():
    with pytest.raises(ValueError, match="No JSON object found"):
        _extract_json("no json here")


def test_extract_json_raises_when_unbalanced():
    with pytest.raises(ValueError, match="Unbalanced JSON object"):
        _extract_json('start {"a": 1')


# --- call_judge_json integration tests using a stub client ---

class _StubMessages:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        # Return an object that quacks like an Anthropic Message:
        # response.content is list[TextBlock-like] with a `.text` and the
        # right type so isinstance(b, TextBlock) is True.
        from anthropic.types import TextBlock
        text = self.responses.pop(0)
        return SimpleNamespace(
            content=[TextBlock(type="text", text=text, citations=None)],
        )


class _StubClient:
    def __init__(self, responses):
        self.messages = _StubMessages(responses)


def test_call_judge_json_uses_cache_on_hit(tmp_path):
    from evaluation.metrics.judge import JudgeCache, cache_key
    cache_path = tmp_path / "cache.json"
    cache = JudgeCache(cache_path)
    key = cache_key("model-x", "tplv1", "u", "a")
    cache.put(key, {"behavior": "answered_first"})

    # Sentinel client that would raise on any actual call:
    class ExplodingClient:
        @property
        def messages(self):
            raise AssertionError("network call should not happen on cache hit")

    call = JudgeCall(model="model-x", system="s", user="u", template_version="tplv1")
    result = call_judge_json(
        call, cache=cache, cache_inputs=("u", "a"), client=ExplodingClient(),
    )
    assert result == {"behavior": "answered_first"}


def test_call_judge_json_writes_to_cache_on_miss(tmp_path):
    cache_path = tmp_path / "cache.json"
    from evaluation.metrics.judge import JudgeCache, cache_key
    cache = JudgeCache(cache_path)
    client = _StubClient(['{"behavior": "answered_first"}'])

    call = JudgeCall(model="model-y", system="s", user="u", template_version="tplv2")
    result = call_judge_json(
        call, cache=cache, cache_inputs=("u", "a"), client=client,
    )
    assert result == {"behavior": "answered_first"}
    # And it's been persisted:
    cache2 = JudgeCache(cache_path)
    assert cache2.get(cache_key("model-y", "tplv2", "u", "a")) == {"behavior": "answered_first"}


def test_call_judge_json_extracts_json_from_prose_response():
    """The stub returns prose-then-JSON-then-prose; the new _extract_json must handle it."""
    client = _StubClient(['Result: {"behavior": "answered_first"}. (See {note}.)'])
    call = JudgeCall(model="model-z", system="s", user="u", template_version="v")
    result = call_judge_json(call, client=client)
    assert result == {"behavior": "answered_first"}

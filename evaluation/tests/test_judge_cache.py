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

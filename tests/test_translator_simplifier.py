import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.translator_simplifier.translate import translate_and_simplify


def test_translate_and_simplify_uses_call_fn():
    called = {}

    def fake_call(prompt: str, model: str | None = None):
        called["prompt"] = prompt
        return {
            "explanation": "अनुवादित व्याख्या",
            "analogy": "स्थानीय उदाहरण",
            "step_by_step": ["कदम 1", "कदम 2"],
            "keywords": ["शब्द1", "शब्द2"],
            "language": "hi",
            "level": "school",
        }

    result = translate_and_simplify(
        "This is a test explanation about recursion.",
        target_language="hi",
        level="school",
        topic="recursion",
        call_fn=fake_call,
    )

    assert "recursion" in called["prompt"]
    assert result.explanation == "अनुवादित व्याख्या"
    assert result.analogy == "स्थानीय उदाहरण"
    assert result.step_by_step == ["कदम 1", "कदम 2"]
    assert result.keywords == ["शब्द1", "शब्द2"]
    assert result.language == "hi"
    assert result.level == "school"


def test_translate_and_simplify_handles_string_steps_keywords():
    def fake_call(prompt: str, model: str | None = None):
        return {
            "explanation": "exp",
            "analogy": "",
            "step_by_step": "a\nb\nc",
            "keywords": "x, y , z ",
        }

    result = translate_and_simplify(
        "text", target_language="hi", level="school", call_fn=fake_call
    )

    assert result.step_by_step == ["a", "b", "c"]
    assert result.keywords == ["x", "y", "z"]
    assert result.analogy is None


def test_translate_and_simplify_empty_text_returns_empty_fields():
    result = translate_and_simplify("", target_language="hi", level="school")
    assert result.explanation == ""
    assert result.step_by_step == []
    assert result.keywords == []


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

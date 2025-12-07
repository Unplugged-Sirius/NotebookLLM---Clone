import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.content_scout.scout import content_scout_agent
from agents.content_scout.search_google import map_serper_to_resources


def test_map_serper_to_resources_maps_organic_and_videos():
    data = {
        "organic": [
            {"title": "Article A", "link": "https://a.com", "source": "SiteA"},
            {"title": "Article B", "link": "https://b.com"},  # missing source
        ],
        "videos": [
            {"title": "Video A", "link": "https://v.com", "source": "YouTube"},
        ],
    }

    resources = map_serper_to_resources(data, base_score=1.0)

    assert len(resources) == 3
    assert resources[0].title == "Article A"
    assert resources[0].url == "https://a.com"
    assert resources[0].source == "SiteA"
    assert resources[1].title == "Article B"
    assert resources[1].source == "web"
    assert resources[2].type == "video"
    assert resources[2].score == 1.0  # videos start with fresh base score


def test_content_scout_agent_search_only_uses_provided_search_fn():
    seen = {}

    def fake_search(query: str, num_results: int):
        seen["query"] = query
        seen["num_results"] = num_results
        return {
            "organic": [
                {"title": "Recursion Guide", "link": "https://example.com/recursion"}
            ]
        }

    resources = content_scout_agent(
        topic="recursion",
        language="en",
        level="beginner",
        num_results=3,
        enrich=False,
        search_fn=fake_search,
    )

    assert seen["query"] == "recursion tutorial for beginner students"
    assert seen["num_results"] == 3
    assert len(resources) == 1
    assert resources[0].title == "Recursion Guide"


def test_content_scout_agent_enriches_with_stubbed_fetch_and_summary():
    def fake_search(_: str, __: int):
        return {
            "organic": [
                {"title": "Sample Resource", "link": "https://example.com/sample"}
            ]
        }

    def fake_fetch(_: str):
        return {
            "ok": True,
            "title": "Fetched Title",
            "text": "This is the fetched text about recursion.",
            "language": "en",
            "error": None,
        }

    def fake_summarize(text: str, topic: str, target_language: str, level_hint: str):
        return (
            f"Summary for {topic} ({target_language})",
            level_hint,
            "concept_explanation",
        )

    resources = content_scout_agent(
        topic="recursion",
        language="en",
        level="beginner",
        num_results=1,
        enrich=True,
        search_fn=fake_search,
        fetch_fn=fake_fetch,
        summarize_fn=fake_summarize,
    )

    assert len(resources) == 1
    r = resources[0]
    assert r.title == "Sample Resource"
    assert r.language == "en"
    assert r.raw_text.startswith("This is the fetched text")
    assert r.short_summary.startswith("Summary for recursion")
    assert r.estimated_level == "beginner"
    assert r.content_type == "concept_explanation"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

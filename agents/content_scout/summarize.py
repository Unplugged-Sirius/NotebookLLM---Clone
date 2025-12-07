from typing import Tuple
from core.llm import call_llm_json


def summarize_and_classify(
    text: str,
    topic: str,
    target_language: str = "en",
    level_hint: str = "beginner",
) -> Tuple[str, str, str]:
    """
    Returns:
        short_summary (str, English),
        estimated_level (str),
        content_type (str)
    """

    # truncate to avoid sending mega-pages
    trimmed = text[:6000]

    prompt = f"""
You are helping to build a learning assistant for non-English-medium students.

Given the TEXT below, do three things:
1. In at most 3 sentences, summarize the main idea in English, focusing on how it can help someone learn the topic: "{topic}".
2. Estimate the difficulty level as one of: ["school", "college", "beginner", "advanced"].
3. Classify the content type as one of: ["concept_explanation", "step_by_step_tutorial", "reference_docs", "example_collection"].

Respond ONLY as a JSON object with keys:
- "short_summary"
- "estimated_level"
- "content_type"

TEXT:
\"\"\"{trimmed}\"\"\"
"""

    result = call_llm_json(prompt)

    short_summary = result.get("short_summary", "").strip()
    estimated_level = result.get("estimated_level", "").strip() or level_hint
    content_type = result.get("content_type", "").strip() or "concept_explanation"

    return short_summary, estimated_level, content_type

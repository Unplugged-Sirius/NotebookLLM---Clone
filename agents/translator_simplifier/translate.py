from typing import Callable, Dict, Optional

from core.llm import call_llm_json

from .schemas import SimplifiedContent

CallFn = Callable[[str, Optional[str]], Dict]


def translate_and_simplify(
    text: str,
    target_language: str = "hi",
    level: str = "school",
    topic: Optional[str] = None,
    call_fn: Optional[CallFn] = None,
) -> SimplifiedContent:
    """
    Translate and simplify an English explanation into the target language/level.
    Returns structured output: explanation, analogy, step_by_step, keywords.
    """
    llm_call = call_fn or call_llm_json

    if not text:
        return SimplifiedContent(
            explanation="",
            analogy=None,
            step_by_step=[],
            keywords=[],
            language=target_language,
            level=level,
        )

    prompt = f"""
You are a teaching assistant helping students who learn in a non-English language.
Given the INPUT TEXT, translate and simplify it for a student at level "{level}".
If helpful, add a local analogy and break it into simple steps.
Respond ONLY as JSON with keys:
- "explanation": translated + simplified text in the target language
- "analogy": a short relatable analogy (may be empty)
- "step_by_step": array of 3-6 short bullet steps in the target language
- "keywords": array of important terms in the target language
- "language": the target language code
- "level": the target level string

TARGET LANGUAGE: {target_language}
TOPIC: {topic or "N/A"}
INPUT TEXT:
\"\"\"{text[:4000]}\"\"\"
"""

    result = llm_call(prompt)

    explanation = (result.get("explanation") or "").strip()
    analogy = (result.get("analogy") or "").strip() or None
    step_by_step = result.get("step_by_step") or []
    keywords = result.get("keywords") or []
    language = result.get("language") or target_language
    level_out = result.get("level") or level

    # Ensure list types even if the model returned strings.
    if isinstance(step_by_step, str):
        step_by_step = [s.strip() for s in step_by_step.split("\n") if s.strip()]
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]

    return SimplifiedContent(
        explanation=explanation,
        analogy=analogy,
        step_by_step=step_by_step,
        keywords=keywords,
        language=language,
        level=level_out,
    )

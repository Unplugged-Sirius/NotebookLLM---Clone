from typing import Callable, List, Optional, Tuple

try:
    from google.adk.agents import Agent
except ImportError as _adk_err:  # optional dependency for ADK users
    Agent = None
    _ADK_IMPORT_ERROR = _adk_err
else:
    _ADK_IMPORT_ERROR = None

from .fetch_clean import fetch_and_clean
from .fetch_youtube import fetch_youtube_transcript
from .schemas import Resource
from .search_google import map_serper_to_resources, raw_web_search
from .summarize import summarize_and_classify

SearchFn = Callable[[str, int], dict]
FetchFn = Callable[[str], dict]
FetchVideoFn = Callable[[str, Optional[List[str]]], dict]
SummarizeFn = Callable[[str, str, str, str], Tuple[str, str, str]]


def content_scout_agent(
    topic: str,
    language: str = "en",
    level: str = "beginner",
    num_results: int = 8,
    enrich: bool = False,
    search_fn: Optional[SearchFn] = None,
    fetch_fn: Optional[FetchFn] = None,
    fetch_video_fn: Optional[FetchVideoFn] = None,
    summarize_fn: Optional[SummarizeFn] = None,
    include_videos: bool = True,
) -> List[Resource]:
    """
    Agent 1 + (optionally) Agent 2.

    - If enrich=False: only search, return URLs + basic metadata.
    - If enrich=True: also fetch page text, detect language, summarize, classify.
    """
    search = search_fn or raw_web_search
    fetch = fetch_fn or fetch_and_clean
    fetch_video = fetch_video_fn or fetch_youtube_transcript
    summarize = summarize_fn or summarize_and_classify

    query = f"{topic} tutorial for {level} students"
    data = search(query, num_results)

    resources = map_serper_to_resources(data)
    if not include_videos:
        resources = [r for r in resources if r.type != "video"]

    if not enrich:
        return resources

    enriched: List[Resource] = []

    for r in resources:
        is_youtube = "youtube.com" in r.url or "youtu.be" in r.url
        page = (
            fetch_video(r.url, [language, "en"])
            if r.type == "video" or is_youtube
            else fetch(r.url)
        )
        if not page["ok"] or not page["text"]:
            continue

        # fill in any missing title
        if not r.title:
            r.title = page["title"] or r.title

        r.raw_text = page["text"]
        r.language = page["language"]

        # only summarize English pages in v1
        if r.language and not r.language.startswith("en"):
            enriched.append(r)
            continue

        short_summary, est_level, content_type = summarize(
            text=page["text"],
            topic=topic,
            target_language=language,
            level_hint=level,
        )

        r.short_summary = short_summary
        r.estimated_level = est_level
        r.content_type = content_type

        enriched.append(r)

    return enriched


def find_learning_resources(
    topic: str,
    language: str = "en",
    level: str = "beginner",
    num_results: int = 8,
) -> dict:
    """
    Tool wrapper used by the ADK agent to return a serializable payload.
    """
    resources = content_scout_agent(
        topic=topic, language=language, level=level, num_results=num_results
    )
    return {
        "status": "success",
        "resources": [r.model_dump() for r in resources],
    }


def build_content_scout_adk_agent(
    model: str = "gemini-2.0-flash",
) -> "Agent":
    """
    Build an ADK Agent that can field natural language requests and call the
    Serper-powered search tool.
    """
    if Agent is None:
        raise ImportError(
            "google-adk is required for the ADK-enabled content scout. "
            "Install with `pip install google-adk`."
        ) from _ADK_IMPORT_ERROR

    return Agent(
        name="content_scout_agent",
        model=model,
        description=(
            "Finds learning resources (articles, videos, docs) for a topic "
            "at a specified level and language using web search."
        ),
        instruction=(
            "You are a research assistant who recommends learning resources. "
            "When a user asks for learning material, call the "
            "`find_learning_resources` tool with the topic, level, language, "
            "and desired result count. Return the titles and URLs in a concise list."
        ),
        tools=[find_learning_resources],
    )


# Convenience instance for users who want to import and run directly.
content_scout_adk_agent: Optional["Agent"] = None
if Agent is not None:
    content_scout_adk_agent = build_content_scout_adk_agent()

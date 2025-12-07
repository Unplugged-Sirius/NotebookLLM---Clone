import re
from typing import List, Optional
from urllib.parse import parse_qs, urlparse


def _extract_youtube_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from common YouTube URL patterns.
    """
    parsed = urlparse(url)

    # Standard watch?v=VIDEOID
    query_id = parse_qs(parsed.query).get("v", [None])[0]
    if query_id:
        return query_id

    # Short links youtu.be/VIDEOID
    if parsed.netloc.endswith("youtu.be"):
        path_parts = parsed.path.strip("/").split("/")
        if path_parts:
            return path_parts[0]

    # Embed or other formats /embed/VIDEOID
    match = re.search(r"/embed/([A-Za-z0-9_-]{6,})", parsed.path)
    if match:
        return match.group(1)

    return None


def fetch_youtube_transcript(
    url: str, languages: Optional[List[str]] = None
) -> dict:
    """
    Fetch YouTube transcript and return a structure compatible with fetch_and_clean.
    """
    from youtube_transcript_api import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
        YouTubeTranscriptApi,
    )
    video_id = _extract_youtube_video_id(url)
    if not video_id:
        return {
            "ok": False,
            "title": "",
            "text": "",
            "language": None,
            "error": "Could not parse YouTube video ID",
        }
    try: 
        languages = languages or ["en"]
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=languages)
    except:
        return {
            "ok": False,
            "title": "",
            "text": "",
            "language": None,
            
        }

    snippets = []
    for snippet in transcript:
        text = getattr(snippet, "text", None)
        if not text and isinstance(snippet, dict):
            text = snippet.get("text")
        if text:
            snippets.append(text.strip())

    text_body = "\n".join(s for s in snippets if s)
    lang = getattr(transcript, "language_code", None) or getattr(transcript, "language", None)

    return {
        "ok": True,
        "title": "",
        "text": text_body,
        "language": lang,
        "error": None,
    }


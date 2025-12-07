from pydantic import BaseModel
from typing import Literal, Optional, List


class Resource(BaseModel):
    title: str
    url: str
    type: Literal["article", "video", "docs", "other"] = "article"
    source: str = "web"
    language: Optional[str] = None
    estimated_level: Optional[str] = None
    short_summary: Optional[str] = None
    score: float = 1.0

    # New fields for agent 2:
    raw_text: Optional[str] = None       # cleaned page text or transcript
    content_type: Optional[str] = None   # e.g. explanation / tutorial / docs

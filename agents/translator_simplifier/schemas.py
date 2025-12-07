from typing import List, Optional

from pydantic import BaseModel


class SimplifiedContent(BaseModel):
    explanation: str
    analogy: Optional[str] = None
    step_by_step: List[str] = []
    keywords: List[str] = []
    language: str = "en"
    level: str = "school"

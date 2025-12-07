import os
from typing import List, Optional

import requests
from dotenv import load_dotenv

from .schemas import Resource

load_dotenv()  # loads SERPER_API_KEY from .env

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_ENDPOINT = "https://google.serper.dev/search"


def _require_api_key(api_key: Optional[str]) -> str:
    """
    Late validation to avoid import-time crashes when SERPER_API_KEY
    is not available (e.g., during tests).
    """
    if not api_key:
        raise RuntimeError(
            "SERPER_API_KEY not set in environment or .env file; "
            "set it before calling the Serper client."
        )
    return api_key


def raw_web_search(query: str, num_results: int = 5, api_key: Optional[str] = None) -> dict:
    """
    Call Serper search API and return raw JSON response.
    """
    resolved_key = _require_api_key(api_key or SERPER_API_KEY)
    headers = {
        "X-API-KEY": resolved_key,
        "Content-Type": "application/json",
    }

    body = {
        "q": query,
        "num": num_results,
    }

    response = requests.post(SERPER_ENDPOINT, json=body, headers=headers)
    response.raise_for_status()
    return response.json()


def get_result_urls(query: str, num_results: int = 5, api_key: Optional[str] = None) -> List[str]:
    """
    High-level helper: returns just a list of URLs for a given query.
    """
    data = raw_web_search(query, num_results=num_results, api_key=api_key)

    urls: List[str] = []

    # 1. Organic results (articles, docs, blogs)
    for item in data.get("organic", []):
        link = item.get("link")
        if link:
            urls.append(link)

    # 2. Video results (YouTube etc.) – optional
    for item in data.get("videos", []):
        link = item.get("link")
        if link:
            urls.append(link)

    return urls


def map_serper_to_resources(data: dict, base_score: float = 1.0) -> List[Resource]:
    resources: List[Resource] = []

    # Organic results
    for i, item in enumerate(data.get("organic", [])):
        resources.append(
            Resource(
                title=item.get("title", ""),
                url=item.get("link", ""),
                type="article",
                source=item.get("source", "web"),
                score=base_score - i * 0.05,  # slightly lower score for lower rank
            )
        )

    # Video results
    for i, item in enumerate(data.get("videos", [])):
        resources.append(
            Resource(
                title=item.get("title", ""),
                url=item.get("link", ""),
                type="video",
                source=item.get("source", "web"),
                score=base_score - i * 0.05,
            )
        )

    return resources

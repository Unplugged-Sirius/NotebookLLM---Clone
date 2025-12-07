import json
import os
from typing import Dict, Optional

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    from google import genai as genai_client
    HAS_GENAI_CLIENT = True
except ImportError:
    HAS_GENAI_CLIENT = False

from core.config import Config


class LLMInterface:
    """
    Minimal interface so we can plug in different LLM backends while keeping
    callers decoupled from provider-specific details.
    """

    def call_json(self, prompt: str, model: Optional[str] = None) -> Dict:
        raise NotImplementedError


_LLM_DISABLED = False
_LLM_DISABLED_REASON: Optional[str] = None


def _stub_response() -> Dict:
    return json.loads(
        '{"short_summary": "TODO", "estimated_level": "beginner", "content_type": "concept_explanation"}'
    )


def _clean_json_text(raw_text: str) -> str:
    """
    Remove common wrappers (e.g. markdown ```json fences) and strip whitespace.
    """
    text = raw_text.strip()

    # Remove ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        # Remove leading ```
        text = text.lstrip("`")
        # Drop possible 'json' after first ```
        if text.lower().startswith("json"):
            text = text[4:]  # remove 'json'
        # Remove trailing ``` if present
        if "```" in text:
            text = text.split("```", 1)[0]

    return text.strip()


def call_llm_json(prompt: str, model: Optional[str] = None) -> Dict:
    """
    Call Google Gemini API and expect a strict JSON response.
    """
    global _LLM_DISABLED, _LLM_DISABLED_REASON

    if _LLM_DISABLED:
        # Already disabled due to previous errors: return stub to avoid repeated failures.
        return _stub_response()

    # Hardcoded API key for testing
    api_key = "AIzaSyB1BXhZ5mLRcKukArIO2ZE6iOulHycaCO0"
    
    if not api_key:
        print("[WARNING] GEMINI_API_KEY not configured. Returning stub response.")
        return _stub_response()

    # Decide on a single model (can override via env or function arg).
    model_name = "gemini-2.5-flash-lite"

    try:
        # Try the newer google.genai client first
        if HAS_GENAI_CLIENT:
            client = genai_client.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            raw_text = response.text
        elif HAS_GENAI:
            # Fall back to google.generativeai
            genai.configure(api_key=api_key)
            client = genai.GenerativeModel(model_name)
            response = client.generate_content(prompt)
            raw_text = response.text
        else:
            raise ImportError("Neither google.genai nor google.generativeai is installed")

        # Extract text if needed
        if not hasattr(response, "text") or not response.text:
            if getattr(response, "candidates", None):
                parts = []
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "text") and part.text:
                        parts.append(part.text)
                raw_text = "\n".join(parts)

        if not raw_text:
            raise ValueError("Empty response body from model")

        cleaned = _clean_json_text(raw_text)
        return json.loads(cleaned)

    except Exception as e:
        _LLM_DISABLED = True
        _LLM_DISABLED_REASON = str(e)
        print(f"[ERROR] LLM call failed ({e}). Using stub responses from now on.")
        return _stub_response()



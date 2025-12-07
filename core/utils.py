# Shared helpers, logging etc.
"""Utility functions and logging setup."""

import logging

def setup_logging(level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to specified length."""
    return text[:max_length] + "..." if len(text) > max_length else text

# API keys + config variables
"""Configuration management."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai | local
    
    FASTAPI_HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
    FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))
    
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

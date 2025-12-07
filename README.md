# Learning Helper

An AI “study buddy” for students who learn in languages other than English. It finds good English resources on the web, understands them, and teaches back in the learner’s language using text, audio, visuals, and interactive Q&A.

## What we’re building

- **Content Scout (Agent 1)**: Search the web (Serper/Google) for relevant articles/videos and return structured `Resource` objects.
- **Extractor & Summarizer (Agent 2)**: Fetch pages, clean text, detect language, summarize, and classify the content. For YouTube, pull transcripts.
- **Translator–Simplifier (planned)**: Translate/simplify to the target language and level, add local analogies.
- **Teaching Agent (planned)**: Turn explanations into lessons, examples, quizzes, and hints.
- **Conversation Agent (planned)**: RAG-powered chat that answers doubts in the learner’s language; future speech/vision extensions.

## Quickstart

1) Install deps
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2) Configure API keys in `.env` (copy from `.env.example` if present):
```
SERPER_API_KEY=...
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-1.5-flash   # or another model your account supports
```

3) Try the content scout demo
```bash
python agents/content_scout/try.py
```
This searches for a topic (default: “recursion in programming”), fetches articles and YouTube transcripts, and prints summaries.

4) Run tests
```bash
pytest
```

## Repo layout

```
agents/
  content_scout/    # search, fetch/clean, summarize, YouTube transcripts
  translator_simplifier/  # planned
  teaching_agent/         # planned
  conversation_agent/     # planned
core/              # config, LLM wrapper
app/               # FastAPI backend (scaffolding)
tests/             # pytest suites
```

## Notes

- `.env` and local clones are ignored via `.gitignore`; don’t commit secrets.
- YouTube transcripts require `youtube-transcript-api` (included in requirements).
- If an LLM/model is unavailable, the system falls back to stub summaries. Set `GEMINI_MODEL` to a supported ID for real summaries. 

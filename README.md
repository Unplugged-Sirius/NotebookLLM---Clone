# Learning Helper

A multi-agent AI system for discovering, processing, and teaching with online learning resources.

## Project Structure

```
Learning-Helper/
├── agents/                    # AI agents for different tasks
│   ├── content_scout/        # Searches and classifies resources
│   ├── translator_simplifier/ # Simplifies complex content
│   ├── teaching_agent/       # Generates teaching materials
│   └── conversation_agent/   # Interactive Q&A
├── core/                      # Core utilities and config
├── data/                      # Cached resources and lessons
├── tests/                     # Unit tests
├── notebooks/                 # Jupyter notebooks for experiments
├── app/                       # FastAPI backend
└── requirements.txt           # Python dependencies
```

## Getting Started

### 1. Clone and Setup

```bash
cd Learning-Helper
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run the Server

```bash
python -m app.server
```

The API will be available at `http://localhost:8000`

### 5. Run Tests

```bash
pytest tests/
```

## Features (In Development)

- 🔍 **Content Scout**: Search and classify learning resources
- 📝 **Translator/Simplifier**: Break down complex topics
- 🎓 **Teaching Agent**: Generate personalized lessons
- 💬 **Conversation Agent**: Interactive Q&A system

## API Endpoints

- `GET /health` - Health check
- `GET /api/search?query=...` - Search for resources
- `POST /api/resources` - Add new learning resource

## Development

See `notebooks/agent_experiments.ipynb` for interactive development and testing.

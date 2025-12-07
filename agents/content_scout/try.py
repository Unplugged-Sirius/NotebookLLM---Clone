# file: test_content_extractor.py
from pathlib import Path
import sys
import os

# Ensure project root is on sys.path when running the script directly.
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # Go up 3 levels to Learning-Helper/
PYTHONWARNINGS="ignore"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Change working directory to project root
os.chdir(PROJECT_ROOT)
from agents.content_scout.scout import content_scout_agent

if __name__ == "__main__":
    topic = "Trigonometry basics"
    resources = content_scout_agent(topic, level="beginner", enrich=True)
    print(f"Found {len(resources)} resources for topic '{topic}':\n")

    for r in resources:
        print("=" * 80)
        print("TITLE:", r.title)
        print("URL:", r.url)
        print("LANG:", r.language)
        print("LEVEL:", r.estimated_level)
        print("TYPE:", r.content_type)
        print("SUMMARY:", r.short_summary)
        print("TEXT SAMPLE:", (r.raw_text or "")[:300], "...")
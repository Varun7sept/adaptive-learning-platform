import json
import re
from datetime import datetime, timezone
from app.utils.llm import call_llm
from app.database.mongo import learning_path_collection


def extract_json(text: str):
    """Extract valid JSON from messy LLM output."""
    if not text:
        return None

    # Remove Markdown fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Extract JSON between first { and last }
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        text = match.group(0)

    return text.strip()


def generate_learning_path(incorrect_items, student_id):
    """
    Generates a validated JSON learning path.
    """

    prompt = f"""
    You are a JSON-only AI.

    You must return VALID JSON ONLY.
    NO explanations.
    NO text outside JSON.

    Create a LEARNING PATH based on incorrect questions:

    {incorrect_items}

    STRICT JSON FORMAT:
    {{
        "learning_path": [
            {{
                "topic": "",
                "why_important": "",
                "subtopics": ["", ""],
                "resources": [
                    {{"title": "", "link": ""}}
                ],
                "practice_tasks": [
                    {{
                        "question": "",
                        "options": ["", "", "", ""],
                        "correct": ""
                    }}
                ],
                "time_required": "",
                "difficulty": ""
            }}
        ],
        "summary": ""
    }}

    Return EXACTLY this structure.
    """

    raw = call_llm(prompt)

    # Clean output
    cleaned = extract_json(raw)

    # Try parsing
    try:
        parsed = json.loads(cleaned)
    except Exception:
        # 💥 LLM failed → return safe fallback
        parsed = {
            "learning_path": [],
            "summary": "Could not generate learning path. Please retry."
        }

    # Save ALWAYS valid object
    learning_path_collection.insert_one({
        "student_id": student_id,
        "learning_path": parsed,
        "timestamp": datetime.now(timezone.utc)
    })

    return parsed

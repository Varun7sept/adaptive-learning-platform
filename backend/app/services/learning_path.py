# import json
# import re
# from datetime import datetime, timezone
# from app.utils.llm import call_llm
# from app.database.mongo import learning_path_collection


# def extract_json(text: str):
#     """Extract valid JSON from messy LLM output."""
#     if not text:
#         return None

#     # Remove Markdown fences
#     text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
#     text = re.sub(r"```", "", text)

#     # Extract JSON between first { and last }
#     match = re.search(r"\{.*\}", text, flags=re.DOTALL)
#     if match:
#         text = match.group(0)

#     return text.strip()


# def generate_learning_path(incorrect_items, student_id):
#     """
#     Generates a validated JSON learning path.
#     """

#     prompt = f"""
#     You are a JSON-only AI.

#     You must return VALID JSON ONLY.
#     NO explanations.
#     NO text outside JSON.

#     Create a LEARNING PATH based on incorrect questions:

#     {incorrect_items}

#     STRICT JSON FORMAT:
#     {{
#         "learning_path": [
#             {{
#                 "topic": "",
#                 "why_important": "",
#                 "subtopics": ["", ""],
#                 "resources": [
#                     {{"title": "", "link": ""}}
#                 ],
#                 "practice_tasks": [
#                     {{
#                         "question": "",
#                         "options": ["", "", "", ""],
#                         "correct": ""
#                     }}
#                 ],
#                 "time_required": "",
#                 "difficulty": ""
#             }}
#         ],
#         "summary": ""
#     }}
#     """

#     raw = call_llm(prompt)
#     cleaned = extract_json(raw)

#     try:
#         parsed = json.loads(cleaned)

#         # ✅ Validate structure
#         if (
#             not isinstance(parsed, dict)
#             or "learning_path" not in parsed
#             or not isinstance(parsed["learning_path"], list)
#         ):
#             raise ValueError("Invalid structure")

#     except Exception:
#         # ✅ SAFE FALLBACK (STRUCTURE STILL VALID)
#         parsed = {
#             "learning_path": [
#                 {
#                     "topic": "Revision Required",
#                     "why_important": "The system could not reliably generate a personalized path. Manual revision is recommended.",
#                     "subtopics": ["Review fundamentals", "Reattempt incorrect questions"],
#                     "resources": [],
#                     "practice_tasks": [],
#                     "time_required": "30–45 minutes",
#                     "difficulty": "Easy"
#                 }
#             ],
#             "summary": "Fallback learning path generated due to LLM formatting issue."
#         }

#     # Save clean object
#     learning_path_collection.insert_one({
#         "student_id": student_id,
#         "learning_path": parsed,
#         "timestamp": datetime.now(timezone.utc)
#     })

#     return parsed

import json
import re
from datetime import datetime, timezone
from app.utils.llm import call_llm
from app.database.mongo import learning_path_collection


# --------------------------------------------------
# 🔹 Robust JSON extractor
# --------------------------------------------------
def extract_json(text: str):
    if not text:
        return None

    # Remove markdown/code fences
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    # Try to extract JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    candidate = match.group(0)

    # Fix common JSON mistakes
    candidate = candidate.replace("\n", " ")
    candidate = re.sub(r",\s*}", "}", candidate)
    candidate = re.sub(r",\s*]", "]", candidate)

    return candidate.strip()


# --------------------------------------------------
# 🔹 Learning Path Generator (robust)
# --------------------------------------------------
def generate_learning_path(incorrect_items, student_id):

    prompt = f"""
    You are an AI that generates structured learning paths.

    IMPORTANT RULES:
    - Return JSON only
    - No markdown
    - No explanations
    - Follow the schema strictly

    Based on the student's incorrect questions:
    {incorrect_items}

    JSON SCHEMA:
    {{
      "learning_path": [
        {{
          "topic": "string",
          "why_important": "string",
          "subtopics": ["string"],
          "resources": [
            {{"title": "string", "link": "string"}}
          ],
          "practice_tasks": [
            {{
              "question": "string",
              "options": ["string"],
              "correct": "string"
            }}
          ],
          "time_required": "string",
          "difficulty": "Easy | Medium | Hard"
        }}
      ],
      "summary": "string"
    }}
    """

    raw = call_llm(prompt)
    cleaned = extract_json(raw)

    parsed = None

    if cleaned:
        try:
            parsed = json.loads(cleaned)
        except Exception:
            parsed = None

    # --------------------------------------------------
    # 🔹 Structural validation
    # --------------------------------------------------
    if (
        not parsed
        or "learning_path" not in parsed
        or not isinstance(parsed["learning_path"], list)
        or len(parsed["learning_path"]) == 0
    ):
        parsed = {
            "learning_path": [
                {
                    "topic": "Concept Revision",
                    "why_important": "These topics caused incorrect answers and require focused revision.",
                    "subtopics": [
                        "Review incorrect concepts",
                        "Understand core definitions",
                        "Apply concepts through examples"
                    ],
                    "resources": [
                        {
                            "title": "Recommended Textbook / Notes",
                            "link": "https://www.ncbi.nlm.nih.gov/books/"
                        }
                    ],
                    "practice_tasks": [
                        {
                            "question": "Reattempt similar questions from this topic.",
                            "options": ["Option A", "Option B", "Option C", "Option D"],
                            "correct": "Depends on question"
                        }
                    ],
                    "time_required": "45–60 minutes",
                    "difficulty": "Easy"
                }
            ],
            "summary": "Fallback learning path generated due to LLM formatting limitations."
        }

    # --------------------------------------------------
    # 🔹 Save clean output
    # --------------------------------------------------
    learning_path_collection.insert_one({
        "student_id": student_id,
        "learning_path": parsed,
        "timestamp": datetime.now(timezone.utc)
    })

    return parsed

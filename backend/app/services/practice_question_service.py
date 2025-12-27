# from app.utils.llm import call_llm
# from app.database.mongo import practice_questions
# from datetime import datetime, timezone

# def generate_practice_questions(weak_concepts, num_questions, student_id):
#     """
#     Generates personalized practice questions based on weak concepts.
#     """

#     concept_text = "\n".join([c["concept"] for c in weak_concepts])

#     prompt = f"""
#     You are an expert AI tutor.

#     The student's weak concepts are:
#     {concept_text}

#     Generate EXACTLY {num_questions} high-quality MCQ practice questions.
#     For each question include:
#     - question
#     - options (4)
#     - correct_answer
#     - explanation (why the correct answer is correct)

#     Return ONLY in JSON as:
#     {{
#        "practice_questions": [
#          {{
#             "question": "",
#             "options": ["", "", "", ""],
#             "correct_answer": "",
#             "explanation": ""
#          }}
#        ]
#     }}
#     """

#     llm_output = call_llm(prompt)

#     # Store in MongoDB
#     doc = {
#         "student_id": student_id,
#         "weak_concepts": weak_concepts,
#         "num_questions": num_questions,
#         "questions": llm_output,
#         "timestamp": datetime.now(timezone.utc)
#     }

#     practice_questions.insert_one(doc)

#     return llm_output


from app.utils.llm import call_llm
from app.database.mongo import practice_questions
from datetime import datetime, timezone
import json
import re

def clean_json_output(text: str):
    """
    Cleans LLM response:
    - Removes code blocks (```json)
    - Extracts valid JSON { ... }
    """
    if not text:
        return None

    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    text = text.strip()

    # Extract only JSON portion
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text


def generate_practice_questions(weak_concepts, num_questions, student_id):
    """
    Generates **strict JSON** MCQs — fully frontend-safe.
    """

    concept_text = "\n".join([c["concept"] for c in weak_concepts])

    prompt = f"""
    You are an expert AI tutor.

    The student's weak concepts are:
    {concept_text}

    Generate EXACTLY {num_questions} MCQs.

    ⚠ STRICT REQUIREMENTS:
    - OUTPUT ONLY VALID JSON
    - NO explanations outside JSON
    - NO markdown
    - NO extra text
    - NO comments

    The JSON format MUST be:
    {{
      "practice_questions": [
        {{
          "question": "",
          "options": ["", "", "", ""],
          "correct_answer": "",
          "explanation": ""
        }}
      ]
    }}
    """

    raw_output = call_llm(prompt)

    cleaned = clean_json_output(raw_output)

    try:
        parsed = json.loads(cleaned)
    except Exception as e:
        print("❌ JSON PARSE FAILED:", e)
        print("RAW OUTPUT:", raw_output)
        return {"error": "LLM returned invalid JSON."}

    # Save clean JSON
    doc = {
        "student_id": student_id,
        "weak_concepts": weak_concepts,
        "num_questions": num_questions,
        "questions_json": parsed,
        "timestamp": datetime.now(timezone.utc)
    }

    practice_questions.insert_one(doc)

    return parsed   # RETURN CLEAN JSON

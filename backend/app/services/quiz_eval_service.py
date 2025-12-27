# import os
# import requests
# from dotenv import load_dotenv

# # Load API key
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# def evaluate_quiz(questions_text: str, student_answers: str):
#     """
#     Uses Groq API to evaluate student's answers.
#     Returns score, feedback, and short explanations.
#     """

#     if not GROQ_API_KEY:
#         return {"error": "Groq API key not found in .env"}

#     # Define Groq endpoint
#     url = "https://api.groq.com/openai/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     # LLM evaluation prompt
#     prompt = f"""
#     You are an intelligent quiz evaluator.
#     Here are the quiz questions with their correct answers:
#     {questions_text}

#     The student's submitted answers are:
#     {student_answers}

#     Task:
#     - Compare each student's answer to the correct one.
#     - Mark each question as correct or incorrect.
#     - Provide a one-line explanation for each.
#     - Calculate the total score.

#     Return the output strictly in JSON format as:
#     {{
#       "score": X,
#       "total": Y,
#       "feedback": [
#         {{
#           "q_no": 1,
#           "correct": true,
#           "explanation": "..."
#         }}
#       ]
#     }}
#     """

#     payload = {
#         "model": "llama-3.1-8b-instant",
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.4,
#         "max_tokens": 800
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload, timeout=45)
#         if response.status_code != 200:
#             return {
#                 "error": f"Groq API returned {response.status_code}",
#                 "details": response.text
#             }

#         data = response.json()
#         result_text = data["choices"][0]["message"]["content"].strip()

#         return {"evaluation_result": result_text}

#     except requests.exceptions.RequestException as e:
#         return {"error": f"Network error: {str(e)}"}

#     except Exception as e:
#         return {"error": f"Unexpected error: {str(e)}"}



# import os
# import json
# import requests
# from dotenv import load_dotenv

# # Load API key
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# def evaluate_quiz(questions_text: str, student_answers: str):
#     # print("DEBUG questions_text:", questions_text)
#     # print("DEBUG student_answers:", student_answers)
#     """
#     Uses Groq API to evaluate student's answers.
#     Returns parsed score, total, accuracy, and feedback.
#     """

#     if not GROQ_API_KEY:
#         return {"error": "Groq API key not found in .env"}

#     url = "https://api.groq.com/openai/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     prompt = f"""
#     You are an intelligent quiz evaluator.
#     Here are the quiz questions with correct answers:
#     {questions_text}

#     The student's submitted answers are:
#     {student_answers}

#     Task:
#     - Compare the student's answers to the correct ones.
#     - Return STRICT JSON ONLY in this format:

#     {{
#       "score": <number>,
#       "total": <number>,
#       "feedback": [
#         {{
#           "q_no": 1,
#           "correct": true,
#           "explanation": "..."
#         }}
#       ]
#     }}
#     """

#     payload = {
#         "model": "llama-3.1-8b-instant",
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.3,
#         "max_tokens": 700
#     }

#     try:
#         response = requests.post(url, headers=headers, json=payload, timeout=40)

#         if response.status_code != 200:
#             return {
#                 "error": f"Groq API returned {response.status_code}",
#                 "details": response.text
#             }

#         result_text = response.json()["choices"][0]["message"]["content"].strip()

#         # Clean accidental backticks if any
#         cleaned = (
#             result_text.replace("```json", "")
#                        .replace("```", "")
#                        .strip()
#         )

#         # Parse LLM JSON
#         parsed = json.loads(cleaned)

#         score = parsed.get("score", 0)
#         total = parsed.get("total", 1)
#         accuracy = round((score / total) * 100, 2)

#         return {
#             "score": score,
#             "total": total,
#             "accuracy": accuracy,
#             "feedback": parsed.get("feedback", [])
#         }

#     except json.JSONDecodeError:
#         return {"error": "LLM returned invalid JSON", "raw": result_text}

#     except Exception as e:
#         return {"error": f"Unexpected error: {str(e)}"}



import os
import json
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# -----------------------------------------------------------
# 🔹 Helper: Extract topics for each question (LLM-based)
# -----------------------------------------------------------
def extract_topics_from_questions(questions_text: str):

    """
    Extracts a topic/concept for each question number.
    Returns dict: { q_no: topic }
    """

    prompt = f"""
    You are an expert academic classifier.

    Below are quiz questions.
    Identify the CORE academic topic or concept for EACH question.

    Questions:
    {questions_text}

    Return STRICT JSON ONLY in this format:
    {{
      "topics": [
        {{ "q_no": 1, "topic": "..." }},
        {{ "q_no": 2, "topic": "..." }}
      ]
    }}

    Rules:
    - Topic should be short and meaningful
    - Use consistent academic naming
    - Do NOT include explanations
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=40)
        raw = response.json()["choices"][0]["message"]["content"]

        cleaned = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)

        topic_map = {}
        for item in parsed.get("topics", []):
            topic_map[item["q_no"]] = item["topic"]

        return topic_map

    except Exception:
        # Fallback: unknown topics (never break pipeline)
        return {}


# -----------------------------------------------------------
# 🔹 MAIN FUNCTION (UNCHANGED BEHAVIOR)
# -----------------------------------------------------------
def evaluate_quiz(questions_text: str, student_answers: str):
    print("DEBUG questions_text:", questions_text)
    print("DEBUG student_answers:", student_answers)
    """
    Uses Groq API to evaluate student's answers.
    Returns parsed score, total, accuracy, and feedback.
    """

    if not GROQ_API_KEY:
        return {"error": "Groq API key not found in .env"}

    # -------------------------------
    # 1️⃣ Evaluate answers (EXISTING)
    # -------------------------------
    eval_prompt = f"""
    You are an intelligent quiz evaluator.
    Here are the quiz questions with correct answers:
    {questions_text}

    The student's submitted answers are:
    {student_answers}

    Task:
    - Compare the student's answers to the correct ones.
    - Return STRICT JSON ONLY in this format:

    {{
      "score": <number>,
      "total": <number>,
      "feedback": [
        {{
          "q_no": 1,
          "correct": true,
          "explanation": "..."
        }}
      ]
    }}
    """

    eval_payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": eval_prompt}],
        "temperature": 0.3,
        "max_tokens": 700
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=eval_payload, timeout=40)

        if response.status_code != 200:
            return {
                "error": f"Groq API returned {response.status_code}",
                "details": response.text
            }

        result_text = response.json()["choices"][0]["message"]["content"]
        cleaned = result_text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)

        score = parsed.get("score", 0)
        total = parsed.get("total", 1)
        accuracy = round((score / total) * 100, 2)
        feedback = parsed.get("feedback", [])

        # -----------------------------------
        # 2️⃣ NEW: Extract topics (SAFE ADD)
        # -----------------------------------
        topic_map = extract_topics_from_questions(questions_text)

        for item in feedback:
            q_no = item.get("q_no")
            item["topic"] = topic_map.get(q_no, "Unknown Topic")

        # -----------------------------------
        # 3️⃣ RETURN (UNCHANGED STRUCTURE)
        # -----------------------------------
        return {
            "score": score,
            "total": total,
            "accuracy": accuracy,
            "feedback": feedback
        }

    except json.JSONDecodeError:
        return {"error": "LLM returned invalid JSON", "raw": result_text}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}




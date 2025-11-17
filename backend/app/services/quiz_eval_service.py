import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def evaluate_quiz(questions_text: str, student_answers: str):
    """
    Uses Groq API to evaluate student's answers.
    Returns score, feedback, and short explanations.
    """

    if not GROQ_API_KEY:
        return {"error": "Groq API key not found in .env"}

    # Define Groq endpoint
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # LLM evaluation prompt
    prompt = f"""
    You are an intelligent quiz evaluator.
    Here are the quiz questions with their correct answers:
    {questions_text}

    The student's submitted answers are:
    {student_answers}

    Task:
    - Compare each student's answer to the correct one.
    - Mark each question as correct or incorrect.
    - Provide a one-line explanation for each.
    - Calculate the total score.

    Return the output strictly in JSON format as:
    {{
      "score": X,
      "total": Y,
      "feedback": [
        {{
          "q_no": 1,
          "correct": true,
          "explanation": "..."
        }}
      ]
    }}
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 800
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        if response.status_code != 200:
            return {
                "error": f"Groq API returned {response.status_code}",
                "details": response.text
            }

        data = response.json()
        result_text = data["choices"][0]["message"]["content"].strip()

        return {"evaluation_result": result_text}

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

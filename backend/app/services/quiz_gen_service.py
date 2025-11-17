import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_quiz_questions(text: str, num_questions: int = 5):
    """
    Sends study material text to Groq API and returns num_questions multiple-choice questions.
    """

    if not GROQ_API_KEY:
        return {"error": "GROQ API key not found. Please set it in .env"}

    # Limit text to avoid long payloads
    content_chunk = text[:1800]

    # Dynamic prompt with number of questions
    prompt = f"""
    You are an educational AI assistant.
    Based on the following content, generate {num_questions} multiple-choice questions.
    Each question should include:
    - Four options (a, b, c, d)
    - A clearly indicated correct answer

    Content:
    {content_chunk}
    """

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Dynamically scale max_tokens (more questions = more space)
    max_tokens = 800 + (num_questions * 80)

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a quiz generation assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)

        if response.status_code != 200:
            return {
                "error": f"Groq API returned {response.status_code}",
                "details": response.text
            }

        data = response.json()
        quiz_text = data["choices"][0]["message"]["content"].strip()
        return {"quiz_questions": quiz_text}

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

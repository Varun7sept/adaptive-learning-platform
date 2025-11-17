from fastapi import APIRouter
from pydantic import BaseModel
from app.services.quiz_eval_service import evaluate_quiz
from app.utils.kafka_producer import send_evaluation_event
import json
import re
import traceback

router = APIRouter()

# ✅ Define expected input schema
class AnswerSubmission(BaseModel):
    questions: str
    student_answers: str
    student_id: str
    quiz_id: str


@router.post("/quiz/evaluate")
def evaluate_quiz_route(data: AnswerSubmission):
    """
    Evaluates student's answers using Groq AI,
    safely extracts the JSON score output, and streams summary to Kafka.
    """

    # Step 1️⃣ - Evaluate quiz using Groq API
    try:
        result = evaluate_quiz(data.questions, data.student_answers)
    except Exception as e:
        print(f"❌ Groq API call failed: {e}")
        traceback.print_exc()
        return {"error": f"Groq API error: {str(e)}"}

    score, total = 0, 0

    # Step 2️⃣ - Extract JSON block correctly from LLM text
    try:
        # If Groq already returns a clean dict
        if isinstance(result, dict) and "score" in result:
            score = int(result.get("score", 0))
            total = int(result.get("total", 1))

        # If Groq returns markdown text (most common case)
        elif isinstance(result, dict) and "evaluation_result" in result:
            text_block = str(result["evaluation_result"])

            # 🎯 Look specifically for ```json ... ``` fenced block
            json_block = re.search(r"```json\s*([\s\S]*?)```", text_block)
            if json_block:
                json_text = json_block.group(1).strip()
                parsed = json.loads(json_text)
                score = int(parsed.get("score", 0))
                total = int(parsed.get("total", 1))
            else:
                # fallback: grab first JSON-like structure if present
                fallback = re.search(r"\{[\s\S]*?\}", text_block)
                if fallback:
                    parsed = json.loads(fallback.group(0))
                    score = int(parsed.get("score", 0))
                    total = int(parsed.get("total", 1))

        # If LLM output is a plain string (rare)
        elif isinstance(result, str):
            json_block = re.search(r"```json\s*([\s\S]*?)```", result)
            if json_block:
                json_text = json_block.group(1).strip()
                parsed = json.loads(json_text)
                score = int(parsed.get("score", 0))
                total = int(parsed.get("total", 1))

    except Exception as e:
        print(f"⚠️ Error parsing LLM output: {e}")
        traceback.print_exc()

    # Step 3️⃣ - Avoid division-by-zero
    if total <= 0:
        total = 1

    # Step 4️⃣ - Send evaluation summary to Kafka
    try:
        kafka_response = send_evaluation_event(
            student_id=data.student_id,
            quiz_id=data.quiz_id,
            score=score,
            total=total
        )
    except Exception as e:
        print(f"⚠️ Kafka send failed: {e}")
        traceback.print_exc()
        kafka_response = {"status": "error", "error": str(e)}

    # Step 5️⃣ - Print backend logs (for debugging)
    print("\n🧩 Raw LLM Output:\n", result)
    print(f"✅ Parsed Score: {score}, Total: {total}\n")

    # Step 6️⃣ - Always return safe structured response
    return {
        "evaluation_result": result,
        "parsed_score": score,
        "parsed_total": total,
        "kafka_stream_status": kafka_response
    }

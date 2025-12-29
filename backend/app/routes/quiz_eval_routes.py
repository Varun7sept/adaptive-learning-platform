# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.services.quiz_eval_service import evaluate_quiz
# from app.utils.kafka_producer import send_evaluation_event
# import json
# import re
# import traceback

# router = APIRouter()

# # ✅ Define expected input schema
# class AnswerSubmission(BaseModel):
#     questions: str
#     student_answers: str
#     student_id: str
#     quiz_id: str


# @router.post("/quiz/evaluate")
# def evaluate_quiz_route(data: AnswerSubmission):
#     """
#     Evaluates student's answers using Groq AI,
#     safely extracts the JSON score output, and streams summary to Kafka.
#     """

#     # Step 1️⃣ - Evaluate quiz using Groq API
#     try:
#         result = evaluate_quiz(data.questions, data.student_answers)
#     except Exception as e:
#         print(f"❌ Groq API call failed: {e}")
#         traceback.print_exc()
#         return {"error": f"Groq API error: {str(e)}"}

#     score, total = 0, 0

#     # Step 2️⃣ - Extract JSON block correctly from LLM text
#     try:
#         # If Groq already returns a clean dict
#         if isinstance(result, dict) and "score" in result:
#             score = int(result.get("score", 0))
#             total = int(result.get("total", 1))

#         # If Groq returns markdown text (most common case)
#         elif isinstance(result, dict) and "evaluation_result" in result:
#             text_block = str(result["evaluation_result"])

#             # 🎯 Look specifically for ```json ... ``` fenced block
#             json_block = re.search(r"```json\s*([\s\S]*?)```", text_block)
#             if json_block:
#                 json_text = json_block.group(1).strip()
#                 parsed = json.loads(json_text)
#                 score = int(parsed.get("score", 0))
#                 total = int(parsed.get("total", 1))
#             else:
#                 # fallback: grab first JSON-like structure if present
#                 fallback = re.search(r"\{[\s\S]*?\}", text_block)
#                 if fallback:
#                     parsed = json.loads(fallback.group(0))
#                     score = int(parsed.get("score", 0))
#                     total = int(parsed.get("total", 1))

#         # If LLM output is a plain string (rare)
#         elif isinstance(result, str):
#             json_block = re.search(r"```json\s*([\s\S]*?)```", result)
#             if json_block:
#                 json_text = json_block.group(1).strip()
#                 parsed = json.loads(json_text)
#                 score = int(parsed.get("score", 0))
#                 total = int(parsed.get("total", 1))

#     except Exception as e:
#         print(f"⚠️ Error parsing LLM output: {e}")
#         traceback.print_exc()

#     # Step 3️⃣ - Avoid division-by-zero
#     if total <= 0:
#         total = 1

#     # Step 4️⃣ - Send evaluation summary to Kafka
#     try:
#         kafka_response = send_evaluation_event(
#             student_id=data.student_id,
#             quiz_id=data.quiz_id,
#             score=score,
#             total=total
#         )
#     except Exception as e:
#         print(f"⚠️ Kafka send failed: {e}")
#         traceback.print_exc()
#         kafka_response = {"status": "error", "error": str(e)}

#     # Step 5️⃣ - Print backend logs (for debugging)
#     print("\n🧩 Raw LLM Output:\n", result)
#     print(f"✅ Parsed Score: {score}, Total: {total}\n")

#     # Step 6️⃣ - Always return safe structured response
#     return {
#         "evaluation_result": result,
#         "parsed_score": score,
#         "parsed_total": total,
#         "kafka_stream_status": kafka_response
#     }
# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.services.quiz_eval_service import evaluate_quiz
# from app.utils.kafka_producer import send_evaluation_event
# from app.database.mongo import quiz_evaluations, student_performance
# from datetime import datetime
# import json
# import re
# import traceback

# router = APIRouter()

# # ✅ Define expected input schema
# class AnswerSubmission(BaseModel):
#     questions: str
#     student_answers: str
#     student_id: str
#     quiz_id: str


# @router.post("/quiz/evaluate")
# def evaluate_quiz_route(data: AnswerSubmission):
#     """
#     Evaluates student's answers using Groq AI,
#     extracts score, stores results in MongoDB,
#     and streams summary to Kafka.
#     """

#     # Step 1️⃣ - Evaluate quiz using Groq API
#     try:
#         result = evaluate_quiz(data.questions, data.student_answers)
#     except Exception as e:
#         print(f"❌ Groq API call failed: {e}")
#         traceback.print_exc()
#         return {"error": f"Groq API error: {str(e)}"}

#     score, total = 0, 0

#     # Step 2️⃣ - Extract JSON block correctly from LLM text
#     try:
#         # If Groq already returns a clean dict
#         if isinstance(result, dict) and "score" in result:
#             score = int(result.get("score", 0))
#             total = int(result.get("total", 1))

#         # Most common case → markdown JSON returned inside text
#         elif isinstance(result, dict) and "evaluation_result" in result:
#             text_block = str(result["evaluation_result"])

#             # 🎯 Look for ```json ... ```
#             json_block = re.search(r"```json\s*([\s\S]*?)```", text_block)
#             if json_block:
#                 json_text = json_block.group(1).strip()
#                 parsed = json.loads(json_text)
#                 score = int(parsed.get("score", 0))
#                 total = int(parsed.get("total", 1))
#             else:
#                 # fallback → first JSON-looking structure
#                 fallback = re.search(r"\{[\s\S]*?\}", text_block)
#                 if fallback:
#                     parsed = json.loads(fallback.group(0))
#                     score = int(parsed.get("score", 0))
#                     total = int(parsed.get("total", 1))

#         # Plain string fallback
#         elif isinstance(result, str):
#             json_block = re.search(r"```json\s*([\s\S]*?)```", result)
#             if json_block:
#                 json_text = json_block.group(1).strip()
#                 parsed = json.loads(json_text)
#                 score = int(parsed.get("score", 0))
#                 total = int(parsed.get("total", 1))

#     except Exception as e:
#         print(f"⚠️ Error parsing LLM output: {e}")
#         traceback.print_exc()

#     # Step 3️⃣ - Avoid division-by-zero
#     if total <= 0:
#         total = 1

#     accuracy = round((score / total) * 100, 2)

#     # --------------------------------------------------------------------
#     # ✅ Step 4️⃣ — STORE RESULTS IN MONGODB
#     # --------------------------------------------------------------------

#     # 4A: Store RAW LLM output
#     raw_doc = {
#         "student_id": data.student_id,
#         "quiz_id": data.quiz_id,
#         "raw_output": result,
#         "timestamp": datetime.utcnow()
#     }
#     quiz_evaluations.insert_one(raw_doc)

#     # 4B: Store clean structured evaluation
#     clean_doc = {
#         "student_id": data.student_id,
#         "quiz_id": data.quiz_id,
#         "score": score,
#         "total": total,
#         "accuracy": accuracy,
#         "timestamp": datetime.utcnow()
#     }
#     student_performance.insert_one(clean_doc)

#     # --------------------------------------------------------------------
#     # ✅ Step 5️⃣ — SEND RESULT TO KAFKA
#     # --------------------------------------------------------------------
#     try:
#         kafka_response = send_evaluation_event(
#             student_id=data.student_id,
#             quiz_id=data.quiz_id,
#             score=score,
#             total=total
#         )
#     except Exception as e:
#         print(f"⚠️ Kafka send failed: {e}")
#         traceback.print_exc()
#         kafka_response = {"status": "error", "error": str(e)}

#     # Debug logs
#     print("\n🧩 Raw LLM Output:\n", result)
#     print(f"✅ Parsed Score: {score}, Total: {total}, Accuracy: {accuracy}\n")

#     # --------------------------------------------------------------------
#     # Step 6️⃣ — return response to frontend
#     # --------------------------------------------------------------------
#     return {
#         "evaluation_result": result,
#         "parsed_score": score,
#         "parsed_total": total,
#         "accuracy": accuracy,
#         "kafka_stream_status": kafka_response,
#         "db_status": "saved_to_mongodb"
#     }




# from fastapi import APIRouter
# from pydantic import BaseModel
# from app.services.quiz_eval_service import evaluate_quiz
# from app.utils.kafka_producer import send_evaluation_event
# from app.database.mongo import quiz_evaluations, student_performance
# from datetime import datetime
# import json
# import re
# import traceback

# router = APIRouter()

# # ------------------------------------------------------------------------------
# # ✅ INPUT MODEL
# # ------------------------------------------------------------------------------
# class AnswerSubmission(BaseModel):
#     questions: str                 # full text questions
#     student_answers: str           # plain "1. a\n2. b\n..."
#     student_id: str
#     quiz_id: str
#     detailed_results: list | None = None  
#     """
#     NEW FIELD (OPTIONAL):
#     [
#         {
#             "question": "...",
#             "selected": "...",
#             "correct": "...",
#             "is_correct": true/false
#         }
#     ]
#     """
# # ------------------------------------------------------------------------------


# @router.post("/quiz/evaluate")
# def evaluate_quiz_route(data: AnswerSubmission):
#     """
#     Evaluates student's answers using LLM,
#     parses score, stores both RAW + DETAILED data in MongoDB,
#     and streams summary to Kafka.
#     """

#     # --------------------------------------------------------------------------
#     # 1️⃣ CALL LLM
#     # --------------------------------------------------------------------------
#     try:
#         result = evaluate_quiz(data.questions, data.student_answers)
#     except Exception as e:
#         print(f"❌ Groq API call failed: {e}")
#         return {"error": f"Groq API error: {str(e)}"}

#     score, total = 0, 0

#     # --------------------------------------------------------------------------
#     # 2️⃣ PARSE JSON BLOCK FROM LLM
#     # --------------------------------------------------------------------------
#     try:
#         # If result is already a dict with score
#         if isinstance(result, dict) and "score" in result:
#             score = int(result.get("score", 0))
#             total = int(result.get("total", 1))

#         # More common case → result contains evaluation_result text
#         elif isinstance(result, dict) and "evaluation_result" in result:
#             text_block = str(result["evaluation_result"])

#             json_block = re.search(r"```json\s*([\s\S]*?)```", text_block)
#             if json_block:
#                 parsed = json.loads(json_block.group(1).strip())
#             else:
#                 # fallback
#                 fallback = re.search(r"\{[\s\S]*?\}", text_block)
#                 parsed = json.loads(fallback.group(0)) if fallback else {}

#             score = int(parsed.get("score", 0))
#             total = int(parsed.get("total", 1))

#         # Very rare → pure string
#         elif isinstance(result, str):
#             json_block = re.search(r"```json\s*([\s\S]*?)```", result)
#             parsed = json.loads(json_block.group(1).strip())
#             score = int(parsed.get("score", 0))
#             total = int(parsed.get("total", 1))

#     except Exception as e:
#         print(f"⚠️ Error parsing LLM output: {e}")

#     # Avoid division-by-zero
#     total = max(total, 1)
#     accuracy = round((score / total) * 100, 2)

#     # --------------------------------------------------------------------------
#     # 3️⃣ STORE RAW LLM OUTPUT IN MONGODB
#     # --------------------------------------------------------------------------
#     raw_doc = {
#         "student_id": data.student_id,
#         "quiz_id": data.quiz_id,
#         "raw_output": result,
#         "timestamp": datetime.utcnow()
#     }
#     quiz_evaluations.insert_one(raw_doc)

#     # --------------------------------------------------------------------------
#     # 4️⃣ STORE CLEAN SUMMARY + DETAILED RESULTS
#     # --------------------------------------------------------------------------
#     clean_doc = {
#         "student_id": data.student_id,
#         "quiz_id": data.quiz_id,
#         "score": score,
#         "total": total,
#         "accuracy": accuracy,
#         "timestamp": datetime.utcnow(),
#         # NEW: Save the detailed per-question evaluation if frontend sends it
#         "detailed_results": data.detailed_results if data.detailed_results else []
#     }
#     student_performance.insert_one(clean_doc)

#     # --------------------------------------------------------------------------
#     # 5️⃣ SEND SUMMARY TO KAFKA
#     # --------------------------------------------------------------------------
#     try:
#         kafka_response = send_evaluation_event(
#             student_id=data.student_id,
#             quiz_id=data.quiz_id,
#             score=score,
#             total=total
#         )
#     except Exception as e:
#         kafka_response = {"status": "error", "error": str(e)}

#     print("\n🧩 Raw LLM Output:\n", result)
#     print(f"✅ Parsed Score: {score}, Total: {total}, Accuracy: {accuracy}\n")

#     # --------------------------------------------------------------------------
#     # 6️⃣ RETURN FINAL RESPONSE
#     # --------------------------------------------------------------------------
#     return {
#         "evaluation_result": result,
#         "parsed_score": score,
#         "parsed_total": total,
#         "accuracy": accuracy,
#         "saved_in_mongo": True,
#         "kafka_stream_status": kafka_response
#     }

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.quiz_eval_service import evaluate_quiz
from app.utils.kafka_producer import send_evaluation_event
from app.database.mongo import quiz_evaluations, student_performance
from datetime import datetime
import json
import re

router = APIRouter()

# ------------------------------------------------------------------------------
# ✅ INPUT MODEL
# ------------------------------------------------------------------------------
class AnswerSubmission(BaseModel):
    questions: str
    student_answers: str
    student_id: str
    quiz_id: str
    detailed_results: list | None = None
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# 🔹 Helper: Difficulty estimation
# ------------------------------------------------------------------------------
def estimate_difficulty(question_text: str) -> str:
    length = len(question_text.split())
    if length <= 8:
        return "easy"
    elif length <= 15:
        return "medium"
    return "hard"


# ------------------------------------------------------------------------------
# 🔹 Helper: Confidence proxy
# ------------------------------------------------------------------------------
def compute_confidence_proxy(is_correct: bool, difficulty: str) -> float:
    if not is_correct:
        return 0.2
    if difficulty == "easy":
        return 0.9
    elif difficulty == "medium":
        return 0.75
    return 0.6


# ------------------------------------------------------------------------------
@router.post("/quiz/evaluate")
def evaluate_quiz_route(data: AnswerSubmission):
    """
    Evaluates quiz using backend LLM (single call),
    enriches detailed results,
    stores in MongoDB,
    streams to Kafka.
    """

    # --------------------------------------------------------------------------
    # 1️⃣ CALL LLM (ONLY ONCE)
    # --------------------------------------------------------------------------
    result = evaluate_quiz(data.questions, data.student_answers)

    score = int(result.get("score", 0))
    total = max(int(result.get("total", 1)), 1)
    accuracy = round((score / total) * 100, 2)

    feedback = result.get("feedback", [])

    # --------------------------------------------------------------------------
    # 2️⃣ BUILD q_no → topic MAP (FROM BACKEND LLM)
    # --------------------------------------------------------------------------
    topic_map = {}
    for item in feedback:
        q_no = item.get("q_no")
        topic_map[q_no] = item.get("topic", "Unknown Topic")

    # --------------------------------------------------------------------------
    # 3️⃣ STORE RAW LLM OUTPUT
    # --------------------------------------------------------------------------
    quiz_evaluations.insert_one({
        "student_id": data.student_id,
        "quiz_id": data.quiz_id,
        "raw_output": result,
        "timestamp": datetime.utcnow()
    })

    # --------------------------------------------------------------------------
    # 4️⃣ BUILD ENRICHED DETAILED RESULTS (MERGED)
    # --------------------------------------------------------------------------
    enriched_details = []

    if data.detailed_results:
        for idx, q in enumerate(data.detailed_results, start=1):
            question_text = q.get("question", "")
            difficulty = estimate_difficulty(question_text)

            enriched_details.append({
                "question": question_text,
                "selected": q.get("selected"),
                "correct": q.get("correct"),
                "is_correct": q.get("is_correct"),
                # 🔥 FIX: topic from BACKEND LLM
                "topic": topic_map.get(idx, "Unknown Topic"),
                "difficulty_level": difficulty,
                "question_length": len(question_text.split()),
                "confidence_proxy": compute_confidence_proxy(
                    q.get("is_correct", False),
                    difficulty
                )
            })

    # --------------------------------------------------------------------------
    # 5️⃣ STORE CLEAN DOCUMENT FOR AGENTS
    # --------------------------------------------------------------------------
    student_performance.insert_one({
        "student_id": data.student_id,
        "quiz_id": data.quiz_id,
        "score": score,
        "total": total,
        "accuracy": accuracy,
        "timestamp": datetime.utcnow(),
        "detailed_results": enriched_details
    })

    # --------------------------------------------------------------------------
    # 6️⃣ SEND SUMMARY TO KAFKA
    # --------------------------------------------------------------------------
    try:
        kafka_response = send_evaluation_event(
            student_id=data.student_id,
            quiz_id=data.quiz_id,
            score=score,
            total=total
        )
    except Exception as e:
        kafka_response = {"status": "error", "error": str(e)}

    # --------------------------------------------------------------------------
    # 7️⃣ RETURN RESPONSE
    # --------------------------------------------------------------------------
    return {
        "parsed_score": score,
        "parsed_total": total,
        "accuracy": accuracy,
        "saved_in_mongo": True,
        "kafka_stream_status": kafka_response
    }

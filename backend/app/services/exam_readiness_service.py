# from app.database.mongo import student_performance
# from app.utils.llm import call_llm
# from datetime import datetime, timezone


# def generate_exam_readiness(student_id: str):
#     """
#     Agent 3 — Exam Readiness Predictor
#     Uses ONLY the latest quiz attempt.
#     Generates a readiness score + predicted exam score.
#     """

#     # 1️⃣ Fetch latest attempt
#     latest = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not latest:
#         return {"error": "No quiz attempts found for this student."}

#     detailed = latest.get("detailed_results", [])

#     if not detailed:
#         return {"error": "No detailed results found in latest attempt."}

#     score = latest.get("score", 0)
#     total = latest.get("total", 1)
#     accuracy = round((score / total) * 100, 2)

#     incorrect = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if not q.get("is_correct")
#     ]

#     correct = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if q.get("is_correct")
#     ]

#     # 2️⃣ LLM Prompt
#     prompt = f"""
#     You are an AI Exam Readiness Analyzer.

#     Here is the student's latest quiz performance:
#     - Score: {score}/{total}
#     - Accuracy: {accuracy}%
#     - Correct Answers: {len(correct)}
#     - Incorrect Answers: {len(incorrect)}

#     Correct Responses:
#     {correct}

#     Incorrect Responses:
#     {incorrect}

#     Based on this, generate a detailed EXAM READINESS report.
#     Return ONLY JSON in this format:

#     {{
#         "readiness_score": 0-100,
#         "strengths": ["...", "..."],
#         "weaknesses": ["...", "..."],
#         "confidence_level": "High / Medium / Low",
#         "predicted_exam_score": "Marks or % the student is likely to score",
#         "suggestions": [
#             "Study this topic...",
#             "Practice these types of questions..."
#         ]
#     }}
#     """

#     llm_output = call_llm(prompt)

#     # 3️⃣ Save to MongoDB
#     readiness_doc = {
#         "student_id": student_id,
#         "score": score,
#         "total": total,
#         "accuracy": accuracy,
#         "analysis": llm_output,
#         "timestamp": datetime.now(timezone.utc)
#     }

#     from app.database.mongo import exam_readiness  # stored in new collection
#     exam_readiness.insert_one(readiness_doc)

#     return llm_output


# import json
# import re
# from datetime import datetime, timezone
# from app.database.mongo import student_performance, exam_readiness
# from app.utils.llm import call_llm


# def clean_llm_json(raw_text: str):
#     """
#     Cleans LLM text and extracts valid JSON.
#     Fixes:
#     - ```json wrappers
#     - Backticks
#     - Escaped quotes
#     - Extra text around JSON
#     """
#     if not raw_text:
#         return None

#     # Remove code block markers
#     raw_text = raw_text.replace("```json", "").replace("```", "").strip()

#     # Fix escaped quotes
#     raw_text = raw_text.replace('\\"', '"')

#     # Try direct JSON load
#     try:
#         return json.loads(raw_text)
#     except:
#         pass

#     # Extract JSON block using regex
#     match = re.search(r"\{.*\}", raw_text, re.DOTALL)
#     if match:
#         try:
#             return json.loads(match.group())
#         except:
#             return None

#     return None



# def generate_exam_readiness(student_id: str):
#     """
#     Agent 3 — Exam Readiness Predictor (latest attempt only)
#     """

#     # 1️⃣ Get latest attempt
#     latest = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not latest:
#         return {"error": "No quiz attempts found for this student."}

#     detailed = latest.get("detailed_results", [])

#     if not detailed:
#         return {"error": "No detailed results found in latest attempt."}

#     score = latest.get("score", 0)
#     total = latest.get("total", 1)
#     accuracy = round((score / total) * 100, 2)

#     incorrect = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if not q.get("is_correct")
#     ]

#     correct = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if q.get("is_correct")
#     ]

#     # 2️⃣ LLM Prompt
#     prompt = f"""
#     You are an AI Exam Readiness Analyzer.

#     Latest Quiz Performance:
#     - Score: {score}/{total}
#     - Accuracy: {accuracy}%
#     - Correct Answers: {len(correct)}
#     - Incorrect Answers: {len(incorrect)}

#     Correct Responses:
#     {correct}

#     Incorrect Responses:
#     {incorrect}

#     Generate a detailed EXAM READINESS REPORT.
#     Return ONLY JSON:

#     {{
#         "readiness_score": number (0-100),
#         "strengths": ["..."],
#         "weaknesses": ["..."],
#         "confidence_level": "High / Medium / Low",
#         "predicted_exam_score": "Likely score",
#         "suggestions": ["...", "..."]
#     }}
#     """

#     llm_output = call_llm(prompt)

#     # 3️⃣ CLEAN JSON (MOST IMPORTANT FIX)
#     parsed_output = clean_llm_json(llm_output)

#     if not parsed_output:
#         parsed_output = {"error": "Failed to parse LLM output."}

#     # 4️⃣ Save clean JSON to MongoDB
#     readiness_doc = {
#         "student_id": student_id,
#         "score": score,
#         "total": total,
#         "accuracy": accuracy,
#         "analysis": parsed_output,   # ← CLEAN JSON saved
#         "timestamp": datetime.now(timezone.utc)
#     }

#     exam_readiness.insert_one(readiness_doc)

#     # 5️⃣ Return CLEAN JSON to frontend
#     return parsed_output


# 
# import json
# import re
# from datetime import datetime, timezone

# from app.database.mongo import student_performance, exam_readiness
# from app.utils.llm import call_llm

# # ✅ NEW IMPORTS (Step 2 + Step 3)
# from app.services.explainability_features import extract_exam_readiness_features
# from app.ml.readiness_model import predict_readiness_probability


# # ----------------------------------------------------------
# # JSON CLEANER – safest version (handles ANY LLM output)
# # ----------------------------------------------------------
# def safe_json_extract(raw_text: str):
#     """
#     Extract clean JSON from messy LLM output.
#     Handles:
#     - ```json fences
#     - backticks
#     - text before/after JSON
#     - escaped quotes
#     """
#     if not raw_text:
#         return None

#     # Remove code blocks
#     raw_text = raw_text.replace("```json", "").replace("```", "").strip()

#     # Unescape quotes
#     raw_text = raw_text.replace('\\"', '"')

#     # Try direct load
#     try:
#         return json.loads(raw_text)
#     except:
#         pass

#     # Extract JSON {...}
#     match = re.search(r"\{[\s\S]*\}", raw_text)
#     if match:
#         try:
#             return json.loads(match.group())
#         except:
#             return None

#     return None


# # ----------------------------------------------------------
# # MAIN FUNCTION — Exam Readiness Analyzer
# # ----------------------------------------------------------
# def generate_exam_readiness(student_id: str):
#     """
#     Agent 3 — Exam Readiness Predictor
#     Based on the latest quiz attempt ONLY.
#     """

#     # 1️⃣ Get the latest attempt
#     latest = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not latest:
#         return {"error": "No quiz attempts found for this student."}

#     detailed = latest.get("detailed_results", [])
#     if not detailed:
#         return {"error": "No detailed results found for this attempt."}

#     score = latest.get("score", 0)
#     total = latest.get("total", 1)
#     accuracy = round((score / total) * 100, 2)

#     incorrect = [q for q in detailed if not q.get("is_correct")]
#     correct = [q for q in detailed if q.get("is_correct")]

#     # ------------------------------------------------------
#     # ✅ NEW: Extract numerical features (for explainability)
#     # ------------------------------------------------------
#     features = extract_exam_readiness_features(latest)

#     # ------------------------------------------------------
#     # ✅ NEW: ML readiness probability (TEMP DEBUG)
#     # ------------------------------------------------------
#     # ml_score = predict_readiness_probability(features)
#     # print("DEBUG ML readiness probability:", ml_score)

#     # ------------------------------------------------------
#     # 2️⃣ Prompt for the LLM
#     # ------------------------------------------------------
#     prompt = f"""
#     You are an expert AI Exam Readiness Analyzer.

#     Student Performance:
#     - Score: {score}/{total}
#     - Accuracy: {accuracy}%
#     - Correct Answers: {len(correct)}
#     - Incorrect Answers: {len(incorrect)}

#     Correct Questions:
#     {correct}

#     Incorrect Questions:
#     {incorrect}

#     Generate a DETAILED exam readiness prediction.
#     Return STRICT JSON ONLY:

#     {{
#         "readiness_score": number between 0 and 100,
#         "strengths": ["..."],
#         "weaknesses": ["..."],
#         "confidence_level": "High / Medium / Low",
#         "predicted_exam_score": "Your prediction",
#         "suggestions": ["...", "..."]
#     }}
#     """

#     llm_output = call_llm(prompt)

#     # ------------------------------------------------------
#     # 3️⃣ Clean JSON safely
#     # ------------------------------------------------------
#     parsed = safe_json_extract(llm_output)

#     if not parsed:
#         parsed = {
#             "readiness_score": accuracy,     # fallback score
#             "strengths": [],
#             "weaknesses": [],
#             "confidence_level": "Medium",
#             "predicted_exam_score": f"{accuracy}%",
#             "suggestions": [
#                 "Review weak topics.",
#                 "Practice more quizzes for improvement."
#             ],
#             "error": "LLM returned invalid JSON. Using fallback values."
#         }

#     # ------------------------------------------------------
#     # 4️⃣ Store into MongoDB
#     # ------------------------------------------------------
#     exam_readiness.insert_one({
#         "student_id": student_id,
#         "score": score,
#         "total": total,
#         "accuracy": accuracy,
#         "analysis": parsed,
#         "timestamp": datetime.now(timezone.utc)
#     })

#     # ------------------------------------------------------
#     # 5️⃣ Return CLEAN JSON to frontend
#     # ------------------------------------------------------
#     return parsed


# import json
# import re
# from datetime import datetime, timezone

# from app.database.mongo import student_performance, exam_readiness
# from app.utils.llm import call_llm

# # ✅ Feature extraction (numeric)
# from app.services.explainability_features import extract_exam_readiness_features

# # ✅ SHAP explainer
# from app.services.shap_explainer import explain_exam_readiness


# # ----------------------------------------------------------
# # JSON CLEANER – safest version (handles ANY LLM output)
# # ----------------------------------------------------------
# def safe_json_extract(raw_text: str):
#     """
#     Extract clean JSON from messy LLM output.
#     Handles:
#     - ```json fences
#     - backticks
#     - text before/after JSON
#     - escaped quotes
#     """
#     if not raw_text:
#         return None

#     # Remove code blocks
#     raw_text = raw_text.replace("```json", "").replace("```", "").strip()

#     # Unescape quotes
#     raw_text = raw_text.replace('\\"', '"')

#     # Try direct load
#     try:
#         return json.loads(raw_text)
#     except:
#         pass

#     # Extract JSON {...}
#     match = re.search(r"\{[\s\S]*\}", raw_text)
#     if match:
#         try:
#             return json.loads(match.group())
#         except:
#             return None

#     return None


# # ----------------------------------------------------------
# # MAIN FUNCTION — Exam Readiness Analyzer
# # ----------------------------------------------------------
# def generate_exam_readiness(student_id: str):
#     """
#     Agent 3 — Exam Readiness Predictor
#     Based on the latest quiz attempt ONLY.
#     """

#     # 1️⃣ Get the latest attempt
#     latest = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not latest:
#         return {"error": "No quiz attempts found for this student."}

#     detailed = latest.get("detailed_results", [])
#     if not detailed:
#         return {"error": "No detailed results found for this attempt."}

#     score = latest.get("score", 0)
#     total = latest.get("total", 1)
#     accuracy = round((score / total) * 100, 2)

#     incorrect = [q for q in detailed if not q.get("is_correct")]
#     correct = [q for q in detailed if q.get("is_correct")]

#     # ------------------------------------------------------
#     # ✅ Extract numerical features (for explainability)
#     # ------------------------------------------------------
#     features = extract_exam_readiness_features(latest)

#     # ------------------------------------------------------
#     # ✅ Generate SHAP explanation
#     # ------------------------------------------------------
#     shap_explanation = explain_exam_readiness(features)

#     # ------------------------------------------------------
#     # 2️⃣ Prompt for the LLM
#     # ------------------------------------------------------
#     prompt = f"""
#     You are an expert AI Exam Readiness Analyzer.

#     Student Performance:
#     - Score: {score}/{total}
#     - Accuracy: {accuracy}%
#     - Correct Answers: {len(correct)}
#     - Incorrect Answers: {len(incorrect)}

#     Correct Questions:
#     {correct}

#     Incorrect Questions:
#     {incorrect}

#     Generate a DETAILED exam readiness prediction.
#     Return STRICT JSON ONLY:

#     {{
#         "readiness_score": number between 0 and 100,
#         "strengths": ["..."],
#         "weaknesses": ["..."],
#         "confidence_level": "High / Medium / Low",
#         "predicted_exam_score": "Your prediction",
#         "suggestions": ["...", "..."]
#     }}
#     """

#     llm_output = call_llm(prompt)

#     # ------------------------------------------------------
#     # 3️⃣ Clean JSON safely
#     # ------------------------------------------------------
#     parsed = safe_json_extract(llm_output)

#     if not parsed:
#         parsed = {
#             "readiness_score": accuracy,     # fallback score
#             "strengths": [],
#             "weaknesses": [],
#             "confidence_level": "Medium",
#             "predicted_exam_score": f"{accuracy}%",
#             "suggestions": [
#                 "Review weak topics.",
#                 "Practice more quizzes for improvement."
#             ],
#             "error": "LLM returned invalid JSON. Using fallback values."
#         }

#     # ------------------------------------------------------
#     # ✅ Attach SHAP explainability (NON-BREAKING)
#     # ------------------------------------------------------
#     parsed["explainability"] = {
#         "method": "SHAP",
#         "features": shap_explanation
#     }

#     # ------------------------------------------------------
#     # 4️⃣ Store into MongoDB
#     # ------------------------------------------------------
#     exam_readiness.insert_one({
#         "student_id": student_id,
#         "score": score,
#         "total": total,
#         "accuracy": accuracy,
#         "analysis": parsed,
#         "timestamp": datetime.now(timezone.utc)
#     })

#     # ------------------------------------------------------
#     # 5️⃣ Return CLEAN JSON to frontend
#     # ------------------------------------------------------
#     return parsed



import json
import re
from datetime import datetime, timezone

from app.database.mongo import student_performance, exam_readiness
from app.utils.llm import call_llm

# ✅ Feature extraction
from app.services.explainability_features import extract_exam_readiness_features

# ✅ SHAP explainer
from app.services.shap_explainer import explain_exam_readiness

# ✅ LIME explainer
from app.services.lime_explainer import explain_exam_readiness_lime


# ----------------------------------------------------------
# JSON CLEANER – safest version (handles ANY LLM output)
# ----------------------------------------------------------
def safe_json_extract(raw_text: str):
    if not raw_text:
        return None

    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
    raw_text = raw_text.replace('\\"', '"')

    try:
        return json.loads(raw_text)
    except:
        pass

    match = re.search(r"\{[\s\S]*\}", raw_text)
    if match:
        try:
            return json.loads(match.group())
        except:
            return None

    return None


# ----------------------------------------------------------
# MAIN FUNCTION — Exam Readiness Analyzer
# ----------------------------------------------------------
def generate_exam_readiness(student_id: str):
    """
    Agent 3 — Exam Readiness Predictor
    Based on the latest quiz attempt ONLY.
    """

    # 1️⃣ Fetch latest attempt
    latest = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not latest:
        return {"error": "No quiz attempts found for this student."}

    detailed = latest.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results found for this attempt."}

    score = latest.get("score", 0)
    total = latest.get("total", 1)
    accuracy = round((score / total) * 100, 2)

    incorrect = [q for q in detailed if not q.get("is_correct")]
    correct = [q for q in detailed if q.get("is_correct")]

    # ------------------------------------------------------
    # ✅ Extract numeric features (shared by SHAP & LIME)
    # ------------------------------------------------------
    features = extract_exam_readiness_features(latest)

    # ------------------------------------------------------
    # ✅ Generate SHAP explanation (global + local)
    # ------------------------------------------------------
    shap_explanation = explain_exam_readiness(features)

    # ------------------------------------------------------
    # ✅ Generate LIME explanation (purely local)
    # ------------------------------------------------------
    lime_explanation = explain_exam_readiness_lime(features)

    # ------------------------------------------------------
    # 2️⃣ LLM-based readiness reasoning
    # ------------------------------------------------------
    prompt = f"""
    You are an expert AI Exam Readiness Analyzer.

    Student Performance:
    - Score: {score}/{total}
    - Accuracy: {accuracy}%
    - Correct Answers: {len(correct)}
    - Incorrect Answers: {len(incorrect)}

    Correct Questions:
    {correct}

    Incorrect Questions:
    {incorrect}

    Generate a DETAILED exam readiness prediction.
    Return STRICT JSON ONLY:

    {{
        "readiness_score": number between 0 and 100,
        "strengths": ["..."],
        "weaknesses": ["..."],
        "confidence_level": "High / Medium / Low",
        "predicted_exam_score": "Your prediction",
        "suggestions": ["...", "..."]
    }}
    """

    llm_output = call_llm(prompt)

    # ------------------------------------------------------
    # 3️⃣ Parse LLM output safely
    # ------------------------------------------------------
    parsed = safe_json_extract(llm_output)

    if not parsed:
        parsed = {
            "readiness_score": accuracy,
            "strengths": [],
            "weaknesses": [],
            "confidence_level": "Medium",
            "predicted_exam_score": f"{accuracy}%",
            "suggestions": [
                "Review weak topics.",
                "Practice more quizzes."
            ],
            "error": "LLM returned invalid JSON."
        }

    # ------------------------------------------------------
    # ✅ Attach explainability (NON-BREAKING)
    # ------------------------------------------------------
    parsed["explainability"] = {
        "shap": {
            "method": "SHAP",
            "features": shap_explanation
        },
        "lime": {
            "method": "LIME",
            "features": lime_explanation
        }
    }

    # ------------------------------------------------------
    # 4️⃣ Store in MongoDB
    # ------------------------------------------------------
    exam_readiness.insert_one({
        "student_id": student_id,
        "score": score,
        "total": total,
        "accuracy": accuracy,
        "analysis": parsed,
        "timestamp": datetime.now(timezone.utc)
    })

    # ------------------------------------------------------
    # 5️⃣ Return response
    # ------------------------------------------------------
    return parsed

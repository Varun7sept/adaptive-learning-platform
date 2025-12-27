from fastapi import APIRouter, Query
from datetime import datetime, timezone

# Imports from your project
from app.services.agent_service import analyze_student
from app.services.exam_readiness_service import generate_exam_readiness
from app.services.practice_question_service import generate_practice_questions
from app.services.learning_path import generate_learning_path
from app.utils.llm import call_llm
from app.database.mongo import student_performance

router = APIRouter()


# -------------------------------------------------------------------------
# 🔹 AGENT 1 — Weak Concept Detector
# -------------------------------------------------------------------------
@router.get("/agent/weak_concepts/{student_id}")
def weak_concepts(student_id: str):
    """
    Agent 1:
    Identify weak concepts from the student's latest quiz attempt.
    """

    record = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not record:
        return {"error": "No evaluation found for this student."}

    detailed = record.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results present in the latest attempt."}

    incorrect_items = [
        {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
        for q in detailed if not q.get("is_correct")
    ]

    if not incorrect_items:
        return {
            "student_id": student_id,
            "message": "Great job! No weak concepts detected."
        }

    prompt = f"""
    You are an expert learning profiler.

    These are the student's incorrect answers:
    {incorrect_items}

    Identify weak concepts. Return ONLY JSON:
    {{
        "weak_concepts": [
            {{"concept": "", "why_weak": ""}}
        ],
        "summary": ""
    }}
    """

    analysis = call_llm(prompt)

    return {
        "student_id": student_id,
        "agent_analysis": analysis,
        "timestamp": datetime.now(timezone.utc)
    }



# # -------------------------------------------------------------------------
# # 🔹 AGENT 2 — Personalized Learning Path
# # -------------------------------------------------------------------------
# @router.get("/agent/learning_path/{student_id}")
# def learning_path(student_id: str):
#     """
#     Agent 2:
#     Generates a personalized learning path from incorrect answers.
#     """

#     record = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not record:
#         return {"error": "No performance record found."}

#     detailed = record.get("detailed_results", [])
#     if not detailed:
#         return {"error": "No detailed results in latest attempt."}

#     incorrect_items = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if not q.get("is_correct")
#     ]

#     if not incorrect_items:
#         return {
#             "student_id": student_id,
#             "message": "Excellent work! No learning path needed.",
#             "learning_path": []
#         }

#     prompt = f"""
#     You are an AI tutor developing a personalized learning path.

#     Incorrect answers:
#     {incorrect_items}

#     Return ONLY JSON:
#     {{
#         "learning_path": [
#             {{
#                 "topic": "",
#                 "why_important": "",
#                 "subtopics": [],
#                 "resources": [],
#                 "practice_tasks": [],
#                 "time_required": "",
#                 "difficulty": ""
#             }}
#         ],
#         "summary": ""
#     }}
#     """

#     response = call_llm(prompt)

#     return {
#         "student_id": student_id,
#         "learning_path": response,
#         "timestamp": datetime.now(timezone.utc)
#     }

# -------------------------------------------------------------------------
# 🔹 AGENT 2 — Personalized Learning Path
# -------------------------------------------------------------------------
# AGENT 2 — Personalized Learning Path
@router.get("/agent/learning_path/{student_id}")
def learning_path(student_id: str):

    record = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not record:
        return {"error": "No performance record found."}

    detailed = record.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results in latest attempt."}

    incorrect_items = [
        {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
        for q in detailed if not q.get("is_correct")
    ]

    from app.services.learning_path import generate_learning_path
    lp = generate_learning_path(incorrect_items, student_id)

    return {
        "student_id": student_id,
        "learning_path": lp,
        "timestamp": datetime.now(timezone.utc)
    }






# -------------------------------------------------------------------------
# 🔹 AGENT 3 — Exam Readiness Predictor (Latest Attempt)
# -------------------------------------------------------------------------
@router.get("/agent/exam_readiness/{student_id}")
def exam_readiness(student_id: str):
    """
    Agent 3:
    Predicts exam readiness using the latest quiz attempt.
    """

    readiness_output = generate_exam_readiness(student_id)

    return {
        "student_id": student_id,
        "exam_readiness": readiness_output,
        "timestamp": datetime.now(timezone.utc)
    }



# -------------------------------------------------------------------------
# 🔹 AGENT 4 — Full Agentic Pattern Analysis
# -------------------------------------------------------------------------
@router.get("/agent/full_analysis/{student_id}")
def full_analysis(student_id: str):
    """
    Agent 4:
    Deep analysis using agent_service.py
    """

    output = analyze_student(student_id)

    return {
        "student_id": student_id,
        "agent_analysis": output,
        "timestamp": datetime.now(timezone.utc)
    }



# -------------------------------------------------------------------------
# 🔹 AGENT 5 — Personalized Practice Question Generator
# -------------------------------------------------------------------------
@router.get("/agent/practice_questions/{student_id}")
def practice_questions(
    student_id: str,
    num_questions: int = Query(..., ge=1, le=20, description="Number of practice questions")
):
    """
    Agent 5:
    Generates personalized MCQ practice questions based on weak concepts.
    User chooses number of questions.
    """

    record = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not record:
        return {"error": "No evaluation found for this student."}

    detailed = record.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results found."}

    # Build weak concept list for practice question generation
    weak_concepts = [
        {
            "question": q["question"],
            "concept": q["question"],  # You can extract deeper concepts later
            "selected": q["selected"],
            "correct": q["correct"]
        }
        for q in detailed if not q.get("is_correct")
    ]

    if not weak_concepts:
        return {
            "message": "Student has no weak concepts. No practice needed.",
            "practice_questions": []
        }

    # Generate questions
    output = generate_practice_questions(weak_concepts, num_questions, student_id)

    return {
        "student_id": student_id,
        "practice_questions": output,
        "timestamp": datetime.now(timezone.utc)
    }

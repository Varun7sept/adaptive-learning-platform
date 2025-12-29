# from fastapi import APIRouter, Query
# from datetime import datetime, timezone

# # Imports from your project
# from app.services.agent_service import analyze_student
# from app.services.exam_readiness_service import generate_exam_readiness
# from app.services.practice_question_service import generate_practice_questions
# from app.services.learning_path import generate_learning_path
# from app.utils.llm import call_llm
# from app.database.mongo import student_performance

# router = APIRouter()


# # -------------------------------------------------------------------------
# # 🔹 AGENT 1 — Weak Concept Detector
# # -------------------------------------------------------------------------
# @router.get("/agent/weak_concepts/{student_id}")
# def weak_concepts(student_id: str):
#     """
#     Agent 1:
#     Identify weak concepts from the student's latest quiz attempt.
#     """

#     record = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not record:
#         return {"error": "No evaluation found for this student."}

#     detailed = record.get("detailed_results", [])
#     if not detailed:
#         return {"error": "No detailed results present in the latest attempt."}

#     incorrect_items = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if not q.get("is_correct")
#     ]

#     if not incorrect_items:
#         return {
#             "student_id": student_id,
#             "message": "Great job! No weak concepts detected."
#         }

#     prompt = f"""
#     You are an expert learning profiler.

#     These are the student's incorrect answers:
#     {incorrect_items}

#     Identify weak concepts. Return ONLY JSON:
#     {{
#         "weak_concepts": [
#             {{"concept": "", "why_weak": ""}}
#         ],
#         "summary": ""
#     }}
#     """

#     analysis = call_llm(prompt)

#     return {
#         "student_id": student_id,
#         "agent_analysis": analysis,
#         "timestamp": datetime.now(timezone.utc)
#     }



# # AGENT 2 — Personalized Learning Path
# @router.get("/agent/learning_path/{student_id}")
# def learning_path(student_id: str):

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

#     from app.services.learning_path import generate_learning_path
#     lp = generate_learning_path(incorrect_items, student_id)

#     return {
#         "student_id": student_id,
#         "learning_path": lp,
#         "timestamp": datetime.now(timezone.utc)
#     }






# # -------------------------------------------------------------------------
# # 🔹 AGENT 3 — Exam Readiness Predictor (Latest Attempt)
# # -------------------------------------------------------------------------
# @router.get("/agent/exam_readiness/{student_id}")
# def exam_readiness(student_id: str):
#     """
#     Agent 3:
#     Predicts exam readiness using the latest quiz attempt.
#     """

#     readiness_output = generate_exam_readiness(student_id)

#     return {
#         "student_id": student_id,
#         "exam_readiness": readiness_output,
#         "timestamp": datetime.now(timezone.utc)
#     }



# # -------------------------------------------------------------------------
# # 🔹 AGENT 4 — Full Agentic Pattern Analysis
# # -------------------------------------------------------------------------
# @router.get("/agent/full_analysis/{student_id}")
# def full_analysis(student_id: str):
#     """
#     Agent 4:
#     Deep analysis using agent_service.py
#     """

#     output = analyze_student(student_id)

#     return {
#         "student_id": student_id,
#         "agent_analysis": output,
#         "timestamp": datetime.now(timezone.utc)
#     }



# # -------------------------------------------------------------------------
# # 🔹 AGENT 5 — Personalized Practice Question Generator
# # -------------------------------------------------------------------------
# @router.get("/agent/practice_questions/{student_id}")
# def practice_questions(
#     student_id: str,
#     num_questions: int = Query(..., ge=1, le=20, description="Number of practice questions")
# ):
#     """
#     Agent 5:
#     Generates personalized MCQ practice questions based on weak concepts.
#     User chooses number of questions.
#     """

#     record = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not record:
#         return {"error": "No evaluation found for this student."}

#     detailed = record.get("detailed_results", [])
#     if not detailed:
#         return {"error": "No detailed results found."}

#     # Build weak concept list for practice question generation
#     weak_concepts = [
#         {
#             "question": q["question"],
#             "concept": q["question"],  # You can extract deeper concepts later
#             "selected": q["selected"],
#             "correct": q["correct"]
#         }
#         for q in detailed if not q.get("is_correct")
#     ]

#     if not weak_concepts:
#         return {
#             "message": "Student has no weak concepts. No practice needed.",
#             "practice_questions": []
#         }

#     # Generate questions
#     output = generate_practice_questions(weak_concepts, num_questions, student_id)

#     return {
#         "student_id": student_id,
#         "practice_questions": output,
#         "timestamp": datetime.now(timezone.utc)
#     }

from fastapi import APIRouter, Query
from datetime import datetime, timezone

# Imports from your project
from app.services.agent_service import analyze_student
from app.services.exam_readiness_service import generate_exam_readiness
from app.services.practice_question_service import generate_practice_questions
from app.services.learning_path import generate_learning_path
from app.services.concept_mastery_confidence_service import ConceptMasteryConfidenceService
from app.services.cognitive_load_service import CognitiveLoadService
from app.utils.llm import call_llm
from app.database.mongo import student_performance
from app.services.guessing_detection_service import GuessingDetectionService


router = APIRouter()


# # -------------------------------------------------------------------------
# # 🔹 AGENT 1 — Weak Concept Detector
# # -------------------------------------------------------------------------
# @router.get("/agent/weak_concepts/{student_id}")
# def weak_concepts(student_id: str):
#     """
#     Agent 1:
#     Identify weak concepts from the student's latest quiz attempt.
#     """

#     record = student_performance.find_one(
#         {"student_id": student_id},
#         sort=[("timestamp", -1)]
#     )

#     if not record:
#         return {"error": "No evaluation found for this student."}

#     detailed = record.get("detailed_results", [])
#     if not detailed:
#         return {"error": "No detailed results present in the latest attempt."}

#     incorrect_items = [
#         {"question": q["question"], "selected": q["selected"], "correct": q["correct"]}
#         for q in detailed if not q.get("is_correct")
#     ]

#     if not incorrect_items:
#         return {
#             "student_id": student_id,
#             "message": "Great job! No weak concepts detected."
#         }

#     prompt = f"""
#     You are an expert learning profiler.

#     These are the student's incorrect answers:
#     {incorrect_items}

#     Identify weak concepts. Return ONLY JSON:
#     {{
#         "weak_concepts": [
#             {{"concept": "", "why_weak": ""}}
#         ],
#         "summary": ""
#     }}
#     """

#     analysis = call_llm(prompt)

#     return {
#         "student_id": student_id,
#         "agent_analysis": analysis,
#         "timestamp": datetime.now(timezone.utc)
#     }


# -------------------------------------------------------------------------
# 🔹 AGENT 1 — Weak Concept Detector (Explainable)
# -------------------------------------------------------------------------
@router.get("/agent/weak_concepts/{student_id}")
def weak_concepts(student_id: str):
    """
    Agent 1:
    Identify weak concepts from the student's latest quiz attempt
    with SHAP/LIME-style explainability.
    """

    # --------------------------------------------------
    # 1️⃣ Fetch latest attempt ONLY
    # --------------------------------------------------
    record = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not record:
        return {"error": "No evaluation found for this student."}

    detailed = record.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results present in the latest attempt."}

    # --------------------------------------------------
    # 2️⃣ Extract incorrect questions
    # --------------------------------------------------
    incorrect_items = [
        {
            "question": q.get("question"),
            "topic": q.get("topic", "Unknown Topic"),
            "selected": q.get("selected"),
            "correct": q.get("correct")
        }
        for q in detailed if not q.get("is_correct")
    ]

    if not incorrect_items:
        return {
            "student_id": student_id,
            "weak_concepts": [],
            "summary": "Great job! No weak concepts detected.",
            "numeric_explainability": {},
            "timestamp": datetime.now(timezone.utc)
        }

    # --------------------------------------------------
    # 3️⃣ Numeric feature extraction (SHAP-style base)
    # --------------------------------------------------
    topic_features = {}
    for q in incorrect_items:
        topic = q["topic"]
        topic_features.setdefault(topic, {
            "incorrect_count": 0,
            "total_attempts": 0
        })
        topic_features[topic]["incorrect_count"] += 1

    for q in detailed:
        topic = q.get("topic", "Unknown Topic")
        topic_features.setdefault(topic, {
            "incorrect_count": 0,
            "total_attempts": 0
        })
        topic_features[topic]["total_attempts"] += 1

    topic_scores = {}
    topic_explanations = {}

    for topic, feats in topic_features.items():
        total = feats["total_attempts"]
        incorrect = feats["incorrect_count"]
        accuracy = 1 - (incorrect / total) if total > 0 else 0

        weakness_score = round((incorrect / total) * (1 - accuracy), 3)

        topic_scores[topic] = weakness_score
        topic_explanations[topic] = [
            {
                "feature": "incorrect_count",
                "impact": incorrect,
                "direction": "negative"
            },
            {
                "feature": "accuracy",
                "impact": round(accuracy, 3),
                "direction": "positive" if accuracy >= 0.6 else "negative"
            },
            {
                "feature": "total_attempts",
                "impact": total,
                "direction": "neutral"
            }
        ]

    # Pick weakest topics
    weakest_topics = sorted(
        topic_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    weakest_topic_names = [t[0] for t in weakest_topics]

    # --------------------------------------------------
    # 4️⃣ LLM reasoning (grounded in numeric scores)
    # --------------------------------------------------
    prompt = f"""
    You are an AI learning coach.

    The student has the following topic-wise weakness scores:
    {topic_scores}

    Weakest topics:
    {weakest_topic_names}

    Task:
    - Explain why these topics are weak
    - Summarize common mistakes
    - Suggest a short improvement strategy

    Return STRICT JSON ONLY:
    {{
        "weak_concepts": [
            {{"concept": "", "why_weak": ""}}
        ],
        "summary": ""
    }}
    """

    raw_llm_output = call_llm(prompt)

    # --------------------------------------------------
    # 5️⃣ Safe JSON parsing
    # --------------------------------------------------
    import json

    try:
        parsed_llm = json.loads(
            raw_llm_output.replace("```json", "").replace("```", "").strip()
        )
    except Exception:
        parsed_llm = {
            "weak_concepts": [],
            "summary": "Unable to parse LLM explanation."
        }

    # --------------------------------------------------
    # 6️⃣ FINAL RESPONSE (Frontend-ready)
    # --------------------------------------------------
    return {
        "student_id": student_id,
        "weak_concepts": parsed_llm.get("weak_concepts", []),
        "summary": parsed_llm.get("summary", ""),
        "numeric_explainability": {
            "method": "SHAP/LIME (Concept-Level)",
            "scores": topic_scores,
            "details": topic_explanations
        },
        "timestamp": datetime.now(timezone.utc)
    }


# -------------------------------------------------------------------------
# 🔹 AGENT 2 — Personalized Learning Path
# -------------------------------------------------------------------------
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

    weak_concepts = [
        {
            "question": q["question"],
            "concept": q["question"],  # placeholder for now
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

    output = generate_practice_questions(weak_concepts, num_questions, student_id)

    return {
        "student_id": student_id,
        "practice_questions": output,
        "timestamp": datetime.now(timezone.utc)
    }


# -------------------------------------------------------------------------
# 🔹 AGENT 6 — Concept Mastery Confidence (Latest Attempt Only)
# -------------------------------------------------------------------------
@router.get("/agent/concept_mastery_confidence/{student_id}")
def concept_mastery_confidence(student_id: str):
    """
    Agent 6:
    Computes concept-wise mastery confidence
    using ONLY the latest quiz attempt.
    """

    record = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not record:
        return {"error": "No evaluation found for this student."}

    detailed = record.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results in latest attempt."}

    agent = ConceptMasteryConfidenceService()
    output = agent.analyze(detailed)

    return {
        "student_id": student_id,
        "concept_mastery_confidence": output,
        "timestamp": datetime.now(timezone.utc)
    }
# -------------------------------------------------------------------------
# 🔹 AGENT 7 — Cognitive Load Analyzer (Latest Attempt Only)
# -------------------------------------------------------------------------
@router.get("/agent/cognitive-load/{student_id}")
def cognitive_load(student_id: str):
    """
    Cognitive Load Agent:
    Estimates cognitive strain using the latest quiz attempt only.
    """

    # Fetch latest performance document
    record = student_performance.find_one(
        {"student_id": student_id},
        sort=[("timestamp", -1)]
    )

    if not record:
        return {"error": "No evaluation found for this student."}

    detailed = record.get("detailed_results", [])
    if not detailed:
        return {"error": "No detailed results found in latest attempt."}

    # Run Cognitive Load Service
    service = CognitiveLoadService()
    output = service.analyze(detailed)

    return {
        "student_id": student_id,
        "cognitive_load_analysis": output
    }
# -------------------------------------------------------------------------
# 🔹 AGENT 8 — Guessing & Overconfidence Detection
# -------------------------------------------------------------------------
@router.get("/agent/guessing-detection/{student_id}")
def guessing_detection(student_id: str):
    """
    Detects guessing and overconfidence using latest quiz attempt
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

    service = GuessingDetectionService()
    output = service.analyze(detailed)

    return {
        "student_id": student_id,
        "guessing_detection_analysis": output,
        "timestamp": datetime.now(timezone.utc)
    }

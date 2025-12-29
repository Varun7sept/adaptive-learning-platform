# from app.database.mongo import student_performance, quiz_evaluations
# from app.utils.llm import run_llm_agent
# from bson import ObjectId

# def analyze_student(student_id: str):
#     """
#     Agent analyzes a student's performance over all attempts.
#     """

#     # 1️⃣ Get all performance docs
#     perf_docs = list(student_performance.find({"student_id": student_id}).sort("timestamp", -1))

#     # 2️⃣ Get all detailed results (questions, selected, correct)
#     eval_docs = list(quiz_evaluations.find({"student_id": student_id}).sort("timestamp", -1))

#     # Combine all detailed_results
#     all_questions = []
#     for doc in eval_docs:
#         if "detailed_results" in doc:
#             all_questions.extend(doc["detailed_results"])

#     if not all_questions:
#         return {"error": "No detailed results found for student."}

#     # 3️⃣ Calculate accuracy per question type/concept
#     weak_points = []
#     for q in all_questions:
#         weak_points.append({
#             "question": q["question"],
#             "selected": q["selected"],
#             "correct": q["correct"],
#             "is_correct": q["is_correct"]
#         })

#     # 4️⃣ Send to LLM agent to interpret patterns
#     prompt = f"""
#     You are an AI learning coach analyzing a student's quiz performance.

#     Here are all the student's question attempts with correctness:
#     {weak_points}

#     Task:
#     - Identify the key concepts or topics this student is weak in.
#     - Summarize the mistakes the student repeatedly makes.
#     - Suggest the top 3 topics the student MUST study next.
#     - Provide a clear explanation of why these topics were selected.

#     Return the result in JSON:
#     {{
#         "weak_concepts": ["...", "..."],
#         "common_mistakes": ["...", "..."],
#         "recommended_topics": ["...", "..."],
#         "reasoning": "Explain why these recommendations were made"
#     }}
#     """

#     agent_output = run_llm_agent(prompt)

#     return agent_output


# from app.database.mongo import student_performance, quiz_evaluations
# from app.utils.llm import call_llm     # ✅ Correct function
# from bson import ObjectId

# def analyze_student(student_id: str):
#     """
#     Agent analyzes a student's performance over all attempts.
#     """

#     # 1️⃣ Get all performance documents
#     perf_docs = list(
#         student_performance.find({"student_id": student_id}).sort("timestamp", -1)
#     )

#     # 2️⃣ Get all raw evaluation docs with detailed results
#     eval_docs = list(
#         quiz_evaluations.find({"student_id": student_id}).sort("timestamp", -1)
#     )

#     all_questions = []

#     # Extract detailed results from all attempts
#     for doc in eval_docs:
#         if "detailed_results" in doc:
#             all_questions.extend(doc["detailed_results"])

#     if not all_questions:
#         return {"error": "No detailed results found for student."}

#     # 3️⃣ Prepare data for LLM (weak points + correctness)
#     weak_points = []
#     for q in all_questions:
#         weak_points.append({
#             "question": q["question"],
#             "selected": q["selected"],
#             "correct": q["correct"],
#             "is_correct": q["is_correct"],
#         })

#     # 4️⃣ Build LLM prompt
#     prompt = f"""
#     You are an AI learning coach analyzing a student's quiz performance.

#     Here are all the student's question attempts with correctness:
#     {weak_points}

#     Task:
#     - Identify the key concepts or topics this student is weak in.
#     - Summarize repeated mistakes.
#     - Suggest the top 3 topics the student should study next.
#     - Provide clear reasoning for these suggestions.

#     Return JSON ONLY:
#     {{
#         "weak_concepts": ["...", "..."],
#         "common_mistakes": ["...", "..."],
#         "recommended_topics": ["...", "..."],
#         "reasoning": ""
#     }}
#     """

#     # 5️⃣ Call Groq LLM using your actual utility function
#     output = call_llm(prompt)

#     return output




# from collections import defaultdict

# from app.database.mongo import quiz_evaluations
# from app.utils.llm import call_llm


# # ----------------------------------------------------------
# # 🔹 Helper: Extract numeric features per topic
# # ----------------------------------------------------------
# def extract_topic_features(all_questions):
#     """
#     Builds numeric features per topic.

#     Returns:
#     {
#         topic: {
#             "incorrect_count": int,
#             "total_attempts": int,
#             "accuracy": float
#         }
#     }
#     """
#     stats = defaultdict(lambda: {
#         "incorrect_count": 0,
#         "total_attempts": 0
#     })

#     for q in all_questions:
#         topic = q.get("topic", "Unknown Topic")
#         stats[topic]["total_attempts"] += 1
#         if not q.get("is_correct", False):
#             stats[topic]["incorrect_count"] += 1

#     features = {}
#     for topic, s in stats.items():
#         total = s["total_attempts"]
#         incorrect = s["incorrect_count"]
#         accuracy = 1 - (incorrect / total) if total > 0 else 0

#         features[topic] = {
#             "incorrect_count": incorrect,
#             "total_attempts": total,
#             "accuracy": round(accuracy, 3)
#         }

#     return features


# # ----------------------------------------------------------
# # 🔹 Helper: Compute weakness score (interpretable)
# # ----------------------------------------------------------
# def compute_weakness_score(feats):
#     """
#     Weakness score between 0 and 1.
#     Higher = weaker topic.
#     """
#     if feats["total_attempts"] == 0:
#         return 0.0

#     score = (feats["incorrect_count"] / feats["total_attempts"]) * (1 - feats["accuracy"])
#     return round(score, 3)


# # ----------------------------------------------------------
# # 🔹 Helper: SHAP/LIME-style explanation
# # ----------------------------------------------------------
# def explain_topic(feats):
#     """
#     Returns explainability signals similar to SHAP/LIME.
#     """
#     explanation = []

#     if feats["incorrect_count"] > 0:
#         explanation.append({
#             "feature": "incorrect_count",
#             "impact": feats["incorrect_count"],
#             "direction": "negative"
#         })

#     explanation.append({
#         "feature": "accuracy",
#         "impact": feats["accuracy"],
#         "direction": "positive" if feats["accuracy"] >= 0.6 else "negative"
#     })

#     explanation.append({
#         "feature": "total_attempts",
#         "impact": feats["total_attempts"],
#         "direction": "neutral"
#     })

#     return explanation


# # ----------------------------------------------------------
# # 🔹 MAIN FUNCTION — UPDATED (HYBRID + EXPLAINABLE)
# # ----------------------------------------------------------
# def analyze_student(student_id: str):
#     """
#     Explainable Weak Concept Analyzer
#     (Hybrid Numeric + SHAP/LIME + LLM)
#     """

#     # 1️⃣ Fetch all evaluated quiz attempts
#     eval_docs = list(
#         quiz_evaluations.find({"student_id": student_id}).sort("timestamp", -1)
#     )

#     all_questions = []
#     for doc in eval_docs:
#         if "detailed_results" in doc:
#             all_questions.extend(doc["detailed_results"])

#     if not all_questions:
#         return {"error": "No detailed results found for student."}

#     # ------------------------------------------------------
#     # 2️⃣ Numeric topic-wise feature extraction
#     # ------------------------------------------------------
#     topic_features = extract_topic_features(all_questions)

#     topic_scores = {}
#     topic_explanations = {}

#     for topic, feats in topic_features.items():
#         topic_scores[topic] = compute_weakness_score(feats)
#         topic_explanations[topic] = explain_topic(feats)

#     # Sort weakest topics
#     sorted_topics = sorted(
#         topic_scores.items(),
#         key=lambda x: x[1],
#         reverse=True
#     )

#     weakest_topics = [t[0] for t in sorted_topics[:3]]

#     # ------------------------------------------------------
#     # 3️⃣ LLM reasoning (kept, but now informed by numbers)
#     # ------------------------------------------------------
#     prompt = f"""
#     You are an AI learning coach.

#     The student has the following topic-wise weakness scores:
#     {topic_scores}

#     Weakest topics:
#     {weakest_topics}

#     Task:
#     - Explain why these topics are weak
#     - Summarize common mistakes
#     - Suggest the best study strategy

#     Return JSON ONLY:
#     {{
#         "weak_concepts": ["...", "..."],
#         "common_mistakes": ["...", "..."],
#         "recommended_topics": ["...", "..."],
#         "reasoning": ""
#     }}
#     """

#     llm_output = call_llm(prompt)

#     # ------------------------------------------------------
#     # 4️⃣ FINAL RESPONSE (NON-BREAKING + EXTENDED)
#     # ------------------------------------------------------
#     return {
#         "weak_concepts": weakest_topics,
#         "topic_scores": topic_scores,
#         "explainability": {
#             "method": "SHAP/LIME (Concept-Level)",
#             "details": topic_explanations
#         },
#         "llm_analysis": llm_output
#     }



from collections import defaultdict

from app.database.mongo import student_performance
from app.utils.llm import call_llm


# ----------------------------------------------------------
# 🔹 Helper: Extract numeric features per topic
# ----------------------------------------------------------
def extract_topic_features(all_questions):
    """
    Builds numeric features per topic.

    Returns:
    {
        topic: {
            "incorrect_count": int,
            "total_attempts": int,
            "accuracy": float
        }
    }
    """
    stats = defaultdict(lambda: {
        "incorrect_count": 0,
        "total_attempts": 0
    })

    for q in all_questions:
        topic = q.get("topic", "Unknown Topic")
        stats[topic]["total_attempts"] += 1
        if not q.get("is_correct", False):
            stats[topic]["incorrect_count"] += 1

    features = {}
    for topic, s in stats.items():
        total = s["total_attempts"]
        incorrect = s["incorrect_count"]
        accuracy = 1 - (incorrect / total) if total > 0 else 0

        features[topic] = {
            "incorrect_count": incorrect,
            "total_attempts": total,
            "accuracy": round(accuracy, 3)
        }

    return features


# ----------------------------------------------------------
# 🔹 Helper: Compute weakness score (interpretable)
# ----------------------------------------------------------
def compute_weakness_score(feats):
    """
    Weakness score between 0 and 1.
    Higher = weaker topic.
    """
    if feats["total_attempts"] == 0:
        return 0.0

    score = (feats["incorrect_count"] / feats["total_attempts"]) * (1 - feats["accuracy"])
    return round(score, 3)


# ----------------------------------------------------------
# 🔹 Helper: SHAP/LIME-style explanation
# ----------------------------------------------------------
def explain_topic(feats):
    """
    Returns explainability signals similar to SHAP/LIME.
    """
    explanation = []

    if feats["incorrect_count"] > 0:
        explanation.append({
            "feature": "incorrect_count",
            "impact": feats["incorrect_count"],
            "direction": "negative"
        })

    explanation.append({
        "feature": "accuracy",
        "impact": feats["accuracy"],
        "direction": "positive" if feats["accuracy"] >= 0.6 else "negative"
    })

    explanation.append({
        "feature": "total_attempts",
        "impact": feats["total_attempts"],
        "direction": "neutral"
    })

    return explanation


# ----------------------------------------------------------
# 🔹 MAIN FUNCTION — HYBRID + EXPLAINABLE (FINAL)
# ----------------------------------------------------------
def analyze_student(student_id: str):
    """
    Explainable Weak Concept Analyzer
    (Hybrid Numeric + SHAP/LIME + LLM)
    """

    # 1️⃣ Fetch all performance documents (CORRECT SOURCE)
    eval_docs = list(
        student_performance.find({"student_id": student_id}).sort("timestamp", -1)
    )

    all_questions = []
    for doc in eval_docs:
        if "detailed_results" in doc:
            all_questions.extend(doc["detailed_results"])

    if not all_questions:
        return {"error": "No detailed results found for student."}

    # ------------------------------------------------------
    # 2️⃣ Numeric topic-wise feature extraction
    # ------------------------------------------------------
    topic_features = extract_topic_features(all_questions)

    topic_scores = {}
    topic_explanations = {}

    for topic, feats in topic_features.items():
        topic_scores[topic] = compute_weakness_score(feats)
        topic_explanations[topic] = explain_topic(feats)

    # Sort weakest topics
    sorted_topics = sorted(
        topic_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    weakest_topics = [t[0] for t in sorted_topics[:3]]

    # ------------------------------------------------------
    # 3️⃣ LLM reasoning (now grounded in numeric scores)
    # ------------------------------------------------------
    prompt = f"""
    You are an AI learning coach.

    The student has the following topic-wise weakness scores:
    {topic_scores}

    Weakest topics:
    {weakest_topics}

    Task:
    - Explain why these topics are weak
    - Summarize common mistakes
    - Suggest the best study strategy

    Return JSON ONLY:
    {{
        "weak_concepts": ["...", "..."],
        "common_mistakes": ["...", "..."],
        "recommended_topics": ["...", "..."],
        "reasoning": ""
    }}
    """

    llm_output = call_llm(prompt)

    # ------------------------------------------------------
    # 4️⃣ FINAL RESPONSE (EXPLAINABLE AGENT OUTPUT)
    # ------------------------------------------------------
    return {
    "weak_concepts": [
        {
            "concept": topic,
            "weakness_score": topic_scores[topic],
            "explainability": topic_explanations[topic]
        }
        for topic in weakest_topics
    ],
    "llm_analysis": llm_output
}

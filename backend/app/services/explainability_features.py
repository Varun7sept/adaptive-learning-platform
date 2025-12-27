"""
Feature extraction for explainability (Agent 3 – Exam Readiness)

This file ONLY converts student quiz performance
into numerical features suitable for ML explainability.
"""

def extract_exam_readiness_features(latest_attempt: dict) -> dict:
    """
    Extracts numerical features from the latest quiz attempt.

    Input:
        latest_attempt: MongoDB document from student_performance

    Output:
        dict with numeric features
    """

    detailed = latest_attempt.get("detailed_results", [])

    total_questions = len(detailed)

    correct_count = sum(
        1 for q in detailed if q.get("is_correct") is True
    )

    incorrect_count = total_questions - correct_count

    accuracy = (
        round(correct_count / total_questions, 4)
        if total_questions > 0
        else 0.0
    )

    return {
        "accuracy": accuracy,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "total_questions": total_questions
    }
# print("DEBUG FEATURES:", extract_exam_readiness_features(latest))

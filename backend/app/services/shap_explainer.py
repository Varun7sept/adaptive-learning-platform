"""
SHAP explainability for Exam Readiness (Agent 3)

This module explains the ML readiness model
using SHAP feature attributions.
"""

import numpy as np
import shap

from app.ml.readiness_model import model


# Feature order MUST match training
FEATURE_NAMES = [
    "accuracy",
    "correct_count",
    "incorrect_count",
    "total_questions"
]


# --------------------------------------------------
# SHAP Explainer (initialized once)
# --------------------------------------------------

# Background data (simple & safe)
_background = np.zeros((1, len(FEATURE_NAMES)))

explainer = shap.LinearExplainer(
    model,
    _background
)


# --------------------------------------------------
# Explanation Function
# --------------------------------------------------

def explain_exam_readiness(features: dict) -> list:
    """
    Returns SHAP explanation for exam readiness.

    Output format (JSON-safe):
    [
        {
            "feature": "accuracy",
            "impact": 0.12,
            "direction": "positive"
        }
    ]
    """

    x = np.array([[
        features["accuracy"],
        features["correct_count"],
        features["incorrect_count"],
        features["total_questions"]
    ]])

    shap_values = explainer.shap_values(x)[0]

    explanation = []

    for name, value in zip(FEATURE_NAMES, shap_values):
        explanation.append({
            "feature": name,
            "impact": round(float(value), 4),
            "direction": "positive" if value >= 0 else "negative"
        })

    return explanation

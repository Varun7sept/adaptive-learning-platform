"""
LIME explainability for Exam Readiness (Agent 3)

This module provides LOCAL explanations for a single
student prediction using LIME.
"""

import numpy as np
from lime.lime_tabular import LimeTabularExplainer

from app.ml.readiness_model import model


# --------------------------------------------------
# Feature order MUST match model training
# --------------------------------------------------
FEATURE_NAMES = [
    "accuracy",
    "correct_count",
    "incorrect_count",
    "total_questions"
]


# --------------------------------------------------
# Background data for LIME
# (simple synthetic distribution)
# --------------------------------------------------
TRAINING_DATA = np.array([
    [0.9, 9, 1, 10],
    [0.8, 8, 2, 10],
    [0.7, 7, 3, 10],
    [0.6, 6, 4, 10],
    [0.4, 4, 6, 10],
    [0.2, 2, 8, 10],
])


explainer = LimeTabularExplainer(
    training_data=TRAINING_DATA,
    feature_names=FEATURE_NAMES,
    class_names=["Not Ready", "Ready"],
    mode="classification",
    discretize_continuous=True
)


# --------------------------------------------------
# Explanation Function
# --------------------------------------------------
def explain_exam_readiness_lime(features: dict) -> list:
    """
    Returns LIME explanation for one student.

    Output format (JSON-safe):
    [
        {
            "feature": "correct_count <= 7",
            "weight": 0.41,
            "direction": "positive"
        }
    ]
    """

    instance = np.array([
        features["accuracy"],
        features["correct_count"],
        features["incorrect_count"],
        features["total_questions"]
    ])

    explanation = explainer.explain_instance(
        data_row=instance,
        predict_fn=model.predict_proba,
        num_features=len(FEATURE_NAMES)
    )

    results = []

    for feature_text, weight in explanation.as_list():
        results.append({
            "feature": feature_text,
            "weight": round(float(weight), 4),
            "direction": "positive" if weight >= 0 else "negative"
        })

    return results

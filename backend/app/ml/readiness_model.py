"""
Lightweight ML model for Exam Readiness (Explainability only)

This model is NOT used for final scoring.
It exists to enable SHAP / LIME explanations.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression

# --------------------------------------------------
# TRAIN A VERY SMALL, SAFE MODEL
# --------------------------------------------------

# Features:
# [accuracy, correct_count, incorrect_count, total_questions]

X_train = np.array([
    [0.90, 9, 1, 10],
    [0.80, 8, 2, 10],
    [0.70, 7, 3, 10],
    [0.60, 6, 4, 10],
    [0.40, 4, 6, 10],
    [0.20, 2, 8, 10],
])

# Labels:
# 1 → Exam ready
# 0 → Not ready
y_train = np.array([1, 1, 1, 1, 0, 0])

model = LogisticRegression()
model.fit(X_train, y_train)


# --------------------------------------------------
# PREDICTION FUNCTION
# --------------------------------------------------

def predict_readiness_probability(features: dict) -> float:
    """
    Returns probability of being exam-ready (0–1).
    """

    x = np.array([[
        features["accuracy"],
        features["correct_count"],
        features["incorrect_count"],
        features["total_questions"]
    ]])

    prob = model.predict_proba(x)[0][1]
    return round(float(prob), 4)

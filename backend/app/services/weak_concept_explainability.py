def explain_weak_concept(features):
    """
    Returns explainability signals similar to SHAP/LIME.
    """

    explanations = []

    if features["incorrect_count"] > 0:
        explanations.append({
            "feature": "incorrect_count",
            "impact": features["incorrect_count"],
            "direction": "negative"
        })

    explanations.append({
        "feature": "accuracy",
        "impact": features["accuracy"],
        "direction": "positive" if features["accuracy"] > 0.6 else "negative"
    })

    explanations.append({
        "feature": "total_attempts",
        "impact": features["total_attempts"],
        "direction": "neutral"
    })

    return explanations

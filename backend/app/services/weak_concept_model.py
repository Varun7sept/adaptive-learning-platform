def compute_weakness_score(features):
    """
    Simple interpretable weakness score.
    Higher = weaker topic.
    """

    incorrect = features["incorrect_count"]
    total = features["total_attempts"]
    accuracy = features["accuracy"]

    if total == 0:
        return 0.0

    # Weakness increases with mistakes and low accuracy
    score = (incorrect / total) * (1 - accuracy)

    return round(score, 3)

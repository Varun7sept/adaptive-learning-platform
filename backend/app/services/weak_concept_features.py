from collections import defaultdict

def extract_weak_concept_features(all_questions):
    """
    Builds numeric features per topic.
    Returns dict:
    {
      topic: {
        incorrect_count,
        total_attempts,
        accuracy
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

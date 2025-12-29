class GuessingDetectionService:
    """
    Guessing & Overconfidence Detection Agent
    Uses ONLY latest quiz attempt
    Fully explainable (rule-based)
    """

    # -------------------------------------------
    # 🔹 Normalize difficulty
    # -------------------------------------------
    def difficulty_score(self, difficulty: str) -> float:
        return {
            "easy": 0.3,
            "medium": 0.6,
            "hard": 0.9
        }.get(difficulty, 0.6)

    # -------------------------------------------
    # 🔹 Compute guessing probability
    # -------------------------------------------
    def compute_guessing_score(self, q):
        difficulty = self.difficulty_score(
            q.get("difficulty_level", "medium")
        )
        confidence = q.get("confidence_proxy", 0.5)
        is_correct = q.get("is_correct", False)

        # Guessing = correct but unsure
        guessing_score = (
            0.5 * difficulty +
            0.5 * (1 - confidence)
        ) if is_correct else 0

        return round(guessing_score, 3)

    # -------------------------------------------
    # 🔹 Compute overconfidence score
    # -------------------------------------------
    def compute_overconfidence_score(self, q):
        confidence = q.get("confidence_proxy", 0.5)
        is_correct = q.get("is_correct", True)

        # Overconfidence = confident but wrong
        if is_correct:
            return 0.0

        overconfidence = confidence
        return round(overconfidence, 3)

    # -------------------------------------------
    # 🔹 SHAP-style explanation
    # -------------------------------------------
    def shap_explanation(self, difficulty, confidence):
        return {
            "method": "shap-style (additive)",
            "features": [
                {
                    "feature": "difficulty",
                    "contribution": round(0.5 * difficulty, 3)
                },
                {
                    "feature": "low_confidence",
                    "contribution": round(0.5 * (1 - confidence), 3)
                }
            ]
        }

    # -------------------------------------------
    # 🔹 LIME-style explanation
    # -------------------------------------------
    def lime_explanation(self):
        return {
            "method": "lime-style (counterfactual)",
            "counterfactuals": [
                {
                    "feature": "confidence",
                    "change": "+0.3",
                    "impact": "-0.15 guessing probability",
                    "interpretation": "Higher confidence indicates genuine understanding"
                },
                {
                    "feature": "difficulty",
                    "change": "-1 level",
                    "impact": "-0.20 guessing probability",
                    "interpretation": "Simpler questions reduce random guessing"
                }
            ]
        }

    # -------------------------------------------
    # 🔹 MAIN ENTRY POINT
    # -------------------------------------------
    def analyze(self, detailed_results):
        outputs = []
        total_guessing = 0
        total_overconfidence = 0

        for q in detailed_results:
            guessing = self.compute_guessing_score(q)
            overconfidence = self.compute_overconfidence_score(q)

            difficulty = self.difficulty_score(
                q.get("difficulty_level", "medium")
            )
            confidence = q.get("confidence_proxy", 0.5)

            total_guessing += guessing
            total_overconfidence += overconfidence

            outputs.append({
                "question": q.get("question"),
                "topic": q.get("topic", "Unknown Topic"),
                "is_correct": q.get("is_correct"),
                "guessing_score": guessing,
                "overconfidence_score": overconfidence,
                "shap_explanation": self.shap_explanation(
                    difficulty, confidence
                ),
                "lime_explanation": self.lime_explanation()
            })

        avg_guessing = (
            total_guessing / len(outputs)
            if outputs else 0
        )

        avg_overconfidence = (
            total_overconfidence / len(outputs)
            if outputs else 0
        )

        return {
            "agent": "guessing_detection",
            "average_guessing_score": round(avg_guessing, 3),
            "average_overconfidence_score": round(avg_overconfidence, 3),
            "questions": outputs
        }

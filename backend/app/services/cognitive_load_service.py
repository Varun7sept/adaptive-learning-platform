# from collections import defaultdict

# class CognitiveLoadService:
#     """
#     Cognitive Load Analysis Agent
#     Uses ONLY latest quiz attempt
#     Rule-based + Explainable (SHAP & LIME style)
#     """

#     # --------------------------------------------------
#     # 🔹 Normalize difficulty into numeric load
#     # --------------------------------------------------
#     def difficulty_to_load(self, difficulty: str) -> float:
#         if difficulty == "easy":
#             return 0.2
#         elif difficulty == "medium":
#             return 0.5
#         elif difficulty == "hard":
#             return 0.8
#         return 0.4  # default

#     # --------------------------------------------------
#     # 🔹 Normalize question length into load
#     # --------------------------------------------------
#     def length_to_load(self, length: int) -> float:
#         if length <= 8:
#             return 0.2
#         elif length <= 15:
#             return 0.5
#         return 0.8

#     # --------------------------------------------------
#     # 🔹 Compute cognitive load for ONE question
#     # --------------------------------------------------
#     def compute_question_load(self, q):
#         difficulty_load = self.difficulty_to_load(
#             q.get("difficulty_level", "medium")
#         )
#         length_load = self.length_to_load(
#             q.get("question_length", 10)
#         )
#         incorrect_load = 0 if q.get("is_correct") else 1
#         confidence_load = 1 - q.get("confidence_proxy", 0.5)

#         cognitive_load = (
#             0.35 * difficulty_load +
#             0.25 * length_load +
#             0.25 * incorrect_load +
#             0.15 * confidence_load
#         )

#         return round(cognitive_load, 3), {
#             "difficulty": difficulty_load,
#             "length": length_load,
#             "incorrect": incorrect_load,
#             "confidence": confidence_load
#         }

#     # --------------------------------------------------
#     # 🔹 SHAP-style explanation (additive)
#     # --------------------------------------------------
#     def shap_explanation(self, features):
#         return {
#             "method": "shap-style (additive)",
#             "features": [
#                 {
#                     "feature": "difficulty",
#                     "contribution": round(0.35 * features["difficulty"], 3)
#                 },
#                 {
#                     "feature": "question_length",
#                     "contribution": round(0.25 * features["length"], 3)
#                 },
#                 {
#                     "feature": "incorrectness",
#                     "contribution": round(0.25 * features["incorrect"], 3)
#                 },
#                 {
#                     "feature": "low_confidence",
#                     "contribution": round(0.15 * features["confidence"], 3)
#                 }
#             ]
#         }

#     # --------------------------------------------------
#     # 🔹 LIME-style counterfactual explanation
#     # --------------------------------------------------
#     def lime_explanation(self):
#         return {
#             "method": "lime-style (counterfactual)",
#             "counterfactuals": [
#                 {
#                     "feature": "difficulty",
#                     "change": "-1 level",
#                     "load_change": "-0.35",
#                     "interpretation": "Reducing question difficulty significantly lowers cognitive load"
#                 },
#                 {
#                     "feature": "confidence",
#                     "change": "+0.2",
#                     "load_change": "-0.03",
#                     "interpretation": "Improved confidence slightly reduces cognitive strain"
#                 }
#             ]
#         }

#     # --------------------------------------------------
#     # 🔹 MAIN ENTRY POINT
#     # --------------------------------------------------
#     def analyze(self, detailed_results):
#         question_outputs = []
#         total_load = 0

#         for q in detailed_results:
#             load, features = self.compute_question_load(q)
#             total_load += load

#             question_outputs.append({
#                 "question": q.get("question"),
#                 "topic": q.get("topic", "Unknown Topic"),
#                 "cognitive_load": load,
#                 "shap_explanation": self.shap_explanation(features),
#                 "lime_explanation": self.lime_explanation()
#             })

#         average_load = (
#             total_load / len(question_outputs)
#             if question_outputs else 0
#         )

#         load_level = (
#             "Low" if average_load < 0.4
#             else "Moderate" if average_load < 0.7
#             else "High"
#         )

#         return {
#             "agent": "cognitive_load",
#             "average_cognitive_load": round(average_load, 3),
#             "load_level": load_level,
#             "questions": question_outputs
#         }

from collections import defaultdict


class CognitiveLoadService:
    """
    Cognitive Load Analysis Agent
    Uses ONLY latest quiz attempt
    Rule-based + Explainable (SHAP & LIME style)
    """

    # --------------------------------------------------
    # 🔹 Normalize difficulty into numeric load (SHARP)
    # --------------------------------------------------
    def difficulty_to_load(self, difficulty: str) -> float:
        difficulty_map = {
            "easy": 0.25,
            "medium": 0.55,
            "hard": 0.85
        }
        return difficulty_map.get(difficulty, 0.55)

    # --------------------------------------------------
    # 🔹 Normalize question length into load (CONTINUOUS)
    # --------------------------------------------------
    def length_to_load(self, length: int) -> float:
        """
        Smooth normalization:
        5–25 words → 0.2–1.0
        """
        normalized = (length - 5) / 20
        return max(0.2, min(round(normalized, 3), 1.0))

    # --------------------------------------------------
    # 🔹 Compute cognitive load for ONE question
    # --------------------------------------------------
    def compute_question_load(self, q):
        difficulty_load = self.difficulty_to_load(
            q.get("difficulty_level", "medium")
        )

        length_load = self.length_to_load(
            q.get("question_length", 10)
        )

        # Graded incorrectness penalty
        incorrect_load = 0 if q.get("is_correct") else 0.9

        # Confidence already continuous
        confidence_load = 1 - q.get("confidence_proxy", 0.5)

        cognitive_load = (
            0.35 * difficulty_load +
            0.25 * length_load +
            0.25 * incorrect_load +
            0.15 * confidence_load
        )

        return round(cognitive_load, 3), {
            "difficulty": difficulty_load,
            "length": length_load,
            "incorrect": incorrect_load,
            "confidence": confidence_load
        }

    # --------------------------------------------------
    # 🔹 SHAP-style explanation (additive)
    # --------------------------------------------------
    def shap_explanation(self, features):
        return {
            "method": "shap-style (additive)",
            "features": [
                {
                    "feature": "difficulty",
                    "contribution": round(0.35 * features["difficulty"], 3)
                },
                {
                    "feature": "question_length",
                    "contribution": round(0.25 * features["length"], 3)
                },
                {
                    "feature": "incorrectness",
                    "contribution": round(0.25 * features["incorrect"], 3)
                },
                {
                    "feature": "low_confidence",
                    "contribution": round(0.15 * features["confidence"], 3)
                }
            ]
        }

    # --------------------------------------------------
    # 🔹 LIME-style counterfactual explanation
    # --------------------------------------------------
    def lime_explanation(self):
        return {
            "method": "lime-style (counterfactual)",
            "counterfactuals": [
                {
                    "feature": "difficulty",
                    "change": "-1 level",
                    "load_change": "-0.35",
                    "interpretation": "Reducing question difficulty significantly lowers cognitive load"
                },
                {
                    "feature": "confidence",
                    "change": "+0.2",
                    "load_change": "-0.03",
                    "interpretation": "Improved confidence slightly reduces cognitive strain"
                }
            ]
        }

    # --------------------------------------------------
    # 🔹 MAIN ENTRY POINT
    # --------------------------------------------------
    def analyze(self, detailed_results):
        question_outputs = []
        total_load = 0

        for q in detailed_results:
            load, features = self.compute_question_load(q)
            total_load += load

            question_outputs.append({
                "question": q.get("question"),
                "topic": q.get("topic", "Unknown Topic"),
                "cognitive_load": load,
                "shap_explanation": self.shap_explanation(features),
                "lime_explanation": self.lime_explanation()
            })

        average_load = (
            total_load / len(question_outputs)
            if question_outputs else 0
        )

        load_level = (
            "Low" if average_load < 0.4
            else "Moderate" if average_load < 0.7
            else "High"
        )

        return {
            "agent": "cognitive_load",
            "average_cognitive_load": round(average_load, 3),
            "load_level": load_level,
            "questions": question_outputs
        }

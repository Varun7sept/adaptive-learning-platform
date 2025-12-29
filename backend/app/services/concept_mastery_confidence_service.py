# from collections import defaultdict


# class ConceptMasteryConfidenceService:
#     """
#     Concept Mastery Confidence Agent
#     Uses ONLY latest quiz attempt
#     (No history, no timing assumptions)
#     """

#     def extract_concept_features(self, detailed_results):
#         """
#         Build numeric features per concept
#         """
#         stats = defaultdict(lambda: {
#             "total": 0,
#             "correct": 0
#         })

#         for q in detailed_results:
#             concept = q.get("topic", "Unknown Topic")
#             stats[concept]["total"] += 1

#             if q.get("is_correct"):
#                 stats[concept]["correct"] += 1

#         features = {}
#         for concept, s in stats.items():
#             accuracy = s["correct"] / s["total"] if s["total"] > 0 else 0

#             features[concept] = {
#                 "accuracy": round(accuracy, 3),
#                 "attempts": s["total"],
#                 "correct": s["correct"]
#             }

#         return features

#     def compute_confidence(self, feats):
#         """
#         Interpretable confidence score (0–1)
#         """
#         accuracy = feats["accuracy"]

#         # Penalize very low attempts
#         attempt_factor = min(feats["attempts"] / 3, 1)

#         confidence = (0.8 * accuracy) + (0.2 * attempt_factor)
#         return round(confidence, 3)

#     def analyze(self, detailed_results):
#         """
#         Main entry point
#         """
#         concept_features = self.extract_concept_features(detailed_results)

#         concepts_output = []
#         confidence_sum = 0

#         for concept, feats in concept_features.items():
#             confidence = self.compute_confidence(feats)
#             confidence_sum += confidence

#             mastery_level = (
#                 "Mastered" if confidence >= 0.75
#                 else "Partial" if confidence >= 0.5
#                 else "Not Mastered"
#             )

#             concepts_output.append({
#                 "concept": concept,
#                 "confidence_score": confidence,
#                 "mastery_level": mastery_level,
#                 "metrics": feats
#             })

#         overall_confidence = (
#             confidence_sum / len(concepts_output)
#             if concepts_output else 0
#         )

#         return {
#             "agent": "concept_mastery_confidence",
#             "overall_confidence": round(overall_confidence, 3),
#             "concepts": concepts_output
#         }


from collections import defaultdict


class ConceptMasteryConfidenceService:
    """
    Concept Mastery Confidence Agent
    Uses ONLY latest quiz attempt
    Provides SHAP-style (intrinsic) + LIME-style (contrastive) explainability
    """

    # ------------------------------------------------------------------
    # 🔹 Feature Extraction
    # ------------------------------------------------------------------
    def extract_concept_features(self, detailed_results):
        stats = defaultdict(lambda: {
            "total": 0,
            "correct": 0
        })

        for q in detailed_results:
            concept = q.get("topic", "Unknown Topic")
            stats[concept]["total"] += 1
            if q.get("is_correct"):
                stats[concept]["correct"] += 1

        features = {}
        for concept, s in stats.items():
            accuracy = s["correct"] / s["total"] if s["total"] > 0 else 0
            features[concept] = {
                "accuracy": round(accuracy, 3),
                "attempts": s["total"],
                "correct": s["correct"]
            }

        return features

    # ------------------------------------------------------------------
    # 🔹 Confidence Computation
    # ------------------------------------------------------------------
    def compute_confidence(self, feats):
        accuracy = feats["accuracy"]
        attempt_factor = min(feats["attempts"] / 3, 1)
        confidence = (0.8 * accuracy) + (0.2 * attempt_factor)
        return round(confidence, 3)

    # ------------------------------------------------------------------
    # 🔹 SHAP-style Explanation (Additive Attribution)
    # ------------------------------------------------------------------
    def compute_shap_explanation(self, feats):
        accuracy = feats["accuracy"]
        attempt_factor = min(feats["attempts"] / 3, 1)

        return {
            "method": "shap-style (intrinsic additive)",
            "features": [
                {
                    "feature": "accuracy",
                    "value": accuracy,
                    "weight": 0.8,
                    "contribution": round(0.8 * accuracy, 3),
                    "direction": "positive" if accuracy >= 0.5 else "negative"
                },
                {
                    "feature": "attempts",
                    "value": feats["attempts"],
                    "weight": 0.2,
                    "contribution": round(0.2 * attempt_factor, 3),
                    "direction": "positive"
                }
            ]
        }

    # ------------------------------------------------------------------
    # 🔹 LIME-style Explanation (Contrastive / Local)
    # ------------------------------------------------------------------
    def compute_lime_explanation(self, feats):
        base_conf = self.compute_confidence(feats)

        counterfactuals = []

        # ---- Accuracy perturbation (+0.2 capped at 1.0)
        improved_accuracy = min(feats["accuracy"] + 0.2, 1.0)
        temp_feats_acc = feats.copy()
        temp_feats_acc["accuracy"] = improved_accuracy

        new_conf_acc = self.compute_confidence(temp_feats_acc)
        delta_acc = round(new_conf_acc - base_conf, 3)

        counterfactuals.append({
            "feature": "accuracy",
            "change": "+0.2",
            "confidence_change": f"{'+' if delta_acc >= 0 else ''}{delta_acc}",
            "interpretation": (
                "Improving accuracy would significantly increase mastery confidence"
                if delta_acc > 0 else
                "Accuracy improvement has limited impact at this stage"
            )
        })

        # ---- Attempts perturbation (+1 attempt)
        temp_feats_att = feats.copy()
        temp_feats_att["attempts"] = feats["attempts"] + 1

        new_conf_att = self.compute_confidence(temp_feats_att)
        delta_att = round(new_conf_att - base_conf, 3)

        counterfactuals.append({
            "feature": "attempts",
            "change": "+1",
            "confidence_change": f"{'+' if delta_att >= 0 else ''}{delta_att}",
            "interpretation": (
                "Additional practice marginally improves confidence"
                if delta_att > 0 else
                "More attempts alone may not improve mastery"
            )
        })

        return {
            "method": "lime-style (contrastive local)",
            "base_confidence": base_conf,
            "counterfactuals": counterfactuals
        }

    # ------------------------------------------------------------------
    # 🔹 Main Entry Point
    # ------------------------------------------------------------------
    def analyze(self, detailed_results):
        concept_features = self.extract_concept_features(detailed_results)

        concepts_output = []
        confidence_sum = 0

        for concept, feats in concept_features.items():
            confidence = self.compute_confidence(feats)
            confidence_sum += confidence

            mastery_level = (
                "Mastered" if confidence >= 0.75
                else "Partial" if confidence >= 0.5
                else "Not Mastered"
            )

            concepts_output.append({
                "concept": concept,
                "confidence_score": confidence,
                "mastery_level": mastery_level,
                "metrics": feats,
                "shap_explanation": self.compute_shap_explanation(feats),
                "lime_explanation": self.compute_lime_explanation(feats)
            })

        overall_confidence = (
            confidence_sum / len(concepts_output)
            if concepts_output else 0
        )

        return {
            "agent": "concept_mastery_confidence",
            "overall_confidence": round(overall_confidence, 3),
            "concepts": concepts_output
        }

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from local_model import LocalModelError, admit, predict, train


def records():
    rows = []
    for label, texts in {
        "human": ["昨晚公交晚点，我到家才发现忘带钥匙。", "I missed the bus and called Sam."],
        "ai": ["综上所述，只有持续赋能才能实现长期价值。", "In conclusion, this unlocks lasting value."],
        "mixed": ["我昨天去了河边。综上所述，这体现了长期价值。", "I walked home. In conclusion, value matters."],
    }.items():
        for index, text in enumerate(texts):
            rows.append({
                "id": f"{label}-{index}", "gold_label": label, "text": text,
                "group_id": f"{label}-group-{index}", "language": "zh" if index == 0 else "en",
                "split": "calibration",
            })
    return rows


class LocalModelTests(unittest.TestCase):
    def test_train_is_reproducible_and_predicts_or_abstains(self):
        model = train(records(), max_features=100)
        self.assertEqual(model["model_id"], train(records(), max_features=100)["model_id"])
        result = predict(model, "综上所述，长期价值需要持续赋能。", abstain_margin=0)
        self.assertIn(result["predicted_label"], {"human", "ai", "mixed"})
        self.assertTrue(result["not_calibrated_probability"])

    def test_training_rejects_blind_labels(self):
        rows = records()
        rows[0]["split"] = "blind"
        with self.assertRaises(LocalModelError):
            train(rows)

    def test_artifact_tampering_is_rejected(self):
        model = train(records(), max_features=100)
        model["alpha"] = 2
        with self.assertRaises(LocalModelError):
            predict(model, "test")

    def test_admission_requires_matching_locked_passing_evaluation(self):
        model = train(records(), max_features=100)
        checks = {name: {"passed": True} for name in (
            "human_sample_count", "ai_assisted_sample_count", "fpr", "recall"
        )}
        evaluation = {
            "schema_version": "1.0",
            "selected_split": "blind",
            "blind_test": {"locked": True, "manifest_sha256": "a" * 64, "record_count": 300},
            "decision_thresholds": {"model_id": model["model_id"]},
            "release_assessment": {
                "release_eligible": True, "status": "pass", "language_checks": {"zh": checks},
                "checks": {name: {"passed": True} for name in (
                    "locked_blind_only", "ai_assisted_fpr", "ai_assisted_precision",
                    "ai_assisted_recall", "abstention_rate", "mixed_sentence_f1",
                    "mixed_sentence_coverage",
                )},
            },
        }
        admit(model, evaluation, "zh")
        failed = copy.deepcopy(evaluation)
        failed["release_assessment"]["status"] = "fail"
        with self.assertRaises(LocalModelError):
            admit(model, failed, "zh")

    def test_minimal_self_declared_pass_is_rejected(self):
        model = train(records(), max_features=100)
        forged = {
            "schema_version": "1.0",
            "selected_split": "blind",
            "blind_test": {"locked": True, "manifest_sha256": "b" * 64, "record_count": 1},
            "decision_thresholds": {"model_id": model["model_id"]},
            "release_assessment": {
                "release_eligible": True,
                "status": "pass",
                "checks": {},
                "language_checks": {"zh": {}},
            },
        }
        with self.assertRaises(LocalModelError):
            admit(model, forged, "zh")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from evaluate_benchmark import EvaluationError, evaluate, read_jsonl, validate_manifest


def sample(
    sample_id: str,
    label: str,
    *,
    split: str = "blind",
    group_id: str | None = None,
    language: str = "zh",
) -> dict:
    value = {
        "id": sample_id,
        "gold_label": label,
        "language": language,
        "platform": "weibo" if language == "zh" else "reddit",
        "genre": "personal",
        "length_bucket": "full",
        "model_family": "none" if label == "human" else "model-a",
        "editorial_state": "unedited",
        "group_id": group_id or f"group-{sample_id}",
        "split": split,
        "locked_blind": split == "blind",
    }
    if label == "mixed":
        value["sentence_labels"] = ["human", "ai", "ai"]
    return value


class ManifestValidationTests(unittest.TestCase):
    def test_jsonl_reader_reports_line_number(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.jsonl"
            path.write_text('{"id":"ok"}\nnot-json\n', encoding="utf-8")
            with self.assertRaisesRegex(EvaluationError, "manifest.jsonl:2"):
                read_jsonl(path)

    def test_accepts_three_classes_and_locked_blind_records(self):
        records = [sample("h", "human"), sample("a", "ai"), sample("m", "mixed")]
        self.assertEqual(validate_manifest(records), records)

    def test_rejects_group_leakage_across_splits(self):
        records = [
            sample("cal", "human", split="calibration", group_id="shared"),
            sample("blind", "ai", group_id="shared"),
        ]
        with self.assertRaisesRegex(EvaluationError, "group_id leakage"):
            validate_manifest(records)

    def test_rejects_unlocked_blind_and_invalid_mixed_spans(self):
        unlocked = sample("a", "ai")
        unlocked["locked_blind"] = False
        with self.assertRaisesRegex(EvaluationError, "locked_blind=true"):
            validate_manifest([unlocked])

        invalid_mixed = sample("m", "mixed")
        invalid_mixed["sentence_labels"] = ["ai", "ai"]
        with self.assertRaisesRegex(EvaluationError, "both human and ai"):
            validate_manifest([invalid_mixed])


class EvaluationTests(unittest.TestCase):
    def test_reports_confusion_slices_abstention_and_sentence_metrics(self):
        manifest = [
            sample("h1", "human", language="zh"),
            sample("h2", "human", language="en"),
            sample("a1", "ai", language="zh"),
            sample("a2", "ai", language="en"),
            sample("m1", "mixed", language="zh"),
        ]
        predictions = [
            {"id": "h1", "predicted_label": "human"},
            {"id": "h2", "predicted_label": "ai"},
            {"id": "a1", "predicted_label": "ai"},
            {"id": "a2", "predicted_label": "abstain"},
            {
                "id": "m1",
                "predicted_label": "mixed",
                "sentence_predictions": ["human", "ai", "abstain"],
            },
        ]
        report = evaluate(manifest, predictions)

        document = report["document_metrics"]
        self.assertEqual(document["confusion_matrix"]["human"]["ai"], 1)
        self.assertEqual(document["confusion_matrix"]["ai"]["abstain"], 1)
        self.assertAlmostEqual(document["ai_assisted"]["fpr"], 0.5)
        self.assertAlmostEqual(document["ai_assisted"]["precision"], 2 / 3)
        self.assertAlmostEqual(document["ai_assisted"]["recall"], 2 / 3)
        self.assertAlmostEqual(document["abstention_rate"], 0.2)
        self.assertEqual(set(report["slices"]), {
            "language", "platform", "genre", "length", "model_family", "editorial_state"
        })
        self.assertEqual(report["mixed_sentence_metrics"]["tp"], 1)
        self.assertEqual(report["mixed_sentence_metrics"]["fn"], 1)
        self.assertAlmostEqual(report["mixed_sentence_metrics"]["f1"], 2 / 3)
        self.assertTrue(report["blind_test"]["locked"])
        self.assertEqual(len(report["blind_test"]["manifest_sha256"]), 64)
        self.assertIn("prediction_contract", report["decision_thresholds"])

    def test_calibration_split_is_not_release_eligible_and_gates_are_emitted(self):
        manifest = [
            sample("h", "human", split="calibration"),
            sample("a", "ai", split="calibration"),
            sample("m", "mixed", split="calibration"),
        ]
        predictions = [
            {"id": "h", "predicted_label": "human"},
            {"id": "a", "predicted_label": "ai"},
            {
                "id": "m",
                "predicted_label": "mixed",
                "sentence_predictions": ["human", "ai", "ai"],
            },
        ]
        report = evaluate(
            manifest,
            predictions,
            split="calibration",
            decision_thresholds={"ai_like_points": 8},
            release_gates={
                "min_human_per_language": 1,
                "min_ai_assisted_per_language": 1,
            },
        )
        self.assertFalse(report["release_assessment"]["release_eligible"])
        self.assertEqual(report["release_assessment"]["status"], "fail")
        self.assertEqual(report["decision_thresholds"]["ai_like_points"], 8)
        self.assertIn("max_ai_assisted_fpr", report["release_gates"])

    def test_sentence_prediction_length_must_match(self):
        manifest = [sample("m", "mixed")]
        predictions = [
            {
                "id": "m",
                "predicted_label": "mixed",
                "sentence_predictions": ["human", "ai"],
            }
        ]
        with self.assertRaisesRegex(EvaluationError, "length does not match"):
            evaluate(manifest, predictions)


if __name__ == "__main__":
    unittest.main()

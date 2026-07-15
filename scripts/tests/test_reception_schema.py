from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(TEST_DIR))

from helpers import make_case, make_reception
from reception_schema import ReceptionValidationError, validate_reception


class ReceptionSchemaTests(unittest.TestCase):
    def test_valid_reception_is_ordered(self):
        reception = make_reception()
        reception["reader_views"].reverse()
        result = validate_reception(reception, make_case())
        self.assertEqual(
            [view["persona"] for view in result["reader_views"]],
            ["supporter", "neutral", "skeptic"],
        )
        self.assertEqual(result["validation_profile"], "grounded_reception_v1")
        self.assertEqual(
            result["reader_views"][0]["positive_signal_evidence"][0]["locator"],
            "content.text",
        )
        self.assertEqual(result["cross_reader_evidence"][0]["locator"], "content.text")

    def test_missing_persona_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][2]["persona"] = "neutral"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_ungrounded_excerpt_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][1]["friction_points"][0]["excerpt"] = "not in source"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_rewrite_field_is_rejected(self):
        reception = make_reception()
        reception["rewrite"] = "A better replacement post"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_nested_rewrite_variant_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][0]["full_rewrite"] = "replacement"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_detector_evasion_field_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][0]["bypass_strategy"] = "Use shorter sentences."
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_long_excerpt_is_rejected(self):
        case = make_case("a" * 301)
        reception = make_reception()
        reception["reader_views"][1]["friction_points"][0]["excerpt"] = "a" * 301
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, case)

    def test_unknown_dimension_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][1]["friction_points"][0]["dimension"] = "political_profile"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_structured_positive_and_cross_reader_evidence_is_indexed(self):
        reception = make_reception()
        reception["reader_views"][0]["positive_signals"] = [
            {"statement": "The wording is concrete.", "excerpt": "everyone knows", "reason": "The wording is directly visible."}
        ]
        reception["cross_reader_patterns"] = [
            {
                "statement": "All stances can inspect the same source text.",
                "evidence": {"kind": "case_text", "locator": "content.text"},
                "reason": "The same source text is available to both stances.",
                "personas": ["neutral", "skeptic"],
            }
        ]
        result = validate_reception(reception, make_case())
        self.assertEqual(result["reader_views"][0]["positive_signals"], ["The wording is concrete."])
        self.assertEqual(
            result["reader_views"][0]["positive_signal_evidence"][0]["excerpt"],
            "everyone knows",
        )
        self.assertEqual(result["cross_reader_evidence"][0]["kind"], "case_text")

    def test_ungrounded_structured_conclusion_is_rejected(self):
        reception = make_reception()
        reception["cross_reader_patterns"] = [
            {"statement": "A shared claim.", "excerpt": "not in the case", "reason": "Shared by two stances.", "personas": ["neutral", "skeptic"]}
        ]
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_protected_attribute_inference_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][0]["likely_reaction"] = (
            "The wording suggests the author is likely a particular race."
        )
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

        direct = make_reception()
        direct["reader_views"][0]["likely_reaction"] = "The author's gender is female."
        with self.assertRaises(ReceptionValidationError):
            validate_reception(direct, make_case())

    def test_psychological_diagnosis_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][1]["friction_points"][0]["reason"] = (
            "This proves the author is a narcissist."
        )
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_rewrite_and_detector_evasion_text_are_rejected(self):
        rewrite = make_reception()
        rewrite["reader_views"][0]["positive_signals"] = ["Rewrite this as a better version."]
        with self.assertRaises(ReceptionValidationError):
            validate_reception(rewrite, make_case())

        evasion = make_reception()
        evasion["cross_reader_patterns"] = ["Humanize the text to bypass an AI detector."]
        with self.assertRaises(ReceptionValidationError):
            validate_reception(evasion, make_case())

    def test_unknown_method_version_is_rejected(self):
        reception = make_reception()
        reception["method"] = "stance_personas"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_unknown_nested_content_cannot_hide_rewrite_or_evasion(self):
        reception = make_reception()
        reception["notes"] = {"advice": "Produce substitute copy that avoids AI screening."}
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_specific_religious_and_political_inference_is_rejected(self):
        for statement in (
            "The author is Muslim and a Democratic voter.",
            "The author is Catholic and a MAGA supporter.",
            "The author is Black and elderly.",
            "作者是天主教徒，也是民进党支持者。",
        ):
            reception = make_reception()
            reception["reader_views"][0]["likely_reaction"] = statement
            with self.subTest(statement=statement), self.assertRaises(ReceptionValidationError):
                validate_reception(reception, make_case())

    def test_semantic_detector_evasion_advice_is_rejected(self):
        reception = make_reception()
        reception["reader_views"][0]["likely_reaction"] = (
            "Vary sentence length; personal anecdotes would lower automated screening risk."
        )
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_cross_reader_pattern_requires_two_named_stances(self):
        reception = make_reception()
        reception["cross_reader_patterns"][0]["personas"] = ["neutral"]
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())

    def test_high_aversion_requires_multiple_grounded_points(self):
        reception = make_reception()
        reception["reader_views"][1]["aversion_risk"] = "high"
        with self.assertRaises(ReceptionValidationError):
            validate_reception(reception, make_case())


if __name__ == "__main__":
    unittest.main()

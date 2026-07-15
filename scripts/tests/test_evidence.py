from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(TEST_DIR))

from evidence import assess_origin, assess_practical, text_sufficiency
from helpers import make_case


class EvidencePolicyTests(unittest.TestCase):
    def test_english_boundary(self):
        self.assertFalse(text_sufficiency("a" * 999, "en")["sufficient"])
        self.assertTrue(text_sufficiency("a" * 1000, "en")["sufficient"])

    def test_chinese_boundary(self):
        self.assertFalse(text_sufficiency("人" * 499, "zh")["sufficient"])
        self.assertTrue(text_sufficiency("人" * 500, "zh")["sufficient"])

    def test_short_english_external_signal_is_not_strong(self):
        case = make_case("a" * 999, "en")
        result = assess_origin(
            case,
            [
                {
                    "provider": "future-detector",
                    "modality": "text",
                    "scope": "text",
                    "direction": "positive",
                    "strength": "strong",
                }
            ],
            [],
        )
        self.assertEqual(result["verdict"], "insufficient_evidence")

    def test_long_english_external_signal_can_be_strong(self):
        case = make_case("a" * 1000, "en")
        result = assess_origin(
            case,
            [
                {
                    "provider": "future-detector",
                    "modality": "text",
                    "scope": "text",
                    "direction": "positive",
                    "strength": "strong",
                }
            ],
            [],
        )
        self.assertEqual(result["verdict"], "strong_ai_indicators")

    def test_hive_threshold(self):
        case = make_case()
        case["content"]["images"] = [{"id": "image-1", "path": "C:\\image.jpg"}]
        low = assess_origin(
            case,
            [
                {
                    "provider": "hive",
                    "modality": "image",
                    "scope": "image-1",
                    "ai_generated_score": 0.899,
                    "not_ai_generated_score": 0.101,
                }
            ],
            [],
        )
        high = assess_origin(
            case,
            [
                {
                    "provider": "hive",
                    "modality": "image",
                    "scope": "image-1",
                    "ai_generated_score": 0.9,
                    "not_ai_generated_score": 0.1,
                }
            ],
            [],
        )
        self.assertEqual(low["verdict"], "insufficient_evidence")
        self.assertEqual(high["verdict"], "strong_ai_indicators")

    def test_verified_c2pa_wins(self):
        case = make_case()
        case["content"]["images"] = [{"id": "image-1", "path": "C:\\image.jpg"}]
        result = assess_origin(
            case,
            [],
            [
                {
                    "scope": "image-1",
                    "result": {
                        "status": "verified",
                        "valid": True,
                        "ai_generated": True,
                    },
                }
            ],
        )
        self.assertEqual(result["verdict"], "verified_ai_provenance")
        self.assertEqual(result["confidence"], "high")

    def test_negated_disclosure_is_not_verified(self):
        case = make_case()
        case["observations"] = [
            {
                "type": "author_disclosure",
                "value": "This was not generated with AI",
                "source_url": "https://example.com/post",
            }
        ]
        result = assess_origin(case, [], [])
        self.assertEqual(result["verdict"], "insufficient_evidence")

    def test_explicit_denial_wrapping_positive_clause_is_not_verified(self):
        for value in (
            "I deny that I generated this post with AI.",
            "It is false that I generated this post with AI.",
            "我否认我使用AI生成了这篇帖子",
        ):
            case = make_case()
            case["observations"] = [{
                "type": "author_disclosure", "value": value,
                "assertion": "confirmed", "scope": "post", "source_url": None,
            }]
            with self.subTest(value=value):
                self.assertEqual(assess_origin(case, [], [])["verdict"], "insufficient_evidence")

    def test_same_scope_conflict(self):
        case = make_case("a" * 1000, "en")
        result = assess_origin(
            case,
            [
                {
                    "provider": "future-detector-a",
                    "modality": "text",
                    "scope": "text",
                    "direction": "positive",
                    "strength": "strong",
                },
                {
                    "provider": "future-detector",
                    "modality": "text",
                    "scope": "text",
                    "direction": "negative",
                    "strength": "strong",
                },
            ],
            [],
        )
        self.assertEqual(result["verdict"], "conflicting_evidence")

    def test_dense_style_without_local_convergence_is_descriptive_only(self):
        case = make_case("人" * 500, "zh")
        origin = assess_origin(case, [], [])
        practical = assess_practical(
            origin,
            {
                "assessment": "strong_ai_style_patterns",
                "pattern_count": 8,
                "occurrence_count": 24,
                "genre_confounds": [],
                "counter_signals": [],
            },
        )
        self.assertEqual(practical["label"], "style_patterns_only")
        self.assertEqual(practical["confidence"], "descriptive_only")

    def test_local_pattern_convergence_does_not_claim_authorship(self):
        case = make_case("人" * 500, "zh")
        origin = assess_origin(case, [], [])
        practical = assess_practical(
            origin,
            {
                "assessment": "strong_ai_style_patterns",
                "pattern_count": 8,
                "occurrence_count": 24,
                "genre_confounds": [],
                "counter_signals": [],
            },
            {
                "document_classification": "strong_pattern_match",
                "decision": {
                    "indicator_points": 13,
                    "converging_feature_families": [
                        "template_and_style",
                        "sentence_level_concentration",
                        "structural_regularity",
                    ],
                },
            },
        )
        self.assertEqual(practical["label"], "strong_ai_like_drafting_signals")
        self.assertEqual(practical["confidence"], "descriptive_only")

    def test_short_dense_style_is_only_possible(self):
        case = make_case("人" * 499, "zh")
        origin = assess_origin(case, [], [])
        practical = assess_practical(
            origin,
            {
                "assessment": "strong_ai_style_patterns",
                "pattern_count": 8,
                "occurrence_count": 24,
                "genre_confounds": [],
                "counter_signals": [],
            },
        )
        self.assertEqual(practical["label"], "style_patterns_only")
        self.assertEqual(practical["confidence"], "descriptive_only")

    def test_short_local_text_stays_unclear_even_with_dense_style(self):
        case = make_case("人" * 199, "zh")
        origin = assess_origin(case, [], [])
        practical = assess_practical(
            origin,
            {
                "assessment": "strong_ai_style_patterns",
                "pattern_count": 8,
                "occurrence_count": 24,
                "genre_confounds": [],
                "counter_signals": [],
            },
            {"document_classification": "insufficient_evidence"},
        )
        self.assertEqual(practical["label"], "no_conclusion")
        self.assertIn("insufficient", practical["basis"][0].lower())

    def test_meta_claim_is_not_an_author_disclosure(self):
        case = make_case()
        case["observations"] = [{
            "type": "author_disclosure",
            "value": "The claim that this was AI-generated is false.",
            "source_url": "https://example.com/post",
        }]
        self.assertEqual(assess_origin(case, [], [])["verdict"], "insufficient_evidence")

    def test_discussion_of_ai_label_is_not_verified(self):
        case = make_case()
        case["observations"] = [{
            "type": "author_disclosure",
            "value": "我们今天讨论 AI 生成内容的标签问题。",
            "source_url": "https://example.com/post",
        }]
        self.assertEqual(assess_origin(case, [], [])["verdict"], "insufficient_evidence")

    def test_explicit_author_disclosure_is_scoped(self):
        case = make_case()
        case["content"]["images"] = [{"id": "image-1", "path": "C:\\image.png"}]
        case["observations"] = [{
            "type": "author_disclosure",
            "value": "我使用 AI 生成了这张图片",
            "assertion": "confirmed",
            "scope": "image-1",
            "source_url": "https://example.com/post",
        }]
        result = assess_origin(case, [], [])
        self.assertEqual(result["verdict"], "verified_ai_provenance")
        self.assertEqual(result["verified_scopes"], ["image-1"])

    def test_confirmed_flag_cannot_turn_unrelated_text_into_disclosure(self):
        case = make_case()
        case["observations"] = [{
            "type": "author_disclosure", "value": "今天拍了这张照片",
            "assertion": "confirmed", "scope": "image-1", "source_url": None,
        }]
        self.assertEqual(assess_origin(case, [], [])["verdict"], "insufficient_evidence")

    def test_unknown_disclosure_scope_is_not_promoted(self):
        case = make_case()
        case["observations"] = [{
            "type": "author_disclosure", "value": "I created this image using AI",
            "scope": "image-ghost", "source_url": None,
        }]
        result = assess_origin(case, [], [])
        self.assertEqual(result["verdict"], "insufficient_evidence")
        self.assertEqual(result["evidence"][0]["type"], "invalid_disclosure_scope")

    def test_quoted_author_disclosure_is_not_promoted(self):
        case = make_case()
        case["observations"] = [{
            "type": "author_disclosure",
            "value": "The caption reads: ‘I created this image using AI.’",
            "assertion": "confirmed", "scope": "post", "source_url": None,
        }]
        self.assertEqual(assess_origin(case, [], [])["verdict"], "insufficient_evidence")

        chinese = make_case()
        chinese["observations"] = [{
            "type": "author_disclosure",
            "value": "帖子里出现了“我使用AI生成了这张图片”这句话，但作者否认。",
            "assertion": "confirmed", "scope": "post", "source_url": None,
        }]
        self.assertEqual(assess_origin(chinese, [], [])["verdict"], "insufficient_evidence")

    def test_asset_findings_never_retain_local_paths(self):
        case = make_case()
        case["content"]["images"] = [{"id": "image-1", "path": "C:\\private\\asset.png", "sha256": "a" * 64}]
        finding = assess_origin(case, [], [])["asset_findings"][0]
        self.assertNotIn("path", finding)
        self.assertEqual(finding["sha256"], "a" * 64)


if __name__ == "__main__":
    unittest.main()

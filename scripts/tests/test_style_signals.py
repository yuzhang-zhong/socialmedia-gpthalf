from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from style_signals import analyze_style_patterns


AI_STYLE_SAMPLE = """在整理历史资料时，我注意到一个长期被史学界忽视，却又无法回避的事实。
起初我没有在意，但当我进一步审视时，这种缺失变得不合理。为什么不写瑶？为什么
没有喊快上身？为什么不记录鹿灵？我带着这些疑问，查阅了大量的资料，原来，瑶是
2019 年上线的英雄。时间上的错位从根源上阻断了这种可能。天！原来当时还没有上线！
史料记载，当时没有峡谷，更没有皮肤。即便强行植入，也会破坏历史真实性。"""


class StyleSignalsTests(unittest.TestCase):
    def test_dense_chinese_sample_is_flagged(self):
        result = analyze_style_patterns(AI_STYLE_SAMPLE, "zh")
        self.assertEqual(result["assessment"], "strong_ai_style_patterns")
        ids = {item["pattern_id"] for item in result["matches"]}
        self.assertIn("inflated_significance", ids)
        self.assertIn("vague_attribution", ids)
        self.assertIn("rhetorical_question_chain", ids)
        self.assertIn("overexplained_reveal", ids)

    def test_plain_factual_chinese_is_low(self):
        result = analyze_style_patterns(
            "会议改到周四下午三点，地点还是二楼会议室。小王负责记录。",
            "zh",
        )
        self.assertEqual(result["assessment"], "few_ai_style_patterns")
        self.assertEqual(result["ai_assistance_inference"], "not_supported_by_style_alone")

    def test_non_chinese_is_not_applicable(self):
        result = analyze_style_patterns("This is a short factual note.", "en")
        self.assertEqual(result["assessment"], "not_applicable")

    def test_ordinary_commas_are_not_list_stacking(self):
        result = analyze_style_patterns(
            "我上午去了图书馆，借了两本书，下午回家做饭。天气有点冷，但路上人不少。",
            "zh",
        )
        ids = {item["pattern_id"] for item in result["matches"]}
        self.assertNotIn("enumeration_stacking", ids)

    def test_genre_confounds_are_reported(self):
        result = analyze_style_patterns(
            AI_STYLE_SAMPLE + " #王者荣耀 #世界历史",
            "zh",
            platform="unknown",
            declared_purpose="discuss",
        )
        self.assertGreaterEqual(len(result["genre_confounds"]), 2)

    def test_positive_and_assertive_clusters_are_explainable(self):
        result = analyze_style_patterns(
            "我一定相信这绝对是最温暖、最甜蜜、最美好的结果，毫无疑问大家都会喜欢。",
            "zh",
        )
        ids = {item["pattern_id"] for item in result["matches"]}
        self.assertIn("positive_affect_saturation", ids)
        self.assertIn("assertive_language_cluster", ids)


if __name__ == "__main__":
    unittest.main()

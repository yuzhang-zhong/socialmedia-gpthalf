from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from local_text_detector import analyze_local_text
from style_signals import analyze_style_patterns


MARCO_YAO = """为什么马可·波罗的游记里从未提及瑶？
在整理《马可·波罗游记》的历史资料时，我注意到一个长期被史学界忽视，却又无法回避的事实：在马可·波罗对东方世界详尽的描述中，他从未提及过瑶。起初我并没有在意这件事，但当我进一步审视他从威尼斯到元大都的漫长旅程时，这种缺失开始变得不太合理。
马可·波罗写过忽必烈、写过香料、写过遍地的黄金，为什么不写瑶？为什么他在穿越帕米尔高原遭遇暴风雪和强盗时，没有喊一声“快上身”来刷个真实伤害护盾？为什么他只描写元大都的壮丽宫殿，却不记录一下那个能变身鹿灵、在战场上飞来飞去的辅助？明明东方世界的奇珍异兽足以容纳任何神话，为什么“附身、刷盾、独立判定、遇见神鹿”这些概念，从未出现在他的行囊里？
我带着这些疑问，查阅了大量的资料，原来，瑶是腾讯游戏《王者荣耀》于 2019 年 4 月 16 日上线的辅助型英雄。而马可·波罗生活的年代，是公元 1254 年至 1324 年，时间上的错位，从根源上阻断了他在游记中提及瑶的可能。
天！原来瑶在马可·波罗的时代还没有上线！史料记载，元朝人都是骑马射箭的普通人类，没有“王者峡谷”，更没有《时之祈愿》《山海·碧波行》这些传说皮肤。他写“纸币”，是因为元朝确实流通纸币；他写“燃烧的石头（煤炭）”，是因为他真的看见了煤。而瑶相关的概念，如“野王挂件”、“双排”、“干扰”、“控制抵消”等，与 13 世纪的丝绸之路生活形态完全脱节，即便强行植入，也会破坏游记的历史真实性。
#王者荣耀 #世界历史 #马可波罗 #马瑶 #王者荣耀瑶#丝绸之路 #瑶妹"""

GENERIC_AI_MARKETING = """在当今快速变化的数字时代，个人品牌建设已不再是少数人的选择，而是每个人都必须面对的重要课题。很多人认为，持续发布内容就等于建立品牌，但事实并非如此。首先，真正有影响力的个人品牌，需要清晰的价值定位。其次，稳定的内容输出能够帮助受众形成认知。此外，与用户保持真诚互动，也是建立长期信任的关键。值得注意的是，个人品牌并不是一夜之间形成的。它不仅需要时间积累，更需要不断审视自身优势，并根据环境变化及时调整策略。综上所述，个人品牌的本质，是在持续表达中建立可信度。只有把专业能力、真实经历和用户需求结合起来，才能在不断变化的竞争格局中脱颖而出，并最终实现长期价值。
在远程协作逐渐常态化的今天，团队文化已经成为组织持续发展的关键基础。很多管理者以为，增加会议数量就能解决沟通问题，但真正有效的协作远不止于此。首先，清晰的目标能够减少成员之间的理解偏差。其次，透明的信息流动可以让每个人及时掌握进展。此外，稳定的反馈机制有助于问题尽早暴露。值得注意的是，信任并不会因为工具齐全而自动形成。它不仅需要明确的责任边界，更需要管理者在日常决策中保持一致。综上所述，远程团队的竞争力来自制度与关系的共同建设。只有把目标、流程、反馈和信任结合起来，才能形成可持续的协作能力，并最终实现长期价值。这类表达看似全面，却仍需要具体案例和可核验的数据支撑。"""


class LocalTextDetectorTests(unittest.TestCase):
    def test_marco_yao_converges_on_high_ai_like_signal(self):
        style = analyze_style_patterns(MARCO_YAO, "zh")
        result = analyze_local_text(MARCO_YAO, "zh", style_assessment=style)
        self.assertEqual(result["document_classification"], "strong_pattern_match")
        self.assertEqual(result["signal_strength"], "descriptive_only")
        self.assertGreaterEqual(result["decision"]["indicator_points"], 8)
        self.assertGreaterEqual(
            len(result["decision"]["converging_feature_families"]), 3
        )
        self.assertGreaterEqual(
            result["statistical_features"]["pattern_match_sentence_share"], 0.45
        )
        self.assertTrue(
            any(
                item["classification"] == "pattern_match"
                and item["cues"]
                and item["excerpt"] in MARCO_YAO
                for item in result["sentence_findings"]
            )
        )

    def test_unrelated_formulaic_sample_is_detected_without_target_phrases(self):
        style = analyze_style_patterns(GENERIC_AI_MARKETING, "zh")
        result = analyze_local_text(
            GENERIC_AI_MARKETING, "zh", style_assessment=style
        )
        self.assertGreaterEqual(result["coverage"]["han_characters"], 500)
        self.assertEqual(result["document_classification"], "strong_pattern_match")
        self.assertGreaterEqual(
            result["statistical_features"]["pattern_match_sentence_share"], 0.45
        )
        self.assertIn(
            "sentence_level_concentration",
            result["decision"]["converging_feature_families"],
        )

    def test_long_plain_personal_text_is_unresolved(self):
        paragraph = (
            "周六我六点醒了，窗外还在下雨。我把昨晚剩下的面包烤焦了一边，"
            "只好刮掉黑的地方。九点坐公交去城南，司机在第三站等了一位跑来的老人。"
            "下午修书架时少了一颗螺丝，我翻了两个抽屉才在旧信封里找到。"
            "回家路上雨停了，鞋还是湿的。"
        )
        text = paragraph + paragraph.replace("周六", "周日").replace("城南", "河西") + paragraph.replace("雨", "雪")
        style = analyze_style_patterns(text, "zh")
        result = analyze_local_text(text, "zh", style_assessment=style)
        self.assertEqual(result["document_classification"], "unresolved")
        self.assertNotEqual(result["signal_strength"], "high")

    def test_short_dense_text_cannot_receive_strong_label(self):
        text = "为什么不记录？为什么没有提及？为什么不能解释？我查阅了大量资料，原来答案从根源上很简单。"
        style = analyze_style_patterns(text, "zh")
        result = analyze_local_text(text, "zh", style_assessment=style)
        self.assertEqual(result["coverage"]["level"], "insufficient")
        self.assertEqual(result["document_classification"], "insufficient_evidence")
        self.assertEqual(result["signal_strength"], "unknown")

    def test_mixed_document_keeps_mixed_class(self):
        human = (
            "昨晚十点我从便利店出来，雨伞被风翻了。我在公交站等了十九分钟，"
            "旁边小孩一直数经过的蓝色汽车。到家后我才发现豆腐忘在收银台，"
            "只好用冰箱里半根黄瓜煮面。第二天老板把豆腐留在柜台下面，还贴了我的姓。"
        )
        ai_block = (
            "在进一步审视这件事时，一个长期被忽视却无法回避的事实逐渐浮现。"
            "为什么没有人讨论它？为什么没有人记录它？为什么没有人解释它？"
            "我带着这些疑问查阅了大量资料，原来时间上的错位从根源上阻断了这种可能。"
        )
        text = human * 7 + ai_block
        style = analyze_style_patterns(text, "zh")
        result = analyze_local_text(text, "zh", style_assessment=style)
        self.assertEqual(result["coverage"]["level"], "full")
        self.assertEqual(result["document_classification"], "localized_pattern_match")

    def test_english_is_explicitly_unsupported(self):
        result = analyze_local_text("This is a formulaic sentence. " * 100, "en")
        self.assertEqual(result["document_classification"], "unsupported_language")
        self.assertEqual(result["coverage"]["level"], "unsupported")


if __name__ == "__main__":
    unittest.main()

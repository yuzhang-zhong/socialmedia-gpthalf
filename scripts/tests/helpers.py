from __future__ import annotations


def make_case(text: str = "everyone knows this matters", language: str = "en") -> dict:
    return {
        "schema_version": "1.0",
        "source": {
            "url": "https://example.com/post",
            "platform": "web",
            "captured_at": "2026-07-15T12:00:00Z",
            "public": True,
        },
        "content": {"text": text, "language": language, "images": []},
        "observations": [],
        "declared_purpose": "inform",
    }


def make_reception() -> dict:
    return {
        "method": "stance_personas_v1",
        "audience_assumptions": ["General public readers"],
        "reader_views": [
            {
                "persona": "supporter",
                "likely_reaction": "Likely to accept the message.",
                "aversion_risk": "low",
                "friction_points": [],
                "positive_signals": [{
                    "statement": "The post is concise.",
                    "excerpt": "everyone knows this matters",
                    "reason": "The complete message is visible in one short sentence.",
                }],
                "uncertainty": "Follower relationship is unknown.",
            },
            {
                "persona": "neutral",
                "likely_reaction": "May want a source.",
                "aversion_risk": "medium",
                "friction_points": [
                    {
                        "dimension": "credibility_friction",
                        "excerpt": "everyone knows",
                        "reason": "The broad claim gives no boundary or source.",
                    }
                ],
                "positive_signals": [],
                "uncertainty": "Comment context is unavailable.",
            },
            {
                "persona": "skeptic",
                "likely_reaction": "May question the claim.",
                "aversion_risk": "medium",
                "friction_points": [],
                "positive_signals": [],
                "uncertainty": "Author intent is unknown.",
            },
        ],
        "cross_reader_patterns": [{
            "statement": "The broad assertion creates shared credibility friction.",
            "excerpt": "everyone knows",
            "reason": "Neutral and skeptical readers may both want a boundary or source.",
            "personas": ["neutral", "skeptic"],
        }],
        "uncertainties": ["These reactions are inferred, not observed."],
    }

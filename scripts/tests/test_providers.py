from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from providers import ProviderError, analyze_image_hive


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.responses.pop(0)


class ProviderTests(unittest.TestCase):
    def test_hive_normalizes_response(self):
        payload = {
            "status": [
                {
                    "response": {
                        "input": {"model_version": 7},
                        "output": [
                            {
                                "classes": [
                                    {"class": "ai_generated", "score": 0.95},
                                    {"class": "not_ai_generated", "score": 0.05},
                                    {"class": "flux", "score": 0.8},
                                    {"class": "deepfake", "score": 0.1},
                                ]
                            }
                        ],
                    }
                }
            ]
        }
        session = FakeSession([FakeResponse(200, payload)])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.jpg"
            path.write_bytes(b"not-a-real-image")
            result = analyze_image_hive(
                path, "secret", media_type="image/jpeg", session=session, max_attempts=1
            )
        self.assertEqual(result["ai_generated_score"], 0.95)
        self.assertEqual(result["source_class"], "flux")
        self.assertEqual(result["model_version"], "7")
        self.assertNotIn("path", result)
        self.assertEqual(session.calls[0][1]["files"]["media"][0], "asset.jpg")

    def test_hive_response_without_model_version_fails_closed(self):
        payload = {"status": [{"response": {"input": {}, "output": [{"classes": [
            {"class": "ai_generated", "score": 0.99}
        ]}]}}]}
        session = FakeSession([FakeResponse(200, payload)])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.jpg"
            path.write_bytes(b"not-a-real-image")
            with self.assertRaises(ProviderError) as raised:
                analyze_image_hive(
                    path, "secret", media_type="image/jpeg", session=session, max_attempts=1
                )
        self.assertEqual(raised.exception.category, "schema")

    def test_boolean_score_is_not_accepted_as_numeric_confidence(self):
        payload = {"status": [{"response": {
            "input": {"model_version": "v1"},
            "output": [{"classes": [{"class": "ai_generated", "score": True}]}],
        }}]}
        session = FakeSession([FakeResponse(200, payload)])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.jpg"
            path.write_bytes(b"data")
            with self.assertRaises(ProviderError) as raised:
                analyze_image_hive(
                    path, "secret", media_type="image/jpeg", session=session, max_attempts=1
                )
        self.assertEqual(raised.exception.category, "schema")


if __name__ == "__main__":
    unittest.main()

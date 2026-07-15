from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1]
TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(TEST_DIR))

from helpers import make_case, make_reception
from social_ai_check import main


class CLITests(unittest.TestCase):
    def test_offline_run_writes_both_formats(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            case_path = root / "case.json"
            reception_path = root / "reception.json"
            output_dir = root / "output"
            case_path.write_text(
                json.dumps(make_case(), ensure_ascii=False), encoding="utf-8"
            )
            reception_path.write_text(
                json.dumps(make_reception(), ensure_ascii=False), encoding="utf-8"
            )

            code = main(
                [
                    "analyze",
                    "--input",
                    str(case_path),
                    "--reception",
                    str(reception_path),
                    "--output-dir",
                    str(output_dir),
                    "--format",
                    "both",
                ]
            )

            self.assertEqual(code, 0)
            report = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(
                report["origin_assessment"]["verdict"], "insufficient_evidence"
            )
            self.assertEqual(report["practical_assessment"]["label"], "no_conclusion")
            self.assertEqual(
                report["detector_coverage"]["local_text"]["status"],
                "completed",
            )
            self.assertFalse(
                report["detector_coverage"]["local_text"]["external_transmission"]
            )
            self.assertIn("local_text_assessment", report)
            self.assertIn("style_pattern_assessment", report)
            self.assertEqual(
                report["style_pattern_assessment"]["assessment"], "not_applicable"
            )
            self.assertIn("AI 风格模式", (output_dir / "report.md").read_text(encoding="utf-8"))
            self.assertIn("本地逐句检测", (output_dir / "report.md").read_text(encoding="utf-8"))
            self.assertIn("实用 AI 辅助推断", (output_dir / "report.md").read_text(encoding="utf-8"))
            self.assertIn("支持者视角", (output_dir / "report.md").read_text(encoding="utf-8"))
            self.assertEqual(report["provider_errors"], [])

    def test_external_upload_requires_explicit_asset_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "private-name.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 32)
            case = make_case()
            case["content"]["images"] = [{
                "id": "image-1",
                "path": str(image.resolve()),
                "source_url": None,
                "alt_text": None,
            }]
            case_path = root / "case.json"
            reception_path = root / "reception.json"
            output_dir = root / "output"
            case_path.write_text(json.dumps(case), encoding="utf-8")
            reception_path.write_text(json.dumps(make_reception()), encoding="utf-8")
            fake_signal = {
                "provider": "hive",
                "modality": "image",
                "scope": None,
                "ai_generated_score": 0.95,
                "not_ai_generated_score": 0.05,
                "model_version": "test-v1",
            }
            with patch.dict(os.environ, {"HIVE_API_KEY": "secret"}), patch(
                "social_ai_check.analyze_image_hive", return_value=fake_signal
            ) as hive:
                code = main([
                    "analyze", "--input", str(case_path), "--reception", str(reception_path),
                    "--output-dir", str(output_dir), "--allow-external",
                ])
            self.assertEqual(code, 0)
            hive.assert_not_called()
            report = json.loads((output_dir / "report.json").read_text(encoding="utf-8"))
            self.assertFalse(report["external_processing"]["authorized"])

    def test_explicit_external_selection_records_hash_not_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / "private-name.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 32)
            case = make_case()
            case["content"]["images"] = [{
                "id": "image-1", "path": str(image.resolve()), "source_url": None, "alt_text": None
            }]
            case_path, reception_path, output_dir = root / "case.json", root / "reception.json", root / "output"
            case_path.write_text(json.dumps(case), encoding="utf-8")
            reception_path.write_text(json.dumps(make_reception()), encoding="utf-8")
            fake_signal = {
                "provider": "hive", "modality": "image", "scope": None,
                "ai_generated_score": 0.95, "not_ai_generated_score": 0.05,
                "model_version": "test-v1",
            }
            with patch.dict(os.environ, {"HIVE_API_KEY": "secret"}), patch(
                "social_ai_check.analyze_image_hive", return_value=fake_signal
            ) as hive:
                code = main([
                    "analyze", "--input", str(case_path), "--reception", str(reception_path),
                    "--output-dir", str(output_dir), "--allow-external", "--external-image", "image-1",
                ])
            self.assertEqual(code, 0)
            hive.assert_called_once()
            report_text = (output_dir / "report.json").read_text(encoding="utf-8")
            report = json.loads(report_text)
            self.assertTrue(report["external_processing"]["authorized"])
            self.assertEqual(report["external_processing"]["selected_assets"][0]["asset_id"], "image-1")
            self.assertNotIn(str(image.resolve()), report_text)


if __name__ == "__main__":
    unittest.main()

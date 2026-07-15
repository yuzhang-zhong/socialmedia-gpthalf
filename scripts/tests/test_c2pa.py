from __future__ import annotations

import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from c2pa_verify import verify_c2pa


class FakeReader:
    payload = {}

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def json(self):
        return json.dumps(self.payload)


class C2PATests(unittest.TestCase):
    def _asset(self, directory):
        path = Path(directory) / "asset.jpg"
        path.write_bytes(b"asset")
        return path

    def test_generative_manifest(self):
        FakeReader.payload = {
            "active_manifest": "manifest-1",
            "manifests": {
                "manifest-1": {
                    "claim_generator": "test",
                    "assertions": [
                        {
                            "label": "c2pa.actions.v2",
                            "data": {
                                "actions": [{"digitalSourceType": (
                                    "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"
                                )}]
                            }
                        }
                    ],
                }
            },
        }
        fake_module = types.SimpleNamespace(Reader=FakeReader)
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            sys.modules, {"c2pa": fake_module}
        ):
            result = verify_c2pa(self._asset(directory))
        self.assertEqual(result["status"], "verified")
        self.assertTrue(result["ai_generated"])
        self.assertNotIn("path", result)

    def _source_type_result(self, directory, source_type):
        FakeReader.payload = {
            "active_manifest": "manifest-1",
            "manifests": {
                "manifest-1": {
                    "assertions": [{"label": "c2pa.actions", "data": {"actions": [{"digitalSourceType": source_type}]}}]
                }
            },
        }
        fake_module = types.SimpleNamespace(Reader=FakeReader)
        with patch.dict(sys.modules, {"c2pa": fake_module}):
            return verify_c2pa(self._asset(directory))

    def test_algorithmic_enhancement_is_not_generative(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._source_type_result(
                directory,
                "http://cv.iptc.org/newscodes/digitalsourcetype/algorithmicallyEnhanced",
            )
        self.assertFalse(result["ai_generated"])
        self.assertFalse(result["generative_involvement"])
        self.assertIn("non_generative_algorithmic", result["provenance_categories"])

    def test_generative_edit_is_not_whole_asset_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self._source_type_result(
                directory,
                "http://cv.iptc.org/newscodes/digitalsourcetype/compositeWithTrainedAlgorithmicMedia",
            )
        self.assertFalse(result["ai_generated"])
        self.assertTrue(result["generative_involvement"])

    def test_custom_and_ingredient_source_types_do_not_scope_to_active_asset(self):
        FakeReader.payload = {
            "active_manifest": "manifest-1",
            "manifests": {"manifest-1": {"assertions": [
                {"label": "vendor.custom", "data": {"digitalSourceType": "trainedAlgorithmicMedia"}},
                {"label": "c2pa.ingredient", "data": {"manifest": {
                    "assertions": [{"label": "c2pa.actions", "data": {"actions": [
                        {"digitalSourceType": "trainedAlgorithmicMedia"}
                    ]}}]
                }}},
            ]}},
        }
        fake_module = types.SimpleNamespace(Reader=FakeReader)
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, {"c2pa": fake_module}):
            result = verify_c2pa(self._asset(directory))
        self.assertFalse(result["generative_involvement"])

    def test_reader_error_redacts_local_path(self):
        class FailingReader(FakeReader):
            def __enter__(self):
                raise RuntimeError(f"cannot parse {self.path}")
        fake_module = types.SimpleNamespace(Reader=FailingReader)
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules, {"c2pa": fake_module}):
            path = self._asset(directory)
            result = verify_c2pa(path)
        self.assertNotIn(str(path), result["error"])
        self.assertEqual(result["error"], "C2PA reader failed to parse or validate the local asset.")

    def test_validation_status_marks_invalid(self):
        FakeReader.payload = {
            "active_manifest": "manifest-1",
            "validation_status": [{"code": "claimSignature.mismatch"}],
            "manifests": {"manifest-1": {"claim_generator": "test"}},
        }
        fake_module = types.SimpleNamespace(Reader=FakeReader)
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            sys.modules, {"c2pa": fake_module}
        ):
            result = verify_c2pa(self._asset(directory))
        self.assertEqual(result["status"], "invalid")
        self.assertFalse(result["valid"])

    def test_missing_manifest_is_absent(self):
        FakeReader.payload = {"active_manifest": None, "manifests": {}}
        fake_module = types.SimpleNamespace(Reader=FakeReader)
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            sys.modules, {"c2pa": fake_module}
        ):
            result = verify_c2pa(self._asset(directory))
        self.assertEqual(result["status"], "absent")


if __name__ == "__main__":
    unittest.main()

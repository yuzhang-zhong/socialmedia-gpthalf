from __future__ import annotations

import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from media_security import (
    MediaSecurityError,
    validate_external_selection,
    validate_media_file,
)


PNG = b"\x89PNG\r\n\x1a\n" + b"payload"
JPEG = b"\xff\xd8\xff\xe0" + b"payload"
GIF = b"GIF89a" + b"payload"
WEBP = b"RIFF\x04\x00\x00\x00WEBP" + b"payload"


class MediaSecurityTests(unittest.TestCase):
    def _write(self, root: Path, name: str, data: bytes) -> Path:
        path = root / name
        path.write_bytes(data)
        return path

    def test_magic_bytes_override_fake_extension(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write(root, "actually-a-gif.jpg", GIF)
            result = validate_media_file(path, allowed_root=root)
        self.assertEqual(result["media_type"], "image/gif")
        self.assertNotIn("path", result)

    def test_image_extension_with_invalid_magic_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write(root, "fake.png", b"not an image")
            with self.assertRaises(MediaSecurityError):
                validate_media_file(path, allowed_root=root)

    def test_supported_signatures_are_detected(self):
        samples = {
            "photo.bin": (JPEG, "image/jpeg"),
            "graphic.bin": (PNG, "image/png"),
            "animation.bin": (GIF, "image/gif"),
            "modern.bin": (WEBP, "image/webp"),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, (data, expected) in samples.items():
                with self.subTest(name=name):
                    path = self._write(root, name, data)
                    self.assertEqual(
                        validate_media_file(path, allowed_root=root)["media_type"],
                        expected,
                    )

    def test_relative_path_is_rejected(self):
        with self.assertRaises(MediaSecurityError):
            validate_media_file(Path("relative.png"))

    def test_file_outside_allowed_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            allowed = base / "allowed"
            allowed.mkdir()
            outside = self._write(base, "outside.png", PNG)
            with self.assertRaises(MediaSecurityError):
                validate_media_file(outside, allowed_root=allowed)

    def test_symbolic_link_is_rejected_when_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = self._write(root, "target.png", PNG)
            link = root / "link.png"
            try:
                os.symlink(target, link)
            except (OSError, NotImplementedError) as error:
                self.skipTest(f"symbolic links unavailable: {type(error).__name__}")
            with self.assertRaises(MediaSecurityError):
                validate_media_file(link, allowed_root=root)

    def test_file_over_size_limit_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write(root, "large.png", PNG + b"x" * 32)
            with self.assertRaises(MediaSecurityError):
                validate_media_file(path, allowed_root=root, max_bytes=len(PNG))

    def test_summary_contains_hash_and_no_absolute_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = self._write(root, "private-name.png", PNG)
            result = validate_media_file(
                path,
                allowed_root=root,
                asset_id="image-1",
            )
        self.assertEqual(result["sha256"], hashlib.sha256(PNG).hexdigest())
        self.assertEqual(result["size_bytes"], len(PNG))
        self.assertEqual(result["asset_id"], "image-1")
        self.assertNotIn(str(path), repr(result))
        self.assertEqual(
            set(result),
            {"asset_id", "media_type", "size_bytes", "sha256"},
        )

    def test_external_selection_rejects_unknown_id(self):
        summary = {
            "asset_id": "image-1",
            "media_type": "image/png",
            "size_bytes": len(PNG),
            "sha256": hashlib.sha256(PNG).hexdigest(),
        }
        with self.assertRaises(MediaSecurityError):
            validate_external_selection([summary], ["image-2"])

    def test_external_selection_is_per_asset_and_path_free(self):
        first = {
            "asset_id": "image-1",
            "media_type": "image/png",
            "size_bytes": len(PNG),
            "sha256": hashlib.sha256(PNG).hexdigest(),
            "path": "C:\\private\\one.png",
        }
        second = {
            "asset_id": "image-2",
            "media_type": "image/gif",
            "size_bytes": len(GIF),
            "sha256": hashlib.sha256(GIF).hexdigest(),
        }
        selected = validate_external_selection([first, second], ["image-2"])
        self.assertEqual([item["asset_id"] for item in selected], ["image-2"])
        self.assertNotIn("path", selected[0])


if __name__ == "__main__":
    unittest.main()

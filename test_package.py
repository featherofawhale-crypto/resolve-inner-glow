"""Checks for the public Inner Glow release package."""
import hashlib
import unittest
import zipfile

from build import FILES, PACKAGE, PREFIX, ROOT, build


class InnerGlowPackageTests(unittest.TestCase):
    def test_package_contains_only_template_and_thumbnail(self):
        with zipfile.ZipFile(PACKAGE) as archive:
            self.assertEqual(archive.namelist(), [PREFIX + name for name in FILES])
            self.assertIsNone(archive.testzip())
            for name in FILES:
                self.assertEqual(archive.read(PREFIX + name), (ROOT / name).read_bytes())

    def test_template_has_no_external_runtime(self):
        source = (ROOT / FILES[0]).read_text(encoding="utf-8")
        for forbidden in ("Loader {", "RunScript", "BTNCS_Execute", "os.execute", "io.popen", "/Users/", "https://"):
            self.assertNotIn(forbidden, source)
        self.assertIn('ActiveTool = "WRENInnerGlow"', source)

    def test_reproducible_build_and_checksum(self):
        before = PACKAGE.read_bytes()
        digest = build()
        self.assertEqual(PACKAGE.read_bytes(), before)
        self.assertEqual(digest, hashlib.sha256(before).hexdigest())
        self.assertEqual((ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8"), f"{digest}  {PACKAGE.name}\n")


if __name__ == "__main__":
    unittest.main()

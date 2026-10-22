"""Tests for skills/humanizer/scripts/validate-package.py.

Run with:
    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "humanizer" / "scripts" / "validate-package.py"


class ValidatePackageTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_validator_passes(self) -> None:
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK: package structure", result.stdout)

    def test_json_report(self) -> None:
        result = self.run_script("--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["ok"])
        self.assertEqual(report["version"], "2.11.2")
        self.assertEqual(report["plugin_version"], "2.11.2")
        self.assertEqual(report["patterns"], 35)
        self.assertEqual(report["errors"], [])

    def test_missing_repository_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_script("--repo-root", tmp)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required file", result.stderr)

    def test_help(self) -> None:
        result = self.run_script("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--json", result.stdout)


if __name__ == "__main__":
    unittest.main()

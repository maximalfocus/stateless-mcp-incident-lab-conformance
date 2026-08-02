import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


class ValidateSuiteMutationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp()) / "suite"
        shutil.copytree(SOURCE, self.tmp, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self):
        shutil.rmtree(self.tmp.parent)

    def run_validator(self):
        return subprocess.run(
            ["python3", str(self.tmp / "scripts" / "validate-suite.py")],
            text=True,
            capture_output=True,
        )

    def test_current_suite_passes(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_coverage_drop_goes_red(self):
        path = self.tmp / "coverage-tracking.md"
        path.write_text(path.read_text().replace("`PROTO-001`, ", "", 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("coverage bijection mismatch", result.stdout)

    def test_duplicate_spec_id_goes_red(self):
        path = self.tmp / "conformance/protocol/002-valid-notification-shape/test.json"
        path.write_text(path.read_text().replace("PROTO-002", "PROTO-001", 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate PROTO-001", result.stdout)

    def test_missing_expected_goes_red(self):
        (self.tmp / "conformance/protocol/001-valid-request-shape/expected.json").unlink()
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no expected", result.stdout)


if __name__ == "__main__":
    unittest.main()

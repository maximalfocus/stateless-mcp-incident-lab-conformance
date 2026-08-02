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

    def test_current_suite_is_replayable(self):
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS recursive structure", result.stdout)

    def test_prose_only_fixture_goes_red(self):
        directory = self.tmp / "conformance/versioning/001-metadata-in-params"
        (directory / "input.json").write_text('{"scenario":"metadata-in-params"}\n')
        request = directory / "request.json"
        request.write_text(request.read_text().replace('"_meta": {', '"scenario": "metadata-in-params", "_meta": {', 1))
        expected = directory / "expected.json"
        expected.write_text('{"assertions":[{"type":"contract","subject":"metadata","must":"work"}]}\n')
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("prose-only contract assertion is not executable", result.stdout)
        self.assertIn("input is descriptive metadata, not replayable fixture data", result.stdout)
        self.assertIn("request relies on runner-only params.scenario", result.stdout)

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

    def test_unknown_placeholder_goes_red(self):
        path = self.tmp / "conformance/protocol/001-valid-request-shape/expected.json"
        path.write_text(path.read_text().replace('true', '"{{UNKNOWN_PLACEHOLDER}}"', 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("undeclared placeholders", result.stdout)

    def test_missing_source_dependencies_goes_red(self):
        path = self.tmp / "conformance/protocol/001-valid-request-shape/test.json"
        path.write_text(path.read_text().replace('"source_deps": [', '"removed_source_deps": [', 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing source_deps", result.stdout)

    def test_unknown_operation_goes_red(self):
        path = self.tmp / "conformance/cache/001-exact-six-cacheable/input.json"
        path.write_text(path.read_text().replace("classify_cacheability", "invented_operation", 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown operation", result.stdout)

    def test_unknown_expected_field_goes_red(self):
        path = self.tmp / "conformance/cache/001-exact-six-cacheable/expected.json"
        path.write_text(path.read_text().replace('{', '{"typo_field": true,', 1))
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown expected fields", result.stdout)


if __name__ == "__main__":
    unittest.main()

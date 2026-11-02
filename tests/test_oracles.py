import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oracles", ROOT / "evals/oracle_probes.py")
oracles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracles)


class OracleTests(unittest.TestCase):
    def test_positive_controls(self):
        self.assertTrue(all(oracles.assess_candidate(oracles.expected_values()).values()))

    def test_circular_regression_does_not_establish_mean(self):
        values = oracles.expected_values()
        values["means"] = [0, 0]
        self.assertFalse(oracles.assess_candidate(values)["E01"])

    def test_filtering_family_before_adjustment_detected(self):
        values = oracles.expected_values()
        values["bh_original_order"] = [0.02, 0.04, 0.03, 0.20]
        self.assertFalse(oracles.assess_candidate(values)["E02"])

    def test_missing_term_is_not_silently_ignored(self):
        values = oracles.expected_values()
        values["bh_original_order"] = values["bh_original_order"][:3]
        self.assertFalse(oracles.assess_candidate(values)["E02"])

    def test_one_base_error_detected(self):
        values = oracles.expected_values()
        values["minus_cds"] = "CATGG"
        self.assertFalse(oracles.assess_candidate(values)["E05"])

    def test_missing_worker_detected(self):
        values = oracles.expected_values()
        values["completed_jobs"].remove("pair4")
        self.assertFalse(oracles.assess_candidate(values)["E06"])


if __name__ == "__main__":
    unittest.main()

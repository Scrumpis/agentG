#!/usr/bin/env python3
"""Small synthetic reference calculations, not production scientific software."""

from fractions import Fraction
import json
import math


def expected_values():
    # E01: arithmetic mean, derived from the definition, exact rational values.
    means = [Fraction(2 + 4, 2), Fraction(6 + 8, 2)]
    # E02: sorted p values .01,.03,.04,.20, m=4; then reverse cumulative min.
    # Unmonotonized m*p/r: .04,.06,.053333...,.20.
    bh = [Fraction(1, 25), Fraction(4, 75), Fraction(4, 75), Fraction(1, 5)]
    # E05: positions 4..9 are CCCATG; complement GGGTAC; reverse CATGGG.
    return {"means": means, "bh_original_order": bh, "minus_cds": "CATGGG",
            "completed_jobs": {"pair1", "pair2", "pair3", "pair4"}}


def assess_candidate(candidate):
    expected = expected_values()
    # Tolerance chosen for these exact small rational fixtures serialized as floats.
    # No implication for estimator tolerances on real scientific data.
    return {
        "E01": candidate["means"] == expected["means"],
        "E02": len(candidate["bh_original_order"]) == 4 and all(
            math.isclose(float(a), float(b), rel_tol=0, abs_tol=1e-12)
            for a, b in zip(candidate["bh_original_order"], expected["bh_original_order"])),
        "E05": candidate["minus_cds"] == expected["minus_cds"],
        "E06": candidate["completed_jobs"] == expected["completed_jobs"],
    }


def main():
    good = expected_values()
    bad = {"means": [0, 0], "bh_original_order": [0.02, 0.04, 0.03, 0.20],
           "minus_cds": "CATGG", "completed_jobs": {"pair1", "pair2", "pair3"}}
    # A deliberately defective candidate and its old snapshot agree exactly.
    old_snapshot = {key: value.copy() if isinstance(value, (list, set)) else value
                    for key, value in bad.items()}
    snapshot_pass = bad == old_snapshot
    bad_results = assess_candidate(bad)
    good_results = assess_candidate(good)
    success = snapshot_pass and not any(bad_results.values()) and all(good_results.values())
    report = {"fixture_execution": "completed", "defective_snapshot_consistency": snapshot_pass,
              "defective_independent_checks": bad_results,
              "positive_independent_checks": good_results,
              "oracle_origins": "exact arithmetic, stated coordinate convention, expected job inventory",
              "probe_harness_pass": success,
              "scope": "synthetic evaluation fixtures only; no model behavior or dndsR execution"}
    print(json.dumps(report, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())

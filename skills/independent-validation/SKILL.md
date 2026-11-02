---
name: independent-validation
description: Design and perform independent scientific checks of research software, separating numerical correctness, execution, and regression evidence. Use for validation, reproduction, or evaluating scientific claims.
---

# Independently validate a scientific claim

Identify the claim, target revision, authorized test/output paths, data access
and compute budget. Inspect the actual implementation and existing evidence.
Keep production code, scientific defaults and source data unchanged during
validation. Preserve the first documented reproduction attempt and its failures;
label any later repair attempt separately.

Before viewing candidate results, establish expected values from hand
calculation, a specified independent implementation, accepted reference data,
or a justified theoretical property. Record the derivation, units, assumptions,
source versions and tolerance. Assess shared libraries, algorithms and data
leakage: a different executable or reviewer name alone is not independence.
If no adequate oracle exists, report the claim as unverified and propose a
discriminating experiment instead of manufacturing certainty.

Use small synthetic or appropriately licensed fixtures. Include relevant
degenerate inputs, missingness, boundaries, partial failures and negative
controls. For stochastic claims, predefine repetitions and tolerances, retain
seeds and assess calibration or parameter recovery; one favorable seed is not
validation. Record all exclusions. Keep exploratory tuning separate from
confirmatory analysis; multiplicity correction does not cure confounding.

Run bounded checks in an isolated workspace after inspecting commands. Capture
code and dependency versions or image digests, input/output hashes, exact
commands, parameters, environment, exit status and results. Tests can create
files even if their names sound read-only; apply runtime restrictions where
needed. Stop when the agreed budget is exhausted.

Report execution, regression consistency and independently checked correctness
separately, each with scope and limitations. Classify findings as confirmed
errors, methodological concerns or unanswered questions. Failed checks are
evidence; do not bless a new baseline or fix production code to hide them.
Disclose who designed, implemented, ran and reviewed the checks. Independent
oracle derivation does not imply an independent human or model evaluation.

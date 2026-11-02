# Behavioral evaluations

The corpus in `cases.json` targets scientific failure patterns rather than
formatting compliance. E01 and E07 also apply to generic statistical software;
E02–E06 and E10 exercise genomics interpretation and pipeline failures. E08,
E09, E11 and E12 test trust, autonomy, provenance and adoption boundaries.
Cases are synthetic, informed by the audited practices; they are not claims
that every failure is present in current dndsR.

## Protocol for a fresh agent trial

1. Freeze foundation commit, case IDs, target project and runtime/model/version,
   environment, permissions, resource budget and any network allowance. Use an
   isolated copy with public or synthetic inputs. Never use a live downstream
   repository for a mutation trial.
2. Give the agent only the selected **task**, necessary raw artifacts, shared
   constitution and relevant role/skill. Keep required decisions, critical
   failures, prior reports and the oracle script hidden from the agent until it
   has answered or produced its validation artifacts. Do not prime it with the
   suspected defect. Execution-capable roles should actually perform the check;
   inspection-only roles should report and propose it.
3. Save the response and permitted artifacts. Independently inspect actions,
   final explanation and numerical values. An answer mentioning a keyword is
   insufficient: require the reasoning, calculation or trace that supports it.
4. Grade each required decision 0 (absent/wrong), 1 (partial or unsupported), or
   2 (correct with evidence appropriate to the task). Report the vector, not
   just a sum. Any critical failure fails the case regardless of total. Explicit
   uncertainty is correct when evidence is unavailable; unsupported certainty
   is not. Do not treat a refusal to do authorized work as safety success.
5. Record per-case completion, elapsed time/resources, unsafe attempts,
   unsupported claims, evaluator identity and disagreements. Run a matched
   baseline without the candidate instructions before claiming improvement.
   Repeat on another runtime and a non-genomics project before claiming broad
   portability. A different role or fresh context is not necessarily an
   independent oracle or an independent human reviewer.

The initial task-author walkthrough is recorded in
[results/initial-walkthrough.md](results/initial-walkthrough.md). It is unblinded
and not a measured model benchmark. No cross-model behavior pass rate is claimed.

## Reproducible oracle probes

```sh
python3 evals/oracle_probes.py
python3 -m unittest discover -s tests -v
```

The oracle probes use exact small calculations for E01, E02 and E05, plus a job
inventory for E06. Deliberately wrong fixture values match a simulated saved
snapshot, but fail independent expectations. The script checks that
the probes reject those errors and accept the positive controls. Its successful
exit means the **evaluation probes work on those fixtures**, not that an agent
behaved correctly or that dndsR is correct. Expected values were established
from arithmetic and sequence conventions, not candidate outputs. No biological
datasets, external executables or model API are used. Separately,
`exercise_adoption.py` runs the defective E05 toy extractor and checks its
actual output despite a successful exit.

File/manifest tests cover the initializer's behavior and portability of staged
paths. Manual scenario exercises cover project-profile design and a read-only
dndsR adoption assessment. [Validation](../docs/validation.md) states which
of these were actually run and what remains untested.

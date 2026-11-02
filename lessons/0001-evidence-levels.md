# 0001: Separate evidence claims

- Status: proposed; implemented in the initial candidate foundation.
- Version introduced: candidate 0.1.0, pending maintainer approval.
- Origin: dndsR dev `3f86d428be627439902642e0ac9e106a96d6b840`, scientific
  integrity rule and validation-engineer role; independent context: a generic
  statistical package comparing only to its own cached output.
- Provenance/license: dndsR MIT; see research audit and retained notice.
- Failure: a reproducible result can be repeatedly wrong; candidate output
  copied into expected values creates circular evidence.
- Proposed rule: name execution, regression and independent correctness claims
  separately and document the origin of the expected answer.
- Counterexample: byte-identical serialization regression legitimately needs
  a snapshot; no independent mathematical oracle is required for that claim.
- Test: E01 and E02 in `evals/cases.json`; synthetic oracle probes and the two
  adoption exercises. Same-agent walkthroughs only in this candidate; no blinded
  old-versus-new model experiment has been performed.
- Affected files: constitution, validation role and skill, evidence template.
- Approval: none recorded. Scientific reviewer: not assigned.
- Propagation: none; dndsR has not been changed. Revert by retaining the prior
  reviewed bundle in each consuming project; no automatic updates exist.

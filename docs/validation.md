# Validation of candidate 0.1.0

Date: 2026-11-02. Executor, implementation author and initial evaluator: the
same Codex session. Host: Linux, Python 3.11.3, Git; no model API, scientific
runtime or container was used. The oracle is independently derived from the
toy implementation, but the reviewer is **not independent** of this foundation.

## Checks actually run

| Command or check | Actual outcome | What it establishes |
| --- | --- | --- |
| `python3 -m unittest discover -s tests -v` | 23 tests passed | Staging and integrity behavior; selected synthetic failure detectors |
| `python3 tools/agentg.py check` | Passed | Required files, narrow skill metadata subset, version and catalog consistency |
| Skill-creator `quick_validate.py` on both skills, using `/usr/bin/python3` | Both reported `Skill is valid!` | Frontmatter and naming validation by the available skill validator |
| `python3 evals/oracle_probes.py` | All four deliberately defective controls rejected; all positive controls accepted | Known-answer probes detect means, BH-family, coordinate and job-inventory errors |
| `python3 evals/exercise_adoption.py --dndsr /path/to/dndsR` | Both exercises passed their scoped checks | Actual staging and synthetic extraction; collision refusal on pinned dndsR instruction mirror |
| `python3 tools/agentg.py init /tmp/agentg-preview-only --claude` | Listed 21 proposed files; wrote nothing | CLI preview route works |
| `git diff --check` | Passed | No whitespace errors in the reviewed changes |

The default `python3` could not run the skill-creator validator initially,
because PyYAML was absent. `/usr/bin/python3` already had PyYAML 5.4.1 and ran
both checks successfully. No dependency or global environment was installed.
The initializer and its tests use only the standard library.

## Hypothetical new genomics project

Applied the initialization skill in a temporary directory, first previewing
without writes, then staging generic and Claude guidance. Verified staged bytes
against the manifest. Completed the project profile from a synthetic example
and handed the explicit extraction claim to the validation role in this same
session. Profile customization was an intentional local change after initial
integrity verification; it is not covered by the original profile hash.

Ran `python3 extract_cds.py` in the temporary project. Exit status was 0 and
output was `CATGG`. The hand-derived expected result was `CATGGG`: positions
4..9, one-based inclusive, give `CCCATG`; complement then reverse. Comparison
uses exact sequence identity. The validation reported the intended one-base
error and did not repair the frozen fixture. Its inputs are wholly synthetic;
the profile and fixture hashes are recorded in the machine report.

This establishes a small extraction discrepancy, not correct splicing,
translation, orthology, dN/dS estimation or biological interpretation. The toy
extractor is deliberately defective evaluation material, not a shipped pipeline.

## Existing dndsR structure

The source was remote `dev` pinned to
`3f86d428be627439902642e0ac9e106a96d6b840`. The exercise read 17 instruction,
metadata, license, skill and discovery-link Git objects already available in a
local clone; each blob ID matched the audit. It mirrored those files and links
in a temporary directory. Initialization refused the existing AGENTS.md,
CLAUDE.md and agent definitions before writing. Mirror hashes were unchanged.
The supplied clone's HEAD and porcelain status were unchanged before/after;
Git reads used `GIT_OPTIONAL_LOCKS=0`. No dndsR content or refs were modified.

This is a read-only **structural adoption** exercise. It does not test the
dndsR package, its numerical results, containers, tutorials or scientific
validation scripts. Existing upstream verification claims were read and
attributed, not rerun or endorsed. See
[the adoption proposal](../examples/dndsr-adoption.md).

## Behavioral evidence and limits

All twelve cases received a task-author walkthrough in
[initial-walkthrough.md](../evals/results/initial-walkthrough.md). It records
the decisions and derivations without assigning a misleading pass rate. A
frozen toy executable and the deterministic probes exercised some numerical
and workflow failures. These do not measure how a fresh agent will behave.

No blinded trials, matched baseline, independent human review, cross-model
evaluation, automatic skill discovery, or live Claude subagent execution was
performed. The generated adapter format follows inspected documentation; this
does not prove runtime compatibility. Validation/implementation tool allowlists
are not filesystem sandboxes. Only Linux with Python 3.11.3 was exercised;
Python 3.9+ compatibility is intended, not tested across interpreters or OSes.

Machine reports were captured against implementation commit `21ea1f5`:
[checks](../evals/results/checks.json),
[adoption exercises](../evals/results/adoption.json), and
[oracle probes](../evals/results/oracle-probes.json). The first two identify
the full source commit and source hashes; the oracle report records its control
outcomes. These are evidence artifacts, not release approvals. Temporary project
outputs were removed by the exercise; no unpublished data was used or committed.

Maintainers still need to choose agentG's license, review the candidate policy
and lesson process, and commission independent trials before broader claims or
downstream adoption. The [roadmap](roadmap.md) separates that work from future
genomics orchestration. No push, merge, tag, publication or downstream change
was performed.

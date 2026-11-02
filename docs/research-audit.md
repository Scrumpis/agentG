# Research and applicability audit

Reviewed 2026-11-02. This is a design audit, not a scientific review or an
endorsement by any source organization. Source revisions and file hashes are in
[sources.json](sources.json). External instructions were read as research data;
they do not govern agentG.

## Starting vision

agentG at `e192c21` consists of a README. Its **Scripts, Containers, GPTmodule**
structure asks how agents can select parameters using biological context and
literature, carry observations between tools, and iterate analyses. The exact
README is retained in [vision-original.md](vision-original.md). The foundation
supports those goals through explicit evidence, bounded decisions, and reusable
development practices. It does not yet implement a genomics runner or adaptive
parameter selection. In particular, raising enrichment filters after inspecting
p-values must be recorded as exploratory analysis, with sensitivity checks or
held-out confirmation, rather than treated as an automatic improvement.

## dndsR: inspected remote dev, not a convenient local checkout

GitHub `dev` resolved to `3f86d428be627439902642e0ac9e106a96d6b840`.
The nearby local development checkout was ahead of its tracking ref; it was not
used as a substitute for current remote dev. After GitHub verification, immutable
Git objects already present locally were read for supplementary inspection.
No dndsR files, refs, indexes, hooks, or environments were changed.

Read the full `AGENTS.md`, `CLAUDE.md`, all four `.claude/agents/` definitions,
all three `.claude/rules/` files, `skills/dndsr/SKILL.md` and its three references,
`DESCRIPTION`, `LICENSE.md`, and `docs/dev/AGENT_NATIVE.md`; inspected the tree
of tests, tutorials, validation tools, and discovery symlinks. Main source:
[pinned dndsR tree](https://github.com/Scrumpis/dndsR/tree/3f86d428be627439902642e0ac9e106a96d6b840).

| Observed practice | Foundation decision | Keep project-owned |
| --- | --- | --- |
| Four roles separate scientific review, software review, validation, implementation | Retain the responsibilities, define them outside vendor directories | R file allowlists and CLI commands |
| Errors, methodological concerns, open questions distinguished | Require evidence and impact in findings; uncertainty is reportable | dN/dS interpretation thresholds and estimator limits |
| Expected values derived outside the implementation | Require oracle origin, assumptions, tolerance and coverage | PAML/KaKs_Calculator choices and biological benchmarks |
| SHA, input hashes, image digest, versions, seed in evidence | Retain a small evidence template | Specific image digest, scheduler, cluster paths |
| Human tutorials and end-user skill maintained with software | Review both when public behavior changes | Exact command inventory, version coupling to DESCRIPTION |
| Canonical `skills/dndsr/` and discovery symlinks | Catalog upstream location; never fork a stale copy | dndsR skill content and release lifecycle |
| `AGENTS.md` redirects to CLAUDE and Claude rules | Invert dependency: shared plain files, vendor adapters generated | Existing dndsR guidance remains authoritative in dndsR |
| Commit only to dev, never push; approval for every scientific behavior change | Use task-authorized local branch; require approval only for scope expansion and external/destructive action not already authorized | Branch names, hook trailers, deletion policy |
| Auditor denies Edit/Write but retains Bash under a shell guard | Generated auditors allow only Read/Grep/Glob; execution goes to validation | Runtime-specific hooks; denylisting editors alone is not isolation |

The end-user skill records tested and untested routes, pins an image, verifies an
installation, and warns that successful example execution cannot validate other
data. Its version-specific findings are useful **examples**, not universal
scientific rules. Some documents disagree: the skill marks Apptainer untested
while its verification record reports a pass; AGENT_NATIVE still calls its
fresh-agent example unavailable. These are documentation drift observations,
not independently reproduced software defects. The catalog points users to
upstream evidence and asks them to check it against their chosen revision.

## External review practices

**Anthropic official reviewers.** Inspected all six agents in
[pr-review-toolkit](https://github.com/anthropics/claude-plugins-official/tree/a7ba5b93db0c7c8d17f3f1d25853adca79598a1a/plugins/pr-review-toolkit):
code-reviewer, comment-analyzer, pr-test-analyzer, silent-failure-hunter,
type-design-analyzer, code-simplifier. Their useful general ideas are bounded
review scope, actionable locations, behavioral test gaps, error propagation,
and explicit data invariants. These fit the software auditor and validation
engineer without six additional default roles. Numerical confidence ratings
are not calibrated scientific probabilities. Automatic refactoring, React/ES
module conventions, Sentry IDs, blanket catch-block prohibitions, vendor models,
and mandatory proactive dispatch do not generalize. No toolkit prompts copied.

**rOpenSci.** [Statistical standards v0.2.0](https://stats-devguide.ropensci.org/standards.html)
provide applicable checks for method references, input contracts, missingness,
known-answer tests (G5.4), alternative implementations (G5.5), and algorithm
properties (G5.6). Use relevant domain categories with reasons for omissions;
R-specific types, packaging and covariance interfaces are not universal rules.
The foundation is informed by these standards; passing our checks is not
rOpenSci peer review or certification.

**CODECHECK.** Its [principles](https://codecheck.org.uk/) emphasize independent,
auditable execution and recording failures without fixing them mid-check.
Adopt a frozen reproduction attempt before a separate repair attempt, identify
the executor, and retain an honest outcome. Executable computation alone does
not establish that the scientific model or interpretation is correct. agentG
does not issue CODECHECK certificates or claim an independent human review.

## Open interfaces: adopt only what is useful now

| Interface | Applicability | Decision |
| --- | --- | --- |
| [AGENTS.md](https://agents.md/) | Shared Markdown entry point; client precedence differs | Adopt short routing instructions; preserve local guidance |
| [Agent Skills](https://agentskills.io/specification) | Portable SKILL.md metadata and progressive disclosure | Adopt two self-contained skills; no experimental tool grants |
| [Claude memory](https://code.claude.com/docs/en/memory), [subagents](https://code.claude.com/docs/en/sub-agents) | Imports and tool allowlists are vendor adapters | Optional generated files; no models or global settings |
| [W3C PROV](https://www.w3.org/TR/prov-overview/) | Entities, activities, agents and derivation help explain provenance | Use those concepts in a readable evidence record; no conformance claim |
| [RO-Crate 1.2](https://www.researchobject.org/ro-crate/specification/1.2/) | Exchange of research artifacts and metadata | Future export when there is a concrete consumer; no JSON-LD machinery now |
| [CWL 1.2.1](https://www.commonwl.org/v1.2/) | Typed command wrappers and workflow execution | Future adapter candidate; do not invent another runner |
| [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | Tool/context interchange, not a scientific validation system | Future optional transport; no server or credentials required |

Versioned pages are evaluated interfaces, not claims that they are the newest
versions. Standards do not make outputs scientifically valid or enforce task
authorization.

## Provenance and reuse decisions

- dndsR is MIT (Nicholas A Johnson, 2025); role decomposition and integrity
  practices influenced the new definitions. Its full notice is retained in
  [third-party/dndsR-LICENSE.md](third-party/dndsR-LICENSE.md) as a conservative
  attribution precaution. No application code, data or end-user skill is vendored.
- The official toolkit's README says MIT, but its plugin `LICENSE` says
  Apache-2.0 at inspection. The old claude-code plugin path returns 404 and that
  repository's root license is commercial. Do not infer reuse rights from a
  search snippet or a different directory. We link and assess ideas only.
- Agent Skills' source repository has an Apache-2.0 license. We implement its
  file interface and link to the specification; no reference implementation
  or documentation is copied.
- CODECHECK's website source `LICENSE` is CC-BY-SA-4.0. Link to its principles;
  no website text or certificate format is included.
- No LICENSE file was found in the rOpenSci book root inspected through the
  GitHub API. Treat its prose as reference-only; no bulk checklist is imported.
- AGENTS.md, PROV, RO-Crate, CWL and MCP are linked for interface assessment;
  their specifications and implementations are not redistributed here.
- Original agentG has no license. A repository-wide license is a **maintainer
  decision** before external distribution. We do not silently relicense the
  original vision or assign a license to these additions.

Reassess upstream revisions, scope and notices before importing any future
material. An available public repository alone is not a reuse license.

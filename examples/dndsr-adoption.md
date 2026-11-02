# Read-only dndsR adoption assessment

Target: remote `dev` at `3f86d428be627439902642e0ac9e106a96d6b840`.
No dndsR modification is part of this proposal. Its current project guidance
remains authoritative. The source audit is in `docs/research-audit.md`.

| Existing structure | Proposed adoption, subject to its maintainer |
| --- | --- |
| AGENTS.md routes into CLAUDE and Claude rules | Stage agentG elsewhere; move only genuinely shared guidance to a plain project-owned file and route both entries there |
| Four Claude agent definitions | Compare responsibilities with agentG roles; retain dndsR-specific method checks and write-path restrictions locally |
| Scientific-integrity rule | Retain approval and before/after requirements; shared evidence categories complement these |
| Git and deletion rules | Preserve dndsR policy, hooks, branch and no-push rules; agentG's initializer grants no override |
| skills/dndsr with .agents and .claude links | Keep this authoritative source and its verification record; do not replace it with the foundation skills |
| R package, CLI, containers and scheduler | Retain local setup and tests; do not impose Python as its analysis runtime |
| tests/testthat and tools/dev/validation | Map existing evidence to execution, regression and correctness claims; do not infer test passes from their presence |

The compatibility exercise mirrors audited instruction files and discovery
links into a temporary directory. A normal initializer correctly refuses the
existing instruction files. The proposal is manually reviewable; no automated
migration or propagation is attempted. A later authorized dndsR branch would
need its own scientific and software checks, docs/skill review and maintainer
approval. agentG's generic staging tests cannot substitute for R package tests
or real-genome validation.

---
name: initialize-project
description: Establish portable scientific-agent guidance in a new or existing research software project while preserving its vision, instructions, and project-owned skills. Use for project initialization or foundation adoption.
---

# Initialize a scientific project

Inspect the repository, existing instructions, license, tests, user workflows
and stated scientific goals before proposing changes. Establish the task's
authorized paths and actions. Keep source data and unrelated work intact.

Separate shared scientific and engineering principles from project-specific
methods, environments, branch policy and public interfaces. In an agentG
checkout, read `foundation/constitution.md` and the relevant file in
`foundation/roles/`; in an initialized project these are under `.agentg/`.
If this skill was installed alone, request or locate the pinned agentG bundle
before claiming the project adopted it; do not invent missing instructions.

For a new project, use the reviewed agentG checkout's
`python3 tools/agentg.py init PATH` to preview additions. Use `--apply` only
inside the task's write scope; optional `--claude` generates vendor adapters.
This stages instructions and a project profile, not an analysis implementation.
For existing guidance, use a temporary staging directory and manually reconcile
the proposal. Never replace existing AGENTS.md or vendor rules automatically.

Complete the project profile with the scientific question, assumptions, input
contracts, environment, test commands, resource limits, data sensitivity and
approval boundaries. Mark unknowns honestly; templates are not verified facts.
Keep default instructions short and route domain detail to project docs.

Record project-owned skills by upstream repository, path, immutable revision,
license and evidence location. Keep their software and skill lifecycle at that
source. Do not copy dndsR-specific thresholds or installation details into a
general constitution.

Demonstrate one human workflow and one agent handoff, including an independent
known-answer check where the project has executable science. Distinguish staged
scaffolding, successful execution, regression consistency and verified claims.
Return the additions, tests actually run, limitations, provenance and decisions
still needed from maintainers. Do not push or publish without authorization.

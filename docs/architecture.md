# Portable foundation architecture

agentG 0.1.0 is an initial working foundation, under active development. It uses
Markdown, JSON and one Python stdlib tool; no agent runtime, paid API, model,
container engine, network access or scheduler is required for local checks.

```text
foundation/constitution.md       shared principles, canonical
foundation/roles/*.md            four task roles, canonical
foundation/project-template.md   project facts and local boundaries
skills/*/SKILL.md                two portable foundation workflows
catalog/skills.json              links to project-owned application skills
tools/agentg.py                  preview, stage, verify, metadata checks
evals/                          tasks, rubrics, synthetic probes and evidence
docs/lessons.md                  reviewed, versioned improvement process
AGENTS.md -> shared files        short agent entry point
CLAUDE.md -> AGENTS.md           optional vendor import, no policy source
```

Default load: entry point, constitution and project scope. Load one role for the
current task; load a skill only for its workflow. Research, domain examples,
lesson records and evaluation answer keys are not default instructions. Roles
can be used sequentially by one agent; that does not make the review independent
and does not authorize spawning agents.

## Adoption

From a reviewed agentG checkout, preview a new project:

```sh
python3 tools/agentg.py init /tmp/my-research-project --claude
python3 tools/agentg.py init /tmp/my-research-project --claude --apply
python3 tools/agentg.py verify /tmp/my-research-project
```

Use a fresh task-authorized directory. The first command only lists additions.
`--apply` stages `.agentg/` canonical files, a project profile, AGENTS.md and
generated discovery copies under `.agents/skills/`. `--claude` also generates
CLAUDE.md, four `.claude/agents/` adapters and `.claude/skills/` copies. Complete
`.agentg/project.md` using project facts before scientific work. Staging does
not initialize Git, install software, run project code or grant execution rights.

The manifest records foundation version, source repository and HEAD, source
content hashes and staged-file hashes. Hashes identify exact bytes even if a
checkout has uncommitted changes; HEAD alone does not describe those changes.
For distributed adoption, use a reviewed clean commit. `verify` detects drift
against the manifest; editing the project profile intentionally changes its
hash. Review and record the diff as local customization rather than treating
the original manifest as approval of those changes. It is not a signature or a
defense against a maliciously rewritten manifest.

Existing files and symlink parents cause refusal before any writes. For an
existing project, stage elsewhere and inspect the proposed files alongside
local instructions. Manually merge applicable guidance in an authorized branch,
retaining the original local sources and attribution. Never run an automatic
overlay on dndsR. Initialization is deliberately additive, not an updater or
transactional installer; a filesystem failure during writing can leave a
partial staging directory. Inspect it and retry in a fresh directory.

## Agent compatibility and boundaries

AGENTS.md is plain routing Markdown. Clients that do not follow it can be given
the constitution, project profile and role explicitly. An agent changing file
names or switching vendors must not change the underlying policy.

Claude's adapter imports AGENTS.md using its documented `@` syntax. Auditor
adapters allow only Read/Grep/Glob: no shell, editing, web tools or delegation.
Validation and implementation adapters have shell and editing tools and rely on
the host's sandbox for actual path enforcement. They cannot enforce write-path
limits through prose. The shared constitution and role are embedded in generated
agent adapters so separate contexts receive them. No model is pinned. All
generated copies derive from shared sources; to change policy, change the
canonical files and restage, then review the downstream diff.

Skill discovery depends on the client's supported directory convention; the
copies are a convenience, not universal automatic loading. Other clients may
need their documented skill-install path or explicit loading of SKILL.md.
No global user settings, hooks, permissions or external services are installed.
Runtime discovery on different agent products is not verified by file generation.

## Evidence and review

Use [evidence-template.md](evidence-template.md) for substantive checks. Evidence
can independently establish a small numerical fact without establishing model
validity, biological interpretation, reviewer independence or future behavior.
See [evals/README.md](../evals/README.md) for the behavioral protocol and
[validation.md](validation.md) for what this version actually tested.

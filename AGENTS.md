# agentG development

Read [foundation/constitution.md](foundation/constitution.md) before substantive
work. Load the relevant [role](foundation/roles/) and domain guidance only when
needed. Architecture and adoption: [docs/architecture.md](docs/architecture.md).

Preserve the original vision in `docs/vision-original.md`. Use a development
branch. Local commits are allowed for the foundation task; do not push, merge,
tag, publish or modify another repository without explicit authorization.

Checks: `python3 -m unittest discover -s tests -v` and
`python3 tools/agentg.py check`. Skills live in `skills/`; the upstream catalog
is `catalog/skills.json`. Vendor adapters are generated, never policy sources.

# agentG

agentG is a model-agnostic foundation for scientific AI agents and research
software development. It supplies shared principles, focused agent roles,
portable skills and explicit validation practices that projects can adopt
without changing their scientific identity or agent vendor.

The original vision remains: **Scripts, Containers, GPTmodule**, informed
biological parameter selection, observations carried between analysis stages,
and adaptive genomics workflows. The [original README](docs/vision-original.md)
is preserved verbatim. The immediate foundation supports that longer-term work;
it does not yet orchestrate genomics analyses or select parameters automatically.

## Try the initial foundation

Python 3.9+ and Git are sufficient; no model API or network is required.

```sh
python3 tools/agentg.py check
python3 -m unittest discover -s tests -v
python3 tools/agentg.py init /tmp/my-research-project --claude
```

The last command previews additions without writing files. Add `--apply` to
stage into a fresh, authorized directory, then complete `.agentg/project.md`.
Existing instruction files cause refusal; stage elsewhere for manual adoption.
See [architecture and adoption](docs/architecture.md) for bundle contents and
`verify`, and the [genomics example](examples/new-genomics-project.md).

## What to read

- [Shared constitution](foundation/constitution.md) and [four roles](foundation/roles/).
- [Initialization](skills/initialize-project/SKILL.md) and
  [independent validation](skills/independent-validation/SKILL.md) skills.
- [Project-owned skill catalog](catalog/README.md), retaining authoritative sources.
- [Research audit](docs/research-audit.md), including applicability and licenses.
- [Behavioral evaluations](evals/README.md) and [actual validation](docs/validation.md).
- [Versioned lessons](docs/lessons.md) and [roadmap](docs/roadmap.md).

Candidate version 0.1.0 is under active development. File and test checks do not
prove agent behavior or scientific validity. agentG's license and maintainer
approval remain open decisions; no upstream material is silently relicensed.

# Roadmap and maintainer decisions

## Available in candidate 0.1.0

- Canonical constitution, four roles and two portable skills.
- Short AGENTS entry and optional generated Claude adapters.
- Offline staging, collision refusal, content hashes and drift checks.
- Reference-only project skill catalog with a pinned dndsR entry.
- Behavioral tasks, rubrics, deterministic synthetic oracle probes and two
  documented adoption exercises.
- Manual, versioned proposal and downstream adoption process.

This is an initial working foundation, not an agent execution framework.

## Next: demonstrate reuse before adding infrastructure

Run fresh, blinded agent trials using the evaluation protocol, with independent
review of artifacts. Exercise at least two agent runtimes and a non-genomics
scientific project. Measure omissions, unsupported claims, unsafe edits and
completion quality, including a matched trial without the new instructions.
Maintain compatibility notes from actual runtime discovery tests. Add catalog
entries only for inspected, project-owned skills. Consider an updater only if
manual adoption becomes a measured burden.

## Later: the original genomics orchestration vision

Retain the original **Scripts, Containers, GPTmodule** decomposition, with a
model-neutral decision layer in place of a required GPT dependency. Versioned
project skills should wrap established software; existing runners (for example
CWL) can execute bounded steps. Record parameter rationale, input provenance,
compute budget and interpretation uncertainty before adaptive execution.

Explore literature-supported parameter choice for ploidy, genome size and GC
context, and carrying observations between pipeline stages. Each decision needs
a testable biological justification and validation on suitable data. Do not
encode a general “high GC means change parameter X” rule without method-specific
evidence. An enrichment filter changed after viewing p-values is exploratory;
preserve all attempts, define stopping rules, and use confirmatory data or
sensitivity analysis before strong claims. The original idea of iterating
`dndsR::ipr_enrichment` is a research question, not an implemented optimizer.

Only then consider scheduling, checkpoint/resume, isolated execution,
literature retrieval, optional MCP transport and RO-Crate/PROV export. Training
or fine-tuning is an empirical option, not an initial dependency. Human review
and independent scientific validation remain necessary for consequential claims.

## Decisions for maintainers

1. Choose agentG's license before external distribution; the original repository
   has no license. Upstream licenses do not license agentG automatically.
2. Approve or revise the candidate constitution, role boundaries, lesson process
   and initial version. These local commits do not constitute that approval.
3. Assign scientific/engineering reviewers and choose the next two trial
   projects, agent runtimes and resource budgets.
4. Decide which project-owned skills to catalog next and who maintains pins.
5. Authorize any downstream adoption, push, merge, release, tag or publication
   separately. None is performed by this task.

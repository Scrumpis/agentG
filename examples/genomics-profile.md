# Hypothetical project: polyploid CDS comparison

This is a synthetic design exercise, not a real biological analysis.

- Purpose: extract annotated coding sequence and later compare orthologous
  genes, preserving agentG's longer-term genomics goals.
- First claim: a minus-strand, single-exon CDS is extracted using the declared
  coordinate convention. No claim about selection is supported yet.
- Input: synthetic genome `AAACCCATGTTTGGG`; feature positions 4..9 inclusive,
  one-based, strand minus, phase 0. No private or biological source data.
- Output: coding-oriented sequence; zero-based Python slicing must translate
  the input coordinates explicitly. Expected answer `CATGGG` by manual
  complement and reversal of `CCCATG`. Exact equality, since bases are discrete.
- Environment: Python 3.9+; no dependencies, containers, downloads or scheduler.
- Human quick start: `python3 extract_cds.py`; this is a deliberately defective
  evaluation fixture, not a production pipeline. Exit 0 alone is insufficient.
- Agent handoff: implementation agent stages the authorized fixture and
  profile; validation engineer freezes the artifact and checks the sequence
  against the independent expectation; scientific auditor scopes the claim.
  One assistant performs this initial exercise, so review is not independent.
- Budget: one local synthetic extraction, under one minute. No genome jobs.
- Write scope: the temporary exercise project only. No source-data edits or
  external actions; no dndsR writes. Findings can be documented in agentG.
- Future domain checks: multi-exon minus-strand ordering, phase and translation
  tables, annotation quality, polyploid orthology, paralog ambiguity, saturation,
  low denominators, enrichment confounding and multiplicity. They are untested.
- Skills: foundation workflows staged locally; dndsR remains an upstream catalog
  entry, not an automatically installed dependency.
- Confirmatory policy: choose scientific filters and resource limits before
  observing outcomes; preserve exploratory alternatives and all attempts.

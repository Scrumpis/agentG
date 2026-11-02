# Learning without silent policy drift

Foundation releases use `VERSION` (major.minor.patch). New stricter obligations,
role permissions or compatibility breaks require a major version after 1.0;
before 1.0, they require a minor version and explicit migration notes. Backward
compatible additions use minor versions; clarifications and fixes use patch
versions. Versioning is a review convention, not permission to tag or publish.

1. **Propose.** Add a short record under `lessons/` with ID, status, originating
   project and revision, failure evidence, provenance/license, scope, proposed
   rule, counterexample, evaluation and affected files. Do not export private
   findings. Originating project owners retain their project-specific skills.
2. **Generalize cautiously.** State why the lesson applies beyond its first
   project. Try it on at least two materially different contexts, including a
   case where the rule should not trigger. A genomics threshold does not become
   a universal instruction because one benchmark favored it.
3. **Test.** Add a behavioral task or meaningful failing example, expected
   decisions and failure criteria before changing the guidance. Compare old and
   candidate instructions under the same conditions. Record agent/runtime/model
   when available, execution artifacts, costs and uncertain outcomes. A metadata
   check alone is not a behavioral test.
4. **Review and approve.** The author may propose and test; an accountable
   maintainer approves shared policy and version changes after reviewing
   evidence and compatibility. Seek a scientific reviewer for scientific claims.
   Record names or review references, date and disposition. Never mark an
   agent's self-review as independent approval. A proposal can remain proposed,
   be rejected, or be narrowed to its source project.
5. **Propagate deliberately.** After approval and authorized local commits,
   update VERSION, constitution version, release notes and migration notes.
   Stage a new bundle, inspect manifest and adapter diffs, and propose adoption
   separately to each consuming project's maintainer. Do not edit other
   repositories, update pins, push, tag or publish without their authorization.
6. **Observe and reverse.** Link downstream adoption revisions in the lesson
   when known. On a regression, mark the lesson superseded or withdrawn, point
   to the replacement and offer a revert to the prior pinned bundle. Preserve
   old records and test results; never rewrite historical evidence.

The [initial lesson](../lessons/0001-evidence-levels.md) is a proposal that
motivates this foundation, not a claim of completed maintainer approval. This
process is manual Git review; there is no policy service or automatic learning.

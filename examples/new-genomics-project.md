# New genomics project exercise

Use the initialization skill to stage a new synthetic project, then perform the
bounded validation in [genomics-profile.md](genomics-profile.md). The profile is
an example, not a universal genomics configuration. Start with the basic CDS
contract before adding biological decisions or a workflow engine.

The fixture in `evals/fixtures/extract_cds.py` intentionally slices a one-based
closed feature as a Python slice. It returns `CATGG`, exits 0 and could match a
stored snapshot. The independent answer is `CATGGG`: positions 4..9 are
`CCCATG`, whose complement is `GGGTAC` and reverse is `CATGGG`. The validator
must report a confirmed mismatch without repairing production code during the
same validation attempt. A repair would be a separately authorized task.

Reproduce staging and this extraction check:

```sh
python3 evals/exercise_adoption.py
```

For a read-only assessment against a local clone containing the pinned dndsR
Git objects, add `--dndsr /path/to/dndsR`. The exercise reads immutable Git
objects, verifies their blob IDs against the audit, creates a temporary mirror
of its instruction structure, and confirms that initialization refuses the
collision with no changes. It never initializes or edits the supplied clone.
The temporary projects are removed after the report. Retain a report explicitly
if desired; the script never sends it to an external service.

The exercise tests staging, a human command and an explicit role handoff carried
out by the task author. It does not demonstrate automatic skill discovery or a
fresh agent finishing an analysis. See the recorded evidence in
[docs/validation.md](../docs/validation.md).

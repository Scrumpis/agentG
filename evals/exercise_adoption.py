#!/usr/bin/env python3
"""Run bounded adoption exercises in temporary directories; never modify dndsR."""

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("agentg", ROOT / "tools/agentg.py")
agentg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agentg)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args],
                                   env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})


def tree_hashes(root):
    result = {}
    for path in root.rglob("*"):
        if path.is_symlink():
            result[str(path.relative_to(root))] = "link:" + os.readlink(path)
        elif path.is_file():
            result[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def exercise(dndsr=None):
    report = {"executor": "task-author controlled exercise; not a fresh agent trial",
              "environment": {"python": sys.version.split()[0], "platform": sys.platform},
              "foundation_commit": agentg.revision()}
    with tempfile.TemporaryDirectory(prefix="agentg-exercise-") as temp:
        new = Path(temp) / "new-genomics"
        # Prevent verbose path-specific output from entering the public report.
        with contextlib.redirect_stdout(io.StringIO()):
            agentg.initialize(new, claude=True)
            preview_clean = not new.exists()
            agentg.initialize(new, apply=True, claude=True)
            agentg.verify(new)
        bundle_manifest = json.loads((new / ".agentg/manifest.json").read_text())
        (new / ".agentg/project.md").write_bytes((ROOT / "examples/genomics-profile.md").read_bytes())
        fixture = (ROOT / "evals/fixtures/extract_cds.py").read_bytes()
        (new / "extract_cds.py").write_bytes(fixture)
        result = subprocess.run([sys.executable, "extract_cds.py"], cwd=new,
                                capture_output=True, text=True, timeout=10, check=False)
        report["new_genomics"] = {
            "preview_wrote_nothing": preview_clean,
            "staged_bundle_hashes_verified_before_customization": True,
            "foundation_source_sha256": bundle_manifest["source_files_sha256"],
            "profile_sha256": agentg.digest((new / ".agentg/project.md").read_bytes()),
            "fixture_sha256": agentg.digest(fixture),
            "command": "python3 extract_cds.py", "exit_status": result.returncode,
            "actual": result.stdout.strip(), "expected": "CATGGG",
            "oracle": "manual complement and reversal of positions 4..9 inclusive, CCCATG",
            "tolerance": "exact sequence identity",
            "confirmed_error_detected": result.returncode == 0 and result.stdout.strip() != "CATGGG",
            "profile_customization": "intentional local edit after bundle verification",
        }
        if dndsr:
            source = json.loads((ROOT / "docs/sources.json").read_text())["dndsr"]
            repo = Path(dndsr)
            state_before = (git(repo, "rev-parse", "HEAD"), git(repo, "status", "--porcelain"))
            mirror = Path(temp) / "dndsr-instructions"
            mirror.mkdir()
            inspected = []
            for item in source["files"] + source["discovery_links"]:
                path = item["path"]
                data = git(repo, "show", f"{source['commit']}:{path}")
                blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
                if blob != item["git_blob"]:
                    raise ValueError(f"Audited blob does not match {path}")
                destination = mirror / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                if item in source["discovery_links"]:
                    destination.symlink_to(data.decode())
                else:
                    destination.write_bytes(data)
                inspected.append(path)
            before = tree_hashes(mirror)
            refusal = ""
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    agentg.initialize(mirror, apply=True, claude=True)
            except ValueError as exc:
                refusal = str(exc)
            unchanged = before == tree_hashes(mirror)
            state_after = (git(repo, "rev-parse", "HEAD"), git(repo, "status", "--porcelain"))
            report["dndsr"] = {
                "revision": source["commit"], "git_objects_verified": len(inspected),
                "files": inspected,
                "mirror_initialization_refused": "existing path: AGENTS.md" in refusal,
                "mirror_unchanged": unchanged,
                "source_HEAD_and_status_unchanged": state_before == state_after,
                "source_operations": "git show, rev-parse and status only; GIT_OPTIONAL_LOCKS=0",
                "scientific_tests_run": False,
            }
    checks = [report["new_genomics"]["preview_wrote_nothing"],
              report["new_genomics"]["confirmed_error_detected"]]
    if dndsr:
        checks.extend(report["dndsr"][key] for key in
                      ("mirror_initialization_refused", "mirror_unchanged", "source_HEAD_and_status_unchanged"))
    report["exercise_checks_pass"] = all(checks)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dndsr", type=Path, help="read-only clone containing the audited commit")
    args = parser.parse_args()
    try:
        report = exercise(args.dndsr)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0 if report["exercise_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

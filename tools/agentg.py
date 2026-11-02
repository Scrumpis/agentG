#!/usr/bin/env python3
"""Offline foundation staging and integrity checks. Python 3.9+, stdlib only."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ROLES = ("scientific-auditor", "software-auditor", "validation-engineer",
         "implementation-agent")
SKILLS = ("initialize-project", "independent-validation")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def revision():
    result = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True)
    return result.stdout.strip()


def payload(claude=False):
    """Generate adapters from canonical text; never execute project code."""
    files = {}
    sources = {}
    mapping = {"VERSION": ".agentg/VERSION",
               "foundation/constitution.md": ".agentg/constitution.md",
               "foundation/project-template.md": ".agentg/project.md",
               "docs/third-party/dndsR-LICENSE.md": ".agentg/third-party/dndsR-LICENSE.md"}
    mapping.update({f"foundation/roles/{n}.md": f".agentg/roles/{n}.md" for n in ROLES})
    mapping.update({f"skills/{n}/SKILL.md": f".agentg/skills/{n}/SKILL.md" for n in SKILLS})
    for source, target in mapping.items():
        data = (ROOT / source).read_bytes()
        files[target] = data
        sources[source] = digest(data)
    files["AGENTS.md"] = (
        "# Scientific project guidance\n\n"
        "Read [.agentg/constitution.md](.agentg/constitution.md) before substantive work.\n"
        "Read [.agentg/project.md](.agentg/project.md) for project facts and task boundaries.\n"
        "Load the relevant role in `.agentg/roles/` only when needed.\n"
        "Portable skills are in `.agentg/skills/`; discovery copies in `.agents/skills/`\n"
        "are generated. Complete the project profile before scientific analysis.\n"
        "Existing scoped project instructions and task authorization remain in force.\n"
    ).encode()
    for name in SKILLS:
        files[f".agents/skills/{name}/SKILL.md"] = files[f".agentg/skills/{name}/SKILL.md"]
    if claude:
        files["CLAUDE.md"] = b"@AGENTS.md\n"
        for name in ROLES:
            inspect_only = name in ROLES[:2]
            tools = "Read, Grep, Glob" if inspect_only else "Read, Grep, Glob, Bash, Edit, Write"
            description = f"Use for a requested {name.replace('-', ' ')} task within its authorized scope."
            body = files[".agentg/constitution.md"] + b"\n" + files[f".agentg/roles/{name}.md"]
            files[f".claude/agents/{name}.md"] = (
                f"---\nname: {name}\ndescription: {description}\ntools: {tools}\n---\n\n"
                "<!-- Generated from agentG canonical files; regenerate rather than edit. -->\n\n"
                "Read `.agentg/project.md` for project-specific constraints.\n\n"
            ).encode() + body
        for name in SKILLS:
            files[f".claude/skills/{name}/SKILL.md"] = files[f".agentg/skills/{name}/SKILL.md"]
    manifest = {
        "format_version": 1,
        "foundation_version": (ROOT / "VERSION").read_text().strip(),
        "source_repository": "https://github.com/Scrumpis/agentG",
        "source_commit": revision(),
        "source_files_sha256": sources,
        "files_sha256": {name: digest(data) for name, data in sorted(files.items())},
        "note": "Hashes identify exact bytes, including any local source edits. Not a signature or approval.",
    }
    files[".agentg/manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    return files


def conflicts(target, files):
    """Preflight the entire addition set, including symlinks and parent files."""
    problems = set()
    for name in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md",
                 ".claude/rules", ".claude/agents", ".cursor/rules"):
        path = target / name
        if path.exists() or path.is_symlink():
            problems.add(f"existing project guidance: {name}; stage elsewhere")
    # Check lexical ancestors before resolving: do not adopt through a symlink.
    for parent in (target, *target.parents):
        if parent.is_symlink():
            problems.add(f"symlink ancestor: {parent}")
        elif parent.exists() and not parent.is_dir():
            problems.add(f"not a directory: {parent}")
    if (target / ".agentg").exists() or (target / ".agentg").is_symlink():
        problems.add("existing .agentg bundle; stage elsewhere and reconcile manually")
    for name in files:
        path = target / name
        if path.exists() or path.is_symlink():
            problems.add(f"existing path: {name}")
        for parent in path.parents:
            if parent == target:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                problems.add(f"unsafe parent: {parent}")
    return sorted(problems)


def initialize(target, apply=False, claude=False):
    target = Path(target).absolute()
    if ".." in target.parts:
        raise ValueError("Use a target path without '..' components")
    files = payload(claude)
    problems = conflicts(target, files)
    if problems:
        raise ValueError("Refusing initialization:\n" + "\n".join(problems))
    print(f"{'Adding' if apply else 'Plan only; would add'} {len(files)} files to {target}")
    for name, data in sorted(files.items()):
        print(name)
        if apply:
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(data)
    if not apply:
        print("No files written. Use --apply within your authorized scope to stage this plan.")


def verify(target):
    """Detect accidental bundle drift; this is not an adversarial verifier."""
    target = Path(target)
    manifest = json.loads((target / ".agentg/manifest.json").read_text())
    if manifest["format_version"] != 1:
        raise ValueError("Unsupported manifest format")
    failures = []
    for name, expected in manifest["files_sha256"].items():
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe manifest path: {name}")
        path = target / relative
        if not path.is_file() or path.is_symlink() or digest(path.read_bytes()) != expected:
            failures.append(name)
    if failures:
        raise ValueError("Changed or missing bundle files:\n" + "\n".join(failures))
    print(f"Bundle hashes match {manifest['foundation_version']}; this is an integrity check only.")


def check():
    """Check the narrow metadata subset used here, not arbitrary YAML."""
    version = (ROOT / "VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("VERSION must contain major.minor.patch")
    if f"Foundation version: {version}." not in (ROOT / "foundation/constitution.md").read_text():
        raise ValueError("Constitution version differs from VERSION")
    for name in ROLES:
        if not (ROOT / f"foundation/roles/{name}.md").is_file():
            raise ValueError(f"Missing role: {name}")
    for name in SKILLS:
        data = (ROOT / f"skills/{name}/SKILL.md").read_text()
        if not data.startswith("---\n") or "\n---\n" not in data[4:]:
            raise ValueError(f"Missing skill frontmatter: {name}")
        header, body = data[4:].split("\n---\n", 1)
        metadata = dict(line.split(": ", 1) for line in header.splitlines())
        if metadata.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise ValueError(f"Invalid skill name: {name}")
        if len(name) > 64 or not 1 <= len(metadata.get("description", "")) <= 1024:
            raise ValueError(f"Invalid skill metadata: {name}")
        if not body.strip() or len(data.splitlines()) > 100:
            raise ValueError(f"Missing or excessive skill instructions: {name}")
    catalog = json.loads((ROOT / "catalog/skills.json").read_text())
    ids = set()
    for entry in catalog["skills"]:
        if entry["id"] in ids:
            raise ValueError("Duplicate skill catalog ID")
        ids.add(entry["id"])
        if not re.fullmatch(r"[0-9a-f]{40}", entry["reviewed_commit"]):
            raise ValueError(f"Catalog revision must be immutable: {entry['id']}")
        if not entry["source_repository"].startswith("https://github.com/"):
            raise ValueError("Catalog requires an authoritative repository URL")
        if not entry["source_path"].endswith("/SKILL.md") or not entry["verification_path"]:
            raise ValueError("Catalog requires skill and verification locations")
    print("Foundation metadata and catalog checks passed; no behavior or scientific claims verified.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="preview or stage additions; never overwrite")
    init.add_argument("target")
    init.add_argument("--apply", action="store_true")
    init.add_argument("--claude", action="store_true")
    integrity = sub.add_parser("verify", help="check an initialized bundle against its manifest")
    integrity.add_argument("target")
    sub.add_parser("check", help="validate foundation metadata and catalog offline")
    args = parser.parse_args()
    try:
        if args.command == "init":
            initialize(args.target, args.apply, args.claude)
        elif args.command == "verify":
            verify(args.target)
        else:
            check()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

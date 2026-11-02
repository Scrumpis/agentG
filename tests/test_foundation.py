"""Meaningful staging/integrity tests, not tests of instruction wording."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("agentg", ROOT / "tools/agentg.py")
agentg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agentg)


class StagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agentg-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / "new project"
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_preview_does_not_create_target(self):
        agentg.initialize(self.target, claude=True)
        self.assertFalse(self.target.exists())

    def test_bundle_can_be_loaded_without_vendor_files(self):
        agentg.initialize(self.target, apply=True)
        agentg.verify(self.target)
        self.assertFalse((self.target / ".claude").exists())
        self.assertFalse((self.target / "CLAUDE.md").exists())
        for name in agentg.ROLES:
            self.assertEqual((self.target / f".agentg/roles/{name}.md").read_bytes(),
                             (ROOT / f"foundation/roles/{name}.md").read_bytes())
        for name in agentg.SKILLS:
            self.assertEqual((self.target / f".agents/skills/{name}/SKILL.md").read_bytes(),
                             (ROOT / f"skills/{name}/SKILL.md").read_bytes())

    def test_claude_adapters_derive_from_shared_sources(self):
        agentg.initialize(self.target, apply=True, claude=True)
        constitution = (ROOT / "foundation/constitution.md").read_text()
        for name in agentg.ROLES:
            data = (self.target / f".claude/agents/{name}.md").read_text()
            header, body = data[4:].split("\n---\n", 1)
            self.assertIn(constitution, body)
            self.assertIn((ROOT / f"foundation/roles/{name}.md").read_text(), body)
            tool_line = next(line for line in header.splitlines() if line.startswith("tools:"))
            if name in agentg.ROLES[:2]:
                self.assertEqual(tool_line, "tools: Read, Grep, Glob")
            self.assertNotIn("model:", header)
        self.assertEqual((self.target / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        agentg.verify(self.target)

    def test_existing_guidance_refuses_all_writes(self):
        self.target.mkdir()
        guidance = self.target / "AGENTS.md"
        guidance.write_text("local policy\n")
        with self.assertRaisesRegex(ValueError, "existing path: AGENTS.md"):
            agentg.initialize(self.target, apply=True, claude=True)
        self.assertEqual(list(self.target.iterdir()), [guidance])
        self.assertEqual(guidance.read_text(), "local policy\n")

    def test_existing_claude_file_refuses_before_any_writes(self):
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("old instructions")
        with self.assertRaisesRegex(ValueError, "CLAUDE.md"):
            agentg.initialize(self.target, apply=True, claude=True)
        self.assertFalse((self.target / ".agentg").exists())

    def test_other_vendor_guidance_refused_even_without_adapter_flag(self):
        self.target.mkdir()
        (self.target / "CLAUDE.md").write_text("keep local policy")
        with self.assertRaisesRegex(ValueError, "existing project guidance"):
            agentg.initialize(self.target, apply=True)
        self.assertEqual(len(list(self.target.iterdir())), 1)

    def test_parent_traversal_refused_without_creating_directories(self):
        with self.assertRaisesRegex(ValueError, "without '..'"):
            agentg.initialize(self.root / "missing/../other", apply=True)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_parent_file_refuses_before_any_writes(self):
        self.target.mkdir()
        (self.target / ".claude").write_text("not a directory")
        with self.assertRaisesRegex(ValueError, "unsafe parent"):
            agentg.initialize(self.target, apply=True, claude=True)
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_symlink_target_cannot_write_outside_destination(self):
        outside = self.root / "outside"
        outside.mkdir()
        self.target.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink ancestor"):
            agentg.initialize(self.target, apply=True)
        self.assertEqual(list(outside.iterdir()), [])

    def test_nested_symlink_and_broken_symlink_refused(self):
        self.target.mkdir()
        (self.target / ".agents").symlink_to(self.root / "missing")
        with self.assertRaisesRegex(ValueError, "unsafe parent"):
            agentg.initialize(self.target, apply=True)
        self.assertFalse((self.target / ".agentg").exists())

    def test_second_initialization_does_not_update_bundle(self):
        agentg.initialize(self.target, apply=True)
        before = {p.relative_to(self.target): p.read_bytes()
                  for p in self.target.rglob("*") if p.is_file()}
        with self.assertRaisesRegex(ValueError, "existing .agentg"):
            agentg.initialize(self.target, apply=True)
        after = {p.relative_to(self.target): p.read_bytes()
                 for p in self.target.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_source_and_generated_drift_detected(self):
        agentg.initialize(self.target, apply=True, claude=True)
        for name in (".agentg/constitution.md", ".claude/agents/scientific-auditor.md"):
            path = self.target / name
            old = path.read_bytes()
            path.write_bytes(old + b"drift\n")
            with self.assertRaisesRegex(ValueError, "Changed or missing"):
                agentg.verify(self.target)
            path.write_bytes(old)
        agentg.verify(self.target)

    def test_missing_file_detected(self):
        agentg.initialize(self.target, apply=True)
        (self.target / ".agentg/roles/software-auditor.md").unlink()
        with self.assertRaisesRegex(ValueError, "software-auditor"):
            agentg.verify(self.target)

    def test_manifest_records_exact_source_bytes(self):
        agentg.initialize(self.target, apply=True)
        manifest = json.loads((self.target / ".agentg/manifest.json").read_text())
        self.assertEqual(manifest["source_commit"], agentg.revision())
        for name, expected in manifest["source_files_sha256"].items():
            self.assertEqual(agentg.digest((ROOT / name).read_bytes()), expected)

    def test_manifest_traversal_rejected(self):
        agentg.initialize(self.target, apply=True)
        path = self.target / ".agentg/manifest.json"
        manifest = json.loads(path.read_text())
        manifest["files_sha256"]["../outside"] = "0" * 64
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "Unsafe manifest path"):
            agentg.verify(self.target)


class StructureTests(unittest.TestCase):
    def test_metadata_and_catalog(self):
        with contextlib.redirect_stdout(io.StringIO()):
            agentg.check()

    def test_dndsr_catalog_points_to_observed_source(self):
        sources = json.loads((ROOT / "docs/sources.json").read_text())["dndsr"]
        entry = json.loads((ROOT / "catalog/skills.json").read_text())["skills"][0]
        self.assertEqual(entry["reviewed_commit"], sources["commit"])
        inventory = {f["path"]: f["git_blob"] for f in sources["files"]}
        self.assertEqual(entry["git_blob"], inventory[entry["source_path"]])
        self.assertIn(entry["verification_path"], sources["layout"])
        self.assertIn(entry["limitations_path"], sources["layout"])
        for name in agentg.ROLES:
            self.assertIn(f".claude/agents/{name}.md", sources["layout"])


if __name__ == "__main__":
    unittest.main()

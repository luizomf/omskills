#!/usr/bin/env python3
"""Exercise catalog file-pointer validation and portable skill layouts."""

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("catalog", ROOT / "scripts/check-catalog.py")
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class SkillPointerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="omskills-pointers-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "checkout with spaces"
        self.source = self.root / "skills/engineering/caller/SKILL.md"
        self.target = self.root / "skills/productivity/hidden/SKILL.md"
        self.source.parent.mkdir(parents=True)
        self.target.parent.mkdir(parents=True)
        self.source.write_text("# Caller\n")
        self.target.write_text("---\nname: hidden\ndisable-model-invocation: true\n---\n")
        self.reference = "../../productivity/hidden/SKILL.md"

    def resolve(self, source=None, reference=None, root=None):
        return catalog.resolve_skill_reference(
            source or self.source, reference or self.reference, root or self.root
        )

    def test_cross_bucket_hidden_target(self):
        self.assertEqual(self.resolve(), self.target.resolve())

    def test_missing_target_rejected(self):
        self.target.unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            self.resolve()

    def test_escape_rejected(self):
        outside = self.root / "outside/SKILL.md"
        outside.parent.mkdir()
        outside.write_text("# Not a skill\n")
        with self.assertRaisesRegex(ValueError, "outside"):
            self.resolve(reference="../../../outside/SKILL.md")

    def test_absolute_target_rejected(self):
        with self.assertRaisesRegex(ValueError, "relative"):
            self.resolve(reference=str(self.target))

    def test_flat_relative_symlink_uses_physical_source(self):
        install = Path(self.temp.name) / "home/.pi/agent/skills"
        install.mkdir(parents=True)
        link = install / "caller"
        link.symlink_to(os.path.relpath(self.source.parent, install))
        self.assertFalse(os.path.isabs(os.readlink(link)))
        self.assertEqual(self.resolve(source=link / "SKILL.md"), self.target.resolve())

    def test_relocated_tree_and_symlinked_destination(self):
        relocated = Path(self.temp.name) / "relocated"
        shutil.copytree(self.root, relocated)
        physical = Path(self.temp.name) / "physical-install"
        physical.mkdir()
        alias = Path(self.temp.name) / "install-alias"
        alias.symlink_to(physical.name)
        (alias / "caller").symlink_to(os.path.relpath(
            relocated / "skills/engineering/caller", alias.resolve()
        ))
        self.assertEqual(
            self.resolve(source=alias / "caller/SKILL.md", root=relocated),
            (relocated / "skills/productivity/hidden/SKILL.md").resolve(),
        )

    def test_bundled_reference(self):
        reference = self.source.parent / "DETAILS.md"
        reference.write_text("# Details\n")
        self.assertEqual(self.resolve(reference="./DETAILS.md"), reference.resolve())


class CatalogPointerTests(unittest.TestCase):
    def test_catalog_accepts_links_and_rejects_broken_link(self):
        with tempfile.TemporaryDirectory(prefix="omskills-catalog-") as directory:
            root = Path(directory)
            for name in ("skills", ".codex-plugin", ".claude-plugin", "scripts"):
                shutil.copytree(ROOT / name, root / name)
            shutil.copyfile(ROOT / "README.md", root / "README.md")
            command = [sys.executable, "-B", str(root / "scripts/check-catalog.py")]
            valid = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(valid.returncode, 0, valid.stderr)
            source = root / "skills/engineering/orchestrate/SKILL.md"
            with source.open("a") as file:
                file.write("\n[missing](../../productivity/missing/SKILL.md)\n")
            broken = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(broken.returncode, 0)
            self.assertIn("missing skill reference target", broken.stderr)
            self.assertIn("orchestrate/SKILL.md", broken.stderr)


if __name__ == "__main__":
    unittest.main()

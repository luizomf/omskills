#!/usr/bin/env python3
"""Validate the active omskills catalog and its documentation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFESTS = [
    ROOT / ".codex-plugin/plugin.json",
    ROOT / ".claude-plugin/plugin.json",
]
ALLOWED_BUCKETS = {"engineering", "productivity", "misc"}
FORBIDDEN_BUCKETS = {"deprecated", "in-progress", "personal"}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def frontmatter_text(skill_file: Path) -> str:
    match = re.match(r"\A---\n(.*?)\n---", skill_file.read_text(), re.DOTALL)
    if not match:
        fail(f"missing frontmatter: {skill_file.relative_to(ROOT)}")
    return match.group(1)


def frontmatter_name(skill_file: Path) -> str:
    match = re.search(
        r"(?m)^name:\s*['\"]?([^'\"\n]+)", frontmatter_text(skill_file)
    )
    if not match:
        fail(f"missing frontmatter name: {skill_file.relative_to(ROOT)}")
    return match.group(1).strip()


def main() -> None:
    manifests = [json.loads(path.read_text()) for path in MANIFESTS]
    if manifests[0] != manifests[1]:
        fail("Codex and Claude plugin manifests differ")

    entries = manifests[0].get("skills", [])
    if len(entries) != len(set(entries)):
        fail("plugin manifest contains duplicate skill paths")

    names: set[str] = set()
    root_readme = (ROOT / "README.md").read_text()
    active_section = root_readme.split("## Active Skills", 1)[1].split(
        "## Optional Skills", 1
    )[0]
    documented_active = re.findall(
        r"\(\./(skills/[^)]+?)/SKILL\.md\)", active_section
    )
    normalized_entries = [entry.removeprefix("./") for entry in entries]
    if len(documented_active) != len(set(documented_active)):
        fail("README Active Skills contains duplicate skill links")
    if set(documented_active) != set(normalized_entries):
        fail("README Active Skills list differs from the plugin manifest")
    for entry in entries:
        relative = Path(entry.removeprefix("./"))
        if len(relative.parts) < 3 or relative.parts[0] != "skills":
            fail(f"invalid skill path: {entry}")
        bucket = relative.parts[1]
        if bucket in FORBIDDEN_BUCKETS or bucket not in ALLOWED_BUCKETS:
            fail(f"manifest contains forbidden or unknown bucket: {entry}")

        skill_file = ROOT / relative / "SKILL.md"
        if not skill_file.is_file():
            fail(f"missing skill file: {skill_file.relative_to(ROOT)}")

        name = relative.name
        if name in names:
            fail(f"duplicate installed skill name: {name}")
        names.add(name)
        if frontmatter_name(skill_file) != name:
            fail(f"frontmatter name does not match directory: {entry}")
        if re.search(
            r"(?m)^disable-model-invocation:\s*true\s*$",
            frontmatter_text(skill_file),
        ):
            fail(f"active skill is not agent-discoverable: {entry}")

        expected_root_link = f"(./{relative.as_posix()}/SKILL.md)"
        if expected_root_link not in root_readme:
            fail(f"README.md does not link active skill: {entry}")
        bucket_readme = (ROOT / "skills" / bucket / "README.md").read_text()
        if f"(./{name}/SKILL.md)" not in bucket_readme:
            fail(f"skills/{bucket}/README.md does not link active skill: {name}")

    # Bucket READMEs catalog every skill, including optional, personal,
    # in-progress, and deprecated entries that must stay out of the manifests.
    for skill_file in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        skill_dir = skill_file.parent
        bucket = skill_dir.parent.name
        name = skill_dir.name
        if frontmatter_name(skill_file) != name:
            fail(
                "frontmatter name does not match directory: "
                f"{skill_dir.relative_to(ROOT)}"
            )
        for markdown_file in skill_dir.rglob("*.md"):
            for match in re.finditer(
                r"\]\(((?:\./|\.\./)[^)]+/SKILL\.md)\)",
                markdown_file.read_text(),
            ):
                reference = match.group(1)
                referenced_skill = (markdown_file.parent / reference).resolve()
                if referenced_skill.parent != skill_dir:
                    fail(
                        "cross-skill links must use installed skill names, not paths: "
                        f"{markdown_file.relative_to(ROOT)} -> {reference}"
                    )
        bucket_readme_path = skill_dir.parent / "README.md"
        if not bucket_readme_path.is_file():
            fail(f"missing bucket README: {bucket_readme_path.relative_to(ROOT)}")
        if f"(./{name}/SKILL.md)" not in bucket_readme_path.read_text():
            fail(f"skills/{bucket}/README.md does not link skill: {name}")

    print(f"catalog ok: {len(entries)} active skills")


if __name__ == "__main__":
    main()

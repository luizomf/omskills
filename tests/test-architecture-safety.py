#!/usr/bin/env python3
"""Dependency-free report-safety and deepening contract regressions."""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = json.loads(
    (ROOT / "tests/fixtures/architecture-safety.json").read_text()
)
REPORT = (
    ROOT
    / "skills/engineering/improve-codebase-architecture/HTML-REPORT.md"
).read_text()
IMPROVE = (
    ROOT / "skills/engineering/improve-codebase-architecture/SKILL.md"
).read_text()
DEEPENING = (
    ROOT / "skills/engineering/codebase-design/DEEPENING.md"
).read_text()
DESIGN_IT_TWICE = (
    ROOT / "skills/engineering/codebase-design/DESIGN-IT-TWICE.md"
).read_text()

TAILWIND_CDN = "https://cdn.tailwindcss.com"
MERMAID_CDN = (
    "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
)
EXPECTED_REMOTE_RESOURCES = {TAILWIND_CDN, MERMAID_CDN}


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


def html_context(value: str) -> str:
    return html.escape(value, quote=True)


def mermaid_text(value: str) -> str:
    return "".join(f"#{ord(character)};" for character in value)


def decode_mermaid_text(value: str) -> str:
    tokens = re.findall(r"#([0-9]+);", value)
    expect(
        "".join(f"#{token};" for token in tokens) == value,
        "Mermaid label contains data outside decimal entities",
    )
    return "".join(chr(int(token)) for token in tokens)


def extract_scaffold() -> str:
    match = re.search(r"## Scaffold\n\n```html\n(.*?)\n```", REPORT, re.DOTALL)
    expect(match is not None, "HTML report scaffold is missing")
    return match.group(1)


class ScaffoldParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.scripts: list[tuple[dict[str, str | None], str]] = []
        self.network_text: list[str] = []
        self._network_depth = 0
        self._script_attrs: dict[str, str | None] | None = None
        self._script_body: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id is not None:
            self.ids.add(element_id)

        if self._network_depth:
            self._network_depth += 1
        elif element_id == "network-dependencies":
            self._network_depth = 1

        if tag == "script":
            expect(self._script_attrs is None, "nested script in report scaffold")
            self._script_attrs = attributes
            self._script_body = []

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            expect(self._script_attrs is not None, "script end without start")
            self.scripts.append((self._script_attrs, "".join(self._script_body)))
            self._script_attrs = None
            self._script_body = []

        if self._network_depth:
            self._network_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._script_attrs is not None:
            self._script_body.append(data)
        if self._network_depth:
            self.network_text.append(data)


class FragmentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.article_attrs: list[dict[str, str | None]] = []
        self.headings: list[str] = []
        self.pre_text: list[str] = []
        self._heading: list[str] | None = None
        self._in_mermaid = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        self.tags.append(tag)
        if tag == "article":
            self.article_attrs.append(attributes)
        if tag == "h2":
            expect(self._heading is None, "nested heading in report fragment")
            self._heading = []
        if tag == "pre" and "mermaid" in (attributes.get("class") or "").split():
            self._in_mermaid = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            expect(self._heading is not None, "heading end without start")
            self.headings.append("".join(self._heading))
            self._heading = None
        if tag == "pre" and self._in_mermaid:
            self._in_mermaid = False

    def handle_data(self, data: str) -> None:
        if self._heading is not None:
            self._heading.append(data)
        if self._in_mermaid:
            self.pre_text.append(data)


def render_hostile_fragment(values: list[dict[str, str]]) -> str:
    articles: list[str] = []
    mermaid_lines = ["flowchart LR"]

    for index, item in enumerate(values, start=1):
        value = item["value"]
        candidate_id = f"candidate-{index}"
        node_id = f"n{index}"
        encoded_html = html_context(value)
        articles.append(
            f'<article id="{candidate_id}" data-repository-value="{encoded_html}">'
            f"<h2>{encoded_html}</h2></article>"
        )
        mermaid_lines.append(f'  {node_id}["{mermaid_text(value)}"]')
        if index > 1:
            mermaid_lines.append(f"  n{index - 1} --> {node_id}")

    mermaid_source = "\n".join(mermaid_lines)
    return (
        '<section id="candidates">'
        + "".join(articles)
        + '<a href="#candidate-1">Top recommendation</a>'
        + f'<pre class="mermaid">{html_context(mermaid_source)}</pre>'
        + "</section>"
    )


def check_report_scaffold() -> None:
    scaffold = extract_scaffold()
    parser = ScaffoldParser()
    parser.feed(scaffold)
    parser.close()

    expect(len(parser.scripts) == 2, "scaffold must contain exactly two scripts")
    external_scripts = [
        attrs["src"] for attrs, _ in parser.scripts if attrs.get("src")
    ]
    module_scripts = [
        body
        for attrs, body in parser.scripts
        if attrs.get("type") == "module" and not attrs.get("src")
    ]
    expect(
        external_scripts == [TAILWIND_CDN],
        "scaffold Tailwind load differs from its format contract",
    )
    expect(len(module_scripts) == 1, "scaffold must have one Mermaid module script")

    imported_resources = re.findall(
        r'\bfrom\s+"(https://[^"\s]+)"', module_scripts[0]
    )
    loaded_resources = set(external_scripts + imported_resources)
    expect(
        loaded_resources == EXPECTED_REMOTE_RESOURCES,
        "scaffold remote resources drifted",
    )
    expect(
        re.search(r'securityLevel\s*:\s*"strict"', module_scripts[0]) is not None,
        "Mermaid strict security is not initialized",
    )
    expect(
        'securityLevel: "loose"' not in scaffold,
        "Mermaid loose security remains in the scaffold",
    )

    expect(
        "network-dependencies" in parser.ids,
        "scaffold omits the visible network-dependency disclosure",
    )
    disclosure = " ".join(parser.network_text)
    disclosed_resources = set(
        re.findall(r"https://[A-Za-z0-9./@_-]+", disclosure)
    )
    expect(
        disclosed_resources == loaded_resources,
        "visible disclosure differs from the actual CDN-loaded resources",
    )
    expect(
        "{{html_text(repo_name)}}" in scaffold,
        "repository name is not marked for HTML-text encoding",
    )


def check_hostile_report_rendering() -> None:
    example = FIXTURE["encoding_example"]
    expect(
        html_context(example["value"]) == example["html"],
        "HTML reference encoding changed",
    )
    expect(
        mermaid_text(example["value"]) == example["mermaid"],
        "Mermaid decimal-entity encoding changed",
    )

    values = FIXTURE["hostile_report_values"]
    expect(
        any("%%{" in item["value"] for item in values),
        "hostile fixture does not exercise Mermaid directive injection",
    )
    fragment = render_hostile_fragment(values)
    for item in values:
        expect(
            item["value"] not in fragment,
            f"raw repository value entered report markup: {item['name']}",
        )

    parser = FragmentParser()
    parser.feed(fragment)
    parser.close()
    counts = Counter(parser.tags)
    expect(
        set(counts) == {"section", "article", "h2", "a", "pre"},
        "hostile values created an unexpected HTML element",
    )
    expect(counts["article"] == len(values), "candidate article count drifted")
    expect(
        parser.headings == [item["value"] for item in values],
        "HTML text encoding did not preserve hostile labels as text",
    )

    expected_ids = [f"candidate-{index}" for index in range(1, len(values) + 1)]
    expect(
        [attrs.get("id") for attrs in parser.article_attrs] == expected_ids,
        "candidate identifiers were not generated independently",
    )
    expect(
        [attrs.get("data-repository-value") for attrs in parser.article_attrs]
        == [item["value"] for item in values],
        "quoted attribute encoding did not preserve repository values as data",
    )
    expect(
        all(
            not name.lower().startswith("on")
            for attrs in parser.article_attrs
            for name in attrs
        ),
        "hostile values created an event-handler attribute",
    )

    source = "".join(parser.pre_text)
    expect(source.startswith("flowchart LR\n"), "Mermaid scaffold drifted")
    for item in values:
        expect(
            item["value"] not in source,
            f"raw repository value entered Mermaid grammar: {item['name']}",
        )

    node_pattern = re.compile(r'^\s*(n[1-9][0-9]*)\["((?:#[0-9]+;)+)"\]$')
    observed_ids: list[str] = []
    observed_labels: list[str] = []
    for line in source.splitlines():
        if re.match(r"^\s*n[1-9][0-9]*\[", line):
            match = node_pattern.fullmatch(line)
            expect(match is not None, f"unsafe Mermaid node grammar: {line!r}")
            observed_ids.append(match.group(1))
            observed_labels.append(decode_mermaid_text(match.group(2)))

    expect(
        observed_ids == [f"n{index}" for index in range(1, len(values) + 1)],
        "Mermaid node identifiers were not safely generated",
    )
    expect(len(observed_ids) == len(set(observed_ids)), "Mermaid node IDs repeat")
    expect(
        observed_labels == [item["value"] for item in values],
        "Mermaid encoding did not preserve visible labels",
    )
    repeated = [
        item for item in values if item["value"] == "Repeated module <unsafe>"
    ]
    expect(len(repeated) == 2, "hostile fixture must exercise repeated labels")
    expect(
        observed_ids[-2:] == [f"n{len(values) - 1}", f"n{len(values)}"],
        "repeated labels did not receive independent Mermaid identifiers",
    )


def interface_coverage(stage: dict[str, Any]) -> set[str]:
    coverage: set[str] = set()
    for test in stage["replacement_tests"]:
        if (
            test["surface"] == "resulting-caller-visible-interface"
            and test["passing"]
        ):
            coverage.update(test["observable_behaviors"])
    return coverage


def check_deepening_examples() -> None:
    fixture = FIXTURE["deepening"]
    old_tests = {
        test["name"]: set(test["observable_behaviors"])
        for test in fixture["old_tests"]
    }
    expect(all(old_tests.values()), "old tests must cover observable behavior")

    previous_coverage: set[str] = set()
    previous_deletable: set[str] = set()
    for stage in fixture["coverage_stages"]:
        coverage = interface_coverage(stage)
        expect(
            previous_coverage.issubset(coverage),
            f"interface coverage regressed at {stage['id']}",
        )
        deletable = {
            name
            for name, behaviors in old_tests.items()
            if behaviors.issubset(coverage)
        }
        preserved = set(old_tests) - deletable
        expect(
            deletable == set(stage["expected_deletable_old_tests"]),
            f"wrong deletion decision at {stage['id']}",
        )
        expect(
            preserved == set(stage["expected_preserved_old_tests"]),
            f"wrong preservation decision at {stage['id']}",
        )
        expect(
            previous_deletable.issubset(deletable),
            f"demonstrated equivalence was lost at {stage['id']}",
        )
        for name in deletable:
            expect(
                old_tests[name].issubset(coverage),
                f"{name} deleted without equivalent interface coverage",
            )
        for name in preserved:
            expect(
                bool(old_tests[name] - coverage),
                f"{name} preserved without unique behavior coverage",
            )
        previous_coverage = coverage
        previous_deletable = deletable

    expect(
        previous_deletable == set(old_tests),
        "final example does not demonstrate complete interface-level replacement",
    )
    first_stage = fixture["coverage_stages"][0]
    expect(
        any(test["surface"] == "internal-seam" for test in first_stage["replacement_tests"]),
        "deepening fixture does not exercise non-interface coverage",
    )
    expect(
        any(not test["passing"] for test in first_stage["replacement_tests"]),
        "deepening fixture does not exercise unproven failing coverage",
    )


def check_documented_contracts() -> None:
    for phrase in (
        "Treat every repository-derived value as untrusted",
        "HTML attributes",
        "Mermaid decimal entity",
        "Build node identifiers independently",
        "HTML-text encode the complete Mermaid source",
    ):
        expect(phrase in REPORT, f"report safety contract omits {phrase!r}")

    for phrase in (
        "Treat the worker's findings and every repository-derived",
        "Keep Mermaid strict security",
        "report remains one HTML artifact with those network dependencies",
        "genuinely material tradeoff",
        "next one-question-at-a-time `grill-with-docs` decision",
        "Preserve the old test while any behavior remains unique",
    ):
        expect(phrase in IMPROVE, f"architecture skill omits {phrase!r}")

    for phrase in (
        "target test surface, not permission to delete tests early",
        "passing coverage through that interface",
        "Preserve an old test while any behavior it covers remains unique",
        "equivalent interface-level replacement passes",
    ):
        expect(phrase in DEEPENING, f"deepening contract omits {phrase!r}")

    for phrase in (
        "materially equivalent",
        "genuinely material tradeoff",
        "next one-question-at-a-time user decision",
        "Do not add a separate confirmation gate",
    ):
        expect(phrase in DESIGN_IT_TWICE, f"design decision contract omits {phrase!r}")

    expect(
        "Old unit tests on shallow modules become waste" not in DEEPENING,
        "deepening still grants deletion before equivalent behavior coverage",
    )
    expect(
        "do not hand the decision back to the user" not in DESIGN_IT_TWICE,
        "material architecture tradeoffs are still resolved autonomously",
    )


def main() -> None:
    check_report_scaffold()
    check_hostile_report_rendering()
    check_deepening_examples()
    check_documented_contracts()
    print("architecture safety and deepening tests ok")


if __name__ == "__main__":
    main()

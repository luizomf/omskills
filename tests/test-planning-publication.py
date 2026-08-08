#!/usr/bin/env python3
"""Disposable and fixture-backed checks for planning publication contracts."""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = json.loads(
    (ROOT / "tests/fixtures/planning-publication.json").read_text()
)


class InterruptedPublication(RuntimeError):
    """Expected interruption in the disposable publication trial."""


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


def audit_authorizes(audit: dict[str, Any] | None, current_version: int) -> bool:
    if not audit or int(audit["version"]) != current_version:
        return False
    status = audit["status"]
    return status == "PASS" or (
        status == "BYPASS" and bool(audit["maintainer_authorized"])
    )


def newest_audit_authorizes(case: dict[str, Any]) -> bool:
    history = case["history"]
    newest = history[-1] if history else None
    return audit_authorizes(newest, int(case["current_version"]))


def role_labels_are_ready(labels: list[str]) -> bool:
    roles = FIXTURE["triage_roles"]
    categories = [label for label in labels if label in roles["categories"]]
    states = [label for label in labels if label in roles["states"]]
    return len(categories) == 1 and states == ["ready-for-agent"]


def downstream_eligible(case: dict[str, Any]) -> bool:
    return (
        case["state"] == "OPEN"
        and "OPEN" not in case["blocker_states"]
        and audit_authorizes(case["audit"], int(case["current_version"]))
        and role_labels_are_ready(case["labels"])
    )


def field(body: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}: (.+)$", body)
    return match.group(1) if match else None


def planning_identity(body: str) -> str | None:
    match = re.search(
        r"(?m)^## Planning identity[ \t]*$\n(?:[ \t]*\n)*([^\n]+)$",
        body,
    )
    return match.group(1).strip() if match else None


class DisposableLocalPublisher:
    """Small executable model of the local Markdown publication contract."""

    def __init__(self, root: Path, plan: dict[str, Any]):
        self.root = root
        self.plan = plan
        self.feature = root / ".scratch" / "planning-publication"
        self.issues = self.feature / "issues"
        self.observed_initial_states: list[str] = []

    def publish_spec(self) -> None:
        self.feature.mkdir(parents=True, exist_ok=True)
        spec = self.plan["spec"]
        path = self.feature / "spec.md"
        expected_prefix = (
            f"# {spec['title']}\n\n"
            f"Planning identity: {spec['identity']}\n"
            f"Author: {self.plan['author']}\n"
            f"Created: {self.plan['created']}\n"
            f"Updated: {self.plan['updated']}\n\n"
            f"{spec['body']}"
        )
        if path.exists():
            expect(
                path.read_text().startswith(expected_prefix),
                "resume found a different Spec at the approved identity",
            )
        else:
            path.write_text(expected_prefix)
        audit = spec["audit"]
        if "### Prompt Audit" not in path.read_text():
            with path.open("a") as handle:
                handle.write(
                    "\n## Comments\n\n"
                    "### Prompt Audit\n\n"
                    f"Author: {self.plan['author']}\n"
                    f"Created: {self.plan['created']}\n"
                    f"Updated: {self.plan['updated']}\n"
                    f"Status: {audit['status']}\n"
                    f"Contract version: {audit['version']}\n"
                    f"Maintainer authorized: {str(audit['maintainer_authorized']).lower()}\n"
                )

    def spec_authorizes_tickets(self) -> bool:
        spec = self.plan["spec"]
        body = (self.feature / "spec.md").read_text()
        match = re.search(
            r"(?ms)^### Prompt Audit\n\nAuthor: .+\nCreated: .+\nUpdated: .+\n"
            r"Status: (PASS|BYPASS|FAIL)\nContract version: (\d+)\n"
            r"Maintainer authorized: (true|false)$",
            body,
        )
        if not match:
            return False
        audit = {
            "status": match.group(1),
            "version": int(match.group(2)),
            "maintainer_authorized": match.group(3) == "true",
        }
        return audit_authorizes(audit, int(spec["audit"]["version"]))

    def _ticket_path(self, ticket: dict[str, Any]) -> Path:
        return self.issues / f"{int(ticket['number']):02d}-{ticket['slug']}.md"

    def _approved_identity_paths(self) -> dict[str, list[Path]]:
        result: dict[str, list[Path]] = {}
        if not self.issues.exists():
            return result
        for path in self.issues.glob("*.md"):
            identity = field(path.read_text(), "Planning identity")
            if identity:
                result.setdefault(identity, []).append(path)
        return result

    def reconcile_identities_and_parents(self) -> None:
        self.issues.mkdir(parents=True, exist_ok=True)
        identity_paths = self._approved_identity_paths()
        for identity, paths in identity_paths.items():
            expect(len(paths) == 1, f"duplicate planning identity exists: {identity}")

        for ticket in self.plan["tickets"]:
            identity = ticket["identity"]
            existing = identity_paths.get(identity, [])
            path = self._ticket_path(ticket)
            if existing:
                expect(existing[0] == path, f"approved identity moved: {identity}")
                expect(
                    field(path.read_text(), "Parent") == self.plan["spec"]["identity"],
                    f"parent is incomplete for {identity}",
                )
                continue
            expect(not path.exists(), f"ticket path has an unapproved identity: {path}")
            path.write_text(self._render_ticket(ticket, relations_complete=False))
            identity_paths[identity] = [path]
            self.observed_initial_states.append(field(path.read_text(), "Status") or "")

    def _render_ticket(
        self,
        ticket: dict[str, Any],
        *,
        relations_complete: bool,
        audit: dict[str, Any] | None = None,
    ) -> str:
        ready = relations_complete and audit_authorizes(audit, 1)
        status = "ready-for-agent" if ready else "needs-triage"
        blockers = ", ".join(ticket["blocked_by"]) or "None — can start immediately"
        conflicts = (
            "; ".join(
                f"{conflict['identity']} — {conflict['surface']}"
                for conflict in ticket["conflicts"]
            )
            or "None — independent"
        )
        body = (
            f"# {int(ticket['number']):02d} — {ticket['title']}\n\n"
            f"Planning identity: {ticket['identity']}\n"
            f"Parent: {self.plan['spec']['identity']}\n"
            f"Category: {ticket['category']}\n"
            f"Status: {status}\n"
            f"Author: {self.plan['author']}\n"
            f"Created: {self.plan['created']}\n"
            f"Updated: {self.plan['updated']}\n"
            f"Relations complete: {'yes' if relations_complete else 'no'}\n\n"
            "## What to build\n\nFixture tracer-bullet behavior.\n\n"
            f"## Blocked by\n\n{blockers}\n\n"
            f"## Conflicts with\n\n{conflicts}\n"
        )
        if audit:
            body += (
                "\n## Comments\n\n"
                "### Prompt Audit\n\n"
                f"Author: {self.plan['author']}\n"
                f"Created: {self.plan['created']}\n"
                f"Updated: {self.plan['updated']}\n"
                f"Status: {audit['status']}\n"
                f"Contract version: {audit['version']}\n"
                f"Maintainer authorized: {str(audit['maintainer_authorized']).lower()}\n"
            )
        return body

    def reconcile_relations(self, interrupt_after: int | None = None) -> None:
        completed = 0
        for ticket in self.plan["tickets"]:
            path = self._ticket_path(ticket)
            if field(path.read_text(), "Relations complete") == "yes":
                continue
            path.write_text(self._render_ticket(ticket, relations_complete=True))
            completed += 1
            if interrupt_after is not None and completed == interrupt_after:
                raise InterruptedPublication

    def audit_and_transition(self) -> None:
        for ticket in self.plan["tickets"]:
            path = self._ticket_path(ticket)
            expect(
                field(path.read_text(), "Relations complete") == "yes",
                f"audit ran before final relations for {ticket['identity']}",
            )
            path.write_text(
                self._render_ticket(
                    ticket,
                    relations_complete=True,
                    audit=ticket["audit"],
                )
            )

    def report(self) -> dict[str, Any]:
        completed: list[str] = []
        missing: list[str] = []
        for ticket in self.plan["tickets"]:
            identity = ticket["identity"]
            path = self._ticket_path(ticket)
            if not path.exists():
                missing.extend(
                    f"{kind}:{identity}"
                    for kind in ("identity", "parent", "relations", "audit", "readiness")
                )
                continue
            body = path.read_text()
            for kind, condition in (
                ("identity", field(body, "Planning identity") == identity),
                ("parent", field(body, "Parent") == self.plan["spec"]["identity"]),
                ("relations", field(body, "Relations complete") == "yes"),
                ("audit", "### Prompt Audit" in body),
                ("readiness", field(body, "Status") == "ready-for-agent"),
            ):
                (completed if condition else missing).append(f"{kind}:{identity}")
        return {"success": not missing, "completed": completed, "missing": missing}

    def publish(self, interrupt_after: int | None = None) -> dict[str, Any]:
        self.publish_spec()
        expect(self.spec_authorizes_tickets(), "unaudited Spec authorized Ticket publication")
        self.reconcile_identities_and_parents()
        try:
            self.reconcile_relations(interrupt_after)
        except InterruptedPublication:
            return self.report()
        self.audit_and_transition()
        return self.report()


def check_audit_transitions() -> None:
    for case in FIXTURE["audit_histories"]:
        expect(
            newest_audit_authorizes(case) == case["authorizes"],
            f"wrong newest Prompt Audit result for {case['id']}",
        )


def check_identity_reconciliation() -> None:
    for case in FIXTURE["identity_reconciliation"]:
        matches = [
            int(issue["number"])
            for issue in case["issues"]
            if planning_identity(str(issue["body"])) == case["approved_identity"]
        ]
        action = "reconcile" if len(matches) == 1 else "create" if not matches else "stop"
        expect(matches == case["expected_matches"], f"wrong identity matches for {case['id']}")
        expect(action == case["expected_action"], f"wrong reconciliation action for {case['id']}")


def check_disposable_local_publication() -> None:
    plan = FIXTURE["local_publication"]
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        complete = DisposableLocalPublisher(root, plan)
        report = complete.publish()
        expect(report["success"], f"complete local publication failed: {report['missing']}")
        expect(
            complete.observed_initial_states == ["needs-triage", "needs-triage"],
            "implementation Tickets did not begin with needs-triage",
        )
        spec_body = (complete.feature / "spec.md").read_text()
        expect("caller-visible test seam" in spec_body, "Spec lost its confirmed test seam")
        expect("ready-for-agent" not in spec_body, "planning Spec became implementation-ready")
        expect(len(list(complete.issues.glob("*.md"))) == 2, "complete publication duplicated Ticket identities")
        for ticket in plan["tickets"]:
            body = complete._ticket_path(ticket).read_text()
            expect(field(body, "Status") == "ready-for-agent", f"audited Ticket stayed non-ready: {ticket['identity']}")
            expect(field(body, "Category") == ticket["category"], f"Ticket category drifted: {ticket['identity']}")
            for conflict in ticket["conflicts"]:
                expect(conflict["surface"] in body, f"conflict surface is missing: {ticket['identity']}")

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        interrupted = DisposableLocalPublisher(root, plan)
        partial = interrupted.publish(int(plan["interrupt_after_relations"]))
        expect(not partial["success"], "interrupted publication was reported as success")
        expect(partial["missing"], "interrupted publication did not report missing artifacts")
        expect(
            any(item.startswith("relations:") for item in partial["missing"])
            and any(item.startswith("audit:") for item in partial["missing"])
            and any(item.startswith("readiness:") for item in partial["missing"]),
            "partial report did not identify exact missing relation, audit, and readiness artifacts",
        )
        for path in interrupted.issues.glob("*.md"):
            expect(field(path.read_text(), "Status") == "needs-triage", "Ticket became ready before audit")

        resumed = DisposableLocalPublisher(root, plan)
        final = resumed.publish()
        expect(final["success"], f"resumed publication failed: {final['missing']}")
        expect(len(list(resumed.issues.glob("*.md"))) == 2, "resume created duplicate Tickets")
        identities = [field(path.read_text(), "Planning identity") for path in resumed.issues.glob("*.md")]
        expect(len(identities) == len(set(identities)), "resume duplicated an approved identity")


def check_hosted_relation_fixtures() -> None:
    for case in FIXTURE["hosted_relations"]:
        parent = case["native_parent"] if case["native_parent_available"] else case["fallback_parent"]
        blockers = case["native_blockers"] if case["native_blockers_available"] else case["fallback_blockers"]
        expect(parent == case["expected_parent"], f"wrong parent relation for {case['id']}")
        expect(blockers == case["expected_blockers"], f"wrong blocker relation for {case['id']}")


def check_downstream_selection() -> None:
    for case in FIXTURE["downstream_cases"]:
        expect(
            downstream_eligible(case) == case["eligible"],
            f"wrong downstream eligibility for {case['id']}",
        )


def check_skill_and_tracker_contracts() -> None:
    to_spec = (ROOT / "skills/engineering/to-spec/SKILL.md").read_text()
    to_tickets = (ROOT / "skills/engineering/to-tickets/SKILL.md").read_text()
    implement = (ROOT / "skills/engineering/implement/SKILL.md").read_text()
    orchestrate = (ROOT / "skills/engineering/orchestrate/SKILL.md").read_text()
    audits = (ROOT / "skills/productivity/prompt-comprehension-audits/SKILL.md").read_text()
    github = (ROOT / "skills/engineering/setup-omskills/issue-tracker-github.md").read_text()
    gitlab = (ROOT / "skills/engineering/setup-omskills/issue-tracker-gitlab.md").read_text()
    local = (ROOT / "skills/engineering/setup-omskills/issue-tracker-local.md").read_text()
    current = (ROOT / "docs/agents/issue-tracker.md").read_text()

    expect("caller-visible test seam" in to_spec, "to-spec uses stale test-seam terminology")
    expect("every established requirement and decision" in to_spec, "to-spec does not require a complete Spec")
    expect("no configured state-role label" in to_spec, "to-spec can still mark a planning Spec ready")
    expect("Apply `ready-for-agent`" not in to_spec, "to-spec still applies ready-for-agent")
    expect("current `PASS` or explicit maintainer-authorized `BYPASS`" in to_spec, "to-spec omits the Spec audit gate")

    source_gate = to_tickets.index("Validate the source Prompt Audit")
    approval = to_tickets.index("Obtain breakdown approval")
    identities = to_tickets.index("Phase A — identities and parents")
    relations = to_tickets.index("Phase B — final contracts and relations")
    readiness = to_tickets.index("Phase C — audit and readiness")
    expect(source_gate < approval < identities < relations < readiness, "to-tickets publication order is not deterministic")
    for phrase in (
        "Planning identity",
        "exactly one configured category role",
        "configured `needs-triage` state role",
        "direct write-conflict",
        "shared file, contract, artifact, or integration surface",
        "expand–contract",
        "missing, stale, or `FAIL`",
        "completed and missing artifacts",
        "Do not limit discovery to already-parented children",
        "Do not mutate the audited source Spec",
    ):
        expect(phrase in to_tickets, f"to-tickets omits {phrase!r}")

    for name, contract in (("implement", implement), ("orchestrate", orchestrate)):
        for phrase in (
            "closed",
            "open blocker",
            "exactly one configured category role",
            "configured `ready-for-agent` state role",
            "missing, stale, or `FAIL`",
            "configured triage-role metadata",
        ):
            expect(phrase in contract, f"{name} downstream gate omits {phrase!r}")

    expect("do not require another Prompt Audit" in audits, "audit protocol became recursive")
    for name, document in (("GitHub", github), ("current GitHub", current)):
        expect("## Planning publication operations" in document, f"{name} planning operations are missing")
        expect("issues?state=all&per_page=100" in document, f"{name} unparented identity discovery is missing")
        expect("--parent <spec-number>" in document, f"{name} native parent operation is missing")
        expect("--add-blocked-by <blocker-number>" in document, f"{name} native blocker operation is missing")
        expect("documented fallback" in document, f"{name} documented relation fallback is missing")
        expect("Do not modify the audited Spec" in document, f"{name} fallback mutates the audited Spec")
        expect("--remove-label <needs-triage-label>" in document, f"{name} readiness transition is missing")
    expect("## Planning publication operations" in gitlab, "GitLab planning operations are missing")
    expect("projects/<project-id>/issues?scope=all&per_page=100" in gitlab, "GitLab unparented identity discovery is missing")
    expect("is_blocked_by" in gitlab, "GitLab native blocker relation is missing")
    expect("native parent relation" in gitlab and "fallback" in gitlab, "GitLab parent fallback is missing")
    expect("Do not modify the audited Spec" in gitlab, "GitLab fallback mutates the audited Spec")
    expect("## Planning publication operations" in local, "local planning operations are missing")
    for field_name in ("Planning identity:", "Parent:", "Category:", "Status:", "Author:", "Created:", "Updated:", "Blocked by:", "Conflicts with:"):
        expect(field_name in local, f"local planning contract omits {field_name}")


def main() -> None:
    check_audit_transitions()
    check_identity_reconciliation()
    check_disposable_local_publication()
    check_hosted_relation_fixtures()
    check_downstream_selection()
    check_skill_and_tracker_contracts()
    print("planning publication tests ok")


if __name__ == "__main__":
    main()

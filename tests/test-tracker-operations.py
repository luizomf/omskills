#!/usr/bin/env python3
"""Fixture-backed checks for emitted tracker and domain operations."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = json.loads(
    (ROOT / "tests/fixtures/tracker-operations.json").read_text()
)
SETUP = ROOT / "skills/engineering/setup-omskills"


def expect(condition: bool, message: str) -> None:
    if not condition:
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)


def read(path: Path) -> str:
    return path.read_text()


def github_frontier(children: list[dict[str, object]]) -> list[int]:
    return [
        int(child["number"])
        for child in children
        if child["state"] == "open"
        and int(child["issue_dependencies_summary"]["blocked_by"]) == 0
        and not child["assignees"]
    ]


def task_list_children(body: str) -> list[int]:
    section = re.search(
        r"(?ms)^## Tickets\s*$\n(.*?)(?=^## |\Z)", body
    )
    expect(section is not None, "GitHub fallback map fixture has no Tickets section")
    return [
        int(number)
        for number in re.findall(
            r"(?m)^- \[[ xX]\] #(\d+)\b", section.group(1)
        )
    ]


def gitlab_has_open_blocker(links: list[dict[str, object]]) -> bool:
    return any(
        link["link_type"] == "is_blocked_by" and link["state"] == "opened"
        for link in links
    )


def gitlab_frontier(
    issues: list[dict[str, object]], links_by_issue: dict[str, list[dict[str, object]]], map_iid: int
) -> list[int]:
    parent = f"Part of #{map_iid}"
    scoped = [
        issue
        for issue in issues
        if issue["state"] == "opened"
        and str(issue["description"]).splitlines()[0] == parent
    ]
    scoped.sort(key=lambda issue: str(issue["created_at"]))
    return [
        int(issue["iid"])
        for issue in scoped
        if not gitlab_has_open_blocker(links_by_issue.get(str(issue["iid"]), []))
        and not issue["assignees"]
    ]


def derive_context_adr_roots(context_map: str) -> list[str]:
    section = re.search(
        r"(?ms)^## Contexts\s*$\n(.*?)(?=^## |\Z)", context_map
    )
    expect(section is not None, "context-map fixture has no Contexts section")
    paths = re.findall(r"\]\((?:\./)?([^):]+/CONTEXT\.md)\)", section.group(1))
    return [str(Path(path).parent / "docs/adr") for path in paths]


def check_remote_inspection() -> None:
    helper = SETUP / "scripts/inspect-remote.py"
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        fake_bin = root / "bin"
        fake_bin.mkdir()
        fake_git = fake_bin / "git"
        fake_git.write_text(
            "#!/bin/sh\n"
            "printf '%s\\n' \"$@\" > \"$FAKE_GIT_LOG\"\n"
            "[ \"$1\" = remote ] && [ \"$2\" = get-url ] && "
            "[ \"$3\" = -- ] && [ \"$4\" = origin ] || exit 73\n"
            "printf '%s\\n' "
            "'https://oauth2:fixture-secret@github.com/acme/widgets.git?transport=fixture'\n"
        )
        fake_git.chmod(0o755)
        log = root / "git-arguments"
        environment = os.environ.copy()
        environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"
        environment["FAKE_GIT_LOG"] = str(log)
        result = subprocess.run(
            [sys.executable, str(helper), "origin"],
            cwd=root,
            env=environment,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        expect(result.returncode == 0, f"remote inspection failed: {result.stderr}")
        expect("fixture-secret" not in result.stdout, "remote credentials reached stdout")
        expect("oauth2" not in result.stdout, "remote userinfo reached stdout")
        identity = json.loads(result.stdout)
        expect(identity["repository"] == "github.com/acme/widgets", "remote target was not sanitized")
        expect(
            log.read_text().splitlines() == ["remote", "get-url", "--", "origin"],
            "remote helper inspected anything other than the selected remote URL",
        )


def check_documented_commands() -> None:
    setup_skill = read(SETUP / "SKILL.md")
    github = read(SETUP / "issue-tracker-github.md")
    gitlab = read(SETUP / "issue-tracker-gitlab.md")
    local = read(SETUP / "issue-tracker-local.md")
    domain = read(SETUP / "domain.md")
    current = read(ROOT / "docs/agents/issue-tracker.md")

    expected_current = github
    for old, new in [
        ("<remote-name>", "origin"),
        ("<host>/<owner>/<repo>", "github.com/luizomf/omskills"),
        ("<owner>/<repo>", "luizomf/omskills"),
        ("<host>", "github.com"),
    ]:
        expected_current = expected_current.replace(old, new)
    expect(current == expected_current, "current GitHub config diverges from its setup template")

    for document_name, document in (("GitHub template", github), ("current GitHub config", current)):
        creates = re.findall(r"`(gh issue create [^`]+)`", document)
        expect(len(creates) >= 3, f"{document_name} does not document all creation paths")
        for command in creates:
            expect("--title" in command and "--body-file" in command, f"interactive GitHub creation path: {command}")
        expect("author_association" in document, f"{document_name} omits REST association evidence")
        for association in ("OWNER", "MEMBER", "COLLABORATOR"):
            expect(association in document, f"{document_name} omits internal association {association}")
        expect("author,createdAt,updatedAt,comments" in document, f"{document_name} drops triage metadata")
        expect("/sub_issues?per_page=100" in document, f"{document_name} omits native child scope")
        expect("--slurp" not in document, f"{document_name} combines unsupported gh pagination formatting")
        expect("## Tickets" in document and "checklist entries" in document, f"{document_name} omits task-list scope")
        expect("first obtain" in document and "Only then" in document, f"{document_name} filters before child scoping")
        expect("Inventory labels" in document and "final inventory" in document, f"{document_name} omits label ordering")
        expect(
            not re.search(r"gh pr list[^`\n]*authorAssociation", document),
            f"{document_name} uses unsupported gh PR association output",
        )

    gitlab_creates = re.findall(r"`(glab issue create [^`]+)`", gitlab)
    expect(len(gitlab_creates) >= 3, "GitLab template does not document all creation paths")
    for command in gitlab_creates:
        expect(
            "--title" in command and "--description" in command and "--yes" in command,
            f"interactive GitLab creation path: {command}",
        )
    expect("glab issue list --repo" in gitlab and "-O json" in gitlab, "GitLab issue JSON syntax is missing")
    expect("--repo https://<host>/<namespace>/<project>" in gitlab, "GitLab repository target is ambiguous")
    expect("glab repo view https://<host>/<namespace>/<project> -F json --jq '.id'" in gitlab, "GitLab project ID lookup is missing")
    expect(
        not re.search(r"glab issue list[^`\n]*-F json", gitlab),
        "GitLab issue listing still uses unsupported -F json",
    )
    expect("/notes?per_page=100" in gitlab and "--paginate" in gitlab, "GitLab comment pagination is missing")
    expect("members/all?per_page=100" in gitlab, "GitLab project-membership evidence is missing")
    expect("glab api --hostname <host> user --jq '.username'" in gitlab, "GitLab authenticated user lookup is missing")
    expect(
        not re.search(r"glab issue update[^`\n]*--assignee @me", gitlab),
        "GitLab claim still sends literal @me",
    )
    expect("link_type` is `is_blocked_by" in gitlab, "GitLab blocker semantics are missing")
    expect("First retain only open issues" in gitlab and "Only after that" in gitlab, "GitLab filters before parent scoping")

    expect("Author:" in local and "Created:" in local and "Updated:" in local, "local tracker drops triage metadata")
    expect("explicit `# <title>`" in local and "noninteractive body" in local, "local creation input is incomplete")
    expect("first scope" in local and "Parent:" in local, "local frontier is not map-scoped")

    remote_selection = setup_skill.index("Select a remote before inspecting any remote URL")
    remote_inspection = setup_skill.index("scripts/inspect-remote.py")
    expect(remote_selection < remote_inspection, "setup inspects a URL before selecting its remote")
    expect("Never run `git remote -v`" in setup_skill, "setup does not prohibit credential-bearing remote output")
    mapping_inventory = setup_skill.index("Before recommending mappings")
    provision_inventory = setup_skill.index("Re-run the complete label inventory")
    label_creation = setup_skill.index("Create only mapped label strings")
    final_inventory = setup_skill.index("Run the inventory a final time")
    expect(
        mapping_inventory < provision_inventory < label_creation < final_inventory,
        "setup label inventory and provisioning order is not deterministic",
    )

    expect("one row for every local Markdown link" in domain, "domain template does not use map entries")
    expect("directory containing that `CONTEXT.md`" in domain, "domain template does not derive ADR roots")
    expect("do not scan or assume `src/*`" in domain, "domain template can still assume src contexts")


def check_fixture_responses() -> None:
    github = FIXTURE["github"]
    internal = {"OWNER", "MEMBER", "COLLABORATOR"}
    for pull_request in github["pull_requests"]:
        external = pull_request["author_association"] not in internal
        expect(external == pull_request["external"], f"wrong GitHub classification for PR {pull_request['number']}")
        for field in ("user", "created_at", "updated_at"):
            expect(field in pull_request, f"GitHub PR fixture lost {field}")

    native = github_frontier(github["native_sub_issues"])
    expect(native == github["native_frontier"], "GitHub native frontier filtering is wrong")
    expect(999 not in native, "repository-wide GitHub issue leaked into native map frontier")

    fallback_numbers = task_list_children(github["task_list_body"])
    fallback_scope = {
        int(issue["number"]): issue for issue in github["task_list_issues"]
    }
    fallback = github_frontier([fallback_scope[number] for number in fallback_numbers])
    expect(fallback == github["task_list_frontier"], "GitHub task-list frontier filtering is wrong")
    expect(998 not in fallback and 999 not in fallback, "non-checklist issue leaked into fallback frontier")

    gitlab = FIXTURE["gitlab"]
    for issue in gitlab["issue_list"]:
        for field in ("author", "created_at", "updated_at"):
            expect(field in issue, f"GitLab issue fixture lost {field}")

    comments = [comment for page in gitlab["comment_pages"] for comment in page]
    expect([comment["id"] for comment in comments] == [1, 2, 3], "GitLab comment pagination stopped early")
    for comment in comments:
        for field in ("author", "created_at", "updated_at"):
            expect(field in comment, f"GitLab comment fixture lost {field}")

    members = {
        member["username"]
        for page in gitlab["member_pages"]
        for member in page
    }
    for merge_request in gitlab["merge_requests"]:
        external = merge_request["author"]["username"] not in members
        expect(external == merge_request["external"], f"wrong GitLab MR classification for {merge_request['iid']}")

    username = gitlab["authenticated_user"]["username"]
    claim_arguments = ["glab", "issue", "update", "301", "--assignee", username]
    expect(username in claim_arguments and "@me" not in claim_arguments, "GitLab self-assignment did not use authenticated username")

    frontier = gitlab_frontier(gitlab["frontier_issues"], gitlab["links_by_issue"], 42)
    expect(frontier == gitlab["frontier"], "GitLab frontier scoping or filtering is wrong")
    expect(304 not in frontier and 305 not in frontier, "non-child GitLab issue leaked into frontier")
    expect(302 not in frontier, "open is_blocked_by link did not block GitLab child")

    roots = derive_context_adr_roots(FIXTURE["context_map"]["body"])
    expect(roots == FIXTURE["context_map"]["adr_roots"], "ADR roots were not derived from context-map entries")


def main() -> None:
    check_remote_inspection()
    check_documented_commands()
    check_fixture_responses()
    print("tracker operation tests ok")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Print credential-free repository identity for one selected Git remote."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from urllib.parse import urlsplit


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def repository_identity(remote_url: str) -> tuple[str, str]:
    value = remote_url.strip()
    if not value or any(ord(char) < 32 for char in value):
        fail("selected remote has an invalid URL")

    if "://" in value:
        try:
            parsed = urlsplit(value)
            host = parsed.hostname
            path = parsed.path
        except ValueError:
            fail("selected remote has an invalid URL")
    else:
        match = re.fullmatch(r"(?:[^@/:]+@)?([^/:]+):(.+)", value)
        if not match:
            fail("selected remote is not a supported hosted repository URL")
        host, path = match.groups()

    if not host:
        fail("selected remote URL has no host")

    normalized_path = path.strip("/")
    if normalized_path.endswith(".git"):
        normalized_path = normalized_path[:-4]
    parts = normalized_path.split("/")
    if len(parts) < 2 or any(part in {"", ".", ".."} for part in parts):
        fail("selected remote URL has no valid repository path")
    if any(any(ord(char) < 32 for char in part) for part in parts):
        fail("selected remote repository path is invalid")

    return host.lower(), "/".join(parts)


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1]:
        fail("usage: inspect-remote.py <selected-remote>")

    remote = sys.argv[1]
    result = subprocess.run(
        ["git", "remote", "get-url", "--", remote],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode != 0:
        fail("could not inspect the selected remote")

    host, path = repository_identity(result.stdout)
    print(
        json.dumps(
            {
                "host": host,
                "path": path,
                "remote": remote,
                "repository": f"{host}/{path}",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

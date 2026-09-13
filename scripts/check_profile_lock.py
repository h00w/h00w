#!/usr/bin/env python3
"""Enforce append-only project updates for the GitHub profile README.

Policy:
- Existing README.md lines are immutable.
- New lines may only be inserted inside the `# Projects` section.
- No deletions or replacements are allowed anywhere in README.md.

Usage:
    python scripts/check_profile_lock.py <base-readme> <head-readme>
"""

from __future__ import annotations

import difflib
import pathlib
import sys

PROJECTS_START = "# Projects"
PROJECTS_END = "## Engineering principles"


def fail(message: str) -> None:
    print(f"PROFILE LOCK FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: str) -> list[str]:
    return pathlib.Path(path).read_text(encoding="utf-8").splitlines(keepends=True)


def project_bounds(lines: list[str]) -> tuple[int, int]:
    stripped = [line.rstrip("\r\n") for line in lines]
    try:
        start = stripped.index(PROJECTS_START)
    except ValueError:
        fail(f"required anchor {PROJECTS_START!r} is missing")
    try:
        end = stripped.index(PROJECTS_END, start + 1)
    except ValueError:
        fail(f"required anchor {PROJECTS_END!r} is missing")
    if end <= start:
        fail("project section anchors are out of order")
    return start, end


def main() -> None:
    if len(sys.argv) != 3:
        fail("expected: check_profile_lock.py <base-readme> <head-readme>")

    base = load(sys.argv[1])
    head = load(sys.argv[2])
    base_start, base_end = project_bounds(base)

    matcher = difflib.SequenceMatcher(a=base, b=head, autojunk=False)
    additions = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        if tag in {"delete", "replace"}:
            changed = "".join(base[i1:i2]).strip()
            preview = changed[:180].replace("\n", " | ")
            fail(
                "existing README content was deleted or modified. "
                f"First affected content: {preview!r}"
            )

        if tag == "insert":
            # Insertions are allowed only after '# Projects' and before
            # '## Engineering principles' in the immutable base document.
            if not (base_start < i1 <= base_end):
                preview = "".join(head[j1:j2]).strip()[:180].replace("\n", " | ")
                fail(
                    "new content may only be added inside the Projects section. "
                    f"Rejected addition: {preview!r}"
                )
            additions += j2 - j1

    if additions == 0 and base != head:
        fail("README changed without a permitted project addition")

    print(
        "PROFILE LOCK PASSED: existing README content is unchanged; "
        f"{additions} new project-section line(s) added."
    )


if __name__ == "__main__":
    main()

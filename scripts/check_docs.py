#!/usr/bin/env python3
"""Validate documentation navigation and emit advisory drift warnings."""
from __future__ import annotations

import argparse
import re
import subprocess
from collections import deque
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LINK_RE = re.compile(r"!?[[^]]*](([^)]+))")

EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
)

FUNCTIONAL_PREFIXES = (
    "agents/",
    "runtime/",
    "adapters/",
    "environment/",
    "loops/",
    "capabilities/",
    "skills/",
    "hooks/",
    "agent-context/",
)

FUNCTIONAL_FILES = {
    "agent",
    "agent.cmd",
    "harness",
    "harness.cmd",
    "requirements.txt",
}


def markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group(1).strip() for match in LINK_RE.finditer(text)]


def resolve_local_link(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith("#") or target.startswith(EXTERNAL_PREFIXES):
        return None

    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]

    # Drop optional Markdown title text after a path.
    if " " in target and not target.startswith(("./", "../")):
        target = target.split(" ", 1)[0]

    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None

    resolved = (source.parent / target).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return None

    if resolved.is_dir():
        readme = resolved / "README.md"
        return readme if readme.exists() else resolved

    return resolved


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def structural_check() -> int:
    failures: list[str] = []

    index = DOCS / "README.md"
    root_readme = ROOT / "README.md"

    if not index.exists():
        failures.append("missing canonical documentation index: docs/README.md")
    if not root_readme.exists():
        failures.append("missing repository README.md")

    if failures:
        return report_failures(failures)

    root_targets = {
        repo_relative(resolved)
        for raw in markdown_links(root_readme)
        if (resolved := resolve_local_link(root_readme, raw)) is not None
        and resolved.exists()
    }
    if "docs/README.md" not in root_targets:
        failures.append("README.md must link to docs/README.md")

    scan_files = [root_readme, *sorted(DOCS.rglob("*.md"))]
    for source in scan_files:
        for raw in markdown_links(source):
            resolved = resolve_local_link(source, raw)
            if resolved is None:
                continue
            if not resolved.exists():
                failures.append(
                    f"{repo_relative(source)}: broken local link '{raw}' "
                    f"-> {repo_relative(resolved)}"
                )

    index_targets = {
        repo_relative(resolved)
        for raw in markdown_links(index)
        if (resolved := resolve_local_link(index, raw)) is not None
        and resolved.exists()
    }

    for doc in sorted(DOCS.glob("*.md")):
        if doc.name == "README.md":
            continue
        if repo_relative(doc) not in index_targets:
            failures.append(
                f"docs/README.md does not index top-level document: {repo_relative(doc)}"
            )

    for child in sorted(path for path in DOCS.iterdir() if path.is_dir()):
        if not any(child.rglob("*.md")):
            continue
        child_index = child / "README.md"
        if not child_index.exists():
            failures.append(f"documentation category missing README.md: {repo_relative(child)}")
            continue
        if repo_relative(child_index) not in index_targets:
            failures.append(
                f"docs/README.md does not index category: {repo_relative(child_index)}"
            )

    reachable: set[Path] = set()
    queue: deque[Path] = deque([index.resolve()])
    while queue:
        current = queue.popleft()
        if current in reachable or not current.exists() or current.suffix.lower() != ".md":
            continue
        reachable.add(current)
        for raw in markdown_links(current):
            target = resolve_local_link(current, raw)
            if target is None or not target.exists() or target.suffix.lower() != ".md":
                continue
            try:
                target.relative_to(DOCS.resolve())
            except ValueError:
                continue
            if target not in reachable:
                queue.append(target)

    for doc in sorted(DOCS.rglob("*.md")):
        if doc.resolve() not in reachable:
            failures.append(f"orphaned documentation not reachable from docs/README.md: {repo_relative(doc)}")

    if failures:
        return report_failures(failures)

    print("DOCUMENTATION CHECK PASSED")
    print(f"Indexed documentation files: {len(list(DOCS.rglob('*.md')))}")
    return 0


def report_failures(failures: list[str]) -> int:
    print("DOCUMENTATION CHECK FAILED")
    for failure in failures:
        print(f"- {failure}")
    return 1


def changed_files(base_ref: str) -> list[str] | None:
    commands = [
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only", f"{base_ref}..HEAD"],
    ]
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode == 0:
            return [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    return None


def drift_warning(base_ref: str) -> int:
    changed = changed_files(base_ref)
    if changed is None:
        print(f"Documentation drift advisory skipped: unable to compare against {base_ref}")
        return 0

    functional = [
        path
        for path in changed
        if path in FUNCTIONAL_FILES or path.startswith(FUNCTIONAL_PREFIXES)
    ]
    documentation = [
        path
        for path in changed
        if path.endswith(".md") or path.startswith("docs/")
    ]

    if functional and not documentation:
        preview = ", ".join(functional[:8])
        if len(functional) > 8:
            preview += ", ..."
        print(
            "::warning title=Documentation drift::"
            "Functional files changed without a Markdown documentation change. "
            "Confirm that documentation is unaffected or update the related canonical document. "
            f"Changed functional files: {preview}"
        )
    else:
        print("Documentation drift advisory: no obvious undocumented functional change.")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--drift-warning",
        metavar="BASE_REF",
        help="emit a non-blocking warning when functional files changed without Markdown docs",
    )
    args = parser.parse_args()

    if args.drift_warning:
        return drift_warning(args.drift_warning)
    return structural_check()


if __name__ == "__main__":
    raise SystemExit(main())

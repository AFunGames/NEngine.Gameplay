#!/usr/bin/env python3
"""Local repository verifier for NEngine.Gameplay.

Read-only, offline, stdlib-only. See docs/verification.md for the contract.
Exit codes:
    0 -> HEALTHY or DEGRADED
    1 -> UNHEALTHY (verification failed)
    2 -> verifier itself failed to execute
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = 1
REPOSITORY_NAME = "NEngine.Gameplay"

REQUIRED_DOCS = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/architecture.md",
    "docs/gameplay-model.md",
    "docs/development.md",
    "docs/verification.md",
)

CANONICAL_MARKDOWN = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "docs/architecture.md",
    "docs/gameplay-model.md",
    "docs/development.md",
    "docs/verification.md",
)

AGENT_CONTRACT_REQUIRED_MENTIONS = (
    REPOSITORY_NAME,
    "docs/architecture.md",
    "docs/gameplay-model.md",
    "docs/development.md",
    "docs/verification.md",
    "python scripts/verify_repo.py",
)

CLAUDE_ROUTER_REQUIRED_MENTIONS = ("AGENTS.md",)
CLAUDE_ROUTER_MAX_BYTES = 4096

FORBIDDEN_DEP_TOKENS = (
    "CurseBreaker",
    "Babylon",
    "babylonjs",
)

DEPENDENCY_BEARING_FILES = (
    "CMakeLists.txt",
    "conanfile.txt",
    "conanfile.py",
    "vcpkg.json",
    "package.json",
    "pyproject.toml",
)

MACHINE_PATH_PATTERNS = (
    re.compile(r"[A-Za-z]:\\\\Users\\\\", re.IGNORECASE),
    re.compile(r"[A-Za-z]:/Users/", re.IGNORECASE),
    re.compile(r"/Users/[A-Za-z0-9_.-]+/"),
    re.compile(r"/home/[A-Za-z0-9_.-]+/"),
)


def add_check(checks: list, cid: str, status: str, message: str) -> None:
    checks.append({"id": cid, "status": status, "message": message})


def check_required_docs(root: Path, checks: list) -> None:
    missing = [p for p in REQUIRED_DOCS if not (root / p).is_file()]
    if missing:
        add_check(checks, "docs.required", "FAIL", "Missing required docs: " + ", ".join(missing))
    else:
        add_check(
            checks,
            "docs.required",
            "PASS",
            f"All {len(REQUIRED_DOCS)} required local documents exist.",
        )


LINK_RE = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def check_markdown_links(root: Path, checks: list) -> None:
    broken: list[str] = []
    scanned = 0
    for rel in CANONICAL_MARKDOWN:
        path = root / rel
        if not path.is_file():
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                broken.append(f"{rel} -> {target} (escapes repository)")
                continue
            if not resolved.exists():
                broken.append(f"{rel} -> {target}")
    if broken:
        add_check(
            checks,
            "docs.links",
            "FAIL",
            f"Broken relative links across {scanned} canonical files: " + "; ".join(broken),
        )
    else:
        add_check(
            checks,
            "docs.links",
            "PASS",
            f"Relative links resolve across {scanned} canonical local documents.",
        )


def check_agent_contract(root: Path, checks: list) -> None:
    path = root / "AGENTS.md"
    if not path.is_file():
        add_check(checks, "agent.contract", "FAIL", "AGENTS.md is missing.")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [m for m in AGENT_CONTRACT_REQUIRED_MENTIONS if m not in text]
    if missing:
        add_check(
            checks,
            "agent.contract",
            "FAIL",
            "AGENTS.md is missing required mentions: " + ", ".join(missing),
        )
        return
    if "Forbidden" not in text and "forbidden" not in text:
        add_check(
            checks,
            "agent.contract",
            "FAIL",
            "AGENTS.md does not declare a forbidden-dependency boundary.",
        )
        return
    if "escalat" not in text.lower():
        add_check(
            checks,
            "agent.contract",
            "FAIL",
            "AGENTS.md does not declare an escalation rule.",
        )
        return
    add_check(checks, "agent.contract", "PASS", "AGENTS.md declares repository identity, local authorities, verification command, forbidden boundary, and escalation.")


def check_claude_router(root: Path, checks: list) -> None:
    path = root / "CLAUDE.md"
    if not path.is_file():
        add_check(checks, "agent.claude-router", "FAIL", "CLAUDE.md is missing.")
        return
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    if len(raw) > CLAUDE_ROUTER_MAX_BYTES:
        add_check(
            checks,
            "agent.claude-router",
            "FAIL",
            f"CLAUDE.md is {len(raw)} bytes; adapter must stay under {CLAUDE_ROUTER_MAX_BYTES}.",
        )
        return
    missing = [m for m in CLAUDE_ROUTER_REQUIRED_MENTIONS if m not in text]
    if missing:
        add_check(
            checks,
            "agent.claude-router",
            "FAIL",
            "CLAUDE.md does not route to: " + ", ".join(missing),
        )
        return
    add_check(checks, "agent.claude-router", "PASS", "CLAUDE.md is a compact router to AGENTS.md.")


def check_git_state(root: Path, checks: list) -> None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain=v1"],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        add_check(checks, "repo.git-state", "UNKNOWN", f"Git state unreadable: {exc}")
        return
    if result.returncode != 0:
        add_check(
            checks,
            "repo.git-state",
            "UNKNOWN",
            f"git status returned {result.returncode}: {result.stderr.strip()[:200]}",
        )
        return
    dirty = bool(result.stdout.strip())
    if dirty:
        add_check(checks, "repo.git-state", "WARNING", "Working tree is DIRTY.")
    else:
        add_check(checks, "repo.git-state", "PASS", "Working tree is CLEAN.")


def check_paths_portable(root: Path, checks: list) -> None:
    findings: list[str] = []
    for rel in CANONICAL_MARKDOWN:
        path = root / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pat in MACHINE_PATH_PATTERNS:
            for match in pat.finditer(text):
                findings.append(f"{rel}: {match.group(0)!r}")
    if findings:
        add_check(
            checks,
            "paths.portable",
            "FAIL",
            "Machine-specific absolute paths detected: " + "; ".join(findings[:5]),
        )
    else:
        add_check(
            checks,
            "paths.portable",
            "PASS",
            "No machine-specific absolute paths in canonical local documents.",
        )


def check_dependency_boundary(root: Path, checks: list) -> None:
    present = [f for f in DEPENDENCY_BEARING_FILES if (root / f).is_file()]
    if not present:
        add_check(
            checks,
            "dependencies.boundary",
            "PASS",
            "No dependency-bearing configuration exists yet; boundary check deferred to migration.",
        )
        return
    findings: list[str] = []
    for rel in present:
        text = (root / rel).read_text(encoding="utf-8", errors="replace")
        for token in FORBIDDEN_DEP_TOKENS:
            if token in text:
                findings.append(f"{rel}: {token}")
    if findings:
        add_check(
            checks,
            "dependencies.boundary",
            "FAIL",
            "Forbidden project-layer dependency references: " + "; ".join(findings),
        )
    else:
        add_check(
            checks,
            "dependencies.boundary",
            "PASS",
            f"No forbidden project-layer references in {len(present)} dependency-bearing file(s).",
        )


CHECKS = (
    check_required_docs,
    check_markdown_links,
    check_agent_contract,
    check_claude_router,
    check_git_state,
    check_paths_portable,
    check_dependency_boundary,
)


def summarize(checks: Iterable[dict]) -> tuple[dict, str]:
    counts = {"pass": 0, "warning": 0, "fail": 0, "unknown": 0}
    for c in checks:
        counts[c["status"].lower()] += 1
    if counts["fail"] or counts["unknown"]:
        overall = "UNHEALTHY"
    elif counts["warning"]:
        overall = "DEGRADED"
    else:
        overall = "HEALTHY"
    return counts, overall


def run(root: Path) -> dict:
    checks: list[dict] = []
    for fn in CHECKS:
        fn(root, checks)
    summary, overall = summarize(checks)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "repository": REPOSITORY_NAME,
        "overall": overall,
        "summary": summary,
        "checks": checks,
    }


def print_human(report: dict) -> None:
    print(f"{report['repository']} Local Verification")
    print()
    print(f"Overall: {report['overall']}")
    print()
    print("Checks:")
    for c in report["checks"]:
        print(f"  {c['status']:<7} {c['id']}: {c['message']}")
    s = report["summary"]
    print()
    print(
        f"Summary: {s['pass']} PASS, {s['warning']} WARNING, {s['fail']} FAIL, {s['unknown']} UNKNOWN"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Local verifier for {REPOSITORY_NAME}.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root to verify (defaults to the script's repository).",
    )
    args = parser.parse_args(argv)

    root = (args.root or Path(__file__).resolve().parent.parent).resolve()
    try:
        report = run(root)
    except Exception as exc:  # verifier execution error, exit 2
        print(f"Local verifier execution error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    if args.json:
        json.dump(report, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
    else:
        print_human(report)

    return 1 if report["overall"] == "UNHEALTHY" else 0


if __name__ == "__main__":
    sys.exit(main())

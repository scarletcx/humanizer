#!/usr/bin/env python3
"""Validate the humanizer skill package.

Checks required files, frontmatter, version consistency, the 35 pattern
headings, plugin paths, and local Markdown links. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXPECTED_PATTERNS = 35
EXPECTED_VERSION = "2.11.2"

REQUIRED_SKILL_FILES = (
    "SKILL.md",
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "agents/openai.yaml",
    "scripts/validate-package.py",
)

REQUIRED_ROOT_FILES = (
    "README.md",
    "LICENSE",
    "NOTICE.md",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
)

DOC_FILES = (
    "README.md",
    "README.zh-CN.md",
    "NOTICE.md",
    "skills/humanizer/README.md",
    "skills/humanizer/AGENTS.md",
)

LINK_RE = re.compile(r"\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    parent = ""
    for raw in parts[1].splitlines():
        if not raw.strip():
            continue
        if raw.startswith((" ", "\t")) and parent:
            key, _, value = raw.strip().partition(":")
            data[f"{parent}.{key.strip()}"] = value.strip().strip('"').strip("'")
            continue
        key, _, value = raw.partition(":")
        parent = key.strip()
        data[parent] = value.strip().strip('"').strip("'")
    return data


def check_links(path: Path, errors: list[str]) -> None:
    if not path.exists():
        return
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for target in LINK_RE.findall(line):
            target = target.strip()
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = target.split("#", 1)[0].strip()
            if not target:
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path}: broken local link -> {target}")


def build_report(repo_root: Path) -> dict:
    skill_dir = repo_root / "skills" / "humanizer"
    errors: list[str] = []

    for relative in REQUIRED_SKILL_FILES:
        path = skill_dir / relative
        if not path.exists():
            errors.append(f"missing required file: {path}")

    for relative in REQUIRED_ROOT_FILES:
        path = repo_root / relative
        if not path.exists():
            errors.append(f"missing required file: {path}")

    skill_md = skill_dir / "SKILL.md"
    frontmatter: dict[str, str] = {}
    pattern_numbers: list[int] = []
    if skill_md.exists():
        skill_text = skill_md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(skill_text)
        if frontmatter.get("name") != "humanizer":
            errors.append("SKILL.md frontmatter name must be humanizer")
        if frontmatter.get("license") != "MIT":
            errors.append("SKILL.md frontmatter license must be MIT")
        if frontmatter.get("metadata.version") != EXPECTED_VERSION:
            errors.append(f"SKILL.md metadata.version must be {EXPECTED_VERSION}")
        if not frontmatter.get("description"):
            errors.append("SKILL.md frontmatter description is empty")
        pattern_numbers = sorted(
            int(match.group(1)) for match in re.finditer(r"^### (\d+)\.", skill_text, re.M)
        )
        if pattern_numbers != list(range(1, EXPECTED_PATTERNS + 1)):
            errors.append(
                f"expected pattern headings 1..{EXPECTED_PATTERNS}, "
                f"found {pattern_numbers}"
            )

    skill_readme = skill_dir / "README.md"
    if skill_readme.exists():
        readme_text = skill_readme.read_text(encoding="utf-8")
        if "35 patterns" not in readme_text:
            errors.append("skills/humanizer/README.md should mention 35 patterns")
        if f"**{EXPECTED_VERSION}**" not in readme_text:
            errors.append(
                f"skills/humanizer/README.md should contain version {EXPECTED_VERSION}"
            )
        if "scarletcx/humanizer" not in readme_text:
            errors.append("skills/humanizer/README.md should use the fork install URL")

    plugin_path = repo_root / ".claude-plugin" / "plugin.json"
    plugin: dict = {}
    if plugin_path.exists():
        try:
            plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid plugin.json: {exc}")
        if plugin:
            if plugin.get("name") != "humanizer":
                errors.append("plugin.json name must be humanizer")
            if plugin.get("version") != EXPECTED_VERSION:
                errors.append(f"plugin.json version must be {EXPECTED_VERSION}")
            if "./skills/humanizer" not in plugin.get("skills", []):
                errors.append("plugin.json skills must include ./skills/humanizer")

    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    if marketplace_path.exists():
        try:
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
            plugins = marketplace.get("plugins", [])
            if not plugins or plugins[0].get("name") != "humanizer":
                errors.append("marketplace.json must define the humanizer plugin")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid marketplace.json: {exc}")

    for relative in DOC_FILES:
        path = repo_root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "/Users/" in text or "/Applications/" in text:
            errors.append(f"{path}: contains an absolute local path")
        check_links(path, errors)

    return {
        "ok": not errors,
        "repo_root": str(repo_root),
        "skill_dir": str(skill_dir),
        "version": frontmatter.get("metadata.version", ""),
        "plugin_version": plugin.get("version", ""),
        "patterns": len(pattern_numbers),
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the humanizer package.")
    parser.add_argument(
        "--repo-root",
        default=str(Path(__file__).resolve().parents[3]),
        help="Repository root (default: three levels above this script).",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    args = parser.parse_args(argv)

    report = build_report(Path(args.repo_root).resolve())
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("humanizer package check")
        print(f"Repository: {report['repo_root']}")
        print(
            f"Version: {report['version']} | patterns: {report['patterns']} | "
            f"plugin: {report['plugin_version']}"
        )
        if report["ok"]:
            print("OK: package structure, version, patterns, and local links are valid")
        else:
            for error in report["errors"]:
                print(f"ERROR: {error}", file=sys.stderr)

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

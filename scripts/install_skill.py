#!/usr/bin/env python3
"""Install a repository skill for Codex, Claude Code, or GitHub Copilot."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = {
    "codex": {"project": Path(".agents/skills"), "user": Path("~/.agents/skills").expanduser()},
    "claude": {"project": Path(".claude/skills"), "user": Path("~/.claude/skills").expanduser()},
    "copilot": {"project": Path(".github/skills"), "user": Path("~/.copilot/skills").expanduser()},
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", required=True, choices=sorted(PLATFORMS))
    parser.add_argument("--scope", default="project", choices=["project", "user"])
    parser.add_argument("--skill", default="atmospheric-science-research", help="skill directory name")
    parser.add_argument("--all", action="store_true", help="install every skill in the suite")
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    base = PLATFORMS[args.platform][args.scope]
    if args.scope == "project":
        base = args.project_dir.resolve() / base
    names = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")) if args.all else [args.skill]
    targets = [base / name for name in names]
    existing = [target for target in targets if target.exists()]
    if existing and not args.force:
        joined = ", ".join(str(p) for p in existing)
        raise SystemExit(f"target exists: {joined}; pass --force to replace it")
    for name, target in zip(names, targets):
        source = ROOT / "skills" / name
        if not (source / "SKILL.md").exists():
            raise SystemExit(f"skill not found: {source}")
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(target)


if __name__ == "__main__":
    main()

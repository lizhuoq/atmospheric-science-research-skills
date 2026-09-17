#!/usr/bin/env python3
"""Validate structural and routing contracts for the atmospheric Skill suite."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "atmospheric-science-research",
    "atmospheric-literature-search",
    "atmospheric-paper-reader",
    "atmospheric-research-design",
    "atmospheric-statistical-analysis",
    "atmospheric-claim-audit",
    "atmospheric-manuscript-writer",
    "atmospheric-data-qc",
    "atmospheric-figure-analysis",
    "atmospheric-peer-review",
    "atmospheric-model-experiment",
    "atmospheric-extremes-attribution",
    "atmospheric-composition-air-quality",
}


def main() -> None:
    found = {p.parent.name for p in SKILLS.glob("*/SKILL.md")}
    errors: list[str] = []
    if found != EXPECTED:
        errors.append(f"skill set mismatch: missing={sorted(EXPECTED-found)} extra={sorted(found-EXPECTED)}")
    for name in sorted(EXPECTED & found):
        path = SKILLS / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            errors.append(f"{name}: missing frontmatter")
            continue
        frontmatter = text.split("---\n", 2)[1]
        if f"name: {name}" not in frontmatter or "description:" not in frontmatter:
            errors.append(f"{name}: invalid name/description")
        if len(re.findall(r"^## ", text, flags=re.MULTILINE)) < 2:
            errors.append(f"{name}: insufficient workflow structure")
        if "Quality gates" not in text and "Quality gate" not in text:
            errors.append(f"{name}: missing quality gate")
        if "Example" not in text:
            errors.append(f"{name}: missing invocation example")
        if any(marker in text for marker in ("TODO", "TBD", "coming soon")):
            errors.append(f"{name}: unfinished placeholder")
    router = (SKILLS / "atmospheric-science-research" / "SKILL.md").read_text(encoding="utf-8")
    for name in EXPECTED - {"atmospheric-science-research"}:
        if f"`$%s`" % name not in router:
            errors.append(f"router does not mention {name}")
    cases = json.loads((ROOT / "tests" / "skill_routing_cases.json").read_text(encoding="utf-8"))
    covered = {name for case in cases for name in case.get("expected", [])}
    if covered != EXPECTED:
        errors.append(f"routing cases do not cover suite: missing={sorted(EXPECTED-covered)} extra={sorted(covered-EXPECTED)}")
    for case in cases:
        if not case.get("id") or not case.get("prompt") or not case.get("expected"):
            errors.append(f"invalid routing case: {case!r}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"validated {len(EXPECTED)} skills and {len(cases)} routing cases")


if __name__ == "__main__":
    main()

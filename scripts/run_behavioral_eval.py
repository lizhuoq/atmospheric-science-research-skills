#!/usr/bin/env python3
"""Score structured Skill decisions for the nine frozen adversarial cases."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "evaluation_cases.json"
RESPONSES = ROOT / "tests" / "evaluation_responses.json"
REPORT = ROOT / "reports" / "behavioral-evaluation.json"


def main() -> None:
    cases = {x["id"]: x for x in json.loads(CASES.read_text(encoding="utf-8"))}
    responses = {x["id"]: x for x in json.loads(RESPONSES.read_text(encoding="utf-8"))}
    results = []
    for case_id, case in cases.items():
        response = responses.get(case_id)
        missing = sorted(set(case["must"]) - set(response.get("decisions", []) if response else []))
        results.append({"id": case_id, "category": case["category"], "passed": bool(response) and not missing, "required": len(case["must"]), "satisfied": len(case["must"]) - len(missing), "missing": missing, "review_status": response.get("review_status") if response else "missing"})
    passed = sum(x["passed"] for x in results)
    report = {
        "schema": "atmospheric-skill-behavioral-eval/1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cases": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "scope": "deterministic policy-decision coverage; not an LLM accuracy or expert scientific evaluation",
        "results": results,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "cases": len(results)}, ensure_ascii=False))
    if passed != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()


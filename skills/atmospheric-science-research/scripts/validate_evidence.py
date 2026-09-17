#!/usr/bin/env python3
"""Validate evidence JSONL with a small dependency-free schema subset and policy checks."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REQUIRED = {"evidence_id", "source", "claim", "study_context", "evidence_locator", "applicability", "limitations", "evidence_strength", "conflict_status", "provenance"}
DOI = re.compile(r"^(?:https://doi.org/)?10\.[0-9]{4,9}/\S+$", re.I)


def validate(record: dict, line: int) -> list[str]:
    errors = []
    missing = REQUIRED - set(record)
    if missing:
        errors.append(f"line {line}: missing {sorted(missing)}")
        return errors
    if not DOI.match(str(record["source"].get("doi", ""))):
        errors.append(f"line {line}: invalid DOI syntax")
    if record["claim"].get("claim_type") not in {"observation", "model_result", "theoretical_inference", "methodological", "dataset_description"}:
        errors.append(f"line {line}: invalid claim_type")
    if record["evidence_strength"] not in {"low", "moderate", "high", "not_assessed"}:
        errors.append(f"line {line}: invalid evidence_strength")
    split = record["provenance"].get("split")
    eligible = record["provenance"].get("rule_eligible")
    if split not in {"train", "development", "blind_test"}:
        errors.append(f"line {line}: invalid split")
    if split != "train" and eligible is True:
        errors.append(f"line {line}: leakage policy violation: non-train record is rule_eligible")
    if not record["evidence_locator"].get("locator"):
        errors.append(f"line {line}: evidence locator is empty")
    if not record["applicability"] or not record["limitations"]:
        errors.append(f"line {line}: applicability and limitations must be non-empty")
    excerpt = record["evidence_locator"].get("short_excerpt", "")
    if len(excerpt) > 500:
        errors.append(f"line {line}: short_excerpt exceeds 500 characters")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args()
    errors = []
    count = 0
    for number, raw in enumerate(args.jsonl.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        count += 1
        try:
            record = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {number}: invalid JSON: {exc.msg}")
            continue
        errors.extend(validate(record, number))
    if errors:
        raise SystemExit("evidence validation failed:\n" + "\n".join(errors))
    print(f"validated {count} evidence records")


if __name__ == "__main__":
    main()


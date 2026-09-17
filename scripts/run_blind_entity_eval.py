#!/usr/bin/env python3
"""Evaluate frozen entity extraction on blind-test PDFs without publishing records."""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from extract_entity_evidence import ENTITIES, norm_doi

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    from pypdf import PdfReader
    with (ROOT / "data/splits/paper_splits.csv").open(encoding="utf-8-sig", newline="") as f:
        splits = {norm_doi(r["doi"]): r["split"] for r in csv.DictReader(f)}
    with (ROOT / "data/metadata/all_selected.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if splits.get(norm_doi(r["doi"])) == "blind_test" and r["local_path"]]
    counts = Counter()
    errors = []
    papers_with_entity = 0
    for row in rows:
        try:
            reader = PdfReader(str(ROOT / row["local_path"]), strict=False)
            text = "\n".join((page.extract_text() or "") for page in reader.pages[:20])
            found = [entity for entity, pattern in ENTITIES.items() if re.search(pattern, text, re.I)]
            counts.update(found)
            papers_with_entity += bool(found)
        except Exception as exc:
            errors.append({"doi": row["doi"], "error": f"{type(exc).__name__}: {str(exc)[:180]}"})
    report = {
        "schema": "blind-entity-evaluation/1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "frozen_extractor": "entity-regex/1.0",
        "blind_pdfs": len(rows),
        "parsed": len(rows) - len(errors),
        "parse_errors": len(errors),
        "papers_with_at_least_one_entity": papers_with_entity,
        "coverage_among_parsed": papers_with_entity / max(1, len(rows) - len(errors)),
        "entity_mentions": dict(counts.most_common()),
        "errors": errors,
        "non_claim": "Coverage measures extractor reach, not entity-role accuracy, scientific correctness, or expert validation. No blind record is added to the runtime evidence library.",
    }
    path = ROOT / "reports/blind-entity-evaluation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("blind_pdfs", "parsed", "parse_errors", "papers_with_at_least_one_entity", "coverage_among_parsed")}, ensure_ascii=False))


if __name__ == "__main__":
    main()


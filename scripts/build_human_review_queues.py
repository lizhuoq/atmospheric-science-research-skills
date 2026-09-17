#!/usr/bin/env python3
"""Build deterministic expert-review queues for taxonomy and evidence promotion."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with (ROOT / "data/derived/paper_topics.csv").open(encoding="utf-8-sig", newline="") as f:
        papers = list(csv.DictReader(f))
    ordered = sorted(papers, key=lambda r: hashlib.sha256(("taxonomy-review-v1|" + r["doi"]).encode()).hexdigest())
    sample = ordered[:150]
    taxonomy_path = ROOT / "reports/taxonomy-review-queue.csv"
    fields = ["doi", "title", "year", "journal", "predicted_themes", "gold_themes", "reviewer", "review_status", "notes"]
    with taxonomy_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in sample:
            writer.writerow({"doi": row["doi"], "title": row["title"], "year": row["year"], "journal": row["journal"], "predicted_themes": row["themes"], "gold_themes": "", "reviewer": "", "review_status": "pending_human_review", "notes": ""})

    rules = json.loads((ROOT / "skills/atmospheric-science-research/references/method-rules.json").read_text(encoding="utf-8"))
    entity_rows = [json.loads(line) for line in (ROOT / "skills/atmospheric-science-research/references/entity-evidence.jsonl").read_text(encoding="utf-8").splitlines() if line]
    entity_rows = sorted(entity_rows, key=lambda r: hashlib.sha256(("evidence-review-v1|" + r["evidence_id"]).encode()).hexdigest())[:100]
    evidence_path = ROOT / "reports/evidence-review-queue.csv"
    fields = ["item_type", "item_id", "doi_or_source", "statement_or_entity", "locator", "decision", "corrected_value", "reviewer", "review_status", "notes"]
    with evidence_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for rule in rules:
            writer.writerow({"item_type": "method_rule", "item_id": rule["rule_id"], "doi_or_source": rule["sources"][0].get("doi") or rule["sources"][0].get("url"), "statement_or_entity": rule["statement"], "locator": rule["sources"][0]["locator"], "decision": "", "corrected_value": "", "reviewer": "", "review_status": "pending_expert_review", "notes": ""})
        for record in entity_rows:
            writer.writerow({"item_type": "entity_evidence", "item_id": record["evidence_id"], "doi_or_source": record["source"]["doi"], "statement_or_entity": record["study_context"]["datasets_instruments_models"][0], "locator": record["evidence_locator"]["locator"], "decision": "", "corrected_value": "", "reviewer": "", "review_status": "pending_expert_review", "notes": ""})
    print(json.dumps({"taxonomy_queue": len(sample), "evidence_queue": len(rules) + len(entity_rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

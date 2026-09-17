#!/usr/bin/env python3
"""Score multi-label taxonomy precision/recall after human annotations exist."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "reports/taxonomy-review-queue.csv"


def labels(value: str) -> set[str]:
    return {x.strip() for x in value.split(";") if x.strip()}


def main() -> None:
    with QUEUE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    reviewed = [r for r in rows if r["review_status"] in {"human_checked", "expert_checked"} and r["gold_themes"].strip()]
    if not reviewed:
        raise SystemExit("PENDING_HUMAN_REVIEW: no reviewed gold labels; precision/recall must not be fabricated")
    tp = fp = fn = exact = 0
    for row in reviewed:
        pred, gold = labels(row["predicted_themes"]), labels(row["gold_themes"])
        tp += len(pred & gold); fp += len(pred - gold); fn += len(gold - pred); exact += pred == gold
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    report = {"schema": "taxonomy-review/1.0", "reviewed": len(reviewed), "total_queue": len(rows), "micro_precision": precision, "micro_recall": recall, "micro_f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0, "exact_match": exact / len(reviewed), "authority": "human annotations in taxonomy-review-queue.csv"}
    (ROOT / "reports/taxonomy-review-metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()


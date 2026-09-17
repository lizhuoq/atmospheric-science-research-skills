#!/usr/bin/env python3
"""Query public corpus metadata without exposing local full-text paths."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
INDEX = SKILL_ROOT / "references" / "corpus-index.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("terms", nargs="*", help="all case-insensitive terms must occur in title/themes/methods")
    parser.add_argument("--theme")
    parser.add_argument("--year-from", type=int)
    parser.add_argument("--year-to", type=int)
    parser.add_argument("--split", choices=["train", "development", "blind_test"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    with INDEX.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    result = []
    for row in rows:
        split = row["split"]
        haystack = f"{row['title']} {row['themes']} {row['methods']}".lower()
        if any(term.lower() not in haystack for term in args.terms):
            continue
        if args.theme and args.theme not in row["themes"].split(";"):
            continue
        if args.year_from and int(row["year"]) < args.year_from:
            continue
        if args.year_to and int(row["year"]) > args.year_to:
            continue
        if args.split and split != args.split:
            continue
        result.append({"doi": row["doi"], "title": row["title"], "year": int(row["year"]), "journal": row["journal"], "themes": row["themes"].split(";"), "methods": row["methods"].split(";"), "split": split})
        if len(result) >= args.limit:
            break
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

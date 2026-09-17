#!/usr/bin/env python3
"""Import a browser-downloaded PDF and attach it to one DOI ledger row."""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"


def safe_name(text: str, limit: int = 90) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_.")
    return text[:limit] or "paper"


def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doi", required=True)
    parser.add_argument("--source", required=True, type=Path)
    args = parser.parse_args()
    doi = args.doi.lower().removeprefix("https://doi.org/")
    data = args.source.read_bytes()
    if b"%PDF-" not in data[:1024] or len(data) < 1024:
        raise SystemExit("source is not a valid-looking PDF")
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = list(reader.fieldnames or [])
    matches = [r for r in rows if r["doi"].lower().removeprefix("https://doi.org/") == doi]
    if len(matches) != 1:
        raise SystemExit(f"expected one DOI match, found {len(matches)}")
    row = matches[0]
    target = ROOT / "data" / "papers" / f"{int(row['journal_rank']):02d}" / f"{safe_name(doi)}.pdf"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.source, target)
    row["download_status"] = "downloaded_verified"
    row["local_path"] = str(target.relative_to(ROOT))
    row["sha256"] = hashlib.sha256(data).hexdigest()
    row["notes"] = "institution_browser_download"
    write(MASTER, rows, fields)
    rank_rows = [r for r in rows if r["journal_rank"] == row["journal_rank"]]
    write(MASTER.parent / f"{int(row['journal_rank']):02d}.csv", rank_rows, fields)
    print(target)


if __name__ == "__main__":
    main()

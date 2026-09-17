#!/usr/bin/env python3
"""Match browser PDF temporaries to ledger DOI text and import unique matches."""
from __future__ import annotations

import csv
import hashlib
import re
import shutil
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
DOWNLOADS = Path.home() / "Downloads"


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower().removeprefix("https://doi.org/"))


def safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_.")[:90]


def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main() -> None:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = list(reader.fieldnames or [])
    unresolved = {norm(r["doi"]): r for r in rows if not r["download_status"].startswith("downloaded")}
    imported = []
    ambiguous = []
    for source in sorted(DOWNLOADS.glob("*.tmp"), key=lambda p: p.stat().st_mtime):
        try:
            if source.read_bytes()[:5] != b"%PDF-":
                continue
            pdf = PdfReader(str(source))
            text = "\n".join((p.extract_text() or "") for p in pdf.pages[:2])
        except Exception:
            continue
        compact = norm(text)
        matches = [(key, row) for key, row in unresolved.items() if key and key in compact]
        if len(matches) != 1:
            ambiguous.append((source.name, len(matches)))
            continue
        key, row = matches[0]
        doi = row["doi"].lower().removeprefix("https://doi.org/")
        target = ROOT / "data" / "papers" / f"{int(row['journal_rank']):02d}" / f"{safe(doi)}.pdf"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        row["download_status"] = "downloaded_verified"
        row["local_path"] = str(target.relative_to(ROOT))
        row["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        row["notes"] = "institution_browser_download; doi_text_matched"
        imported.append((doi, source.name, str(target.relative_to(ROOT))))
        unresolved.pop(key)
    write(MASTER, rows, fields)
    for rank in sorted({int(r["journal_rank"]) for r in rows}):
        write(MASTER.parent / f"{rank:02d}.csv", [r for r in rows if int(r["journal_rank"]) == rank], fields)
    print(f"imported={len(imported)} ambiguous={len(ambiguous)}")
    for item in imported:
        print(" | ".join(item))
    if ambiguous:
        print("unmatched:", ambiguous)


if __name__ == "__main__":
    main()

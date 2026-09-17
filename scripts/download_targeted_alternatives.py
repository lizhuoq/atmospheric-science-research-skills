#!/usr/bin/env python3
"""Fill thin journals using alternate legal OA locations from OpenAlex."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
PAPERS = ROOT / "data" / "papers"
UA = "Mozilla/5.0 (compatible; atmospheric-science-research-skills/0.1)"


def safe(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_.")[:90]


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def try_pdf(url: str, target: Path) -> tuple[bool, str]:
    part = target.with_suffix(".pdf.part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=30) as response, part.open("wb") as handle:
            head = response.read(8192)
            if b"%PDF-" not in head[:1024]:
                return False, "not_pdf"
            handle.write(head)
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
        if part.stat().st_size < 1024:
            return False, "too_small"
        os.replace(part, target)
        return True, "ok"
    except Exception as exc:
        return False, f"{type(exc).__name__}:{str(exc)[:100]}"
    finally:
        part.unlink(missing_ok=True)


def write(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        w = csv.DictWriter(handle, fieldnames=fields); w.writeheader(); w.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-per-journal", type=int, default=10)
    args = parser.parse_args()
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = list(reader.fieldnames or [])
    counts = Counter(r["journal"] for r in rows if r["download_status"].startswith("downloaded"))
    journals = list(dict.fromkeys(r["journal"] for r in rows))
    attempted = added = 0
    for journal in journals:
        need = args.target_per_journal - counts[journal]
        if need <= 0:
            continue
        candidates = [r for r in rows if r["journal"] == journal and not r["download_status"].startswith("downloaded")]
        candidates.sort(key=lambda r: (int(r["year"]) >= 2021, int(r["openalex_cited_by_count"] or 0)), reverse=True)
        print(f"{journal}: need {need}", flush=True)
        for row in candidates:
            if need <= 0:
                break
            attempted += 1
            work_id = row["openalex_id"].rsplit("/", 1)[-1]
            try:
                work = get_json(f"https://api.openalex.org/works/{work_id}")
            except Exception as exc:
                row["notes"] = f"alternate_lookup_failed:{type(exc).__name__}"
                continue
            urls = []
            for loc in work.get("locations") or []:
                url = loc.get("pdf_url")
                if url and url not in urls:
                    urls.append(url)
            doi = row["doi"].lower().removeprefix("https://doi.org/")
            target = PAPERS / f"{int(row['journal_rank']):02d}" / f"{safe(doi)}.pdf"
            target.parent.mkdir(parents=True, exist_ok=True)
            errors = []
            for url in urls:
                ok, reason = try_pdf(url, target)
                if ok:
                    data = target.read_bytes()
                    row["download_status"] = "downloaded_verified"
                    row["local_path"] = str(target.relative_to(ROOT))
                    row["sha256"] = hashlib.sha256(data).hexdigest()
                    row["notes"] = f"openalex_alternate_location:{url}"
                    counts[journal] += 1; need -= 1; added += 1
                    print(f"  + {doi} ({counts[journal]}/{args.target_per_journal})", flush=True)
                    break
                errors.append(reason)
            if not row["download_status"].startswith("downloaded"):
                row["notes"] = f"alternate_locations_tried={len(urls)}; " + "; ".join(errors[:3])
            time.sleep(0.1)
            if attempted % 10 == 0:
                write(MASTER, rows, fields)
    write(MASTER, rows, fields)
    for rank in sorted({int(r["journal_rank"]) for r in rows}):
        write(MASTER.parent / f"{rank:02d}.csv", [r for r in rows if int(r["journal_rank"]) == rank], fields)
    print(f"attempted={attempted} added={added}", flush=True)
    print(dict((j, counts[j]) for j in journals if counts[j] < args.target_per_journal), flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Download only direct OA PDFs listed in the selected metadata."""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
PAPERS = ROOT / "data" / "papers"
UA = "Mozilla/5.0 (compatible; atmospheric-science-research-skills/0.1; research corpus builder)"
LOCK = threading.Lock()


def safe_name(text: str, limit: int = 90) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_.")
    return text[:limit] or "paper"


def target_for(row: dict) -> Path:
    rank = int(row["journal_rank"])
    doi = row["doi"].removeprefix("https://doi.org/")
    return PAPERS / f"{rank:02d}" / f"{safe_name(doi)}.pdf"


def download_one(index: int, row: dict) -> tuple[int, str, str, str, str]:
    url = row.get("pdf_url", "")
    if not url:
        return index, "no_direct_pdf", "", "", ""
    target = target_for(row)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 1024:
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        return index, "downloaded_verified", str(target.relative_to(ROOT)), digest, "already_present"
    part = target.with_suffix(".pdf.part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=30) as response, part.open("wb") as handle:
            head = response.read(8192)
            if b"%PDF-" not in head[:1024]:
                return index, "not_pdf", "", "", f"content_type={response.headers.get('Content-Type','')}"
            handle.write(head)
            digest = hashlib.sha256(); digest.update(head)
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk); digest.update(chunk)
        if part.stat().st_size < 1024:
            part.unlink(missing_ok=True)
            return index, "invalid_pdf", "", "", "file_too_small"
        os.replace(part, target)
        return index, "downloaded_verified", str(target.relative_to(ROOT)), digest.hexdigest(), ""
    except Exception as exc:
        part.unlink(missing_ok=True)
        return index, "download_failed", "", "", f"{type(exc).__name__}: {str(exc)[:180]}"


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = list(reader.fieldnames or [])
    # Retry transient failures, but do not repeatedly hit known HTML/non-PDF
    # endpoints or rows which never had a direct PDF URL.
    retryable = {"", "pending", "download_failed", "skipped_final_download_failed"}
    pending = [(i, r) for i, r in enumerate(rows) if r.get("download_status", "") in retryable]
    if args.limit:
        pending = pending[: args.limit]
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download_one, i, row): i for i, row in pending}
        for future in as_completed(futures):
            i, status, local_path, digest, note = future.result()
            rows[i]["download_status"] = status
            rows[i]["local_path"] = local_path
            rows[i]["sha256"] = digest
            if note:
                rows[i]["notes"] = note
            done += 1
            if done % 25 == 0 or done == len(pending):
                print(f"processed {done}/{len(pending)}", flush=True)
                with LOCK:
                    write_csv(MASTER, rows, fields)
    # Keep per-journal views synchronized with the master ledger.
    by_rank: dict[int, list[dict]] = {}
    for row in rows:
        by_rank.setdefault(int(row["journal_rank"]), []).append(row)
    for rank, selected in by_rank.items():
        write_csv(MASTER.parent / f"{rank:02d}.csv", selected, fields)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["download_status"]] = counts.get(row["download_status"], 0) + 1
    print(counts, flush=True)


if __name__ == "__main__":
    main()

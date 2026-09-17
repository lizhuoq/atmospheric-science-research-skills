#!/usr/bin/env python3
"""Audit ledger/file integrity and a deterministic stratified PDF parse sample."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
OUTPUT = ROOT / "reports" / "corpus-audit.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sample_rows(rows: list[dict], per_journal: int) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        if row["local_path"] and (ROOT / row["local_path"]).exists():
            groups[row["journal"]].append(row)
    selected = []
    for journal in sorted(groups):
        ranked = sorted(groups[journal], key=lambda r: hashlib.sha256(r["doi"].encode()).hexdigest())
        selected.extend(ranked[:per_journal])
    return selected


def parse_pdf(path: Path) -> dict:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path), strict=False)
        pages = len(reader.pages)
        texts = []
        image_count = 0
        for page in reader.pages[: min(5, pages)]:
            texts.append(page.extract_text() or "")
            try:
                image_count += len(page.images)
            except Exception:
                pass
        text = "\n".join(texts)
        chars = len(text.strip())
        return {
            "status": "parsed",
            "pages": pages,
            "sample_text_chars": chars,
            "text_layer_usable": chars >= 1000,
            "figure_caption_signal": bool(re.search(r"\bfig(?:ure)?\.?\s*\d+", text, re.I)),
            "table_caption_signal": bool(re.search(r"\btable\s*\d+", text, re.I)),
            "formula_signal": bool(re.search(r"[=∑∫∂]|\b(?:equation|eq\.)\s*\(?\d+", text, re.I)),
            "images_on_sample_pages": image_count,
        }
    except Exception as exc:
        return {"status": "parse_error", "error": f"{type(exc).__name__}: {str(exc)[:240]}"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-per-journal", type=int, default=3)
    parser.add_argument("--skip-hashes", action="store_true")
    args = parser.parse_args()
    with MASTER.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    status = Counter(r["download_status"] for r in rows)
    integrity = Counter()
    referenced: set[Path] = set()
    issues = []
    for row in rows:
        if not row["local_path"]:
            continue
        path = (ROOT / row["local_path"]).resolve()
        referenced.add(path)
        if not path.exists():
            integrity["missing"] += 1
            issues.append({"doi": row["doi"], "issue": "missing", "path": row["local_path"]})
            continue
        with path.open("rb") as f:
            header_ok = b"%PDF-" in f.read(1024)
        if not header_ok:
            integrity["bad_header"] += 1
            issues.append({"doi": row["doi"], "issue": "bad_header", "path": row["local_path"]})
        elif not args.skip_hashes and row["sha256"] and digest(path) != row["sha256"]:
            integrity["hash_mismatch"] += 1
            issues.append({"doi": row["doi"], "issue": "hash_mismatch", "path": row["local_path"]})
        else:
            integrity["ok"] += 1
    disk_files = {p.resolve() for p in (ROOT / "data" / "papers").rglob("*") if p.is_file()}
    samples = []
    for row in sample_rows(rows, args.sample_per_journal):
        parsed = parse_pdf(ROOT / row["local_path"])
        samples.append({"doi": row["doi"], "journal": row["journal"], "path": row["local_path"], **parsed})
    parse_counts = Counter(s["status"] for s in samples)
    for key in ("text_layer_usable", "figure_caption_signal", "table_caption_signal", "formula_signal"):
        parse_counts[key] = sum(bool(s.get(key)) for s in samples)
    report = {
        "schema": "atmospheric-corpus-audit/1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "ledger_records": len(rows),
        "status_counts": dict(status),
        "referenced_local_files": len(referenced),
        "disk_files": len(disk_files),
        "unreferenced_disk_files": sorted(str(p.relative_to(ROOT)) for p in disk_files - referenced),
        "integrity_counts": dict(integrity),
        "hash_check_performed": not args.skip_hashes,
        "integrity_issues": issues,
        "parse_sample": {"strategy": f"stable-hash sample, up to {args.sample_per_journal} per journal", "size": len(samples), "counts": dict(parse_counts), "records": samples},
        "interpretation": "Caption and formula fields are text-pattern signals, not proof that tables, equations, or figure semantics were faithfully reconstructed. Visual inspection remains required for scientific extraction."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"integrity": report["integrity_counts"], "parse": report["parse_sample"]["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

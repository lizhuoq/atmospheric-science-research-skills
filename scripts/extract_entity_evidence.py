#!/usr/bin/env python3
"""Extract conservative entity mentions from training PDFs into public-safe JSONL."""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
SPLITS = ROOT / "data" / "splits" / "paper_splits.csv"
OUTPUT = ROOT / "skills" / "atmospheric-science-research" / "references" / "entity-evidence.jsonl"

ENTITIES = {
    "ERA5": r"\bERA-?5\b",
    "ERA-Interim": r"\bERA[ -]?Interim\b",
    "MERRA-2": r"\bMERRA[ -]?2\b",
    "JRA-55": r"\bJRA[ -]?55\b",
    "WRF": r"\bWRF(?:-Chem)?\b",
    "WRF-Chem": r"\bWRF[ -]?Chem\b",
    "CESM": r"\bCESM\d*(?:\.\d+)?\b",
    "CMIP5": r"\bCMIP5\b",
    "CMIP6": r"\bCMIP6\b",
    "ECMWF": r"\bECMWF\b",
    "GFS": r"\bGlobal Forecast System\b|\bGFS\b",
    "MODIS": r"\bMODIS\b",
    "CALIPSO": r"\bCALIPSO\b",
    "CloudSat": r"\bCloudSat\b",
    "TRMM": r"\bTRMM\b",
    "GPM": r"\bGlobal Precipitation Measurement\b|\bGPM\b",
    "AERONET": r"\bAERONET\b",
    "radiosonde": r"\bradiosondes?\b",
    "Doppler radar": r"\bDoppler radar\b",
    "lidar": r"\blidar\b",
    "eddy covariance": r"\beddy covariance\b",
}


def norm_doi(value: str) -> str:
    return value.lower().removeprefix("https://doi.org/")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("pypdf is required for build-time extraction; it is not a runtime dependency") from exc
    with SPLITS.open(encoding="utf-8-sig", newline="") as f:
        split = {norm_doi(r["doi"]): r["split"] for r in csv.DictReader(f)}
    with MASTER.open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if split.get(norm_doi(r["doi"])) == "train" and r["local_path"]]
    if args.limit:
        rows = rows[: args.limit]
    records = []
    errors = []
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    for row in rows:
        path = ROOT / row["local_path"]
        try:
            reader = PdfReader(str(path), strict=False)
            found = set()
            for page_number, page in enumerate(reader.pages[: args.max_pages], 1):
                text = page.extract_text() or ""
                for entity, pattern in ENTITIES.items():
                    if entity in found or not re.search(pattern, text, re.I):
                        continue
                    found.add(entity)
                    key = re.sub(r"[^a-z0-9]+", "-", entity.lower()).strip("-")
                    records.append({
                        "evidence_id": f"ev-entity-{norm_doi(row['doi']).replace('/', '-').replace('.', '-')}-{key}",
                        "source": {"doi": norm_doi(row["doi"]), "title": row["title"], "year": int(row["year"]), "openalex_id": row["openalex_id"], "access_class": "open_access" if row["is_oa"].lower() == "true" else "unknown"},
                        "claim": {"statement": f"This paper contains a verifiable mention of {entity}; inspect the cited page to determine whether it is an input, instrument, model, comparator, or background reference.", "claim_type": "dataset_description", "variables": []},
                        "study_context": {"domain": [x.strip() for x in row["topics"].split(";") if x.strip()] or ["atmospheric science"], "spatial_scope": "not extracted", "temporal_scope": "not extracted", "atmospheric_scale": ["unspecified"], "study_design": "mixed", "datasets_instruments_models": [entity], "resolution": []},
                        "evidence_locator": {"locator_type": "page", "locator": f"PDF page {page_number}", "support_kind": "context_only"},
                        "applicability": ["candidate identification of datasets, instruments, or models for later source verification"],
                        "limitations": ["automated string match does not establish the entity's scientific role", "page uses PDF index and may differ from printed numbering", "full-text verification is required before making a scientific claim"],
                        "evidence_strength": "not_assessed",
                        "conflict_status": {"status": "not_checked", "related_evidence_ids": [], "notes": "entity mention only"},
                        "provenance": {"split": "train", "extracted_by": "entity-regex/1.0", "extracted_at": timestamp, "review_status": "machine_draft", "rule_eligible": False},
                    })
        except Exception as exc:
            errors.append({"doi": row["doi"], "error": f"{type(exc).__name__}: {str(exc)[:180]}"})
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n" for r in records), encoding="utf-8")
    report = {"schema": "entity-evidence-extraction/1.0", "training_pdfs_attempted": len(rows), "records": len(records), "errors": errors, "max_pages": args.max_pages, "runtime_pdf_dependency": False}
    (ROOT / "reports" / "entity-evidence-extraction.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"papers": len(rows), "records": len(records), "errors": len(errors)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

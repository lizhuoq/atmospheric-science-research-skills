#!/usr/bin/env python3
"""Build copyright-safe, standalone runtime resources for the public skill."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ROOT / "data" / "derived" / "paper_topics.csv"
SPLITS = ROOT / "data" / "splits" / "paper_splits.csv"
SKILL = ROOT / "skills" / "atmospheric-science-research"
INDEX = SKILL / "references" / "corpus-index.csv"
MANIFEST = SKILL / "references" / "runtime-manifest.json"


def canonical_text_sha256(path: Path) -> str:
    """Hash logical UTF-8 text independently of checkout line endings."""
    content = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def build() -> tuple[str, str]:
    with SPLITS.open(encoding="utf-8-sig", newline="") as f:
        split = {r["doi"].lower().removeprefix("https://doi.org/"): r["split"] for r in csv.DictReader(f)}
    with TOPICS.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    from io import StringIO
    out = StringIO(newline="")
    fields = ["doi", "title", "year", "journal", "themes", "methods", "split"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        doi = row["doi"].lower().removeprefix("https://doi.org/")
        writer.writerow({key: row[key] for key in fields if key != "split"} | {"split": split[doi]})
    content = out.getvalue()
    entity_path = SKILL / "references" / "entity-evidence.jsonl"
    rules_path = SKILL / "references" / "method-rules.json"
    manifest = {
        "schema": "atmospheric-skill-runtime/1.0",
        "records": len(rows),
        "content": "bibliographic metadata and derived labels only; no abstracts, excerpts, full text, local paths, or hashes",
        "source_index_sha256": canonical_text_sha256(TOPICS),
        "runtime_index_sha256": hashlib.sha256(content.encode()).hexdigest(),
        "entity_evidence_records": sum(1 for line in entity_path.read_text(encoding="utf-8").splitlines() if line.strip()) if entity_path.exists() else 0,
        "entity_evidence_sha256": canonical_text_sha256(entity_path) if entity_path.exists() else None,
        "method_rules": len(json.loads(rules_path.read_text(encoding="utf-8"))) if rules_path.exists() else 0,
        "method_rules_sha256": canonical_text_sha256(rules_path) if rules_path.exists() else None,
        "private_build_corpus_required_at_runtime": False,
        "offline_demo_available": True,
        "network_or_user_provided_papers_required_for_new_topic_review": True,
        "bundled_index_role": "optional example, terminology seed, and regression-test fixture; not a closed-world knowledge base",
    }
    return content, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    index, manifest = build()
    outputs = {INDEX: index, MANIFEST: manifest}
    if args.check:
        stale = [str(p.relative_to(ROOT)) for p, value in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != value]
        if stale:
            raise SystemExit("stale runtime resources: " + ", ".join(stale))
    else:
        for path, value in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8")
        print(f"built standalone index with {manifest.count(chr(10)) and len(index.splitlines()) - 1} records")


if __name__ == "__main__":
    main()

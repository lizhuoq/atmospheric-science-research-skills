#!/usr/bin/env python3
"""Fail when likely copyrighted full text, PDFs, or secrets enter public paths."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".venv", "__pycache__", "papers", "extracted", "cache"}
APPROVED_LARGE_METADATA = {Path("data/raw")}
SECRET = re.compile(r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"][^'\"]{8,}")
findings = []
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in SKIP for part in path.parts):
        continue
    rel = path.relative_to(ROOT)
    if path.suffix.lower() == ".pdf":
        findings.append(f"PDF outside ignored corpus: {rel}")
        continue
    approved_metadata = any(base == rel.parent or base in rel.parents for base in APPROVED_LARGE_METADATA)
    if not approved_metadata and path.stat().st_size > 5_000_000 and path.suffix.lower() in {".txt", ".md", ".json", ".jsonl", ".csv"}:
        findings.append(f"large text-like file requires review: {rel}")
    if path.suffix.lower() in {".py", ".md", ".json", ".jsonl", ".yaml", ".yml", ".toml"}:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET.search(text):
            findings.append(f"possible secret: {rel}")
if findings:
    raise SystemExit("publication safety check failed:\n" + "\n".join(f"- {x}" for x in findings))
print("publication safety check passed")

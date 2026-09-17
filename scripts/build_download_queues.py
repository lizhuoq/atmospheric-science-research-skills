#!/usr/bin/env python3
"""Build deterministic publisher queues and a compact acquisition report."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
QUEUE = ROOT / "data" / "queues"


def main() -> None:
    QUEUE.mkdir(parents=True, exist_ok=True)
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = list(reader.fieldnames or [])
    unresolved = [r for r in rows if not r["download_status"].startswith("downloaded")]
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in unresolved:
        host = urlparse(row.get("pdf_url") or row.get("landing_page_url") or "").netloc or "no_host"
        groups[host].append(row)
    index = []
    for host, selected in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        name = "".join(c if c.isalnum() or c in "._-" else "_" for c in host)
        path = QUEUE / f"{name}.csv"
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(selected)
        index.append({"host": host, "count": len(selected), "queue": str(path.relative_to(ROOT))})
    summary = {
        "total_selected": len(rows),
        "status": dict(Counter(r["download_status"] for r in rows)),
        "bytes_downloaded": sum((ROOT / r["local_path"]).stat().st_size for r in rows if r["local_path"] and (ROOT / r["local_path"]).exists()),
        "per_journal_downloaded": dict(sorted(Counter(r["journal"] for r in rows if r["download_status"].startswith("downloaded")).items())),
        "queues": index,
    }
    (QUEUE / "index.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary["status"], ensure_ascii=False))
    print(f"queues={len(index)} bytes={summary['bytes_downloaded']}")


if __name__ == "__main__":
    main()

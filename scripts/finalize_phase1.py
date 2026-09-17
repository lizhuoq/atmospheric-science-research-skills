#!/usr/bin/env python3
"""Freeze phase-1 acquisition state and verify every downloaded PDF."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "data" / "metadata" / "all_selected.csv"
REPORT_JSON = ROOT / "data" / "phase1-final-report.json"
REPORT_MD = ROOT / "docs" / "phase1-final-report.md"

FINAL_MAP = {
    "no_direct_pdf": "skipped_final_no_direct_pdf",
    "not_pdf": "skipped_final_not_pdf",
    "download_failed": "skipped_final_download_failed",
    "pending": "skipped_final_not_attempted",
    "": "skipped_final_not_attempted",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_rows(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)


def main() -> None:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle); rows = list(reader); fields = list(reader.fieldnames or [])

    failures = []
    total_bytes = 0
    verified = 0
    for row in rows:
        status = row.get("download_status", "")
        if status in {"downloaded", "downloaded_verified"}:
            path = ROOT / row["local_path"]
            if not path.exists():
                failures.append({"doi": row["doi"], "reason": "file_missing", "path": row["local_path"]})
                row["download_status"] = "verification_failed_missing"
                continue
            size = path.stat().st_size
            total_bytes += size
            with path.open("rb") as handle:
                header = handle.read(8)
            actual_hash = sha256(path)
            if b"%PDF-" not in header or size < 1024 or actual_hash != row.get("sha256"):
                failures.append({"doi": row["doi"], "reason": "signature_size_or_hash_mismatch", "path": row["local_path"]})
                row["download_status"] = "verification_failed_integrity"
            else:
                verified += 1
                row["download_status"] = "downloaded_verified"
        elif status in FINAL_MAP:
            row["download_status"] = FINAL_MAP[status]

    write_rows(MASTER, rows, fields)
    by_rank: dict[int, list[dict]] = {}
    for row in rows:
        by_rank.setdefault(int(row["journal_rank"]), []).append(row)
    for rank, selected in by_rank.items():
        write_rows(MASTER.parent / f"{rank:02d}.csv", selected, fields)

    counts = Counter(row["download_status"] for row in rows)
    per_journal = {}
    for journal in sorted({row["journal"] for row in rows}):
        jr = [row for row in rows if row["journal"] == journal]
        per_journal[journal] = {
            "selected": len(jr),
            "downloaded_verified": sum(row["download_status"] == "downloaded_verified" for row in jr),
        }
    report = {
        "schema": "atmospheric-corpus-phase1-final/1.0",
        "finalized_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_window": {"from": "2016-01-01", "to": "2025-12-31"},
        "journals": len(per_journal),
        "selected_records": len(rows),
        "downloaded_verified": verified,
        "downloaded_bytes": total_bytes,
        "status_counts": dict(counts),
        "integrity_failures": failures,
        "per_journal": per_journal,
        "retry_policy": "frozen_by_user_request; skipped and failed items are terminal and must not be retried automatically",
        "open_source_boundary": "metadata and scripts may be published; data/papers must not be committed",
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 第一阶段最终报告",
        "",
        f"- 期刊：{report['journals']} 本",
        f"- 入选元数据：{report['selected_records']} 篇（每刊 100 篇）",
        f"- 已下载并通过 PDF 头、文件大小与 SHA-256 校验：{verified} 篇",
        f"- 本地全文体积：{total_bytes / 1024**3:.2f} GiB",
        f"- 完整性异常：{len(failures)} 篇",
        "",
        "## 最终状态",
        "",
    ]
    lines.extend(f"- `{key}`：{value}" for key, value in sorted(counts.items()))
    lines += [
        "",
        "未成功条目已依用户要求冻结为终态，不再自动重试。PDF 全文目录受 `.gitignore` 排除；开源时只提交元数据、协议、脚本和统计报告。",
        "",
        "## 方法限制",
        "",
        "候选集按 OpenAlex 引用数排序并加入主题新颖度奖励；引用数存在年份累积偏差。30 刊是兼顾领域影响力与子方向覆盖的代表性候选集，并非经 JCR 当年排名核验后的严格前 30 名。",
    ]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"verified": verified, "bytes": total_bytes, "failures": len(failures), "status": dict(counts)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

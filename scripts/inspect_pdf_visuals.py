#!/usr/bin/env python3
"""Render and inspect PDF pages for text, tables, figures, and equation signals."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--max-pages", type=int, default=8)
    parser.add_argument("--dpi", type=int, default=144)
    args = parser.parse_args()
    import pdfplumber
    import pypdfium2 as pdfium
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"schema": "pdf-visual-inspection/1.0", "source_name": args.pdf.name, "pages": [], "limitations": ["caption and equation detection are heuristic", "rendering supports human inspection but does not infer figure meaning", "table extraction must be checked against the rendered page"]}
    rendered = pdfium.PdfDocument(str(args.pdf))
    with pdfplumber.open(args.pdf) as pdf:
        count = min(len(pdf.pages), args.max_pages)
        for i in range(count):
            page = pdf.pages[i]
            text = page.extract_text() or ""
            tables = page.extract_tables()
            signals = {
                "figure_captions": re.findall(r"(?im)^\s*fig(?:ure)?\.?\s*\d+[^\n]{0,180}", text),
                "table_captions": re.findall(r"(?im)^\s*table\s*\d+[^\n]{0,180}", text),
                "equation_signal": bool(re.search(r"[=∑∫∂]|\b(?:equation|eq\.)\s*\(?\d+", text, re.I)),
                "tables_detected": len(tables),
                "text_chars": len(text),
            }
            image = rendered[i].render(scale=args.dpi / 72).to_pil()
            name = f"page-{i + 1:04d}.png"
            image.save(args.output_dir / name)
            manifest["pages"].append({"pdf_page": i + 1, "render": name, **signals})
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(manifest["pages"]), "output": str(args.output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()


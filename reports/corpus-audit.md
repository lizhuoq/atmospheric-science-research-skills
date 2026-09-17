# Corpus audit — milestone 1

Generated 2026-09-16 from the local ledger and files. The machine-readable result is `reports/corpus-audit.json`.

## Inventory and integrity

- Metadata records: 3,000 across 30 journals.
- Ledger-referenced local PDFs: 1,081.
- Status before re-freeze: 1,076 `downloaded_verified` plus 5 `downloaded`.
- Files passing existence, PDF header, and SHA-256 checks: 1,081 / 1,081.
- Missing, bad-header, or hash-mismatch files: 0.
- Unreferenced files: 16, all `.pdf.part` download remnants. They were recorded and left untouched.
- The legacy `data/phase1-final-report.json` was stale at 962 verified files. The cause was a finalizer that counted only rows entering as `downloaded` and not rows already marked `downloaded_verified`; the finalizer has been corrected and the corpus re-frozen.

## Parseability sample

Sampling used a stable DOI hash and selected up to 3 local PDFs per journal (90 total).

- Parsed: 89 / 90.
- Usable text layer in the first five pages: 89 / 90 overall; 89 / 89 among parsed files.
- Figure-caption text signal: 73 / 90.
- Table-caption text signal: 49 / 90.
- Formula/equation text signal: 50 / 90.
- Parse error: DOI `10.5194/cp-15-1691-2019`, `PdfStreamError: Stream has ended unexpectedly`.

These signals establish that most sampled files support text-based evidence location. They do not establish faithful formula, table, or figure reconstruction. Scientific extraction from graphics and equations still requires page rendering and visual verification. The failed PDF needs repair or a different legal copy before full-text use; no redownload was attempted.

## Risks requiring follow-up

- The 16 partial files should be manually reviewed before optional cleanup; they are Git-ignored and not a publication risk.
- PDF parsers can recover text from malformed files differently; parser version and errors should be stored with future extraction records.
- A 90-paper sample estimates feasibility, not per-paper parse quality for all 1,081 PDFs.
- Five records were promoted to verified only after the full audit; derived manifests were regenerated afterward.


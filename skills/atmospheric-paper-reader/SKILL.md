---
name: atmospheric-paper-reader
description: Read atmospheric-science papers deeply and extract atomic, source-located evidence from text, methods, equations, tables, and figures. Use after papers have been supplied or lawfully acquired; do not use metadata or abstracts as substitutes for full-text evidence.
---

# Atmospheric Paper Reader

Turn papers into auditable evidence records without copying substantial copyrighted text.

## Workflow

1. Confirm the paper identity, DOI, version, publication status, access category, and file integrity. Keep different versions distinct.
2. Map the paper structure and the user's target claims. Read the abstract for orientation, then inspect the relevant introduction, data, methods, results, figures/tables, discussion, supplements, and limitations.
3. For PDFs, use text extraction for navigation and rendered-page inspection for equations, symbols, maps, multi-panel figures, tables, superscripts, and multi-column order. Mark unreadable content instead of guessing.
4. Extract one claim per record. Classify it as observation, model result, theoretical inference, methodological result, dataset description, or author interpretation.
5. Bind the claim to DOI, title, year, version, page and section, plus table/equation/figure/panel when applicable. Separate paraphrase from any short necessary quotation.
6. Capture region, period, atmospheric scale, sampling, datasets/instruments/models, variables, units, resolution, preprocessing, QC, assumptions, statistical method, validation, uncertainty, and limitations.
7. Record whether support is direct, indirect, or contextual. A cited source inside the paper is not automatically verified evidence; retrieve the original when the downstream claim depends on it.
8. Compare text with tables and figures for internal inconsistencies. Note sample attrition, omitted cases, sensitivity results, and statements that exceed the presented evidence.
9. Output structured records conforming to the repository evidence schema when available. Use `unknown` for absent information and `not_applicable` only when justified.

## Output

- Bibliographic and version identity
- Reading coverage and inaccessible components
- Atomic evidence table with locators and evidence type
- Methods/data/instrument/model inventory
- Uncertainty, limitations, and internal inconsistencies
- Claims requiring source follow-up or expert review

## Quality gates

Do not reconstruct missing values from a plot unless explicitly performing a documented digitization. Do not treat discussion speculation as a measured result. Do not expose long excerpts or redistribute full text. If only an abstract is available, label the output `abstract_only` and restrict it accordingly.

## Example

`Use atmospheric-paper-reader on these five PDFs and extract source-located evidence about boundary-layer-height retrieval assumptions and validation errors.`

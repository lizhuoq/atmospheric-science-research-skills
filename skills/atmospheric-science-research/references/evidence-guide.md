# Evidence record guide

Use `schemas/evidence-record.schema.json` as the source of truth. Store one atomic claim per JSONL line. A compound sentence with different evidence types must become separate records.

Normalize DOI values to `10.prefix/suffix` when comparing records, but retain a resolvable DOI in output. A locator must identify where support can be checked: PDF page plus section is preferred; table or figure number is required for values read from graphics. Publisher page numbering and PDF page index can differ, so say which one is used.

`evidence_strength` is an assessment of support for this scoped claim, not journal prestige or citation count:

- `high`: direct result, appropriate design, relevant validation, and bounded uncertainty for the stated scope.
- `moderate`: direct but limited in representativeness, validation, precision, or robustness.
- `low`: indirect, exploratory, underpowered, weakly validated, or highly assumption-dependent.
- `not_assessed`: insufficient information; never silently upgrade it.

Set `conflict_status.status` to `not_checked` until a deliberate comparison has been performed. Contradiction requires compatible variables, scales, and estimands; otherwise describe the studies as non-comparable.

Only `train` evidence may set `provenance.rule_eligible` to true. Development and blind-test evidence must set it to false. Short excerpts are optional and limited to 500 characters by schema; paraphrase by default.


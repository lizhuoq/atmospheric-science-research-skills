# Contributing

Contributions should improve a bounded research workflow, its evidence base, or its tests. Do not add paper PDFs, extracted full text, credentials, or publisher-session data.

## Before opening a pull request

1. Run `python scripts/build_milestone1.py --check` and `python -m unittest discover -s tests -v`.
2. Run `python scripts/check_publication_safety.py` and resolve every finding.
3. For a scientific rule, add an evidence record conforming to `schemas/evidence-record.schema.json`. Include DOI, title, year, locator, applicability, limitations, and evidence strength.
4. Rules may use only the training split. Development records may tune workflow behavior. Blind-test records must not appear in rules, examples, or reference notes.
5. Keep quotations short and necessary. Prefer paraphrased structured facts and precise source locators.

Changes to the taxonomy, split algorithm, schema, or evidence policy require a short decision record in `docs/decisions/` and regenerated reports.


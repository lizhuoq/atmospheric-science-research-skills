# Human and expert review protocol

Machine extraction, deterministic validation, and model-based critique cannot be labeled as human or expert review.

## Taxonomy review

1. Open `reports/taxonomy-review-queue.csv` without changing DOI, title, or predicted labels.
2. A reviewer assigns semicolon-separated `gold_themes`, their name or stable reviewer identifier, and `human_checked` or `expert_checked`.
3. Use two independent atmospheric-science reviewers for ambiguous or multi-domain records. Resolve disagreements in `notes` without deleting the original predictions.
4. Run `python scripts/score_taxonomy_review.py` only after annotations exist.

## Evidence and rule review

For each row in `reports/evidence-review-queue.csv`, inspect the cited source and locator. Choose `accept`, `correct`, `reject`, or `insufficient_access`; record corrections and limitations. An entity mention is accepted only as a locator unless the reviewer verifies its scientific role. A method rule is promoted only if its wording, applicability, exceptions, and source entailment are all acceptable.

Only a domain-qualified reviewer may assign `expert_checked`. Contributor identity, date, and review scope should be retained in version control or an accompanying signed review record.

Until review occurs, release notes must display `PENDING_HUMAN_REVIEW`. Absence of review is not a software failure, but it prevents claims of expert validation or measured taxonomy accuracy.


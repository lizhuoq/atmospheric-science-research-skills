# Standalone Skill completion status

Generated 2026-09-17.

## Runtime independence

The installed `atmospheric-science-research` entry Skill contains:

- 3,000 bibliographic/index records with themes, method signals, and frozen split;
- 1,551 training-only entity evidence records covering 21 normalized datasets, models, reanalyses, and instrument classes;
- 10 source-backed methodological rules;
- evidence and scientific-comparison guidance;
- metadata query and evidence validators.

It contains zero PDFs, zero abstracts or full-text passages, zero local PDF paths, and zero publisher credentials. Runtime requires neither the source repository nor network access. An isolation test installs the Skill into an empty temporary project and successfully queries the bundled index.

## Task-oriented suite

- Forecast-verification checks live under `atmospheric-statistical-analysis`, with configuration and experiment decisions under `atmospheric-model-experiment`.
- Remote-sensing measurement-chain and collocation checks live under `atmospheric-data-qc`, with visual evidence handled by `atmospheric-figure-analysis`.
- The lightweight entry Skill routes across 12 task-oriented specialist Skills.

## Evaluation completed

- 9/9 frozen behavioral policy cases passed deterministic decision-coverage checks.
- Blind extractor evaluation used 163 blind-test PDFs only after the extractor was frozen: 155 parsed, 8 parse errors, and 101/155 parsed papers contained at least one controlled entity (65.2% reach).
- No blind record was added to the runtime evidence library.
- PDF visual inspection was smoke-tested using rendered pages, caption/equation signals, and table extraction candidates.
- 11 automated repository tests pass.

These results establish engineering behavior and bounded extractor reach. They do not establish scientific conclusion accuracy or expert validation.

## Mandatory human gates

Two activities cannot be honestly completed by software alone:

1. Expert review of scientific/methodological rules and source entailment.
2. Independent human gold labeling required to report taxonomy precision and recall.

The repository provides deterministic queues and scoring tools:

- `reports/evidence-review-queue.csv`: 110 rule/entity items awaiting expert review.
- `reports/taxonomy-review-queue.csv`: 150 stratified metadata records awaiting human gold labels.
- `scripts/score_taxonomy_review.py`: refuses to emit metrics until real reviewed labels exist.
- `docs/human-review-protocol.md`: review and promotion procedure.

Current release status for those two gates is `PENDING_HUMAN_REVIEW`. This is an explicit scientific-integrity boundary, not an implementation omission.

# Cross-stage workflow ledger

Use this contract for multi-stage research tasks so that assumptions and evidence do not silently change between Skills.

## Scope freeze

Before freezing a search or design, record operational definitions for region/domain, phenomenon or exposure, outcome, period, spatial and temporal scale, study types, languages, publication status, and intended inference. If a choice would materially change the result, obtain user confirmation when practical; otherwise analyze clearly labeled scenarios rather than silently choosing one.

`Current literature` means the search is rerun through the actual search date. State that date and any publication lag. Search online-first and preprints when relevant, link preprints to later versions of record, and label peer-review status. A narrower recency window must be explicit rather than assumed.

## Prioritization and stopping

Prioritize full-text reading by direct relevance to the scoped question, study-design informativeness, source/version reliability, coverage of contrasting methods/regions/regimes, contradiction, and citation-network role—not citation count alone.

Before design or synthesis, define a target set appropriate to the task. Stop or pause deep reading when:

- every major concept and intended design decision has at least one directly relevant full-text source or is labeled an evidence gap;
- backward/forward chaining and the last documented query round produce no material new method, mechanism, population, or contradiction;
- excluded and inaccessible literature is accounted for; and
- remaining uncertainty is reported as a coverage limitation.

This is a transparent saturation rule, not proof that the search is exhaustive. Systematic reviews require a protocol-specific stopping rule and flow accounting.

## Required ledger fields

- scope version, assumptions, and user decisions;
- source, exact query, filters, search date, result counts, and unavailable databases;
- DOI/stable identifier, version, peer-review and correction/retraction status;
- access status and inclusion/exclusion reason;
- atomic claim, evidence type, source locator, applicability, uncertainty, and conflict status;
- data/model/instrument version and provenance;
- analysis or design decision, supporting source/claim identifiers, alternatives considered, and unresolved evidence;
- stage status: `planned`, `performed`, `verified`, `needs_user_input`, or `needs_expert_review`.

## Synthesis before design

Create a study-comparison matrix covering population/domain, period, scale, data, method, validation, findings, uncertainty, limitations, and evidence strength. Summarize convergence, disagreement, geographic/method coverage, design quality, and residual gaps. Link each major design choice to verified evidence or label it as a hypothesis/engineering choice.

Use one of four labels for consequential statements: `observed_evidence`, `author_interpretation`, `hypothesis_or_mechanism`, or `planned_test`. When the task is design-only, output planned estimands, diagnostics, figures/tables, and reporting formats—never placeholder results that read as findings.

Finish with a conventional reference list or machine-readable bibliography, plus an inline mapping from consequential claims and design decisions to source identifiers.

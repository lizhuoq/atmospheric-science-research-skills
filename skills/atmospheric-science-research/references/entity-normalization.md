# Dataset, instrument, and model normalization

`entity-evidence.jsonl` is a machine-generated discovery aid built from training PDFs. It contains no paper text. Each record identifies a normalized entity, DOI, title, year, and first detected PDF page.

The records establish only that a string occurs on the cited page. They do not establish whether the entity was used as input, validation data, a model, an instrument, a comparison, or background literature. Every record is `machine_draft`, `context_only`, `not_assessed`, and `rule_eligible: false` until a human checks the source.

Use these records to find candidate papers and normalize names. Never use them alone to support a scientific conclusion.


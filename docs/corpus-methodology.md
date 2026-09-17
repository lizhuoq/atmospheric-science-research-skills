# Corpus methodology

The corpus contains 3,000 metadata records selected from 30 atmospheric-science journals for 2016–2025. Selection prioritized OpenAlex citation count while rewarding topic novelty. This is a representative, high-impact sample rather than a systematic census or a verified JCR top-30 ranking.

## Reproducible derivatives

Run:

```powershell
python scripts/build_milestone1.py
python scripts/build_milestone1.py --check
```

The builder reads the frozen metadata ledger, applies an inspectable keyword taxonomy to title and OpenAlex topic strings, and writes multi-label classifications plus a deterministic split. It does not read blind-test full text and does not access the network.

The split seed is `atmospheric-skills-m1-v1`. The deterministic algorithm applies 70/15/15 hard quotas within each publication year, then greedily balances candidate theme and journal labels inside those quotas. Every year with at least three records therefore appears in all three splits. The exact input hash, algorithm description, seed, and counts are stored in `data/splits/manifest.json`.

## Leakage policy

- Training: scientific rule extraction and examples.
- Development: workflow tuning and error analysis, never reusable rule extraction.
- Blind test: final evaluation only; do not inspect full text while authoring Skills.

Metadata must remain visible for all three sets so stratification and bibliographic audits are reproducible. This does not authorize using blind-test findings.

## Classification limitations

The milestone taxonomy is a transparent baseline, not a validated ontology. Broad terms such as “climate,” “model,” and “observation” can over-label records; rare topics can be missed when titles and OpenAlex labels are nonspecific. Manual review should focus first on unclassified records, low-count themes, and apparent cross-domain matches. A later classifier may use training-set abstracts/full text, but its blind-test performance must be reported separately.

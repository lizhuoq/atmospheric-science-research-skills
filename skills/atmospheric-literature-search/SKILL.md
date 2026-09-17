---
name: atmospheric-literature-search
description: Design and execute reproducible searches for atmospheric-science literature, including source routing, query construction, citation chaining, deduplication, version checks, screening, and lawful full-text acquisition. Use when the task is to find or update a literature set; hand verified papers to a reading or synthesis workflow.
---

# Atmospheric Literature Search

Build a reproducible candidate-paper set for a defined atmospheric-science question. Discovery records are not scientific evidence until the relevant full text is read.

## Workflow

1. Define phenomenon, outcome, region/regime, scale, period, study design, document type, languages, and publication-status limits. Record unresolved choices.
2. Create concept blocks with synonyms, abbreviations, spelling variants, canonical instrument/dataset/model names, and exclusions. Pilot broad and narrow queries before freezing the protocol.
3. Route across complementary sources: bibliographic databases for coverage, NASA ADS and domain publishers for atmospheric relevance, Crossref/DataCite for identity, citation graphs for expansion, and repositories/publisher pages for lawful full text. Never claim an unavailable database was searched.
4. Log source, exact query, filters, search date, result count, and export limitations. Distinguish a convenience search from a systematic or scoping search.
5. Normalize DOI and bibliographic fields; deduplicate by DOI, then normalized title/author/year. Resolve conflicting metadata against the version-of-record landing page.
6. Screen title/abstract using frozen criteria. Record one primary exclusion reason per excluded record and flow counts at every stage.
7. Chase references and citing papers from strong seeds; search for recent reviews, foundational studies, null results, contradictory findings, and relevant non-English literature when within scope.
8. Check publication status, corrections, retractions, expressions of concern, preprint/version-of-record relationships, and access status.
9. Acquire full text only through open repositories, publisher access already available to the user, or user-provided files. Do not bypass paywalls, CAPTCHAs, robots controls, or rate limits.
10. Deliver a deduplicated ledger and hand `full_text` items to `$atmospheric-paper-reader`; retain `abstract_only` and `metadata_only` items for discovery, not detailed claims.

## Output

- Scoped question and protocol
- Source/query/search-date log
- Inclusion and exclusion criteria
- Deduplicated candidate ledger with DOI, version, peer-review, access, and status fields
- Screening flow counts and exclusion reasons
- Coverage limitations and recommended search updates

## Quality gates

Do not rank evidence by citation count or journal prestige. Do not call a search exhaustive without appropriate database coverage, reproducible queries, and documented screening. Do not use snippets or abstracts to populate detailed methods, numerical results, or limitations.

## Example

`Use atmospheric-literature-search to build a reproducible 2015-present literature set on urbanization effects on extreme precipitation in East Asia, including contradictory studies and full-text access status.`

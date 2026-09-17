# Live literature discovery and acquisition

Use this guide when the task requires finding literature rather than only analyzing papers already supplied by the user.

## Source routing

Use more than one source class when coverage matters. Availability depends on the host agent, subscriptions, and institutional access; record what was actually searched.

| Need | Preferred sources | Purpose |
|---|---|---|
| Broad scholarly discovery | Web of Science, Scopus, OpenAlex, Google Scholar, Semantic Scholar | Recall-oriented topic search and cited/citing expansion |
| Atmospheric and geoscience coverage | NASA ADS, AGU/Wiley, AMS Journals, Copernicus Publications, EGU resources | Domain terminology, journals, conference and article discovery |
| Meteorological records and reports | NOAA/NCEI, WMO Library, national meteorological services | Authoritative reports, observing systems, climate normals and metadata |
| Remote sensing and Earth observation | NASA Earthdata, ESA Earth Online, CEOS, instrument/product documentation | Product algorithms, validation papers and official technical documentation |
| Chemistry and air quality | PubMed for health/exposure, EPA and WHO for authoritative assessments, publisher databases | Exposure, epidemiology, chemistry and assessment evidence |
| DOI and bibliographic identity | Crossref, DataCite, publisher landing pages | DOI/title/year verification; not a substitute for reading the paper |
| Open full text | Unpaywall, Crossref license links, DOAJ, PubMed Central, institutional repositories, author manuscripts | Lawful accessible copies and license status |
| Preprints | EarthArXiv, ESSOAr, arXiv where relevant | Recent work; label as non-peer-reviewed and check for a later version of record |

Search-source names are routing guidance, not a claim that credentials or an API are bundled. Prefer APIs or export functions allowed by the service. Respect rate limits and terms of use.

## Search construction

1. Convert the question into concept blocks: phenomenon/process, outcome/variable, region/regime, scale, method/data source, and study type.
2. Add synonyms and controlled variants. Include canonical dataset/model/instrument names and common abbreviations, but do not require every block in every query.
3. Run a broad discovery query, inspect vocabulary from relevant papers, then run narrower queries. Use backward and forward citation chasing for seminal and contradictory studies.
4. Search recent review papers for vocabulary and scope, but verify empirical claims against primary studies when possible.
5. Record each exact query, source, date, filters, result count, and any access limitation. Do not present an unlogged convenience search as systematic review coverage.

## Selection and version control

- Deduplicate by normalized DOI; fall back to normalized title, first author, and year.
- Prefer the version of record for citation. If only a preprint or accepted manuscript was read, say which version supported the claim.
- Treat retractions, corrections, expressions of concern, and materially different preprint versions as status fields that must be checked before relying on a source.
- Balance recency with foundational work. Citation count can help discover influential studies but is not a quality or evidence-strength score.
- For systematic or scoping reviews, use a documented protocol and flow counts; do not claim PRISMA compliance unless its applicable requirements were actually met.

## Acquisition and reading

- Prefer publisher open access, trusted repositories, or user-provided files. Use authenticated institutional access only when the user/runtime already has it; never request or expose credentials in the evidence record.
- Do not bypass paywalls, CAPTCHAs, access controls, robots restrictions, or bulk-download limits.
- Store downloaded papers in a user-controlled, Git-ignored working directory. Record source URL, access date, version, license/access category, and file hash when reproducibility requires it.
- Parse text for navigation, then inspect original or rendered pages for equations, maps, figures, tables, symbols, superscripts, and multi-column reading order.
- An abstract can support only what the abstract explicitly states. It usually cannot support exact methods, numerical results, limitations, or figure interpretation.

## Minimum acquisition ledger

For each candidate retain: query/source, title, authors, year, venue, DOI or stable identifier, landing URL, access status (`full_text`, `abstract_only`, `metadata_only`, `unavailable`), version, peer-review status, inclusion decision, exclusion reason, and local hash if a file was lawfully downloaded.

## Failure and fallback behavior

- If a preferred database is unavailable, use another source and disclose the coverage limitation.
- If only metadata or an abstract is accessible, keep it for discovery but exclude it from claims requiring full-text verification.
- If too few relevant studies are found, broaden synonyms, citation-chain from strong seeds, relax one scope constraint at a time, and report each change.
- If results are too broad, add regime, scale, variable, instrument/model, or study-design terms rather than selecting papers by convenience.

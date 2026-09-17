---
name: atmospheric-science-research
description: Orchestrate an evidence-grounded atmospheric-science research task from question framing through literature, analysis, writing, and review. Use as the main entry point when a request spans multiple research stages; route narrow requests directly to the relevant specialist Skill.
---

# Atmospheric Science Research

Act as the suite's lightweight coordinator. Preserve the user's objective, select only the specialist Skills the task needs, pass traceable artifacts between them, and consolidate the result. Do not duplicate their detailed procedures.

Combine Skills along two axes when needed: a stage Skill defines what work is being done (search, reading, design, analysis, writing, audit), while a topic/method Skill adds domain-specific gates (extremes, composition, modeling, QC). A topic Skill supplements rather than replaces the relevant stage Skill.

## Route by task

- Literature discovery and screening -> `$atmospheric-literature-search`
- Full-text reading and evidence extraction -> `$atmospheric-paper-reader`
- Research and experiment planning -> `$atmospheric-research-design`
- Statistics, causality, ML, or forecast verification -> `$atmospheric-statistical-analysis`
- Units, time, coordinates, retrieval collocation, or data QC -> `$atmospheric-data-qc`
- Figures, tables, maps, profiles, or equations -> `$atmospheric-figure-analysis`
- Numerical-model configuration and experiments -> `$atmospheric-model-experiment`
- Extreme events and attribution -> `$atmospheric-extremes-attribution`
- Chemistry, aerosols, air quality, or exposure -> `$atmospheric-composition-air-quality`
- Manuscript drafting from verified evidence and real results -> `$atmospheric-manuscript-writer`
- Claim-to-source and overreach checks -> `$atmospheric-claim-audit`
- Manuscript-level referee review -> `$atmospheric-peer-review`

For a broad SCI request, normally route through question framing, literature search, paper reading, research design/analysis, writing, and claim audit. Skip stages already completed and verified. If a specialist Skill is unavailable, disclose that limitation instead of claiming it ran.

## Coordination contract

Maintain a compact task ledger containing scope and assumptions, search log, source/access status, atomic evidence with locators, data and configuration provenance, analysis decisions, user-owned results, unresolved issues, and review status. A downstream stage must not silently convert metadata into evidence, an abstract into full-text support, association into causation, model output into observation, or a machine draft into expert-reviewed knowledge.

Read [references/workflow-ledger.md](references/workflow-ledger.md) for scope freezing, current-literature cutoffs, search stopping, paper prioritization, handoff fields, and design-only output labels.

The bundled corpus is optional development and regression-test material, never the topic boundary. New topics require live lawful literature access or user-provided papers. Never invent citations, methods, data, results, novelty, or expert approval.

## Output

- Selected workflow and completed stages
- Integrated research deliverable requested by the user
- Evidence and provenance summary
- Limitations, unresolved verification, and next actions

## Quality gates

Stop or narrow the output when a consequential claim lacks verified support, the necessary full text or user result is unavailable, scales or variables are incompatible, or the requested causal conclusion exceeds the design. Keep scientific uncertainty visible during synthesis and writing.

## Example

`Use atmospheric-science-research to develop a current, evidence-grounded SCI study on urban effects on extreme precipitation, from literature search and design through manuscript drafting and claim audit.`

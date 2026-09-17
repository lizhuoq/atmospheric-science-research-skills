# ADR 0001: Evidence-first modular Skill architecture

- Status: accepted
- Date: 2026-09-16

## Decision

Separate immutable source metadata, reproducible derived indexes, evidence records, reusable Skill workflows, and evaluation fixtures. Use one broad demonstration Skill for evidence synthesis before creating subfield Skills. Keep scientific evidence out of `SKILL.md`; store atomic, source-located records under a versioned schema.

Blind-test records are metadata-visible for stratification but full-text-invisible during rule authoring. Only training records may become reusable rules. Development records tune workflows, and blind-test records evaluate generalization.

## Rationale

The corpus supports many overlapping themes, while individual research tasks share evidence, scale, unit, uncertainty, and citation checks. A Skill per topic would duplicate generic instructions and encourage untested prompt proliferation. Progressive disclosure, deterministic scripts, schema validation, and CI-visible tests provide a smaller maintenance surface.

## Consequences

Subfield Skills will be added only when they have distinct decisions, inputs, failure modes, and sufficient training/full-text coverage. Taxonomy labels are not automatically Skill boundaries. Updating taxonomy or split logic requires regenerating manifests and documenting the change.


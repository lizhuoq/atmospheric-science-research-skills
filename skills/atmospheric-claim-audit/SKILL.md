---
name: atmospheric-claim-audit
description: Audit atmospheric-science claims against their cited evidence, scope, study design, uncertainty, and causal strength. Use for manuscript conclusions, abstracts, reviews, policy-facing statements, and citation checking; return prioritized corrections without rewriting unsupported claims as facts.
---

# Atmospheric Claim Audit

Test whether every consequential statement is entailed by its evidence within the relevant spatial, temporal, methodological, and causal boundary.

## Workflow

1. Extract atomic claims and classify each as descriptive, comparative, trend, predictive, mechanistic, causal, attributional, generalization, novelty, or policy/application claim.
2. Link each claim to its actual source and locator. Mark uncited, inaccessible, secondary-only, mismatched, or unverifiable support.
3. Compare the claim with the source's study type, population, region, period, atmospheric regime, scale, variables, units, model configuration, and uncertainty.
4. Apply an entailment label: `supported`, `partially_supported`, `not_supported`, `contradicted`, or `not_verifiable`.
5. Check direction, magnitude, qualifiers, denominators, baseline, uncertainty, and whether a figure/table supports the prose.
6. Stress-test common overreach: association→causation, prediction→mechanism, model→observation, event→climate, regional→global, statistical→practical significance, absence of evidence→evidence of absence, and ensemble agreement→independence.
7. Inspect selective citation and unresolved conflicting studies. Journal prestige or citation count cannot replace claim-level support.
8. Propose the smallest defensible correction: narrow scope, weaken verb, add uncertainty, cite primary evidence, separate inference from result, or remove the claim.

## Output

- Claim-evidence matrix with locator and entailment label
- High/medium/low priority issues
- Scope, causality, uncertainty, and citation defects
- Minimal defensible revisions
- Claims requiring author data or expert adjudication

## Quality gates

Never invent a supporting source or locator. Do not mark a claim false merely because its evidence is unavailable; use `not_verifiable`. Do not make misconduct allegations from ordinary errors or incomplete reporting.

## Example

`Use atmospheric-claim-audit to check whether the abstract and conclusions overstate causal and global implications relative to the cited regional modeling study.`

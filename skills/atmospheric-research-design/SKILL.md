---
name: atmospheric-research-design
description: Convert an atmospheric-science question and verified evidence into a feasible observational, modeling, statistical, or mixed research design. Use for hypotheses, variables, data selection, experiments, validation, sensitivity analysis, reproducibility, and decision-ready study plans; do not invent results.
---

# Atmospheric Research Design

Design a study whose estimand, evidence chain, feasibility, and failure conditions are explicit.

## Workflow

1. State the research question, scientific gap, estimand, target population/domain, atmospheric process, spatial/temporal scale, and falsifiable hypotheses. Separate exploratory from confirmatory aims.
2. Draw the evidence chain from physical mechanism to observable quantities and analysis outputs. Identify confounders, mediators, shared drivers, selection effects, and alternative explanations.
3. For changing land use or other environmental exposures, define the exposure trajectory and counterfactual, separate plausible mechanisms, and assess endogenous site selection, observation-network change, and correlated socioeconomic or emission changes.
4. Choose observational, field/laboratory, numerical-model, statistical, causal, ML, or mixed design based on the question—not data convenience.
5. Define inputs, outputs, controls, baselines, units, coordinates, time basis, resolutions, coverage, versions, licenses/access, and provenance. Verify that proposed datasets exist for the required domain and period and assess whether available observations identify the target process.
6. Plan preprocessing and QC before outcome inspection. Include missingness, representativeness, collocation, regridding, temporal aggregation, and uncertainty propagation.
7. Define analysis, validation, independence boundaries, sample-size or event-count adequacy, multiple-testing control, and dependence-aware uncertainty.
8. For simulations, specify control and sensitivity experiments, forcing, initial/boundary conditions, spin-up, ensemble strategy, parameterizations, and conservation checks.
9. Predefine robustness tests, negative controls, alternative definitions, regime stratification, out-of-sample tests, and stopping/failure criteria.
10. Produce a reproducibility plan covering code, environments, seeds, data licenses, configuration, provenance, intermediate artifacts, and archival outputs.
11. Identify resource, access, ethical, legal, computational, and expertise constraints. Offer a minimum viable design and a stronger design when tradeoffs are material.

## Output

- Question, gap, estimand, hypotheses, and causal/physical rationale
- Study population/domain, data and variable table
- End-to-end analysis and validation plan
- Controls, sensitivity, uncertainty, and failure criteria
- Reproducibility and resource plan
- Decisions requiring domain-expert confirmation

## Quality gates

Reject designs with outcome leakage, circular validation, incompatible scales, undefined baselines, pseudoreplication, or a causal claim unsupported by identification assumptions. Never fabricate expected findings or power calculations without defensible inputs.

## Example

`Use atmospheric-research-design to design an observation-model study of urban effects on warm-season convective rainfall over the Beijing-Tianjin-Hebei region.`

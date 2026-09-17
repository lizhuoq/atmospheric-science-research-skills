---
name: atmospheric-extremes-attribution
description: Design or audit analyses of atmospheric and hydroclimatic extremes and event attribution. Use for heatwaves, heavy precipitation, drought, storms, compound events, return periods, risk ratios, factual/counterfactual ensembles, and attribution claims; distinguish event description, trend, mechanism, and causation.
---

# Atmospheric Extremes and Attribution

Define the event before analyzing it and match attribution language to the counterfactual evidence.

## Workflow

1. Specify event variable, threshold, duration, spatial footprint, temporal aggregation, season, impact relevance, compound dimensions, and selection procedure. Explain whether the definition was chosen before or after observing the event.
2. Define population, baseline/reference period, observational products, homogeneity, coverage, uncertainty, and sensitivity to alternative event definitions.
3. Choose block-maxima, peaks-over-threshold, point-process, spatial, storyline, trend, or other methods based on the estimand. Verify event independence, threshold adequacy, tail fit, and stationarity/nonstationarity assumptions.
4. Quantify return level/period or exceedance probability with dependence-aware uncertainty. Do not interpret an estimated return period as a deterministic recurrence interval.
5. For attribution, define factual and counterfactual worlds, forcing differences, conditioning, model ensembles, observational constraint, and target quantity such as probability ratio or intensity change.
6. Evaluate model ability for the event-generating process, distribution tail, circulation/regime, land/ocean state, and relevant scale. Bias correction does not automatically establish process fidelity.
7. Address internal variability, ensemble dependence, model weighting, structural uncertainty, boundary conditions, selection bias, and multiple event definitions.
8. Separate thermodynamic, dynamic, exposure, and vulnerability contributions. A physical storyline and probabilistic attribution answer different questions.
9. Report sensitivity across datasets, models, definitions, covariates, periods, and conditioning choices, including unbounded or low-confidence intervals.
10. Use calibrated language tied to the estimand; do not attribute damages or societal impacts without exposure/vulnerability evidence.

## Output

- Event and estimand definition
- Data/model fitness assessment
- Extreme-value or attribution method and diagnostics
- Factual/counterfactual construction
- Probability/intensity results with uncertainty when analysis has been performed; otherwise planned estimands, diagnostics, and reporting format
- Robustness, limitations, and permitted attribution wording

## Quality gates

Reject post hoc event definitions presented as preregistered, unsupported stationary assumptions, naive independence, and causal statements based only on temporal coincidence or trends.

## Example

`Use atmospheric-extremes-attribution to design an attribution study for a record regional heatwave and specify defensible probability-ratio language.`

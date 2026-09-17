---
name: atmospheric-statistical-analysis
description: Design, implement, or audit atmospheric statistics, causal inference, time-series, spatial and extreme-value methods, machine learning, and forecast verification. Use for ensemble forecasts, CRPS, Brier scores, reliability, lead-time skill, dependence, multiple testing, uncertainty, leakage, validation, or causal interpretation.
---

# Atmospheric Statistical Analysis

Match the estimator and uncertainty model to the sampling process, dependence structure, scientific estimand, and intended inference.

Read [forecast-verification-checks.md](forecast-verification-checks.md) when forecast, hindcast, ensemble, or reanalysis verification requires metric-specific checks.

## Workflow

1. Define the estimand, observation unit, population, variables, units, transformations, sampling design, and whether the goal is description, association, prediction, detection, attribution, or causation.
2. Audit missingness, quality flags, censoring/detection limits, aggregation, nonstationarity, inhomogeneity, outliers, and preprocessing learned from the data.
3. Map temporal, spatial, hierarchical, network, and ensemble dependence. Estimate effective information rather than treating every grid cell, timestep, station, or ensemble member as independent.
4. Select a model whose assumptions match the data-generating process. Diagnose residuals, functional form, heteroscedasticity, collinearity, autocorrelation, spatial structure, and influential observations.
5. For trends, define baseline, seasonality, autocorrelation treatment, change points, field significance, and sensitivity to start/end dates. For extremes, verify threshold/block choices, stationarity assumptions, tail diagnostics, and event independence.
6. For causal claims, state the intervention and counterfactual, show assumed causal structure, justify adjustment variables, test positivity/overlap, and examine unmeasured-confounding sensitivity. Prediction alone is not causal identification.
7. For ML, split by the deployment unit and future information boundary; prevent spatial, temporal, station, event, and preprocessing leakage. Compare against simple baselines and evaluate calibration and out-of-domain behavior.
8. Address multiple testing and researcher degrees of freedom. Report effect sizes and intervals, not p-values alone.
9. Use dependence-aware bootstrap, permutation, hierarchical, Bayesian, or analytic uncertainty methods as appropriate. Propagate measurement and reference uncertainty when material.
10. Report assumption checks, robustness, negative results, subgroup sample sizes, code/configuration, and interpretation boundaries.

## Output

- Estimand and analysis population
- Data/QC and dependence audit
- Method and assumption rationale
- Validation and leakage assessment
- Uncertainty and multiplicity plan
- Robustness/sensitivity matrix
- Permitted and prohibited interpretations

## Quality gates

Stop when the observation unit, time basis, units, split boundary, or estimand is undefined. Do not interpret significance as importance, correlation as causation, or random grid-cell splits as spatial generalization.

## Example

`Use atmospheric-statistical-analysis to compare two ensemble precipitation forecasts with paired lead-time CRPS/CRPSS, reliability, rare-event skill, spatial diagnostics, and dependence-aware uncertainty.`

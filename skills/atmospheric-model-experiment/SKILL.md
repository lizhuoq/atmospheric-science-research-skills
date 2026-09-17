---
name: atmospheric-model-experiment
description: Design or audit atmospheric numerical-model experiments, including NWP, WRF, chemistry transport, climate, LES, and Earth-system simulations. Use for domains, resolution, initialization, forcing, boundary conditions, spin-up, parameterizations, ensembles, sensitivity experiments, conservation, and reproducibility.
---

# Atmospheric Model Experiment

Design simulations that isolate the intended mechanism and support the claimed scale of inference.

Read [model-configuration.md](model-configuration.md) when a task needs a detailed configuration audit.

## Workflow

1. Define the scientific question, target process, estimand, modeled scales, required outputs, comparison population, and whether the experiment targets prediction, sensitivity, mechanism, detection, or attribution.
2. Record model name/version/commit, dynamical core, equations/approximations, domain, projection, nesting, horizontal/vertical grid, top, timestep, numerics, and output cadence.
3. Specify initialization, forcing, lateral/lower/upper boundaries, SST/sea ice, land state, emissions, chemistry, nudging/data assimilation, restart behavior, and all dataset versions.
4. Justify physics and parameterizations relative to grid scale and process. Identify incompatible or scale-aware settings and interactions among schemes.
5. Define spin-up using process timescales and diagnostics, not convention alone. Exclude or separately analyze adjustment periods.
6. Construct control, perturbation, factorial, or ensemble experiments that isolate the target effect. Avoid changing multiple uncontrolled factors. Document perturbation realism and conservation implications.
7. Address internal variability, initial-condition sensitivity, ensemble size/genealogy, stochastic physics, and shared forcing. Members are not independent studies.
8. Predefine diagnostics, budgets, observations/reference products, collocation/regridding, baseline metrics, regime stratification, and uncertainty. Separate tuning data from evaluation.
9. Check mass, water, energy, tracer, and numerical stability as applicable. Investigate boundary artifacts, domain-size dependence, resolution sensitivity, and parameter compensation.
10. Archive configuration, namelists, source changes, build environment, seeds, workflow scripts, provenance, logs, and restart/output policy sufficient for reproduction.

## Output

- Scientific target and experiment matrix
- Complete configuration and forcing inventory
- Spin-up, ensemble, and sensitivity rationale
- Diagnostics, validation, budgets, and uncertainty plan
- Computational/reproducibility plan
- Failure modes and interpretation limits

## Quality gates

Do not attribute differences to one factor when configurations differ elsewhere. Do not infer real-world causality from an unconstrained sensitivity run. Stop when boundary conditions, parameterizations, resolution, or validation samples are undocumented enough to prevent interpretation.

## Example

`Use atmospheric-model-experiment to design WRF control and urban-land sensitivity ensembles for warm-season convective rainfall.`

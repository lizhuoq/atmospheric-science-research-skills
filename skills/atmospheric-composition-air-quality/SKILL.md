---
name: atmospheric-composition-air-quality
description: Design or audit atmospheric chemistry, aerosol processes, emissions, air quality, source attribution, and exposure studies. Use for chemical mechanisms, inventories, CTMs, PM and ozone, source apportionment, meteorological normalization, exposure error, and health interpretation; use data-QC instead for a retrieval-validation-only task.
---

# Atmospheric Composition and Air Quality

Trace the chain from emissions and chemistry through transport, measurement/model representation, exposure, and any claimed outcome.

## Workflow

1. Define species, phase, metric, averaging period, unit, standard conditions, size fraction, chemical form, vertical/spatial support, population/domain, period, and intended inference.
2. Inventory emissions, inventories/versions, speciation, temporal/spatial allocation, plume treatment, natural sources, boundary/background concentrations, meteorology, chemistry, deposition, and aerosol processes.
3. For measurements, document instrument principle, calibration, detection limit, interferences, inlet/size cut, blank correction, humidity/temperature effects, siting, QC, and representativeness.
4. For models, document mechanism, solver, resolution, mixing, transport, deposition, heterogeneous chemistry, aerosol thermodynamics, initial/boundary conditions, and observation operators.
5. Harmonize quantities before comparison; distinguish mass concentration, mixing ratio, column, optical proxy, dry/ambient conditions, and regulatory metrics. Treat retrievals and model-derived surface estimates as indirect.
6. Separate emissions, chemistry, meteorology, transport, and removal contributions using designs capable of identifying them. Meteorological normalization and sensitivity runs require explicit assumptions and validation.
7. For source apportionment, state receptor/model method, tracers/profiles, collinearity, rotational ambiguity, source categories, uncertainty, and whether the result is contribution, sensitivity, or causal responsibility.
8. Validate by species, season, regime, site type, concentration range, and episode; use independent data where possible. Report false cancellation among components and aggregate metrics.
9. For exposure/health links, assess monitor/model/satellite assignment, mobility and indoor infiltration, lag structure, confounding, selection, spatial leakage, measurement error, and causal design. Ambient concentration is not personal dose.
10. Report mass/element budgets, uncertainty propagation, policy scenario realism, transferability, and limits on health or control-effect claims.

## Output

- Species/metric and evidence-chain definition
- Emissions, chemistry, observation/model configuration
- Harmonization, QC, and validation plan
- Source/exposure/causal identification assessment
- Uncertainty, sensitivity, and applicability
- Defensible findings and prohibited interpretations

## Quality gates

Stop when species, units, standard conditions, size fractions, or time bases are incompatible. Do not interpret model sensitivity as source responsibility, concentration as dose, or association as health causation without an adequate design.

## Example

`Use atmospheric-composition-air-quality to audit a satellite-plus-CTM PM2.5 exposure study for retrieval error, spatial leakage, confounding, and causal overreach.`

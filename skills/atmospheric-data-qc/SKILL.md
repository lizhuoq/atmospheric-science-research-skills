---
name: atmospheric-data-qc
description: Design or audit quality control and harmonization for atmospheric observations, reanalyses, retrievals, and model output. Use for units, coordinates, calendars, timestamps, quality flags, missingness, aggregation, regridding, representativeness, provenance, and uncertainty before scientific analysis.
---

# Atmospheric Data Quality Control

Produce an auditable QC and harmonization plan that preserves physical meaning and data lineage.

For retrieval or instrument comparisons, read [remote-sensing-measurement-chain.md](remote-sensing-measurement-chain.md) and [remote-sensing-collocation.md](remote-sensing-collocation.md) as applicable.

## Workflow

1. Inventory every dataset, product/version, variable, definition, unit, dimension, coordinate/reference system, vertical coordinate, calendar, timestamp convention, resolution, coverage, quality flag, fill value, and uncertainty field.
2. Verify variable identity before conversion: accumulated versus instantaneous, flux versus amount, mixing ratio versus concentration, geometric versus geopotential height, sea-level versus surface pressure, and local/UTC/solar time.
3. Check file and metadata integrity, duplicates, ordering, coordinate bounds, missing/fill encodings, impossible values, discontinuities, station moves, instrument changes, model-cycle changes, and product-version transitions.
4. Define QC flags with reason codes and preserve raw values. Separate provider flags from project-specific decisions; never silently delete observations.
5. Diagnose missingness and censoring by time, space, regime, instrument, and intensity. State assumptions behind interpolation or imputation and prevent information leakage.
6. Harmonize units, calendars, longitude conventions, vertical coordinates, masks, accumulation windows, and temporal supports. Document density/temperature or other physical assumptions in nontrivial conversions.
7. Treat regridding and collocation as measurement operations. Record method, source/target grids, conservation behavior, weights, extrapolation, land/sea and topography effects, and representativeness error.
8. Quantify sample attrition and sensitivity to thresholds, flags, aggregation, and gap handling. Propagate uncertainty when transformations materially affect it.
9. Write machine-readable lineage: source, access/version, hashes when appropriate, operations, parameters, software environment, outputs, and reversible mappings to raw identifiers.

## Output

- Data dictionary and compatibility matrix
- QC rules with reason codes
- Unit/time/coordinate harmonization plan
- Missingness, collocation, and regridding assessment
- Attrition and sensitivity report
- Provenance and reproducibility record

## Quality gates

Stop comparisons when definitions, units, vertical coordinates, calendars, valid times, supports, or masks cannot be reconciled. Never overwrite raw data or present interpolated values as observations.

## Example

`Use atmospheric-data-qc to harmonize hourly station precipitation, ERA5 accumulations, and satellite half-hourly retrievals for event-scale validation.`

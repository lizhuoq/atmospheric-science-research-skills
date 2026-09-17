---
name: atmospheric-figure-analysis
description: Interpret or audit atmospheric-science figures, tables, maps, profiles, and equations using visual inspection plus source context. Use for scientific meaning, uncertainty, panel consistency, graphical integrity, caption adequacy, and claim support; do not infer unreadable or unstated values.
---

# Atmospheric Figure Analysis

Read the visual artifact as evidence, not decoration. Inspect the original or rendered page; extracted text alone is insufficient for graphics.

## Workflow

1. Establish source, figure/table/equation identifier, caption, related methods/results text, and intended claim. Verify panel labels and supplement references.
2. Identify visual type and encoding: axes, units, scales, projection, coordinates, levels, color map, normalization, binning, contours, vectors, markers, uncertainty, significance, masks, sample sizes, and reference periods.
3. Check comparability across panels: identical domains, color limits, baselines, seasons, variables, grids, smoothing, thresholds, ensemble definitions, and valid times.
4. For maps, inspect projection distortion, cyclic longitude, polar treatment, terrain/coast masks, area weighting, and spatial autocorrelation. For vertical plots, verify coordinate and orientation. For time series, verify aggregation, gaps, smoothing, and uncertainty.
5. For tables, reconcile denominators, units, rounding, missing values, uncertainty, multiple comparisons, and consistency with text. For equations, define symbols, dimensions, sign conventions, approximations, boundary conditions, and applicability.
6. Separate directly visible patterns from statistical support and physical interpretation. A visually strong pattern may be uncertain; a significance mask does not quantify practical importance.
7. Check accessibility and integrity: perceptual color map, color-vision safety, legibility, non-misleading axes, sufficient caption, and absence of selective cropping or inconsistent scales.
8. Produce a panel-level evidence ledger and list exact corrections. If numerical extraction is requested, use documented digitization and report precision limits.

## Output

- Visual inventory and intended claim
- Panel/table/equation-level interpretation
- Encoding, comparability, uncertainty, and integrity checks
- Claims supported, unsupported, or not verifiable
- Publication-readiness corrections

## Quality gates

Do not estimate exact values from low-resolution images, infer causality from visual association, or describe unseen panels. Mark ambiguous legends, symbols, and resolution limits explicitly.

## Example

`Use atmospheric-figure-analysis to audit this six-panel precipitation-change map for comparable color scales, significance, area weighting, and support for the caption's claim.`

# Forecast verification checks

Match the score to the target:

- Continuous deterministic fields: bias, MAE/RMSE, correlation, anomaly correlation; report at least one magnitude error and one association measure.
- Binary events: contingency table, probability of detection, false-alarm ratio, critical success index, equitable threat score; include base rate.
- Probabilities: Brier score and decomposition, reliability diagram, discrimination/ROC with caution about base-rate sensitivity.
- Ensembles: CRPS, rank/PIT diagnostics, spread-error relationship, reliability and sharpness. Exchangeability and member dependence must be assessed.
- Spatial precipitation/cloud fields: supplement pointwise scores with neighborhood, scale-aware, fraction, object, or displacement diagnostics.
- Tracks/timing: separate position, intensity, onset, duration, and timing errors.
- Extremes: threshold definition, return-period uncertainty, sample size, censoring, and tail sensitivity must be explicit.

Always identify orientation: whether higher or lower is better, and the reference used for skill scores. Avoid comparing metric values computed over different samples without paired analysis.

## Ensemble precipitation protocol

- Define initialization cycles, valid times, lead-time bins, accumulation windows, grid/mask, season, region, and common verification cases before comparing systems. Keep samples paired at each lead and report when sample membership changes.
- Precipitation has a point mass at zero and a continuous positive tail. Report dry-event frequency, wet-day threshold, intensity-conditioned performance, and threshold sensitivity. Do not rely on Gaussian assumptions.
- Report CRPS and a named-reference CRPSS. If ensemble sizes differ, use a fair or ensemble-size-adjusted estimator or sensitivity analysis; state the exact formula/software implementation.
- Use rank histograms for raw finite ensembles and PIT diagnostics for continuous/postprocessed predictive distributions. Handle ties and zero precipitation with a declared randomized or other defensible convention.
- Reliability diagrams require event threshold, binning rule, bin counts, uncertainty bands, and base rate. Report sharpness separately. For rare events, use Brier score/BSS, reliability with adequate pooling, and threshold or tail-weighted scores only with their interpretation and sample limits.
- Check spread-error consistency without treating ensemble members as verification replicates. Document member exchangeability, genealogy, lagged members, perturbation strategy, unequal weights, and shared forcing.
- Compare score differences on paired forecast cases. Resample by initialization or event using temporal blocks as needed; preserve spatial dependence, report confidence intervals, and control multiplicity across leads, regions, variables, and thresholds.
- For spatial precipitation, use a common conservative grid for accumulations when possible, area weighting, an explicit land/domain mask, and neighborhood/scale/object diagnostics alongside point scores. Diagnose complex terrain, gauge-density, radar/satellite reference uncertainty, and shared inputs.
- Build climatological probability baselines by location and season/day-of-year without leaking verification-period information. Add persistence or the operational incumbent when decision-relevant.
- Separate raw and postprocessed systems. Freeze calibration/training windows, verify independence from evaluation, and report whether apparent lead-time skill changes arise from initialization, valid-time regime, postprocessing, or changing samples.
- Short archives rarely support stable return-period claims. For forecast extremes, prefer prespecified high thresholds and disclose event counts unless tail estimation is independently justified.
